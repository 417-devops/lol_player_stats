# lol_player_stats 
### A Tool for Pulling Player Match Statistics
This tool is designed to pull data from a given player's matches, for later analysis. It also supports displaying numerous statistics in a graphical format. Data is saved to a .JSON file for future retrieval, allowing for caching of data to prevent excessive API calls.

```fetch_rawData.py``` retrieves the player's data.

```data_analysis.py``` calculates various statistics over a specified number of matches and displays them in a graphical format.

# How to use
1. **Retrieve the player data**
    1. Running ```data_analysis.py``` should automatically pull data for the specified player
    2. If not, run ```fetch_rawData.py``` seperately first
2. **Analyze the data**
    1. ```data_analysis.py``` already does some preliminary analysis
	  2. Feel free to add whatever calculated statistics and methods you want here
	  3. If you want to pull additional match statistics beyond what is already recorded, refer to Cassiopeia [documentation](https://readthedocs.org/projects/cassiopeia/downloads/pdf/latest/) to modify the ```fetch_rawData.py``` file.
3. **Using data in the future**
    1. All of the requested player data is stored in a .JSON file with the format: player_name + "_matchStats.json"
	  2. Saving the data this way allows for caching and easy future use

# Questions?
Feel free to contact either of the authors through the information posted on their GitHub profile!
- Karl Roush: [@karoush](https://github.com/karoush)
- Elijah Smith: [@ElijahKSmith](https://github.com/ElijahKSmith)
