import sys, os
import User_Login
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import *
import hashlib

path = "player_data.txt"



class StartingPage(QMainWindow):
    def __init__(self): #the __init__ method of the super() class must always be called
        super().__init__()

        self.setWindowTitle("Battleship") #set title

        self.setFixedSize(QSize(1000, 700)) #set window size

        self.layout = QGridLayout() #create layout


        self.button_text = ["LOGIN","REGISTER"] #list with button text
        self.button_list = [] #list for buttons

        for i in range(len(self.button_text)): #for loop to create buttons
            self.button = QPushButton(self.button_text[i]) #create button
            self.button.setFixedSize(520, 70) #set button size
            self.button.setStyleSheet("font: bold;background-color: white;font-size: 36px;") #set button text font, color and size
            self.button.clicked.connect(self.button_clicked) #connect button to function
            self.button_list.append(self.button) #append button into button_list
            self.layout.addWidget(self.button,i,0) #add button to layout
            self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter) #align button to center


        self.layout.setSpacing(25) #set layout spacing

        self.widget = QWidget() #create widget
        self.widget.setLayout(self.layout) #set widget layout 
        self.setCentralWidget(self.widget) #set widget position

        

    def button_clicked(self): #function for clicked button

        clicked_button = self.sender() #retrieve the object that sent the signal

        if(self.button_list.index(clicked_button) == 0):
            window.setCurrentWidget(page2) #change page

        if(self.button_list.index(clicked_button) == 1):
            window.setCurrentWidget(page3) #change page







class LoginWindow(QMainWindow):
    def __init__(self): #the __init__ method of the super() class must always be called
        super().__init__()

        self.setWindowTitle("Battleship") #set title

        self.setFixedSize(QSize(1000, 700)) #set window size

        self.layout1 = QGridLayout() #create grid layout
        self.layout2 = QVBoxLayout() #create vertical layout


        self.input_field_text = ["login","password"] #list with input field text
        self.input_field_list = [] #list for input fields

        for i in range(len(self.input_field_text)): #for loop to create input fields
            self.input_field = QLineEdit(self) #create input field
            self.input_field.setMaxLength(25) #set input field text max length
            self.input_field.setFixedSize(QSize(600, 90)) #set input field size
            #self.input_field.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.input_field.setFont(QFont('Arial', 18)) #set input field text font and size
            self.input_field.setPlaceholderText(self.input_field_text[i]) #set input field placeholder text
            if(self.input_field_text[i] == "password"): #if password, hide text with *
                self.input_field.setEchoMode(QLineEdit.EchoMode.Password)
            self.layout2.addWidget(self.input_field) #add input field to layout
            self.layout2.setAlignment(Qt.AlignmentFlag.AlignCenter) #align input field to center
            self.input_field_list.append(self.input_field) #append input field into input_field_list


        self.button_text = ["RETURN","OK"] #list with button text
        self.button_list = [] #list for buttons

        for i in range(len(self.button_text)): #for loop to create buttons
            self.button = QPushButton(self.button_text[i]) #create button
            self.button.setFixedSize(290, 90) #set button size
            self.button.setStyleSheet("font: bold;background-color: white;font-size: 36px;") #set button text font, color and size
            self.button.clicked.connect(self.button_clicked) #connect button to function
            self.button_list.append(self.button) #append button into button_list
            self.layout1.addWidget(self.button,0,i) #add button to layout
            self.layout1.setAlignment(Qt.AlignmentFlag.AlignCenter) #align button to center

            
        self.layout2.addLayout(self.layout1) #combine layouts
        self.layout2.setSpacing(20) #set layout spacing

        self.widget = QWidget() #create widget
        self.widget.setLayout(self.layout2) #set widget layout 
        self.setCentralWidget(self.widget) #set widget position



    def button_clicked(self): #function for clicked button

        clicked_button = self.sender() #retrieve the object that sent the signal

        if(self.button_list.index(clicked_button) == 0):
            window.setCurrentWidget(page1) #change page
            for i in self.input_field_list: #for all input fields
                i.setStyleSheet("background-color: white;color: black") #reset color after leaving


        if(self.button_list.index(clicked_button) == 1):

            for i in self.input_field_list: #for all input fields
                i.setStyleSheet("background-color: white;color: black") #set color
            self.correct = True 

            for i in self.input_field_list: #for all input fields
                if(i.text() == ""): #if empty (no text)
                    i.setStyleSheet("background-color: rgb(255, 235, 235);color: red") #change input field color
                    self.correct = False

            if(self.correct == True): #if every input is correct
                #send username, password to server
                global player_data
                player_data = (self.input_field_list[0].text(),hashlib.sha256(self.input_field_list[1].text().encode()).hexdigest(),"L")
                window.close()
            






