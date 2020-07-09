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

def make_matchID_list(match_history):
    matchID_list=[]
    for item in match_history:
        matchID_list.append(item.id)
    return matchID_list

#%% INITIALIZATION
cass.set_riot_api_key(getAPI_key()) #or replace with your own api key
cass.set_default_region("NA") #or replace with another region

#%% SETTING THE PLAYER TO BE ANALYZED
player_name= "RebirthNA"
player_region= "NA"
summoner = Summoner(name=player_name, region=player_region)

#%% GET THE MATCH HISTORY
# for soloQ
match_history = summoner.match_history(queues={cass.Queue.ranked_solo_fives})
matchID_list= make_matchID_list(match_history) #save this for caching somehow
# =============================================================================
# i=1 
# while i<len(matchID_list):
#    if matchID_list[i-1] < matchID_list[i]:
#        print("newer match id is less than older match id")
#    else:
#         pass
#    i+=1
# =============================================================================
   
#%% testing to find right api
# https://readthedocs.org/projects/cassiopeia/downloads/pdf/latest/
match = match_history[0]
# print('Match ID:', match.id)
p = match.participants[summoner]

# if you want to save memory, write to file instead of variables. 
# if you want to do analysis in python, save to variable for ease of use

# End of game stats
endGame= p.stats
gold_earned= endGame.gold_earned
gold_spent= endGame.gold_spent
total_damage= endGame.total_damage_dealt
total_damage_champs= endGame.total_damage_dealt_to_champions
vision_score= endGame.vision_score #maybe some kind of vision score weighted by minute? (should be exponential w/ gametime)
game_outcome= endGame.win
print("Won game?", game_outcome)
print("Gold earned=", gold_earned) # can now get all end of game stats

# Timeline stats; see page 43 of docs
timeData= p.timeline
cs_per_min = timeData.creeps_per_min_deltas #got it!
csd_per_min= timeData.cs_diff_per_min_deltas
dmgDiff_per_min= timeData.damage_taken_diff_per_min_deltas
xpDiff_per_min= timeData.xp_diff_per_min_deltas
print("CS diff/min=", csd_per_min)