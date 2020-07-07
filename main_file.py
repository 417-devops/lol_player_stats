# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 16:19:50 2020

@author: Karl Roush
"""

def getAPI_key():
    #reads the API key from local file
    file= open("../api_key.txt","r")
    return file.read()

#%%

api_key= getAPI_key() #or replace with your own api key

#%
