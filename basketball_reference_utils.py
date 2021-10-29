# import modules 
from basketball_reference_scraper.players import get_stats, get_player_headshot
import logging
import random

# define constants 
STATS = ['PTS', 'AST', 'TRB', 'STL', 'BLK', 'TOV', 'MP', 'FG%']
COLUMNS = ['SEASON', 'TEAM', 'POS'] + STATS
PLAYER_NAMES = [
    'Kobe Bryant',
    'Tim Duncan',
    'Dirk Nowitzki', 
    'Dwyane Wade', 
    'Kevin Durant',
    'Stephen Curry',
    'Nikola Jokić',
    'Giannis Antetokounmpo',
    'Kevin Durant',
    'Luka Dončić',
    'Damian Lillard',
    'Chris Paul',
    'James Harden',
    'Jayson Tatum',
    'LeBron James',
    'Jimmy Butler',
    'Anthony Davis',
    'Rudy Gobert',
    'Bradley Beal',
    'Bam Adebayo',
    'Devin Booker',
    'Joel Embiid',
    'Paul George',
    'Kyrie Irving',
    'Kawhi Leonard',
    'Ben Simmons',
    'Zion Williamson',
    'Karl-Anthony Towns',
    'Donovan Mitchell',
    'Jaylen Brown'
]

def get_player_info(player_name, playoffs=False, career=False): 
    ''' 
    Function to scrape the stats of an NBA player from 
    https://www.basketball-reference.com/. 

    Params: 
    player_name (str) - full name of player 
    playoffs (bool) - True if considering playoffs stats, False if not 
    career (bool) - True if considering career stats, False if not 

    Returns: 
    player_stats (pd.DataFrame) - DataFrame of player stats 
    player_headshot (str) - URL of image of player's head 
    '''

    # initialize player stats and headshot 
    player_stats, player_headshot = None, None

    # get player stats 
    try: 
        player_stats = get_stats(player_name, playoffs=playoffs, career=career, 
            ask_matches=False)
        player_stats = player_stats[COLUMNS]
        player_stats.insert(0, 'NAME', player_name)
    except: 
        logging.error('Could not get player info, provided name might be ' 
            + 'invalid')
        
    # get player headshot 
    try: 
        player_headshot = get_player_headshot(player_name, ask_matches=False)
    except: 
        logging.error('Could not get player headshot, provided name might be ' 
            + 'invalid')
    
    # return player stats and player headshot 
    return player_stats, player_headshot 

def get_specific_pair(player_name1, player_name2, season1, season2, 
    playoffs=False, career=False): 
    '''
    Function to get a pair of stats to compare between two specific NBA 
    players. 

    Params: 
    player_name1 (str) - full name of player 1
    player_name2 (str) - full name of player 2
    season1 (str) - season for player 1 in format YYYY-YY
    season2 (str) - season for player 2 in format YYYY-YY
    playoffs (bool) - True if considering playoffs stats, False if not 
    career (bool) - True if considering career stats, False if not

    Returns: 
    player_stats1 (pd.DataFrame) - DataFrame of player 1 stats 
    player_headshot1 (str) - URL of image of player 1's head 
    player_stats2 (pd.DataFrame) - DataFrame of player 2 stats 
    player_headshot2 (str) - URL of image of player 2's head 
    '''

    # get player1 stats for the provided season 
    player_stats1, player_headshot1 = get_player_info(player_name1, 
        playoffs=playoffs, career=career)
    player_stats1 = player_stats1.loc[player_stats1['SEASON'] == season1]
    if len(player_stats1) == 0: 
        logging.warning(player_name1 + ' did not play during the ' 
            + season1 + 'season')

    # get player 2 stats for the provided season 
    player_stats2, player_headshot2 = get_player_info(player_name2, 
        playoffs=playoffs, career=career)
    player_stats2 = player_stats2.loc[player_stats2['SEASON'] == season2]
    if len(player_stats2) == 0: 
        logging.warning(player_name2 + ' did not play during the ' 
            + season2 + ' season')

    # return player stats and headshots 

    print("Player_stats1")
    print(player_stats1)
    print("Player_stats2")
    print(player_stats2)
    return player_stats1, player_headshot1, player_stats2, player_headshot2

def get_random_pair(playoffs=False, career=False):
    '''
    Function to get a pair of stats to compare between two random NBA players. 

    Params: 
    playoffs (bool) - True if considering playoffs stats, False if not 
    career (bool) - True if considering career stats, False if not 

    Returns: 
    player_stats1 (pd.DataFrame) - DataFrame of player 1 stats 
    player_headshot1 (str) - URL of image of player 1's head 
    player_stats2 (pd.DataFrame) - DataFrame of player 2 stats 
    player_headshot2 (str) - URL of image of player 2's head
    '''

    # randomly select players' names 
    players = random.sample(PLAYER_NAMES, 2)
    player_name1 = players[0] 
    player_name2 = players[1] 

    # get player1 stats for a random season 
    player_stats1, player_headshot1 = get_player_info(player_name1, 
        playoffs=playoffs, career=career)
    player_stats1 = player_stats1.sample() 

    # get player2 stats for a random season 
    player_stats2, player_headshot2 = get_player_info(player_name2, 
        playoffs=playoffs, career=career)
    player_stats2 = player_stats2.sample() 

    # return player stats and headshots 

    return player_stats1, player_headshot1, player_stats2, player_headshot2


get_specific_pair('Stephen Curry', 'Giannis Antetokounmpo', '2018-19', '2018-19')