from login_page import *
from Playerpage import *
import networking
import shipplacement
def dataprep(type ,*data):
    prepdata = (type, (data))
    return prepdata


    
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
#get from server: opponent
opponent = server.receive()

print("Starting Shipplacement...")
shipplacement()
##send to server: Shipplacement

##print(f"{username},{password},{login_or_register}")

while(login):
    fturn = server.receive()
    ##if fturn == True:
        