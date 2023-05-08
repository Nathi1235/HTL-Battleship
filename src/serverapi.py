import sys, os
import User_Login as User_Login
from random import *
from fastapi import FastAPI

app = FastAPI()
playerdata = "E:/FSST\Repos/Battleship/HTL-Battleship/Resources/savefiles/player_data.txt"
chatlog = "E:/FSST/Repos/Battleship/HTL-Battleship/Resources/savefiles/chatlog.txt"

Players = []
gamerequests = []
game = 0

class player:                                                         #create player class 
    def __init__(self,username,wins=0,games=0,in_game = False,field = [],gameid = 0):
        self.username = username
        self.wins = wins
        self.games = games
        self.in_game = in_game
        self.field = field
        self.gameid = gameid

class gamerequest:
    def __init__(self,cname,oname,gameid,accepted = False):
        self.cname = cname
        self.oname = oname
        self.gameid = gameid
        self.accepted = accepted

def checkwin(field):
    for i in field:
        if (i == 1):
            return 0
        else:
            win = 1
    return win

@app.get("/userlogin")
async def login(username: str,password: str):
    userdata = User_Login.user_login(playerdata,username,password)
    if (userdata != 0):
        Players.append(player(userdata[0],userdata[1],userdata[1]+userdata[2]))
        userdata = 1
    return {userdata}

@app.get("/usernew")
async def login(username: str,password: str):
    userdata = User_Login.create_user(playerdata,username,password)
    return {userdata}

@app.get("/chat")
async def sendchat():
    try:
        savefile = open(chatlog, 'r')
        data = savefile.readlines()
        chat = ""
        for i in data:
            chat += str(i)
        savefile.close()
        return {chat}
    except:
        return {0}
    
@app.post("/chatmessage")
async def addchatmessage(username: str, message: str):
    try:
        savefile = open(chatlog, 'a')
        savefile.writelines(f"{username}: {message}\n")
        savefile.close()
        return {1}
    except:
        return {0}
    
@app.post("/addgamerequest")
async def addgamerequest(cname: str, oname: str):
    global game
    request = gamerequest(cname,oname,game)
    game += 1
    gamerequests.append(request)
    response = game - 1
    print(f"{request.cname},{request.oname},{request.gameid}")
    return {response}
    
@app.post("/delgamerequest")
async def delgamerequest(game: int):
    for i in gamerequests:
        if (i.gameid == game):
            i.cname = 0
            i.oname = 0
            i.gameid = 0
            print(f"{i.cname},{i.oname},{i.gameid}")
    return {1}

@app.get("/getgamerequests")
async def getgamerequests(oname: str):
    challengers = ""
    for i in gamerequests:
        if (i.oname == oname):
            if (i.accepted = True):
                
            challengers += f"{i.cname}~{i.gameid}~"
    return {challengers}

@app.post("/acceptgamerequest")
async def acceptgamerequests(game)
