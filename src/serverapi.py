import User_Login as User_Login
from random import *
from fastapi import FastAPI
from datetime import datetime
#import time
#import threading

app = FastAPI()
playerdata = "D:/Schule/4AHEL/FSST/HTL-Battleship/GITHUB/HTL-Battleship/Resources/savefiles/player_data.txt"
chatlog = "D:/Schule/4AHEL/FSST/HTL-Battleship/GITHUB/HTL-Battleship/Resources/savefiles/chatlog.txt"

Players = []
gamerequests = []
game = 0

class player:                                                         #create player class 
    def __init__(self,username,wins=0,games=0,in_game = False,field = [],gameid = 0,turn = False):
        self.username = username
        self.wins = wins
        self.games = games
        self.in_game = in_game
        self.field = field
        self.gameid = gameid
        self.turn = turn

class gamerequest:
    def __init__(self,cname,oname,gameid,accepted = False,winner = ""):
        self.cname = cname
        self.oname = oname
        self.gameid = gameid
        self.accepted = accepted
        self.winner = winner

def checkwin(field):
    for i in field:
        if (i == 1):
            return 0
        else:
            win = 1
    return win

'''
def show_stats():
        for i in gamerequests:
            print(f"cname={i.cname},oname={i.oname},gameid={i.gameid},accepted={i.accepted}")
        for j in Players:
            print(f"username={j.username},wins={j.wins},games={j.games},in_game={j.in_game},field={j.field},gameid={j.gameid},turn={j.turn}")
        #time.sleep(10)

Players.append(player("Nahi"))
Players.append(player("mani"))
for i in Players:

t = threading.Thread(target=lambda:show_stats())
t.start()
'''

@app.get("/userlogin")      #works
async def login(username: str,password: str):
    userdata = User_Login.user_login(playerdata,username,password)
    if (userdata != 0):
        Players.append(player(userdata[0],int(userdata[1]),int(userdata[1])+int(userdata[2])))
        userdata = 1
    return {userdata}

@app.get("/usernew")    #works
async def login(username: str,password: str):
    userdata = User_Login.create_user(playerdata,username,password)
    if (userdata == 1):
        userdata = User_Login.user_login(playerdata,username,password)
        print(userdata)
        Players.append(player(userdata[0],int(userdata[1]),int(userdata[1])+int(userdata[2])))
        userdata = 1
    return {userdata}

@app.get("/activeplayers",)    #works
async def playerlist(selfname: str):
    returnstr = ""
    for i in Players:
        if (i.username != selfname):
            print (i.games)
            returnstr += f"{i.username},{i.wins},{i.games}~"
    return {returnstr}

            
@app.get("/chat")    #works
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
    
@app.post("/chatmessage")   #works
async def addchatmessage(username: str, message: str):
    try:
        savefile = open(chatlog, 'a')
        print("test")
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        savefile.writelines(f"{username}[{current_time}]: {message}\n")
        savefile.close()
        return {1}
    except:
        return {0}
    
@app.post("/addgamerequest")     #works
async def addgamerequest(cname: str, oname: str):
    global game
    for i in Players:
        if (i.username == oname):
            if (i.in_game):
                return {0}                             #return 0 if challenged player is already in game
    request = gamerequest(cname,oname,game)
    game += 1
    gamerequests.append(request)
    response = game - 1
    return {response}
    
@app.post("/delgamerequest")  #works
async def delgamerequest(game: int):
    for i in gamerequests:
        if (i.gameid == int(game)):
            i.cname = "#"
            i.oname = "#"
            i.gameid = "#"
    return {1}

@app.get("/getgamerequests")   #works
async def getgamerequests(oname: str):
    challengers = ""
    for i in gamerequests:
        if (i.oname == oname):
            if(i.accepted == True):
                return {i.gameid,i.cname,i.oname}
            else:    
                challengers += f"{i.cname},{i.gameid}~"
    return {challengers}

@app.post("/acceptgamerequest")   #works
async def acceptgamerequests(game = int):
    for i in gamerequests:
        if (int(i.gameid) == int(game)):
            i.accepted = True
            return {1}
    return {0}

@app.get("/checkifaccepted")
async def checkifaccepted(game = int):
    for i in gamerequests:
        if (int(i.gameid) == int(game)):
            if(i.accepted):
                return {1}
    return {0}


@app.post("/sendplacedships")        #works
async def playerfield(username: str,field: str):
    fieldlist = []
    for char in field:
        if (char != "~"):
            fieldlist.append(int(char))
    for i in Players:
        if (username == i.username):
            i.field = fieldlist
            return{1}
    return{0}

@app.post("/startgame")     #works
async def startgame(username: str,game = int):
    checkstart = 0
    for i in Players:
        if (username == i.username):
            i.in_game = True
    for p in Players:
        if (p.gameid == int(game)):
            if (p.in_game):
                checkstart += 1
    print(checkstart)
    if (checkstart == 2):
        for j in Players:
            if (username == j.username):
                j.turn = True
                return {1}
    else:
        return {0}
    
@app.get("/askturn")          #works
async def askturn(username: str):
    for i in Players:
        if (username == i.username):
            return {i.turn}
    return {"Error"}

@app.post("/sendshot")
async def shottarget(cord: int,targetname: str):
    cord = int(cord)
    for i in Players:
        if (i.username == targetname):
            field = i.field
    target = field[cord]
    if (target != "#"):
        target = "#"
        checkdestroyed = True
        for s in field:
            if (field[s] == target):
                checkdestroyed = False
                break
        return {target,checkdestroyed}
    else:
        return {target}
    
@app.get("/checkwin")
async def checkwin(game: int, username: str):
    game = int(game)
    opponents = []
    for i in Players:
        if (i.gameid == game):
            opponents.append(i)
    for p in opponents:
        win = True
        for s in p.field:
            if (s != '#'):
                win = False
                break
        if (win):
            for g in gamerequests:
                if (g.gameid == game):
                    g.winner = p.username
            break

@app.post("/endgame")
async def endgame(game: int):
    try:
        game = int(game)
        opponents = []
        for i in Players:
            if (i.gameid == game):
                opponents.append(i)
        for g in gamerequests:
            if (g.gameid == game):
                gamerequest = g
        for p in opponents:
            p.games += 1
            if (gamerequest.winner == p.username):
                p.wins += 1
        gamerequest.cname = "#"
        gamerequest = "#"
        gamerequest = "#"
        return {1}
    except:
        return {0}
