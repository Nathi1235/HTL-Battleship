from login_page import *
from Playerpage import *

#LOGIN/REGISTER
username, password, login_or_register = login_register_window() #"L" for Login/"R" for Register
#send to server: username, password
#get from server: true or false
#sendToServer(username,password,login_or_register)
print(f"{username},{password},{login_or_register}")

#ENEMY SELECTION
player_page()


