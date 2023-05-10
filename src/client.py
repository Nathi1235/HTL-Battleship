from login_page import login_register_window
from Playerpage import player_page
import networking
import shipplacement
import game_page
from PyQt6.QtCore import QThread
import requests
import time
from fastapi import FastAPI
import threading

global main_gameid
shipp = False
global ip

ip = "http://127.0.0.1:8000"

app = FastAPI()


def thread_function():
    # Wartezeit von 15 Sekunden
    for i in range(0,15):
        time.sleep(1)
        req = requests.post(ip+"/checkifaccepted"+f"?game={main_gameid}") 
        eq = req.json()
        if(req == 1):
            shipp = True
            return
    
    # löschen der GameRequest
    requests.post(ip+"/delgamerequest"+f"?game={main_gameid}")




     








#LOGIN/REGISTER
username, password, login_or_register = login_register_window() #"L" for Login/"R" for Register

if login_or_register == "L":
    lresponse = requests.get(url+f"?username={username}&password={password}")

else:
    lresponse = requests.get(url+f"?username={username}&password={password}")



if lresponse == 1:           
    login = True

while(login):
    player_page()


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

    if(shipp == True):
        fight = True
        break

    


while(fight):

    #!!!GAME!!!
    print("Starting Shipplacement...")
    shipplacement()
    #send to server: Shipplacement
    game_page.ships() #list with ship coords for coloring
    print("Shipplacement finished!")
  

    #print(f"{username},{password},{login_or_register}")

    while(True):
        myturn = server.receive() #wait for server
        if myturn == True:
            hit = checkifhit(game_page.opp_button_clicked())
            game_page.setcolor(hit[0],hit[1],0)
            game_page.disable_buttons(hit[0],hit[1])

        if myturn == False:
            enemyhit = server.receive()
            game_page.setcolor(enemyhit[0],enemyhit[1],1,enemyhit[2])

        if myturn == "Win":
            #from gui: Winscreen
            break

        if myturn == "Lose":
            #from gui: Losescreen
            break
