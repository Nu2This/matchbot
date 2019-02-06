import pudb
import dota2api
import requests
import json
import sys



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
    with open('id.txt', 'a') as f:
        f.write(name + ' ' + str(id32) +  ' ' + id + '\n')


def isRegisterd(name):
    with open('id.txt', 'r') as f:
        # If the user is in the id file get his steamID number
        found = False
        for line in f:
            if name in line:
                found = True
                id = line.split()[2]
                return id
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
    for item in dotadata['matches']:
        matchDetails = API.get_match_details(item['match_id'])
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








