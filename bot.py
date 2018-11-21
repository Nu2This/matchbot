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
match_id = '4173686982'
print(API.get_match_details(match_id=match_id))
