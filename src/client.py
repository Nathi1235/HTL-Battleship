from login_page import *

player_data = login_register_window()
username, password = player_data[0], player_data[1]
#send to server: username, password
#get from server: true or false
print(f"{username},{password}")


