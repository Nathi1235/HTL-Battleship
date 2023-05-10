import sys
import random
from PyQt6 import QtGui
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
import networking as net



class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.setFixedSize(1920,1080)

        
        self.Layout_1 = QGridLayout()
        self.Layout_2 = QGridLayout()
        self.Layout_3 = QGridLayout()
        self.mainlayout = QHBoxLayout()
        self.sublayout = QVBoxLayout()
        self.sublayout.addLayout(self.Layout_2)
        self.sublayout.addLayout(self.Layout_3)
        self.mainlayout.addLayout(self.Layout_1)
        self.mainlayout.addLayout(self.sublayout)
        self.Layout_2.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)
        self.Layout_1.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignCenter)
        self.Layout_3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #self.Layout.setContentsMargins(0,0,0,0)
        #self.button.addStretch(1)
        self.mainlayout.setSpacing(0)
        self.my_buttons = []
        self.opp_buttons = []
        self.coord_list = []

        self.letter_lsit = "ABCDEFGHIJKLMNO"
        self.test_list = [(1,1),(1,3),(3,3),(3,4),(6,6),(4,6)]
        

        for i in range(15):
            self.numbers = QLabel(f"{self.letter_lsit[i]}")
            self.numbers.setFixedSize(54,54)
            font = self.numbers.font()
            font.setPointSize(20)
            self.numbers.setFont(font)
            self.numbers.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.Layout_1.addWidget(self.numbers,0,i+1)



            for j in range(15):
                self.letters = QLabel(f"{j+1}")
                self.letters.setFixedSize(54,54)
                font = self.letters.font()
                font.setPointSize(20)
                self.letters.setFont(font)
                self.letters.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.Layout_1.addWidget(self.letters,j+1,0)


                self.button = QPushButton("")
                self.button.clicked.connect(self.my_button_clicked)
                self.my_buttons.append(self.button)
                self.button.setFixedSize(60,60)
                
                #self.button.setStyleSheet("background-color: white; border:2px")
                self.button.setStyleSheet("border: 1px solid black;")
                self.Layout_1.addWidget(self.button,i+1,j+1)



                self.button = QPushButton("")
                self.button.clicked.connect(self.opp_button_clicked)
                self.opp_buttons.append(self.button)
                self.button.setFixedSize(40,40)
                
                #self.button.setStyleSheet("background-color: white; border:2px")
                self.button.setStyleSheet("border: 1px solid black;")
                self.Layout_2.addWidget(self.button,i,j)
        
                

                widget = QWidget()
                widget.setLayout(self.mainlayout)
                self.setCentralWidget(widget)

            ship_list = [2,3,3,1,1] #list just for testing


            
            self.widget_ = QLabel(f"ship 1x2 : {ship_list[0]} ship 1x3 : {ship_list[1]} ship 1x4 : {ship_list[2]} ship 1x5 : {ship_list[3]} ship 2x5 : {ship_list[4]}")
            font = self.widget_.font()
            font.setPointSize(30)
            self.widget_.setFont(font)
            self.widget_.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.widget_.setFixedSize(250,270)
            self.widget_.setWordWrap(True)
            self.Layout_3.addWidget(self.widget_,1,1)
            





        self.opp_field(self.test_list)
        self.shoot(10, 10, "blue", 0)





    def my_button_clicked(self):
        chosen_button = self.sender()
        #print(self.my_buttons.index(chosen_button))



        #get coords of pressed button
        x_coord = self.my_buttons.index(chosen_button) % 15 + 1
        y_coord = self.my_buttons.index(chosen_button) // 15 + 1
        
        if((x_coord,y_coord) not in self.coord_list):
            self.coord_list.append((x_coord,y_coord))
            print(f"{x_coord},{y_coord}")
            self.my_buttons[15*(y_coord-1)+x_coord-1].setStyleSheet("background-color: red")
    
                
    
    def opp_button_clicked(self):
        chosen_button = self.sender()
        x_coord = self.opp_buttons.index(chosen_button) % 15 + 1
        y_coord = self.opp_buttons.index(chosen_button) // 15 + 1
        chosen_button = self.sender()
        #print(f"{x_coord},{y_coord}")
        return(x_coord, y_coord)  #return coords of clicked button



    def opp_field(self, shiplist):
        for i in shiplist:
            self.opp_buttons[15*(i[0]-1)+i[1]-1].setStyleSheet("background-color: red")


    def shoot(self, x, y, color, player):
        if (player == 0):
            self.opp_buttons[15*(y-1)+x-1].setStyleSheet(f"background-color: {color}")
        else:
            self.my_buttons[15*(y-1)+x-1].setStyleSheet(f"background-color: {color}")



    def disable_buttons(self, x, y, player):
        if (player == 0):
            self.opp_buttons[15*(y-1)+x-1].setEnabled(False)
        else:
            self.my_buttons[15*(y-1)+x-1].setEnabled(False)





app = QApplication(sys.argv)
window = MainWindow()
window.showFullScreen()
app.exec()  