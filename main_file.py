# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 16:19:50 2020

@author: Karl Roush and Elijah Smith
"""

import cassiopeia as cass

def getAPI_key():
    #reads the API key from local file
    file= open("../api_key.txt","r")
    return file.read()

#%%

cass.set_riot_api_key(getAPI_key()) #or replace with your own api key
cass.set_default_region("NA") #or replace with another region

#%
