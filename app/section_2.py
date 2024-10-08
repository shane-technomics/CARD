# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 17:58:15 2024

@author: sstumvoll
"""

import pandas as pd
import panel as pn
import param
from panel.viewable import Viewer
from io import StringIO
#import docx
import mammoth

pn.extension("tabulator")
pn.extension('texteditor')

class TabulatorExtension(param.Parameterized):
    value: pn.widgets.Tabulator = param.ClassSelector(
        class_=pn.widgets.Tabulator, allow_refs=False, constant=True
    )

    click_event = param.Parameter()
    edit_event = param.Parameter()
    selected_dataframe = param.DataFrame()
    edit_table = param.DataFrame(pd.DataFrame([],columns=['col', 'row', 'old', 'val']))

    def __init__(self, **params):
        super().__init__(**params)

        self.value.on_click(self._handle_click)
        self.value.on_edit(self._handle_edit)


    def _handle_click(self, event):
        self.click_event = event
        
    def _handle_edit(self, e):
        self.edit_event = e
        self.edit_table = self.edit_table._append(\
                dict(zip(['col', 'row', 'old', 'val'],[e.column, e.row, e.old, e.value])), \
                    ignore_index=True)


    @param.depends("value.selection", watch=True)
    def _handle_selection(self):
        self.selected_dataframe = self.value.selected_dataframe
        
        

class SectionExplorer(Viewer):
    data = param.DataFrame(doc="Stores a DataFrame to explore")

    columns = param.ListSelector(
        default=['program', 'year', 'bus1', 'bus2', 'grade', 'usa', 'usn', 'usaf',
               'usphs', 'civ', 'cecom', 'spawar', 'other', 'total']
    )

    year = param.Range(default=(1981, 2022), bounds=(1981, 2022))

    filtered_data = param.Parameter()
    
    edit_data = param.Parameter()
    
    def __init__(self, **params):
        super().__init__(**params)
        self.param.columns.objects = self.data.columns.to_list()

        dfrx = self.param.data.rx()

        p_year_min = self.param.year.rx().rx.pipe(lambda x: x[0])
        p_year_max = self.param.year.rx().rx.pipe(lambda x: x[1])

        self.filtered_data = dfrx[dfrx.year.between(p_year_min, p_year_max)][self.param.columns]
        
        self.table1 = pn.widgets.Tabulator(self.filtered_data, 
                             page_size=10, 
                             pagination="remote")
        
        self.extension = TabulatorExtension(value=self.table1)
                
        """
    def convert_docx_to_text(self, docx_path):
        doc = docx.Document(docx_path)
        full_text = []
    
        for para in doc.paragraphs:
            full_text.append(para.text)
    
        return '\n'.join(full_text)
    """
        
    #download function
    def filteredFile(self, year):
        df = self.data
        print(df)
        sio = StringIO()
        data = df.to_csv(sio)
        sio.seek(0)
        return sio

    def fileDownload(self, file):
      
        fd = pn.widgets.FileDownload(
            callback=pn.bind(self.filteredFile, self.param.year), 
            filename='filtered_data.csv'
        )
        return fd

        
    def __panel__(self):
    
        
        button = pn.widgets.Button(name="Update")
        #button.on_click(self.change_data)
        
        #self.table1.on_edit(self.show_edit)
        
        
        tabData = pn.Column(
                    #pn.Row(
                     #   pn.widgets.MultiChoice.from_param(self.param.columns, width=400)),
                pn.Column(
                        self.param.year),
                        self.table1,
                        self.extension.param.edit_table,
                        self.fileDownload(self.filtered_data),
                        button
                )

  
        narr = pn.pane.PDF('test_docs/DoD5004.pdf', width=1200, height=900)
        #narr_2 = pn.widgets.TextEditor(value=self.convert_docx_to_text('narrative.docx'))
        
        with open("test_docs/narrative_2.docx", "rb") as docx_file:
            result = mammoth.convert_to_html(docx_file)
            html = result.value # The generated HTML
            messages = result.messages # Any messages, such as warnings during conversion
            
        narr_3 = pn.pane.HTML(html)
        editor = pn.pane.HTML(html)

        
        view = pn.Tabs(
            ('Technical',tabData ), 
            ('Reference',narr), 
            ('Narrative', narr_3),
            ('Editor', editor),
            #styles=styles, 
            sizing_mode="stretch_width", 
            height=500, 
            margin=10, 
            dynamic=True)
        
        return view
                
