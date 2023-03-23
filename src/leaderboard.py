def user_leaderboard_wins(pathtofile):
    leaderboard = []
    winlist = []                                                         #temporary list for the win values of all users
    with open(pathtofile, 'r') as savefile:
        data = savefile.readlines()

        for i in range(0,len(data)):
            data[i] = data[i].strip('\n')

        for i in range (2, len(data),4):
            winlist.append(data[i-2])
            winlist.append(int(data[i]))
            winlist.append(data[i+1])

        #print(winlist)

        for i in range(0,len(data)): 
            #print(winlist)
            tempwinlist = []
            #val = 0
            #val2 = 0
            for i in range (1,len(winlist),3):  
                tempwinlist.append(winlist[i])                                        
                val = max(tempwinlist)
            #print(max(tempwinlist))
            #print(tempwinlist)
            #print(val)
            if val == -1:
                break
            leaderboard.append(winlist[winlist.index(val)-1]) 
            leaderboard.append(val)  
            val2 = int(winlist[winlist.index(val)+1]) 
            #print(val)
            #print(val2,"\n")                                   
            leaderboard.append(val+val2)                              
            winlist[winlist.index(val)] = -1
            #print(leaderboard)                         
        return leaderboard
    
#testing
if __name__ == '__main__':
    path = "player_data.txt"
    print(user_leaderboard_wins(path))