from fastapi import FastAPI
import threading
import sys, os
import User_Login as User_Login
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *
from random import *
import time
import requests
from login_page import login_register_window

url = "http://127.0.0.1:8000/"

Buttons = []
Headers = []
Players = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
reqs = [0,0,0,0,0]
layouts = []
Datalabels = []
Challengebuttons = []
gamereqlabels = []
game = None
gameaccepted = False

class player:
    def __init__(self, username = "--------",wins = 0,games = 0):
        self.username = username
        self.wins = wins
        self.games = games

class req:
    def __init__(self,oname = "--------",gameid = -1):
        self.oname = oname
        self.gameid = gameid

class getchat(QThread):
    def __init__(self,chat):
        super(getchat, self).__init__()
        self.chat = chat
        self.data_list = []

    def run(self):
        global inShipplacement
        while not inShipplacement:
            # API
            response = requests.get(url+"chat")
            data = response.json()

            # Daten zur Liste hinzufügen
            #self.data_list.append(data)

            datastr = ""
            for i in data:
                datastr += i    
            self.chat.setText(datastr)
            # TODO Daten GUI übergeben

            # 5 Sekunden warten
            time.sleep(5)

class getplayers(QThread):
    def __init__(self):
        super(getplayers, self).__init__()
        self.data_list = []

    def run(self):
        global inShipplacement
        while not inShipplacement:
            #get username from client
            # API
            global username
            response = requests.get(url+"activeplayers"+f"?selfname={username}")
            data = response.json()
            playerlist = []
            
            for fullstring in data:
                string2 = fullstring.split("~")
                for playerstring in string2:
                    string3 = playerstring.split(",")
                    playerlist.append(string3)
            #fill playerlist with player from api and rest with default
            j = 0
            for i in playerlist:
                if (i != ['']):
                    Players[j] = player(i[0],int(i[1]),int(i[2]))
                    j += 1
            j = 0
            for i in Players:
                if (i == 0):
                    Players[j] = player()
                j += 1

            # TODO Daten GUI übergeben
            j = 0
            for i in Datalabels:
                i[0].setText(Players[j].username)
                i[1].setText(f"{Players[j].wins}")
                i[2].setText(f"{Players[j].games}")
                i[3].setText(calc_winrate(Players[j]))
                Challengebuttons[j].playername = Players[j].username
                Challengebuttons[j].update_Button()
                j += 1

            # 10 Sekunden warten
            time.sleep(10)

class getgamereqs(QThread):
    def __init__(self):
        super(getgamereqs, self).__init__()
        self.data_list = []

    def run(self):
        global inShipplacement
        while not inShipplacement:
            #get username from client
            # API
            global username
            response = requests.get(url+"getgamerequests"+f"?oname={username}")
            data = response.json()
            reqlist = []
            for fullstring in data:
                string2 = fullstring.split("~")
                for playerstring in string2:
                    string3 = playerstring.split(",")
                    reqlist.append(string3)
            j = 0
            for i in reqlist:
                if (i != ['']):
                    reqs[j] = req(i[0],int(i[1]))
                    j += 1
            j = 0
            for i in reqs:
                if (i == 0):
                    reqs[j] = req()
                j += 1

            # TODO Daten GUI übergeben
            j = 0
            for i in gamereqlabels:
                i.setText(f"Challenge from {reqs[j].oname}")
                j += 1
            j = 0  
            for i in Buttons:
                if (j > 14):
                    if (j%2 == 0):
                        i.gameid = reqs[int(j-(18+((j-18)/2)))].gameid
                        print("gameid",i.gameid)
                    elif (j%2 == 1):
                        i.gameid = reqs[int(j-(17+((j-17)/2)))].gameid
                        print("gameid",i.gameid)
                j +=1

            # 2 Sekunden warten
            time.sleep(2)
            
        

