# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 13:56:33 2024

@author: sstumvoll
"""
import sys
sys.path.append('OneDrive - Technomics/CDAO/Code')
import pandas as pd
from pymongo import MongoClient
#import hvplot.pandas
import pandas as pd
import panel as pn
from section_1 import section_1
from section_2 import SectionExplorer
import param

#db connection
ATLAS_URI = 'mongodb+srv://sstumvoll:1qaz%21QAZ@cluster0.xfw60.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
client = MongoClient(host=ATLAS_URI)
staffing = client.test.staffing

#ui settings
pn.extension("tabulator")
ACCENT = "teal"

styles = {
    "box-shadow": "rgba(50, 50, 93, 0.25) 0px 6px 12px -2px, rgba(0, 0, 0, 0.3) 0px 3px 7px -3px",
    "border-radius": "4px",
    "padding": "10px",
}

#tab dev
#@pn.cache()



#sections

#section_1 = section_1(styles=styles, document=staffing)
#table_1 = section_1.table_1(staffing)
#table_2 = section_1.table_2(staffing)
#section_1.tab_create(table_1, table_2)
staff_df = pd.DataFrame(list(staffing.find({})))

section_1 = SectionExplorer(data=staff_df)

#search
def get_search():
    return pd.DataFrame(list(staffing.find({})))


def filter_search(text):
    search_data = get_search()
    search_data = search_data[search_data.apply(lambda r: r.str.contains(text).any(), axis=1)]

    search_data = search_data.drop('_id', axis=1)
    return search_data

search = pn.widgets.TextInput(name='', placeholder='Search')
df_search = pn.rx(filter_search)(text=search)
table_search = pn.widgets.Tabulator(df_search, sizing_mode="stretch_both", name="Search")
column_search = pn.Column(table_search, 
                          styles=styles, 
                          sizing_mode="stretch_width", 
                          height=500, 
                          margin=10)

#column_search.append(section_1)

#sidbar dev
jos_pages = {
    "Roles": pn.Column("# JOS Roles", section_1),
    "Program": pn.Column("# Program", section_1),
    "Milestone": pn.Column("# Milestone", section_1),
    "Acquisition": pn.Column("# Acquisition", section_1),
    "Software": pn.Column("# Software", section_1),
    "Business Processes": pn.Column("# Business Processes", section_1),
    "Manpower": pn.Column("# Manpower", section_1),
    "Search": pn.Column("# JOS  Search", search, pn.layout.Divider(), column_search)

}

dil_pages = {
    "Milestone": pn.Column("# Milestone", section_1),
    "Roles": pn.Column("# Data Integration Layer Roles", section_1),
    "Program": pn.Column("# Program", section_1),
    "Acquisition": pn.Column("# Acquisition", section_1),
    "Software": pn.Column("# Software", section_1),
    "Business Processes": pn.Column("# Business Processes", section_1),
    "Manpower": pn.Column("# Manpower", section_1),
    "Search": pn.Column("# DIL Search", search, pn.layout.Divider(), column_search)

}

#header menu
menu_items = [
    ('Joint Operating Systems', 'jos'), 
    ('Data Integration Layer', 'dil'), 
    ('Global Information Dominance Experiment', 'gide'), 
    ('Mission Command Applications', 'mca')]

menu_button = pn.widgets.MenuButton(
    name='Program Selection', 
    items=menu_items, 
    button_type='light',
    button_style='outline',
    width = 400)

class pageBuilder():
    def __init__(self):
      self.pages =  jos_pages
      
    
    def program_selector(self,event):
        p = f'"{event.new}"'
        if p == '"jos"':
            self.pages = jos_pages
            print(p)
        else:
            self.pages = dil_pages
            print('else')
    
def c(event):
    p = f'"{event.new}"'
    if p == '"jos"':
        program_text.value = 'Joint Operating Systems'
        pb.pages = jos_pages
        section.options = list(pb.pages.keys())

    elif p == '"dil"':
        program_text.value = 'Data Integration Layer'
        pb.pages = dil_pages
        section.options = list(pb.pages.keys())

    elif p == '"gide"':
        program_text.value = 'Global Information Dominance Experiment'
        pb.pages = jos_pages
        section.options = list(pb.pages.keys())
    else:
        program_text.value = 'Mission Command Applications'
        pb.pages = dil_pages
        section.options = list(pb.pages.keys())


pb = pageBuilder()
program_text = pn.widgets.StaticText(value='Joint Operating Systems')

menu_button.on_click(c)


def show(page, program):
    return pb.pages[page]


starting_page = pn.state.session_args.get("page", [b"Roles"])[0].decode()
section = pn.widgets.RadioButtonGroup(
    value=starting_page,
    options=list(pb.pages.keys()),
    name="Section",
    sizing_mode="fixed",
    button_type="success",
    orientation='vertical',
    width=300,
    height=400
)
       
def showPrograms(program):
    section.options = program
    return section
    
    
#main
def main():
    ishow = pn.bind(show, page=section, program=menu_button.param.clicked)
    #pn.state.location.sync(page, {"value": "page"})
    
    
    template = pn.template.FastListTemplate(
        title="Cost Analysis Requirements Document (CARD)",
        header=pn.Row(program_text, menu_button, height=200, width=400),
        sidebar=[section],
        main=[ishow],
        main_layout=None,
        accent=ACCENT,
    ).servable()
    return template

app = pn.serve(main,
         threaded=True
         )

