# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 17:58:15 2024

@author: sstumvoll
"""

import pandas as pd
import panel as pn
import param
from panel.viewable import Viewer

pn.extension("tabulator")


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


    def __panel__(self):

        
        cols = pn.Column(
                 pn.Row(
                     pn.widgets.MultiChoice.from_param(self.param.columns, width=400)),
             pn.Column(
                     self.param.year),
                     pn.widgets.Tabulator(self.filtered_data, page_size=10, pagination="remote"),
             )
        
        view = pn.Tabs(
            ('Technical',cols), 
            ('Staffing',cols), 
            #styles=styles, 
            sizing_mode="stretch_width", 
            height=500, 
            margin=10, 
            dynamic=True)
        
        return view
                