class Playerpage(QMainWindow):
    def __init__(self):
        super(Playerpage, self).__init__()

        self.setWindowTitle("Players")
        self.setFixedSize(1920,1080)
        mainlayout = QHBoxLayout()
        playerlayout = QGridLayout()
        chatlayout = QVBoxLayout()
        gamerequests = QGridLayout()
        exitbox = QHBoxLayout()
        queuebox = QHBoxLayout()
        mainlayout.addLayout(playerlayout)
        mainlayout.addLayout(chatlayout)
        self.move(0,0)
        layouts.append(mainlayout)
        layouts.append(playerlayout)
        layouts.append(chatlayout)
        layouts.append(exitbox)
        layouts.append(gamerequests)
        layouts.append(queuebox)
        for i in layouts:
            i.setSpacing(5)
            i.setContentsMargins(10,5,0,10)

        Headers.append(QLabel("Player"))
        Headers.append(QLabel("Games won"))
        Headers.append(QLabel("Games played"))
        Headers.append(QLabel("Win %"))
        x = 0
        for i in Headers:
            i.setFont(QFont("Arial",20))
            playerlayout.addWidget(i,0,x)
            i.setAlignment(Qt.AlignmentFlag.AlignCenter)
            i.setFixedSize(220,47)
            x += 1 

        playershow_thread = getplayers()
        playershow_thread.start()
        time.sleep(1)
        j = 0
        for i in Players:
            Playerdata = []
            Playerdata.append(QLabel(i.username))
            Playerdata.append(QLabel(f"{i.wins}"))
            Playerdata.append(QLabel(f"{i.games}"))
            Playerdata.append(QLabel(calc_winrate(i)))
            for x in Playerdata:
                x.setFont(QFont("Arial",15))
                x.setAlignment(Qt.AlignmentFlag.AlignCenter)
                x.setFixedSize(220,47)
            Datalabels.append(Playerdata)
            playerlayout.addWidget(Playerdata[0],j+1,0)
            playerlayout.addWidget(Playerdata[1],j+1,1)
            playerlayout.addWidget(Playerdata[2],j+1,2)
            playerlayout.addWidget(Playerdata[3],j+1,3)
            challengebutton = Challengebutton(i.username)
            Challengebuttons.append(challengebutton)
            playerlayout.addWidget(challengebutton,j+1,4)
            j += 1
        
        exitbox.setContentsMargins(0,10,0,0)
        exitbox.addWidget(Back_to_login_button())
        chatlayout.addLayout(exitbox)

        chatlayout.setSpacing(0)
        chatlayout.setContentsMargins(10,15,0,10)
        chatheader = QLabel("Global Chat")
        chatheader.setAlignment(Qt.AlignmentFlag.AlignTop)
        chatinput = QLineEdit("Enter message...")
        chatheader.setFont(QFont("Arial",25))
        chatinput.setFont(QFont("Arial",15))
        chatlayout.addWidget(chatheader)
        chatwindow = Scroll_window(self)
        str = "test \n"
        for i in range(1000):
            str += "test \n"
        chatwindow.setText(str)
        chat = chatwindow
        chatlayout.addWidget(chatwindow)
        chatheader.setFixedSize(650,100)
        chatinput.setFixedWidth(650)
        chatlayout.addWidget(chatinput)

        chat_thread = getchat(chat)
        chat_thread.start()

        gamerequests.setContentsMargins(0,10,0,0)
        gamerequests.setHorizontalSpacing(30)
        for i in range(5):
            playername = "1"
            game_request_message = QLabel(f"Challenge from {playername}")
            game_request_message.setFixedSize(300, 40)
            game_request_message.setFont(QFont("Arial",15))
            gamerequests.addWidget(game_request_message,i,0)
            gamereqlabels.append(game_request_message)
            gamerequests.addWidget(Accept_Game_Button(),i,1)
            gamerequests.addWidget(Decline_Game_Button(),i,2)
        chatlayout.addLayout(gamerequests)
        chatlayout.addSpacerItem(QSpacerItem(1,31))

        reqsshow_thread = getgamereqs()
        reqsshow_thread.start()

        #queuebox.setContentsMargins(0,10,0,0)
        #queuebox.addWidget(queue_button())
        #chatlayout.addLayout(queuebox)

        widget = QWidget()
        widget.setLayout(mainlayout)
        self.setCentralWidget(widget)
    
        
