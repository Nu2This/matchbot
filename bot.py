import dota2api
import requests
import json
import re
import socket
import getstuff
from time import sleep


HOST = 'chat.freenode.net'
PORT = '6667'
NICK = 'Nubot'
IDENT = 'Nubot'
CHANNEL = '#dotanoobs'


s = socket.socket()
APIKEY = '***REMOVED***'
API = dota2api.Initialise(APIKEY)
DOTABUFF = re.compile(":http://www.dotabuff.com/matches\d+")


#getstuff.getID(APIKEY, 'Nu2This')
getstuff.getMatches(APIKEY, 'UnoPolak')
