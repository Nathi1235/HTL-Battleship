import sys, os
import User_Login as User_Login
import networking as networking
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *
from random import *
import threading

IP = "10.10.218.103"
PORT = 65500
Players = []
path = "HTL-Battleship/Resources/savefiles/player_data.txt"
game = 0

class player:                                                         #create player class 
    def __init__(self,username,conn,wins=0,games=0,in_game = False,field = [],gameid = 0):
        self.username = username
        self.wins = wins
        self.games = games
        self.conn = conn
        self.in_game = in_game
        self.field = field
        self.gameid = gameid

def checkwin(field):
    for i in field:
        if (i == 1):
            return 0
        else:
            win = 1
    return win

def loginthread():
    while(1):
        print("in thread")
        client = server.server_Listen()
        data = server.receive(client)
        if (data[0] == 'l'): #login case
            data = data[1]                                            #remove packet identifier
            userdata = User_Login.user_login(path,data[0],data[1])     #get user data
            packet = ('l',userdata)
            server.send(client,packet)                       #send login sucessfull/unsuccesfull to client
            if (userdata != 0):
                playeradd = player(userdata[0],client,userdata[1],userdata[1]+userdata[2])
                Players.append(playeradd)  #create player from userdata and add to playerlist
                t = threading.Thread(target=lambda:messagethread(playeradd))
                t.start()
            

        elif (data[0] == 'n'): #new user case
            data = data[1]
            userdata = User_Login.create_user(path,data[0],data[1])     #create new user
            packet = ('n',userdata)
            server.send(client,packet)    #send user creation sucessfull/unsuccesfull to client
            Players.append(player(data[0],client))    #create player from userdata and add to playerlist

def messagethread(Player):
    while(1):
        client = Player.conn
        print(Player.conn)
        data = server.receive(client)
        print(data)
        if(data != None):
            if (data[0] == 'c'): #chat message case
                data = data[1]
                for i in Players:       #send chat message to all players
                    packet = ('c',data)
                    server.send(i.conn,packet)
            
            elif (data[0] == 'g'): #gamerequest case 
                data = data[1]
                usernamep1 = data[0]   #challenger
                usernamep2 = data[1]   #challenge recipient
                for i in Players:
                    if (i.username == usernamep2):
                        if (i.in_game):       #if recipient is in game already auto decline request
                            server.send(client,0)
                        else:                  #send request to recipient and send ack to challenger
                            server.send(client,1)   
                            packet = ('g',usernamep1)
                            server.send(i.conn,packet)
            #elif (data[0] == 'm'): #matchmaking case

def gamethread():


        if (data[0] == 'r'): #gamerequest accepted/declined case 
            data = data[1]
            usernames = [data[0],data[1]]
            for j in usernames:                           #find connections for both players
                for i in Players:
                    if (i.username == usernames[j]):
                        packet = ('r',usernames[j-1])    #send ack for game and name of opponent
                        server.send(i.conn,packet)
                        i.in_game = True                 #set ingame status to true to prevent further requests
                        i.gameid = game                    #set gameid to know which players are opponents
                        game += 1
            
        elif (data[0] == 'p'): #ship placement cords case
            data = data[1]
            for i in Players:                       #assign fields to player
                if(i.username == data[0]):
                    i.field = data[1]

        elif (data[0] == 's'): #shot cords midgame case
            data = data[1]
            for i in Players:                      #find gameid from username
                if(i.username == data[0]):
                    gameid = i.gameid
                    client2 = i.conn
            for i in Players:                     #find opponent with gameid
                if(i.gameid == gameid):
                    field = i.field
            shot = data[1]
            hit_or_miss = field[shot[0]][shot[1]]             #first is x cord, second is y cord
            if hit_or_miss:
                packet = ('o',1,shot)                      #tell players whos turn it is t = your turn
                packet2 = ('t',1,shot)                      #also send shot cords and whether it hit to both players
                server.send(client,packet)  
                server.send(client2,packet2)                   
                field[shot[0]][shot[1]] = 0                 #if a ship was hit set its cord to zero
            else:
                packet = ('o',shot)
                packet2 = ('t',0,shot)
                server.send(client,packet)
                server.send(client2,packet2)                        
            if(checkwin(field)):                   #check if the shot ended the game
                server.send(client,'w')             #send win/loss
                server.send(client2,'l')
            else:
                server.send(client,'1')         #send continue
                server.send(client2,'1')



if __name__ == "__main__" :
    server = networking.Server_Net(IP,PORT)
    t = threading.Thread(target=loginthread)
    t.start()