class Challengebutton(QWidget):
    def __init__(self,playername): 
        super().__init__()
        self.playername = playername
        self.button = QPushButton(text=f"Challenge {playername}",parent=self)
        self.button.setFixedSize(300, 47)
        self.button.setFont(QFont("Arial",15))
        self.button.clicked.connect(self.button_clicked)
        Buttons.append(self.button)

    def update_Button(self):
        self.button.setText(f"Challenge {self.playername}")

    def button_clicked(self):

        for i in Buttons:
            i.setEnabled(False)
            i.setStyleSheet("background-color: rgba(100, 100, 100, 50)")
        self.button.setText(f"Waiting for {self.playername}")
        self.button.setStyleSheet("background-color: rgba(255, 255, 255, 100);color: red;")
        result = requests.post(url+"addgamerequest"+f"?cname={username}&oname={self.playername}")
        result = result.json()
        self.game = int(result[0])
        self.timer = QTimer()
        self.timer.timeout.connect(lambda: self.reset_buttons(game))
        self.timer.start(15000)
        

    def reset_buttons(self,game):
        global gameaccepted
        print("GAME ID:"+str(self.game))
        result = requests.get(url+"checkifaccepted"+f"?game={self.game}").json()[0]
        print("REQUESTRESULT:"+repr(result))
        if result == 1:
            global login, app
            login = False
            app.exit()
        elif result == 0:
            gameaccepted = False
        j = 0
        for i in Buttons:
            i.setEnabled(True)
            if (j <= 25):
                if (j < 15):
                    i.setStyleSheet("background-color: rgba(255, 255, 255, 100);")
                    i.setText(f"Challenge {Players[j].username}")
                elif (15 <= j < 25 ):
                    if (j%2 == 1):
                        i.setStyleSheet("background-color: red")
                    elif (j%2 == 0):
                        i.setStyleSheet("background-color: #18a330")
                else:
                    i.setStyleSheet("background-color: red")
                j += 1
            else:
                i.setStyleSheet("background-color: #18a330")
        if (not gameaccepted):
            result = requests.post(url+"delgamerequest"+f"?game={game}")
            result = result.json()
        self.timer.stop()


class Back_to_login_button(QWidget):
    def __init__(self):
        super().__init__()
        self.button = QPushButton(text="Quit game",parent = self)
        self.button.setStyleSheet("background-color: red")
        self.button.setFixedSize(650, 100)
        self.button.setFont(QFont("Arial",15))
        self.button.clicked.connect(self.button_clicked)
        Buttons.append(self.button)

    def button_clicked(self):
        sys.exit()
'''
class queue_button(QWidget):
    def __init__(self):
        super().__init__()

        self.button = QPushButton(text="Enter Queue",parent = self)
        self.button.setCheckable(True)
        self.button.setChecked(True)
        self.button.setFocus()
        self.button.setStyleSheet("background-color: #18a330")
        self.button.setFixedSize(650, 100)
        self.button.setFont(QFont("Arial",15))
        self.button.clicked.connect(self.button_clicked)
        Buttons.append(self.button)

    def button_clicked(self):
        if self.button.isChecked():
            self.button.setText("Enter Queue")
            for i in Buttons:
                i.setEnabled(True) 
            self.reset_buttons()
        else:
            self.button.setText("In Queue \n Press again to cancel")
            j = 0
            for i in Buttons:
                if (j <= 25):
                    i.setEnabled(False) 
                    i.setStyleSheet("background-color: rgba(100, 100, 100, 50);")
                    j += 1

                        
    def reset_buttons(self):
        j = 0
        for i in Buttons:
            if (j <= 25):
                i.setEnabled(True)
                if (j < 15):
                    i.setStyleSheet("background-color: rgba(255, 255, 255, 100);")
                elif (15 <= j < 25 ):
                    if (j%2 == 1):
                        i.setStyleSheet("background-color: #18a330")
                    elif (j%2 == 0):
                        i.setStyleSheet("background-color: red")
                else:
                    i.setStyleSheet("background-color: red")
                j += 1
'''

class Accept_Game_Button(QWidget):
    def __init__(self):
        super().__init__()
        self.button = QPushButton(text="Accept",parent = self)
        self.button.setStyleSheet("background-color: #18a330")
        self.button.setFixedSize(140, 40)
        self.button.setFont(QFont("Arial",15))
        self.button.clicked.connect(self.button_clicked)
        self.button.gameid = ""
        Buttons.append(self.button)

    def button_clicked(self):
        self.button.setStyleSheet("background-color: rgba(#18a330, 100);")
        print("gameidbutton",self.button.gameid)
        self.button.setText(f"test{self.button.gameid}")
        requests.post(url+"acceptgamerequest"+f"?game={self.button.gameid}")
        global login, app
        login = False
        app.exit()


