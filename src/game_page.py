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

        QHBoxLayout()
        self.Layout_1 = QGridLayout()
        self.Layout_2 = QGridLayout()
        self.mainlayout = QHBoxLayout()
        self.mainlayout.addLayout(self.Layout_1)
        self.mainlayout.addLayout(self.Layout_2)
        self.Layout_2.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)
        self.Layout_1.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignCenter)
        #self.Layout.setContentsMargins(0,0,0,0)
        #self.button.addStretch(1)
        self.mainlayout.setSpacing(0)
        self.my_buttons = []
        self.opp_buttons = []
        self.coord_list = []

        self.letter_lsit = "ABCDEFGHIJKLMNO"
        

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
            self.disable_buttons(False) #False = disable | True = enable
    
                
    
    def opp_button_clicked(self):
        chosen_button = self.sender()
        print(self.opp_buttons.index(chosen_button))



    def disable_buttons(self, disable):
        for i in self.my_buttons:
            i.setEnabled(disable)




app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()  