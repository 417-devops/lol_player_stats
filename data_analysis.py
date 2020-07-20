# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 15:38:57 2020

@author: Karl Roush and Elijah Smith
"""

# For getting the raw data
from fetch_rawData import * #raw data script

#For analysis
import matplotlib.pyplot as plt
import numpy as np
from statistics import mean 

def calc_average(data):
    clean_data=list(filter((None).__ne__, data))
    return mean(clean_data)

def make_plot(x, data, ylabel, title):
    file_title = title.replace(": ", "_")
    fig, ax = plt.subplots()
    marker_style = dict(color='tab:blue', marker='o', markersize=4)
    plt.plot(x, data, linestyle='--', color='tab:blue')
    plt.plot(x, data, linestyle='', marker='o', fillstyle='none', color='black')
    
    plt.xticks(np.arange(min(x), max(x)+1, 2))
    # ax.set_ylim(top=1.1*max(list(filter((None).__ne__, data))))
    ax.set_ylabel(ylabel)
    ax.set_xlabel('Game, 0= most recent')
    ax.set_title(title)
    
    average= round(calc_average(data),2)
    note= 'Average over '+ str(num_matches)+' games: '+str(average)
    plt.text(-0.5, 0.98*max(list(filter((None).__ne__, data))), note, fontsize=10, bbox=dict(facecolor='green', alpha=0.75))
    plt.savefig(file_title+".png")
    
#%% INITIALIZATION
start_time = time.time()

cass.set_riot_api_key(getAPI_key()) #or replace with your own api key
cass.set_default_region("NA") #or replace with another region

#%% SETTING THE PLAYER TO BE ANALYZED
player_name= "C9 Zven"
player_region= "NA"
summoner = Summoner(name=player_name, region=player_region)
    
#%% GET THE PLAYER DATA
getPlayerData(summoner, player_name, player_region)

#%% NOW WE MAKE PRETTY GRAPHS
#note the graph gets broken if the API had returned None for a field
data_fileName= player_name + "_matchStats.json"
with open(data_fileName, 'r') as openfile: 
    past_stats = json.load(openfile) 
    openfile.close()

num_matches= 20
x= np.linspace(0,num_matches,num_matches)

#%% GRAPH: Damage per gold
dmg_per_gold= np.divide(past_stats['total_damage'][0:num_matches],past_stats['gold_spent'][0:num_matches])
ylabel= 'Damage/Gold'
title= player_name+': Damage per gold spent'
make_plot(x, dmg_per_gold, ylabel, title)

#%% GRAPH: CS per min
cs_per_min= past_stats['cs_per_min'][0:num_matches]
ylabel='CS/min'
title= player_name+': CS per minute'

make_plot(x, cs_per_min, ylabel, title)

#%% GRAPH: CSD at 10min
csd_10min= past_stats['csd_per_min'][0:num_matches]
ylabel='CSD'
title= player_name+': CSD at 10min'

make_plot(x, csd_10min, ylabel, title)

#%% GRAPH: Vision score
vision_score= past_stats['vision_score'][0:num_matches]
ylabel='Vision Score'
title= player_name+': Vision Score'

make_plot(x, vision_score, ylabel, title)

#%% RUNTIME CALCULATION
print("\n--- %s seconds ---" % (time.time() - start_time))