class Decline_Game_Button(QWidget):
    def __init__(self):
        super().__init__()
        self.button = QPushButton(text="Decline",parent = self)
        self.button.setStyleSheet("background-color: red")
        self.button.setFixedSize(140, 40)
        self.button.setFont(QFont("Arial",15))
        self.button.clicked.connect(self.button_clicked)
        self.button.gameid = ""
        Buttons.append(self.button)
    
    def button_clicked(self):
        self.button.setStyleSheet("background-color: rgba(red, 100);")
        print("gameidbutton",self.button.gameid)
        self.button.setText(f"test{self.button.gameid}")
        requests.post(url+"delgamerequest"+f"?game={self.button.gameid}")

class Scroll_window(QScrollArea):
    def __init__(self, *args, **kwargs):
        QScrollArea.__init__(self, *args, **kwargs)
        self.setWidgetResizable(True)
        self.setFixedSize(650,400)
        content = QWidget(self)
        self.setWidget(content)
        lay = QVBoxLayout(content)
        self.label = QLabel(content)
        self.label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.label.setWordWrap(True)
        self.label.setFont(QFont("Arial",15))
        self.label.setStyleSheet("color: white;")
        self.setStyleSheet("border: 3px solid black;background-color: rgba(0, 0, 0, 50);")
        lay.addWidget(self.label)
    def setText(self, text):
        # setting text to the label
        self.label.setText(text)

   
def get_players():
    j = 0 
    for i in Players:
        #data = user_leaderboard_wins()
        #while (j < (len(data)/3)):
            #Players[j] = player(data[0%3 + 3*j],data[1%3 + 3*j],data[2%3 + 3*j])
        Players[j] = player()
        j += 1

def calc_winrate(player):
    try:
        return f"{round(player.wins/player.games*100,1)}%"
    except ZeroDivisionError:
        return "--------"


stylesheet = """
    Playerpage {
        border-image: url("Resources/images/highrecbackground.png"); 
        background-repeat: no-repeat; 
        background-position: center;
    }
    QLabel {
        border: 3px solid black;
        color: white;
        background-color: rgba(0, 0, 0, 50);
    }
    QPushButton {
    
    }
    QLineEdit {
        border: 3px solid black;
        color: white;
        background-color: rgba(0, 0, 0, 50);
    }
"""

#SHIPPLACEMENT GUI

shipheaders = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O']
shipnumbers = [2,3,3,1,1]
fieldbuttons = []
placebuttons = []
rotatebuttons = []
lefttoplace = []
shippics = []
cordentries = []
x_taken_by_ships = []
y_taken_by_ships = []

