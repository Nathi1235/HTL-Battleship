import sys, os
import User_Login as User_Login
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *
from random import *

path = "player_data.txt"
Buttons = []
Headers = []
Players = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]


class player:
    def __init__(self, username = "--------",wins = 0,games = 0):
        self.username = username
        self.wins = wins
        self.games = games
        

class Playerpage(QMainWindow):
    def __init__(self):
        super(Playerpage, self).__init__()

        self.setWindowTitle("Players")
        layout = QGridLayout()
        self.move(0,0)

        Headers.append(QLabel("Player"))
        Headers.append(QLabel("Games won"))
        Headers.append(QLabel("Games played"))
        Headers.append(QLabel("Win %"))
        x = 0
        for i in Headers:
            i.setFont(QFont("Arial",20))
            layout.addWidget(i,0,x)
            i.setAlignment(Qt.AlignmentFlag.AlignCenter)
            x += 1 
        layout.addWidget(Back_to_start_button(),0,4)

        get_players()

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
            layout.addWidget(Playerdata[0],j+1,0)
            layout.addWidget(Playerdata[1],j+1,1)
            layout.addWidget(Playerdata[2],j+1,2)
            layout.addWidget(Playerdata[3],j+1,3)
            layout.addWidget(Challengebutton(i.username),j+1,4)
            j += 1
               

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

'''
class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)
'''        
        

class Challengebutton(QWidget):
    def __init__(self,playername): 
        super().__init__()
        self.playername = playername
        self.button = QPushButton(text=f"Challenge {playername}",parent=self)
        self.button.setFixedSize(300, 47)
        self.button.setFont(QFont("Arial",15))
        self.button.clicked.connect(self.button_clicked)
        Buttons.append(self.button)

    def button_clicked(self):
        self.button.setText(f"Waiting for {self.playername}")
        for i in Buttons:
            i.setEnabled(False)

class Back_to_start_button(QWidget):
    def __init__(self):
        super().__init__()
        self.button = QPushButton(text="Back to Startpage",parent = self)
        self.button.setStyleSheet("background-color: red")
        self.button.setFixedSize(300, 47)
        self.button.setFont(QFont("Arial",15))
        self.button.clicked.connect(self.button_clicked)

    def button_clicked(self):
        self.button.setText("Loading...")
        for i in Buttons:
            i.setEnabled(False)

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
        return f"{round(player.wins/player.games,1)*10}%"
    except ZeroDivisionError:
        return "--------"

  
app = QApplication(sys.argv)

window = Playerpage()
window.showFullScreen()

app.exec()
