from login_page import login_register_window
from Playerpage import player_page
import networking
import shipplacement
def dataprep(type ,*data):
    prepdata = (type, (data))
    return prepdata

def checkifhit (x,y):
    #server bekommt coords von Client
    server.send(dataprep("s",x,y))
    #rückmeldung über Feldstatus
    fieldstate = server.receive()
    return fieldstate




    
IP = "localhost"
Port = 65500

server = networking.Client_Net()
server.client_Connect(IP,Port)

#LOGIN/REGISTER
username, password, login_or_register = login_register_window() #"L" for Login/"R" for Register

#sendToServer(username,password,login_or_register)
if login_or_register == "L":
    server.send(dataprep("l",username, password))
else:
    server.send(dataprep("n",username, password))
#get from server: true or false
login = server.receive()

if login != None:           #TODO: kp was der server da zurück schickt


#!!!MATCHMAKING!!!
    
    player_page()
    #from gui: what player is challenged

#!!!GAME!!!
    print("Starting Shipplacement...")
    shipplacement()
    #send to server: Shipplacement

    #grabbing usefull data for showcase
    opponent = server.receive()

    ##print(f"{username},{password},{login_or_register}")

    while(login):
        myturn = server.receive() #wait for server
        if myturn == True:
            #from gui: coord input
            checkifhit()
            #to gui: show where hit and what

        if myturn == False:
            enemyhit = server.receive()
            #to gui: show where hit and what