class shipplacementpage(QMainWindow):
    def __init__(self):
        super().__init__()

        layouts = []

        self.setWindowTitle("Ship Placement")
        self.setFixedSize(1920,1080)
        mainlayout = QHBoxLayout()
        fieldbox = QVBoxLayout()
        fieldlayout = QGridLayout()
        buttonlayout1 = QVBoxLayout()
        buttonlayout2 = QVBoxLayout()
        mainlayout.addLayout(fieldbox)
        mainlayout.addLayout(buttonlayout1)
        mainlayout.addLayout(buttonlayout2)
        layouts.append(mainlayout)
        layouts.append(fieldlayout)
        layouts.append(buttonlayout1)
        layouts.append(buttonlayout2)
        for i in layouts:
            i.setSpacing(0)
            i.setContentsMargins(100,100,100,100)
        mainlayout.setContentsMargins(0,0,0,0)
        fieldlayout.setContentsMargins(50,60,50,60)

        #fill field grid
        fieldtitle = QLabel("Place your ships!")
        fieldtitle.setFixedHeight(80)
        fieldtitle.setFont(QFont("Arial",30))
        fieldtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        fieldbox.addWidget(fieldtitle)
        fieldsubtitle = QLabel("Enter the coordinates by clicking on the square where you want your ship to be placed!")
        fieldsubtitle.setFixedHeight(80)
        fieldsubtitle.setFont(QFont("Arial",15))
        fieldsubtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        fieldbox.addWidget(fieldsubtitle)
        fieldbox.addLayout(fieldlayout)

        for i in range(2,17):
            row = QLabel(f"{i-1}")
            row.setFixedSize(50,50)
            row.setFont(QFont("Arial",20))
            row.setAlignment(Qt.AlignmentFlag.AlignCenter)
            fieldlayout.addWidget(row,i,0)
            column = QLabel(f"{shipheaders[i-2]}")
            column.setFixedSize(50,50)
            column.setFont(QFont("Arial",20))
            column.setAlignment(Qt.AlignmentFlag.AlignCenter)
            fieldlayout.addWidget(column,1,i)
            for j in range (2,17):
                fieldlayout.addWidget(fieldbutton(i-1,shipheaders[j-2]),i,j)

        #create buttons to place ships
        buttonlayout1.setContentsMargins(0,0,0,0)
        buttonlayout2.setContentsMargins(0,0,0,0)
        for i in range (3):
            placebox = QHBoxLayout()
            placebox.setSpacing(0)
            placebox.setContentsMargins(0,0,0,0)
            buttonbox = QVBoxLayout()
            buttonbox.setSpacing(0)
            buttonbox.setContentsMargins(0,0,0,0)
            buttonbox.addSpacerItem(QSpacerItem(100,70))
            buttonbox.addWidget(placebutton())
            buttonbox.addWidget(rotatebutton())
            entercords = QLabel()
            entercords.setFont(QFont("Arial",12))
            entercords.setFixedSize(150,50)
            cordentries.append(entercords)
            entercords.setAlignment(Qt.AlignmentFlag.AlignCenter)
            entercords.setStyleSheet("border: 1px solid white;")
            buttonbox.addWidget(entercords)
            buttonbox.addSpacerItem(QSpacerItem(100,7))
            left_to_place = QLabel()
            left_to_place.setFont(QFont("Arial",12))
            left_to_place.setText(f" {shipnumbers[i]} left to place")
            left_to_place.setStyleSheet("border: 1px solid white;")
            left_to_place.setFixedSize(150,50)
            left_to_place.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lefttoplace.append(left_to_place)
            buttonbox.addWidget(left_to_place)
            buttonbox.addSpacerItem(QSpacerItem(100,70))
            placebox.addLayout(buttonbox)
            ship = QLabel(self)
            if (i == 0):
                shippic = QPixmap("Resources/images/5x1.png")
            if (i == 1):
                shippic = QPixmap("Resources/images/4x1.png")
            if (i == 2):
                shippic = QPixmap("Resources/images/3x1.png")
            ship.setPixmap(shippic)
            ship.setAlignment((Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignLeft))
            shippics.append(ship)
            placebox.addWidget(ship)
            buttonlayout1.addLayout(placebox)    
        
        for i in range (2):
            placebox = QHBoxLayout()
            placebox.setSpacing(0)
            placebox.setContentsMargins(0,0,0,0)
            buttonbox = QVBoxLayout()
            buttonbox.setContentsMargins(0,0,0,0)
            buttonbox.setSpacing(0)
            buttonbox.addSpacerItem(QSpacerItem(100,160))
            buttonbox.addWidget(placebutton())
            buttonbox.addWidget(rotatebutton())
            entercords = QLabel()
            entercords.setFont(QFont("Arial",12))
            entercords.setFixedSize(150,50)
            cordentries.append(entercords)
            entercords.setAlignment(Qt.AlignmentFlag.AlignCenter)
            entercords.setStyleSheet("border: 1px solid white;")
            buttonbox.addWidget(entercords)
            buttonbox.addSpacerItem(QSpacerItem(100,7))
            left_to_place = QLabel()
            left_to_place.setFont(QFont("Arial",12))
            left_to_place.setText(f"{shipnumbers[i+3]} left to place ")
            left_to_place.setStyleSheet("border: 1px solid white;")
            left_to_place.setFixedSize(150,50)
            left_to_place.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lefttoplace.append(left_to_place)
            buttonbox.addWidget(left_to_place)
            buttonbox.addSpacerItem(QSpacerItem(100,160))
            placebox.addLayout(buttonbox)
            ship = QLabel(self)
            if (i == 0):
                shippic = QPixmap("Resources/images/5x2.png")
            if (i == 1):
                shippic = QPixmap("Resources/images/1x2.png")
            ship.setPixmap(shippic)
            ship.setAlignment((Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignLeft))
            shippics.append(ship)
            placebox.addWidget(ship)
            buttonlayout2.addLayout(placebox)    

        widget = QWidget()
        widget.setLayout(mainlayout)
        self.setCentralWidget(widget)

