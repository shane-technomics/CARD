# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 13:23:29 2024

@author: sstumvoll
"""

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
import numpy as np
import altair as alt
from vega_datasets import data

pn.extension("tabulator")


class Overview(Viewer):
    data = param.DataFrame(doc="Stores a DataFrame to explore")

    year = param.Range(default=(1981, 2022), bounds=(1981, 2022))

    filtered_data = param.Parameter()

    def __init__(self, **params):
        super().__init__(**params)
        #self.param.columns.objects = self.data.columns.to_list()

        dfrx = self.param.data.rx()

        p_year_min = self.param.year.rx().rx.pipe(lambda x: x[0])
        p_year_max = self.param.year.rx().rx.pipe(lambda x: x[1])

        self.filtered_data = dfrx[dfrx.year.between(p_year_min, p_year_max)]
        
        
        


    def __panel__(self):

        #trend = self.filtered_data
        cars = data.cars()

        chart = alt.Chart(cars).mark_circle(size=60).encode(
                    x='Horsepower',
                    y='Miles_per_Gallon',
                    color='Origin',
                    tooltip=['Name', 'Origin', 'Horsepower', 'Miles_per_Gallon']
                ).interactive()
        
        trend = {'x': np.arange(50), 'y': np.random.randn(50).cumsum()}
        cols = pn.Row(
                     
                     pn.indicators.LinearGauge(
                         name='Values Filled In', 
                         value=85, 
                         bounds=(0,100),
                         colors=[(.2, 'red'), (.5, 'gold'), (.9, 'green')],
                         show_boundaries=True,
                         horizontal=True),
                     
                     pn.panel(
                         chart
                     ))
             
        
        view = pn.Tabs(
            ('Overview 1',cols), 
            ('Overview 2',cols), 
            #styles=styles, 
            sizing_mode="stretch_width", 
            height=500, 
            margin=10, 
            dynamic=True)
        
        return view
                
