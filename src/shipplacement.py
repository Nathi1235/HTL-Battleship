import sys, os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *

headers = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O']
shipnumbers = [2,3,3,1,1]
fieldbuttons = []
placebuttons = []
rotatebuttons = []
shippics = []
cordentries = []
x_taken_by_ships = ['#']
y_taken_by_ships = ['#']

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
            column = QLabel(f"{headers[i-2]}")
            column.setFixedSize(50,50)
            column.setFont(QFont("Arial",20))
            column.setAlignment(Qt.AlignmentFlag.AlignCenter)
            fieldlayout.addWidget(column,1,i)
            for j in range (2,17):
                fieldlayout.addWidget(fieldbutton(i-1,headers[j-2]),i,j)

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
                    msg.exec()
                else:
                    cords = cords.split()
                    y = int(cords[1])
                    for k in range(15):
                        if (headers[k] == cords[0]):
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
                    ship.x[k] = headers[x-1]
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
                        msg.exec()
                        checkfree = False
                        break
                for n in range(len(x_taken_by_ships)):
                    if (cord == (y_taken_by_ships[n]+str(x_taken_by_ships[n]))):
                        msg = QMessageBox(self)
                        msg.setWindowTitle("Invalid Input")
                        msg.setText("There is already a ship there!")
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


stylesheet = """
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



if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(stylesheet)
    window = shipplacementpage()
    window.showFullScreen()


    app.exec()