class fieldbutton(QWidget):
    def __init__(self,x,y): 
        super().__init__()
        self.x = x
        self.y = y
        self.button = QPushButton(parent=self)
        self.button.setFixedSize(50,50)
        fieldbuttons.append(self)
        self.button.clicked.connect(self.button_clicked)
        self.used = False

    def button_clicked(self):
        for i in cordentries:
            i.setText(f"{self.y} {self.x}")
            

class placebutton(QWidget):
    def __init__(self): 
        super().__init__()
        self.button = QPushButton(parent=self)
        self.button.setFixedSize(150,50)
        self.button.setText("Place Ship")
        self.button.setFont(QFont("Arial",12))
        placebuttons.append(self.button)
        self.button.clicked.connect(self.button_clicked)

    def button_clicked(self):
        startcords = 0
        j = 0
        for i in placebuttons:
            if (i == self.button):
                cords = cordentries[j].text()
                if (cords == ''):
                    msg = QMessageBox(self)
                    msg.setWindowTitle("Invalid Input")
                    msg.setText("Please enter coordinates!")
                    msg.setStyleSheet("color:black")
                    msg.exec()
                else:
                    cords = cords.split()
                    y = int(cords[1])
                    for k in range(15):
                        if (shipheaders[k] == cords[0]):
                            x = int(k+1)
                    startcords = [x,y]                
                    break
            j+=1
        if startcords != 0:
            checkfree = True
            if (j == 0):
                ship = fivex1(startcords)
            elif (j == 1): 
                ship = fourx1(startcords)
            elif (j == 2):
                ship = threexone(startcords)     
            elif (j == 3):
                ship = fivex2(startcords)
            elif (j == 4):
                ship = twoxone(startcords)
            k = 0
            for i in ship.x:
                if (i < 1 or i > 15):
                    ship.x[k] = '#'
                k+=1        
            k = 0
            for i in ship.y:
                if (i < 1 or i > 15):
                    ship.y[k] = '#'
                k+=1
            k = 0
            for x in ship.x:
                if (x != '#'):
                    ship.x[k] = shipheaders[x-1]
                k += 1
            k = 0
            for y in ship.y:
                if (y != '#'):
                    ship.y[k] = str(y)
                k+=1
            for i in range(len(ship.x)):
                cord = ship.x[i]+ship.y[i]
                for m in cord:
                    if (m == '#'):
                        msg = QMessageBox(self)
                        msg.setWindowTitle("Invalid Input")
                        msg.setText("Out of playing area!")
                        msg.setStyleSheet("color:black")
                        msg.exec()
                        checkfree = False   
                        break
                for n in range(len(x_taken_by_ships)):
                    if (cord == (y_taken_by_ships[n]+str(x_taken_by_ships[n]))):
                        msg = QMessageBox(self)
                        msg.setWindowTitle("Invalid Input")
                        msg.setText("There is already a ship there!")
                        msg.setStyleSheet("color:black")
                        msg.exec()
                        checkfree = False
                        break
                if not checkfree:
                    break
            if checkfree:        
                for i in range(len(ship.x)):
                    cord = ship.x[i]+ship.y[i]
                    for chr in fieldbuttons:
                        if (cord == (chr.y+str(chr.x))):
                            chr.button.setEnabled(False)
                            chr.button.setStyleSheet(("background-color: gray"))
                            x_taken_by_ships.append(chr.x)
                            y_taken_by_ships.append(chr.y)
                            for i in cordentries:
                                i.setText("")
                shipnumbers[j]=shipnumbers[j] - 1
                lefttoplace[j].setText(f"{shipnumbers[j]} left to place ")
                if shipnumbers[j]==0:
                    placebuttons[j].setDisabled(True)
                if sum(shipnumbers) == 0:
                    global placing_ships
                    placing_ships = False
                    app.exit()



