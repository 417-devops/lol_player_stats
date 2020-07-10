# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 16:19:50 2020

@author: Karl Roush and Elijah Smith
"""

import cassiopeia as cass
import json
from pathlib import Path
from cassiopeia import Summoner, Match
from cassiopeia.data import Season, Queue

def getAPI_key():
    #reads the API key from local file
    file= open("../api_key.txt","r")
    return file.read()

def make_matchID_list(match_history):
    #converts t
    matchID_list=[]
    for item in match_history:
        matchID_list.append(item.id)
    return matchID_list

def init_playerData(data_fileName):
    matchStats= {
        "matchIDs": [],
        "gold_earned": [],
        "gold_spent": [],
        "total_damage": [],
        "total_damage_champs": [],
        "vision_score": [],
        "Win": [],
        "cs_per_min": [],
        "csd_per_min": [],
        "dmgDiff_per_min": [],
        "xpDiff_per_min": []
        }
    with open(data_fileName, "w") as outfile: 
        json.dump(matchStats, outfile)
        outfile.close()
        
def getStats(match):
    # https://readthedocs.org/projects/cassiopeia/downloads/pdf/latest/
    p = match.participants[summoner]
    # End of game stats
    endGame= p.stats
    # #maybe some kind of vision score weighted by minute? (should be exponential w/ gametime)
    # Timeline stats; see page 43 of docs
    # currently only looking at 0-10 min mark
    timeData= p.timeline
    cs_per_min = timeData.creeps_per_min_deltas['0-10']
    csd_per_min= timeData.cs_diff_per_min_deltas['0-10']
    dmgDiff_per_min= timeData.damage_taken_diff_per_min_deltas['0-10']
    xpDiff_per_min= timeData.xp_diff_per_min_deltas['0-10']
    
    match_stats= {
        "gold_earned": endGame.gold_earned,
        "gold_spent": endGame.gold_spent,
        "total_damage": endGame.total_damage_dealt,
        "total_damage_champs": endGame.total_damage_dealt_to_champions,
        "vision_score": endGame.vision_score,
        "Win": endGame.win,
        "cs_per_min": cs_per_min,
        "csd_per_min": csd_per_min,
        "dmgDiff_per_min": dmgDiff_per_min,
        "xpDiff_per_min": xpDiff_per_min
        }
    return match_stats
    
#%% INITIALIZATION
cass.set_riot_api_key(getAPI_key()) #or replace with your own api key
cass.set_default_region("NA") #or replace with another region

with open('cache.json', 'r') as cache_file:
    cache = json.load(cache_file)
    cache_file.close()

#%% SETTING THE PLAYER TO BE ANALYZED
player_name= "RebirthNA"
player_region= "NA"
summoner = Summoner(name=player_name, region=player_region)

#%% GET THE MATCH HISTORY
# for soloQ
match_history = summoner.match_history(queues={cass.Queue.ranked_solo_fives})
matchID_list= make_matchID_list(match_history)

# =============================================================================
# Current implementation is as follows:
# 1. Pull the list of match ids
# 2. Store the most recent matchID (probably index 0) to be cached later
# 3. for matchID in matchID_list:
#     3.1. Check IF the current matchID in list is equal to one in cache
#         3.1.1. True, break from loop and discard current and further matchIDs
#         3.1.2. False, append to list of new matchIDs that need to be tracked
# 4. Check to see IF any new matchIDs were actually pulled
#     4.1. True, set the cache last matchID to be the new last matchID
#     4.2. False, don't. (Maybe we can skip the rest of the calculation code and just reprint cache stuff if false)
# =============================================================================
new_last_matchID = matchID_list[0]
new_matchIDs = []

for matchID in matchID_list:
    if matchID == cache['last-matchID']:
        break
    else:
        new_matchIDs.append(matchID)

if len(new_matchIDs) == 0:
    pass
else:
    cache['last-matchID'] = new_last_matchID

#%% CREATING FILE TO SAVE PLAYER'S STATS
data_fileName= player_name + "_matchStats.json"

checkfile=Path("./"+data_fileName)
if not checkfile.is_file():
    print("\nPlayer stats file does not exist.")
    print("Creating initial stats file...")
    init_playerData(data_fileName)
     
with open(data_fileName, 'r') as openfile: 
    past_stats = json.load(openfile) 
    openfile.close()
    
# =============================================================================
# #%% BEGIN ANALYZING MATCHES IN MATCH HISTORY
# with open("cache.json", 'r') as openfile: 
#     json_object = json.load(openfile) 
#     openfile.close()
# last_analyzed_matchID= json_object["last-matchID"]
# 
# #need to prepend stats so that the newest match stats are first in the list!
# for match in match_history:
#     if match.id == last_analyzed_matchID:
#         #reaching the last analyzed match breaks the loop
#         break
#     else:
#         #grab the stats from each match
#         past_stats["matchIDs"].append(match.id)
#         match_stats= getStats(match)
#         for key, value in match_stats.items():    
#             past_stats[key].append(value)
#             
# #%% APPEND THE STATS FROM THE NEW MATCHES TO FILE
# with open(data_fileName, 'w') as output_data_file: 
#     json.dump(past_stats, output_data_file) 
#     output_data_file.close()        
# 
# =============================================================================
#%% WRITE TO CACHE
# Throughout the script we should be writing to the cache dictionary that was created by reading cache.json at the start
# Here it is written back to file
# Done at the end to prevent dirty data from being written midway in the event of a crash
with open('cache.json', 'w') as outfile:
    json.dump(cache, outfile)
    outfile.close()