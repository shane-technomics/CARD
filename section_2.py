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

class SectionExplorer(Viewer):
    data = param.DataFrame(doc="Stores a DataFrame to explore")

    columns = param.ListSelector(
        default=['program', 'year', 'bus1', 'bus2', 'grade', 'usa', 'usn', 'usaf',
               'usphs', 'civ', 'cecom', 'spawar', 'other', 'total']
    )

    year = param.Range(default=(1981, 2022), bounds=(1981, 2022))

    filtered_data = param.Parameter()

    def __init__(self, **params):
        super().__init__(**params)
        self.param.columns.objects = self.data.columns.to_list()

        dfrx = self.param.data.rx()

        p_year_min = self.param.year.rx().rx.pipe(lambda x: x[0])
        p_year_max = self.param.year.rx().rx.pipe(lambda x: x[1])

        self.filtered_data = dfrx[dfrx.year.between(p_year_min, p_year_max)][self.param.columns]
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

        
        cols = pn.Column(
                 #pn.Row(
                  #   pn.widgets.MultiChoice.from_param(self.param.columns, width=400)),
             pn.Column(
                     self.param.year),
                     pn.widgets.Tabulator(self.filtered_data, page_size=10, pagination="remote"),
                     self.fileDownload(self.filtered_data)
             )
        
        narr = pn.pane.PDF('test_docs/DoD5004.pdf', width=1200, height=900)
        #narr_2 = pn.widgets.TextEditor(value=self.convert_docx_to_text('narrative.docx'))
        
        with open("test_docs/narrative_2.docx", "rb") as docx_file:
            result = mammoth.convert_to_html(docx_file)
            html = result.value # The generated HTML
            messages = result.messages # Any messages, such as warnings during conversion
            
        narr_3 = pn.pane.HTML(html)

        
        view = pn.Tabs(
            ('Technical',cols), 
            ('Reference',narr), 
            ('Narrative', narr_3),
            ('Editor', narr_3),
            #styles=styles, 
            sizing_mode="stretch_width", 
            height=500, 
            margin=10, 
            dynamic=True)
        
        return view
                