class rotatebutton(QWidget):
    def __init__(self,rotation = 0): 
        super().__init__()
        self.button = QPushButton(parent=self)
        self.rotation = rotation
        self.button.setFixedSize(150,50)
        self.button.rotation = self.rotation
        self.button.setText("Rotate 90°")
        self.button.setFont(QFont("Arial",12))
        rotatebuttons.append(self.button)
        self.button.clicked.connect(self.button_clicked)
    
    def button_clicked(self):
        j = 0
        for i in rotatebuttons:
            if (i == self.button):
                pic = shippics[j].pixmap()
                pic = pic.transformed(QTransform().rotate(90))
                shippics[j].setPixmap(pic)
                self.button.rotation +=90
                if (self.button.rotation == 360):
                    self.button.rotation = 0
            j+=1


class spacer1(QWidget):
    def __init__(self): 
        super().__init__()
        self.button = QPushButton(parent=self)
        self.button.setFixedSize(100,50)
        self.button.setStyleSheet("background-color: white;border:solid black;border-width : 1px 0px 1px 0px;")


class spacer2(QWidget):
    def __init__(self): 
        super().__init__()
        self.button = QPushButton(parent=self)
        self.button.setFixedSize(100,50)
        self.button.setStyleSheet("background-color: white;border:0px")

class threexone():
    def __init__(self,start,x = [],y = []):
        self.x = x
        self.y = y
        self.start = start
        self.rotation = rotatebuttons[2].rotation
        if (self.rotation == 0):
            self.x = [self.start[0],self.start[0]+1,self.start[0]+2]
            self.y = [self.start[1],self.start[1],self.start[1]]
        elif (self.rotation == 90):
             self.x = [self.start[0],self.start[0],self.start[0]]
             self.y = [self.start[1],self.start[1]+1,self.start[1]+2]
        elif (self.rotation == 180):
             self.x = [self.start[0],self.start[0]-1,self.start[0]-2]
             self.y = [self.start[1],self.start[1],self.start[1]]
        elif (self.rotation == 270):
             self.x = [self.start[0],self.start[0],self.start[0]]
             self.y = [self.start[1],self.start[1]-1,self.start[1]-2]

class fourx1():
    def __init__(self,start,x = [],y = []):
        self.x = x
        self.y = y
        self.start = start
        self.rotation = rotatebuttons[1].rotation
        if (self.rotation == 0):
            self.x = [self.start[0],self.start[0]+1,self.start[0]+2,self.start[0]+3]
            self.y = [self.start[1],self.start[1],self.start[1],self.start[1]]
        elif (self.rotation == 90):
             self.x = [self.start[0],self.start[0],self.start[0],self.start[0]]
             self.y = [self.start[1],self.start[1]+1,self.start[1]+2,self.start[1]+3]
        elif (self.rotation == 180):
             self.x = [self.start[0],self.start[0]-1,self.start[0]-2,self.start[0]-3]
             self.y = [self.start[1],self.start[1],self.start[1],self.start[1]]
        elif (self.rotation == 270):
             self.x = [self.start[0],self.start[0],self.start[0],self.start[0]]
             self.y = [self.start[1],self.start[1]-1,self.start[1]-2,self.start[1]-3]

class fivex1():
    def __init__(self,start):
        self.start = start
        self.rotation = rotatebuttons[0].rotation 
        if (self.rotation == 0):
            self.x = [self.start[0],self.start[0]+1,self.start[0]+2,self.start[0]+3,self.start[0]+4]
            self.y = [self.start[1],self.start[1],self.start[1],self.start[1],self.start[1]]
        elif (self.rotation == 90):
             self.x = [self.start[0],self.start[0],self.start[0],self.start[0],self.start[0]]
             self.y = [self.start[1],self.start[1]+1,self.start[1]+2,self.start[1]+3,self.start[1]+4]
        elif (self.rotation == 180):
             self.x = [self.start[0],self.start[0]-1,self.start[0]-2,self.start[0]-3,self.start[0]-4]
             self.y = [self.start[1],self.start[1],self.start[1],self.start[1],self.start[1]]
        elif (self.rotation == 270):
             self.x = [self.start[0],self.start[0],self.start[0],self.start[0],self.start[0]]
             self.y = [self.start[1],self.start[1]-1,self.start[1]-2,self.start[1]-3,self.start[1]-4]
