# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 15:55:00 2024

@author: sstumvoll
"""

import pandas as pd
from mongoengine import connect
from mongoengine import *
import certifi


#db connection
ca = certifi.where()
ATLAS_URI = 'mongodb+srv://sstumvoll:1qaz%21QAZ@cluster0.xfw60.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
connect(
    host = ATLAS_URI
    
)


# data ingestion objects

"""
data = {'WBS_Number': ['1', '1.1', '1.1.1', '1.1.2'],
        'WBS_element': ['JOS', 'subsystem 1', 'subsystem 2', 'subsystem 3'],
        'notes' : ['Program of record', 'subsystem 1 notes', 'subsystem 2 notes', 'subsystem 3 notes']}

test_collection = pd.DataFrame(data=data)
"""

test_collection = pd.read_csv('OneDrive - Technomics\\CDAO\\Code\\staffing_test.csv')
test_collection = test_collection.to_dict(orient='records')


# data upload objects
class Staffing(Document):
    program = StringField(required=True)
    year = StringField(required=True)
    bus1 = StringField(required=True)
    bus2 = StringField(required=True)
    grade = StringField(required=True)
    usa = StringField()
    usn = StringField()
    usaf = StringField()
    usphs = StringField()
    civ = StringField()
    cecom = StringField()
    spawar = StringField()
    other = StringField()
    total = StringField()


# main
instances = []
for i in range(len(test_collection)):
    staffing = Staffing(
            program = test_collection[i]['Program'],
            year = test_collection[i]['Year'],
            bus1 = test_collection[i]['Business Area 1'],
            bus2 = test_collection[i]['Business Area 2'],
            grade = test_collection[i]['Grade'],
            usa = test_collection[i]['USA'],
            usn = test_collection[i]['USN'],
            usaf = test_collection[i]['USAF'],
            usphs = test_collection[i]['USPHS'],
            civ = test_collection[i]['CIV'],
            cecom = test_collection[i]['CECOM'],
            spawar = test_collection[i]['SPAWAR'],
            other = test_collection[i]['OTHER GOV'],
            total = test_collection[i]['TOTAL']

            )
    instances.append(staffing)

Staffing.objects.insert(instances)

