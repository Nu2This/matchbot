import dota2api
import requests
import json



def getID(APIKEY, name):
    """This function gets the steam ID of a person as long as the have a
    vanity URL. The steam ID is needed in order to use the dota2api"""

    IDAPI = ('http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/'
'?key=' + APIKEY + '&vanityurl=' + name)
    response = requests.get(IDAPI)
    d2 = json.loads(response.content.decode('utf-8'))
    id = d2['response']['steamid']
    print('Steam ID:' + id)
    with open('id.txt', 'a') as f:
        f.write(name + ' ' + id + '\n')


def getMatches(APIKEY, name):
    API = dota2api.Initialise(APIKEY)
    with open('id.txt', 'r') as f:
        # If the user is in the id file get his steamID number
        found = False
        for line in f:
            if name in line:
                found = True
                id = line.split()[1]
                print(line.split()[1])
        if found == False:
            print('ID not Found Searching...')
            getID(APIKEY, name)
    print(API.get_match_history(account_id=id))
