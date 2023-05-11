import sys
from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt
global turn
turn = 0

class GameBoard(QWidget):
    def __init__(self):
        super().__init__()

        self.spielfeld1 = QGridLayout()
        self.spielfeld1.setSpacing(0)
        self.spielfeld2 = QGridLayout()
        self.spielfeld2.setSpacing(0)

        for row in range(15):
            for col in range(15):
                button1 = QPushButton()
                button1.setStyleSheet("background-color: blue;")
                button1.setFixedSize(30, 30)
                button1.setProperty("row", row)
                button1.setProperty("col", col)

                self.setFixedSize(900,500)

                button1.clicked.connect(self.handleButtonClick)

                self.spielfeld1.addWidget(button1, row, col)

                button2 = QPushButton()
                button2.setStyleSheet("background-color: blue;")
                button2.setFixedSize(30, 30)
                button2.setDisabled(True)

                self.spielfeld2.addWidget(button2, row, col)

        mainLayout = QGridLayout()
        mainLayout.addWidget(QLabel("OPPONENT"), 0, 0, alignment=Qt.AlignmentFlag.AlignHCenter)
        mainLayout.addWidget(QLabel("PLAYER"), 0, 1, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.label = QLabel("Ursprünglicher Text")
        mainLayout.addWidget(self.label,0,0,alignment=Qt.AlignmentFlag.AlignVCenter)
        self.setWindowTitle("BattleShip")

        mainLayout.addLayout(self.spielfeld1, 1, 0)
        mainLayout.addLayout(self.spielfeld2, 1, 1)

        self.setLayout(mainLayout)

    def handleButtonClick(self):
        button = self.sender()
        if (turn == 1):
            if button:
                row = button.property("row")
                col = button.property("col")

                print("Koordinaten: (", row, ",", col, ")")

                button.setDisabled(True)
                button.setStyleSheet("background-color: red;")

                return(row, col)
        
    def changeturn(self, turn):
        if(turn == 1):
            self.label.setText("YOUR TURN")

        if(turn == 0):
            self.label.setText("OPPONENTS TURN")
            

            
            

            #self.färbeFeldImSpielfeld2(row, col)

    def färbeFeldImSpielfeld2(self, row, col, color):
        button = self.spielfeld2.itemAtPosition(row, col).widget()
        if button:
            button.setStyleSheet("background-color: {};".format(color))

if __name__ == '__main__':
    app = QApplication(sys.argv)

    gameBoard = GameBoard()
    gameBoard.show()
    gameBoard.färbeFeldImSpielfeld2(0, 0, "gray")
    gameBoard.changeturn(turn)
    sys.exit(app.exec())
