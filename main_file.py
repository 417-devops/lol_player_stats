# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 16:19:50 2020

@author: Karl Roush and Elijah Smith
"""

import cassiopeia as cass
from cassiopeia import Summoner, Match
from cassiopeia.data import Season, Queue

def getAPI_key():
    #reads the API key from local file
    file= open("../api_key.txt","r")
    return file.read()

def matchIDs(match_history):
    matchID_list=[]
    for item in match_history:
        matchID_list.append(item.id)
    return matchID_list
    
#%% INITIALIZATION
cass.set_riot_api_key(getAPI_key()) #or replace with your own api key
cass.set_default_region("NA") #or replace with another region

#% SETTING THE PLAYER TO BE 
player_name= "RebirthNA"
player_region= "NA"
summoner = Summoner(name=player_name, region=player_region)

#% GET THE MATCH HISTORY
# for soloQ only
match_history = summoner.match_history(queues={cass.Queue.ranked_solo_fives})
matchID_list= matchIDs(match_history) #save this for caching somehow