class RegisterWindow(QMainWindow):
    def __init__(self): #the __init__ method of the super() class must always be called
        super().__init__()

        self.setWindowTitle("Battleship") #set title

        self.setFixedSize(QSize(1000, 700)) #set window size

        self.layout1 = QGridLayout() #create grid layout
        self.layout2 = QVBoxLayout() #create vertical layout


        self.input_field_text = ["login","password","repeat password"] #list with input field text
        self.input_field_list = [] #list for input fields

        for i in range(len(self.input_field_text)): #for loop to create input fields
            self.input_field = QLineEdit(self) #create input field
            self.input_field.setMaxLength(25) #set input field text max length
            self.input_field.setFixedSize(QSize(600, 90)) #set input field size
            #self.input_field.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.input_field.setFont(QFont('Arial', 18)) #set input field text font and size
            self.input_field.setPlaceholderText(self.input_field_text[i]) #set input field placeholder text
            if(self.input_field_text[i] == "password" or self.input_field_text[i] == "repeat password"): 
                self.input_field.setEchoMode(QLineEdit.EchoMode.Password) #if password, hide text with *
            self.layout2.addWidget(self.input_field) #add input field to layout
            self.layout2.setAlignment(Qt.AlignmentFlag.AlignCenter) #align input field to center
            self.input_field_list.append(self.input_field) #append input field into input_field_list


        self.button_text = ["RETURN","OK"] #list with button text
        self.button_list = [] #list for buttons

        for i in range(len(self.button_text)): #for loop to create buttons
            self.button = QPushButton(self.button_text[i]) #create button
            self.button.setFixedSize(290, 90) #set button size
            self.button.setStyleSheet("font: bold;background-color: white;font-size: 36px;") #set button text font, color and size
            self.button.clicked.connect(self.button_clicked) #connect button to function
            self.button_list.append(self.button) #append button into button_list
            self.layout1.addWidget(self.button,0,i) #add button to layout
            self.layout1.setAlignment(Qt.AlignmentFlag.AlignCenter) #align button to center


        self.layout2.addLayout(self.layout1) #combine layouts
        self.layout2.setSpacing(20) #set layout spacing

        self.widget = QWidget() #create widget
        self.widget.setLayout(self.layout2) #set widget layout
        self.setCentralWidget(self.widget) #set widget position



    def button_clicked(self): #function for clicked button

        clicked_button = self.sender() #retrieve the object that sent the signal

        if(self.button_list.index(clicked_button) == 0):
            window.setCurrentWidget(page1) #change page
            for i in self.input_field_list: #for all input fields
                i.setStyleSheet("background-color: white;color: black") #reset color after leaving


        if(self.button_list.index(clicked_button) == 1):

            for i in self.input_field_list: #for all input fields
                i.setStyleSheet("background-color: white;color: black") #set color
            self.correct = True

            for i in self.input_field_list: #for all input fields
                if(i.text() == ""): #if empty (no text)
                    i.setStyleSheet("background-color: rgb(255, 235, 235);color: red") #change input field color
                    self.correct = False

            if(self.input_field_list[-2].text() != self.input_field_list[-1].text()): #if passwords not the same
                self.input_field_list[2].setStyleSheet("background-color: rgb(255, 235, 235);color: red") #change input field color
                self.correct = False

            if(self.correct == True): #if every input is correct
                global player_data
                player_data = (self.input_field_list[0].text(),hashlib.sha256(self.input_field_list[1].text().encode()).hexdigest(),"R")
                window.close()
                
                    




                
def login_register_window():
    global app, window, page1, page2, page3
    app = QApplication(sys.argv) #creates instance of QApplication class
    window = QStackedWidget() #create window
    #page system
    page1 = StartingPage()
    page2 = LoginWindow() 
    page3 = RegisterWindow()
    pages = [page1, page2, page3] #page list
    for i in pages:
        window.addWidget(i) #add page
    window.setCurrentWidget(page1) #set starting window
    window.show() #show window
    app.exec() #start the event loop
    return player_data[0], player_data[1], player_data[2]