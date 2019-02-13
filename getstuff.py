from tinydb import TinyDB, Query
from tinydb.operations import increment, set
import pudb
import dota2api
import requests
import json
import sys

db = TinyDB('db.json')
User = Query()

def score(name):
    """ Query the database for the user's score and return it to the bot as a
        string"""
    # If the user is in the database increment the score and then return the
    # value
    if db.search(User.Name==name):
        print('Name found')
        try:
            db.update(increment('score'), User.Name==name)
            return str(db.get(User.Name==name)['score'])
        except KeyError:
            db.update(set('score',1), User.Name==name)
            return str(db.get(User.Name==name)['score'])
    # If the user is not in the database, create entry and set score to 1
    else:
        print('Name not found')
        db.insert({'Name': name, 'score': 1})
        return str(db.get(User.Name==name)['score'])


def getID(APIKEY, name):
    """This function gets the steam ID of a person as long as the have a
    vanity URL. The steam ID is needed in order to use the dota2api"""
    IDAPI = ('http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/'
             '?key=' + APIKEY + '&vanityurl=' + name)
    response = requests.get(IDAPI)
    d2 = json.loads(response.content.decode('utf-8'))
    id = d2['response']['steamid']
    print('Steam ID:' + str(id))
    id32 = int(id) - 76561197960265728
    print(id32)
    print(id)
    # If the user is in the database update the record with STEAMID
    if db.search(User.Name==name):
        db.update({'STEAMID32': id32, 'STEAMID64': id}, User.Name==name)
        print('Updating user ' + name)
    # If the user is not in the database create record.
    else:
        db.insert({'Name': name, 'STEAMID32': id32, 'STEAMID64': id})
        print('Creating record for ' + name)


def isRegisterd(name):
    # If the user is in the id file get his steamID number
    found = False
    if db.search(User.Name==name):
            found = True
            try:
                db.get(User.Name==name)['STEAMID64']
                return db.get(User.Name==name)['STEAMID64']
            except KeyError:
                return False
    # If the user is not in the id file get it
    if found == False:
        print('ID not Found please !register...')
        return False

def getMatches(APIKEY, name, x):
    API = dota2api.Initialise(APIKEY)
    sendBack = []
    STEAMID64 = isRegisterd(name)
    # For some reason the dota2api gets the 32 bit steam Ids so we convert
    # the 64 bit one.
    STEAMID32 = int(STEAMID64) - 76561197960265728
    # dota2api get_match_history params
        # account_id (int, optional)
        # hero_id (int, optional)
        # game_mode (int, optional)
        # skill (int, optional)
        # min_players (int, optional)
        # league_id (int, optional)
        # start_at_match_id (int, optional)
        # matches_requested (int, optional)
        # tournament_games_only (str, optional)
    dotadata = API.get_match_history(account_id=STEAMID64, matches_requested=x)
    # For every item that returns in get_match_history api call
    for item in dotadata['matches']:
        # Get match details for them
        matchDetails = API.get_match_details(item['match_id'])
        # For every player in the match details, check and see if the account
        # ID matches the Query() STEAMID32
        for player in matchDetails['players']:
            if player['account_id'] == STEAMID32:
                pTeam = False
                winlose = 'Loss'
                radire = 'Dire'
                if player['player_slot'] < 5:
                    pTeam = True
                    radire = 'Radiant'
                if pTeam == matchDetails['radiant_win']:
                    winlose = 'Win!'
                sendBack.append(name + ' ' + winlose + ' ' + radire +
                                " {} {} K/D/A:{}/{}/{} "
                                "LH/D:{}/{} XPM:{} "
                                "GPM:{}".format(player['hero_name'],
                                                player['level'],
                                                player['kills'],
                                                player['deaths'],
                                                player['assists'],
                                                player['last_hits'],
                                                player['denies'],
                                                player['xp_per_min'],
                                                player['gold_per_min']))
    return sendBack








