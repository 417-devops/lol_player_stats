# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 16:19:50 2020

@author: Karl Roush and Elijah Smith
"""

import cassiopeia as cass
import json
from datetime import timedelta
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

def init_playerData(data_fileName, matchStats):
    with open(data_fileName, "w") as outfile: 
        json.dump(matchStats, outfile)
        outfile.close()
        
def getStats(match):
    # https://readthedocs.org/projects/cassiopeia/downloads/pdf/latest/
    p = match.participants[summoner]
    # End of game stats
    endGame = p.stats
    # #maybe some kind of vision score weighted by minute? (should be exponential w/ gametime)
    # Timeline stats; see page 43 of docs
    # currently only looking at 0-10 min mark
    timeData = p.timeline

    try:
        cs_per_min = timeData.creeps_per_min_deltas['0-10']
    except:
        cs_per_min = None
    
    try:
        csd_per_min = timeData.cs_diff_per_min_deltas['0-10']
    except:
        csd_per_min = None

    try:
        dmgDiff_per_min = timeData.damage_taken_diff_per_min_deltas['0-10']
    except:
        dmgDiff_per_min = None

    try:
        xpDiff_per_min= timeData.xp_diff_per_min_deltas['0-10']
    except:
        xpDiff_per_min = None
    
    match_stats= {}
    
    try:
        match_stats['MatchID'] = match.id
    except:
        match_stats['MatchID'] = None
    
    try:
        match_stats['gold_earned'] = endGame.gold_earned
    except:
        match_stats['gold_earned'] = None

    try:
        match_stats['gold_spent'] = endGame.gold_spent
    except:
        match_stats['gold_spent'] = None

    try:
        match_stats['total_damage'] = endGame.total_damage_dealt
    except:
        match_stats['total_damage'] = None

    try:
        match_stats['total_damage_champs'] = endGame.total_damage_dealt_to_champions
    except:
        match_stats['total_damage_champs'] = None
    
    try:
        match_stats['vision_score'] = endGame.vision_score
    except:
        match_stats['vision_score'] = None
    
    try:
        match_stats['Win'] = endGame.win
    except:
        match_stats['Win'] = None
    
    match_stats['cs_per_min'] = cs_per_min
    match_stats['csd_per_min'] = csd_per_min
    match_stats['dmgDiff_per_min'] = dmgDiff_per_min
    match_stats['xpDiff_per_min'] = xpDiff_per_min
    
    
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

#%% CREATING FILE TO SAVE PLAYER'S STATS
data_fileName= player_name + "_matchStats.json"

new_matchStats= {
    "MatchID": [None],
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
    
checkfile=Path("./"+data_fileName)
if not checkfile.is_file():
    print("\nPlayer stats file does not exist.")
    print("Creating initial stats file...")
    init_playerData(data_fileName, new_matchStats)

# old match stats     
with open(data_fileName, 'r') as openfile: 
    past_stats = json.load(openfile) 
    openfile.close()
    
#%% BEGIN ANALYZING MATCHES IN MATCH HISTORY
last_analyzed_matchID= past_stats["MatchID"][0]

#need to prepend stats so that the newest match stats are first in the list!
for match in match_history:
    if match.id == last_analyzed_matchID:
        break
    elif match.duration < timedelta(minutes=3, seconds= 15):
        # skip remakes
        pass
    else:
        # grab the stats from each match
        match_stats= getStats(match)
        for key, value in match_stats.items():  
            #append the match stats to the new_matchStats dictionary
            new_matchStats[key].append(value)
            
#%% APPEND THE STATS FROM THE NEW MATCHES TO FILE
for key, value in new_matchStats.items():
    # combined=itertools.chain(new_stats[key], saved_stats[key])
    combined= new_matchStats[key]+past_stats[key]
    past_stats[key]= combined
    
with open(data_fileName, 'w') as output_data_file: 
    json.dump(past_stats, output_data_file) 
    output_data_file.close()        
