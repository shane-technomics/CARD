# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 12:01:38 2024

@author: sstumvoll
"""
#import pandas as pd
import panel as pn
import pandas as pd

class section_1():
  
        
        
    def get_data(self, document):
        return pd.DataFrame(list(document.find({})))

    def filter_data(self, year, document):
        source_data = self.get_data(document)
        data = source_data[(source_data.year <= year)]
        data = data.drop('_id', axis=1)
        return data


    def data_collector(self, document):
    
        min_year = int(self.get_data(document)["year"].min())
        max_year = int(self.get_data(document)["year"].max())
    
        year = pn.widgets.IntSlider(name="Year", value=max_year, start=min_year, end=max_year)
        self.df = pn.bind(self.filter_data, year=year)
        self.df = self.df(document)

    
    def table_1(self, document):
        
        min_year = int(self.get_data(document)["year"].min())
        max_year = int(self.get_data(document)["year"].max())
    
        year = pn.widgets.IntSlider(name="Year", value=max_year, start=min_year, end=max_year)
        df = pn.bind(self.filter_data, year=year)
        df = df(document)

        table_1 = pn.widgets.Tabulator(
                df, 
                sizing_mode="stretch_both", 
                name="Staffing", 
                groupby=['bus1'])
        
        
        return table_1
        

    def table_2(self):
        table_2 = pn.widgets.Tabulator(
                self.df, 
                sizing_mode="stretch_both", 
                name="Technical")
        return table_2

    
    def tab_create(self, table_1, table_2):
        
        self.tabs = pn.Tabs(
                table_1, 
                table_2, 
                styles=self.styles, 
                sizing_mode="stretch_width", 
                height=500, 
                margin=10, 
                dynamic=True
                
)

