import dota2api
import json
import re
import socket
from time import sleep


HOST = 'chat.freenode.net'
PORT = '6667'
NICK = 'Nubot'
IDENT = 'Nubot'
CHANNEL = '#dotanoobs'


s = socket.socket()
API = dota2api.Initialise('***REMOVED***')
DOTABUFF = re.compile(":http://www.dotabuff.com/matches\d+")


def getID(name):
    """This function gets the steam ID of a person as long as they
have a vanity URL. The steam ID is needed in order to use the dota2api"""

    import requests
    IDAPI = ('http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/'
             '?key=***REMOVED***&vanityurl='
             + name
             )

    response = requests.get(IDAPI)
    data = response.content
    d2 = json.loads(data)
    id = d2['response']['steamid']
    print('Steam ID:' + id)

    return id


getID('binaryatrocity')
