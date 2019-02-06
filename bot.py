import argparse
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
CHANNEL = '##nubottest'
ADMINNAME = 'Nu2This'
EXITCODE = "bye " + NICK

ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

APIKEY = '***REMOVED***'
API = dota2api.Initialise(APIKEY)
DOTABUFF = re.compile(":http://www.dotabuff.com/matches\d+")

# Here we connect to the server using the port 6667
ircsock.connect((HOST, 6667))
# We are basically filling out a form with this line and saying to set all 
# the fields to the bot nickname.
ircsock.send(bytes("USER "+ NICK +" "+ NICK +" "+ NICK + " "
                   + NICK + "\n", "UTF-8"))
# assign the nick to the bot
ircsock.send(bytes("NICK "+ NICK +"\n", "UTF-8"))

def joinchan(chan): # join channel(s).
    ircsock.send(bytes("JOIN "+ CHANNEL +"\n", "UTF-8"))
    ircmsg = ""
    while ircmsg.find("End of /NAMES list.") == -1:
        ircmsg = ircsock.recv(2048).decode("UTF-8")
        ircmsg = ircmsg.strip('\n\r')
        print(ircmsg)


def ping(): # respond to server Pings.
    ircsock.send(bytes("PONG :pingis\n", "UTF-8"))
    print('pong')


def sendmsg(msg, target=CHANNEL): # sends messages to the target.
    ircsock.send(bytes("PRIVMSG "+ target +" :"+ msg +"\n", "UTF-8"))


if __name__ == '__main__':
    # Join the CHANNEL
    joinchan(CHANNEL)
    # Run the bot
    while True:
        # These lines listen to the channel
        ircmsg = ''
        ircmsg = ircsock.recv(2048).decode("UTF-8")
        ircmsg = ircmsg.strip('\n\r')
        print(ircmsg)
        # Get the name from the line and Check to make sure it isnt a private
        # message
        message = ''
        if ircmsg.find("PRIVMSG") != -1:
            name = ircmsg.split('!',1)[0][1:]
            message = ircmsg.split('PRIVMSG',1)[1].split(':',1)[1]
            print('name: ' + name)
        if message[:6] == 'PING :':
            ping()
        if message[:8] == '!matches':
            if getstuff.isRegisterd(name) == False:
                sendmsg('ID not found please !register')
            else:
                toSend = getstuff.getMatches(APIKEY, name, 5)
                for item in toSend:
                    sendmsg(item)
        if message[:9] == '!register':
            getstuff.getID(APIKEY, name)
            sendmsg('Registrashion Compreeto!')

        if message[:5] == '!quit':
            ircsock.send(bytes("QUIT \n", "UTF-8"))


   # parser = argparse.ArgumentParser()
   # parser.add_argument('name', type=str)
   # parser.add_argument('-register', action='store_true')

   # args = parser.parse_args()
   # if args.register:
   #     getstuff.getID(APIKEY, args.name)
   # else:
   #     getstuff.getMatches(APIKEY, args.name)