class fivex2():
    def __init__(self,start):
        self.start = start
        self.rotation = rotatebuttons[3].rotation
        if (self.rotation == 0):
            self.x = [self.start[0],self.start[0]+1,self.start[0]+2,self.start[0]+3,self.start[0]+4,self.start[0],self.start[0]+1,self.start[0]+2,self.start[0]+3,self.start[0]+4]
            self.y = [self.start[1],self.start[1],self.start[1],self.start[1],self.start[1],self.start[1]+1,self.start[1]+1,self.start[1]+1,self.start[1]+1,self.start[1]+1]
        elif (self.rotation == 90):
             self.x = [self.start[0],self.start[0],self.start[0],self.start[0],self.start[0],self.start[0]+1,self.start[0]+1,self.start[0]+1,self.start[0]+1,self.start[0]+1]
             self.y = [self.start[1],self.start[1]+1,self.start[1]+2,self.start[1]+3,self.start[1]+4,self.start[1],self.start[1]+1,self.start[1]+2,self.start[1]+3,self.start[1]+4]
        elif (self.rotation == 180):
             self.x = [self.start[0],self.start[0]-1,self.start[0]-2,self.start[0]-3,self.start[0]-4,self.start[0],self.start[0]-1,self.start[0]-2,self.start[0]-3,self.start[0]-4]
             self.y = [self.start[1],self.start[1],self.start[1],self.start[1],self.start[1],self.start[1]+1,self.start[1]+1,self.start[1]+1,self.start[1]+1,self.start[1]+1]
        elif (self.rotation == 270):
             self.x = [self.start[0],self.start[0],self.start[0],self.start[0],self.start[0],self.start[0]+1,self.start[0]+1,self.start[0]+1,self.start[0]+1,self.start[0]+1]
             self.y = [self.start[1],self.start[1]-1,self.start[1]-2,self.start[1]-3,self.start[1]-4,self.start[1],self.start[1]-1,self.start[1]-2,self.start[1]-3,self.start[1]-4]

class twoxone():
    def __init__(self,start):
        self.start = start
        self.rotation = rotatebuttons[4].rotation 
        if (self.rotation == 0):
            self.x = [self.start[0],self.start[0]+1]
            self.y = [self.start[1],self.start[1]]
        elif (self.rotation == 90):
             self.x = [self.start[0],self.start[0]]
             self.y = [self.start[1],self.start[1]+1]
        elif (self.rotation == 180):
             self.x = [self.start[0],self.start[0]-1]
             self.y = [self.start[1],self.start[1]]
        elif (self.rotation == 270):
             self.x = [self.start[0],self.start[0]]
             self.y = [self.start[1],self.start[1]-1]


shipplacement_stylesheet = """
    shipplacementpage {
        border-image: url("Resources/images/bg.jpg"); 
        background-repeat: no-repeat; 
        background-position: center;
    }
    QLabel {
        color: white;
        background-color: rgba(255, 255, 255, 0);
    }
    QPushButton {
        background-color: rgba(255, 255, 255, 0);
        color: white;
        border: 1px solid white;
    }
    QLineEdit {
        border: 1px solid white;
        color: white;
        background-color: white;
    }
"""



#LOGIN/REGISTER
inShipplacement = False
username, password, login_or_register = login_register_window() #"L" for Login/"R" for Register

if login_or_register == "L":
    lresponse = requests.get(url+"userlogin"+f"?username={username}&password={password}")

else:
    lresponse = requests.get(url+"usernew"+f"?username={username}&password={password}")


if lresponse.json()[0] == 1:           
    login = True

while(login):
    app = QApplication(sys.argv)
    app.setStyleSheet(stylesheet)
    window = Playerpage()
    window.show()
    app.exec()
placing_ships = True
while(placing_ships):
    inShipplacement = True
    window = shipplacementpage()
    window.showFullScreen()
    app.exec()


    '''
    # TODO von GUI -> Wer wird challenged
    if():
        gameid = requests.post(url+f"?cname={username}&oname={name2}")
        main_gameid = gameid.json()

    # Erstelle und starte den Thread
        thread = threading.Thread(target=thread_function)
        thread.start()

    # TODO von GUI -> Was wird in Chat geschrieben
    message = None
    if():
        requests.post(url+f"?username={username}&message={message}")

    if(ship == True):
        fight = True
        break
    '''
