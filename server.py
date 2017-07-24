import PodSixNet.Channel
import PodSixNet.Server
from time import sleep
from Dot import *


class ClientChannel(PodSixNet.Channel.Channel):
    
    def Network(self, data):
        print 'ClientChannel.Network'
        print data
        
    def Network_place(self, data):
        print 'ClientChannel.Network_place'

        startP_i = data["startP_i"]
        startP_x = data["startP_x"]
        startP_y = data["startP_y"]  
        endP_i = data["endP_i"]
        endP_x = data["endP_x"]
        endP_y = data["endP_y"]  
        num = data["num"]     
        self.gameid = data["gameid"]
     
        self._server.placeLine(startP_i, startP_x, startP_y, endP_i, endP_x, endP_y, data, self.gameid, num)
        
    def Close(self):
        print 'ClientChannel.Close'
        self._server.close(self.gameid)
        
class GameServer(PodSixNet.Server.Server):
 
    channelClass = ClientChannel
    
    def __init__(self, *args, **kwargs):
        PodSixNet.Server.Server.__init__(self, *args, **kwargs)
        self.games = []
        self.queue = None
        self.currentIndex=0
        
    def Connected(self, channel, addr):
        print 'new connection:', channel
        if self.queue==None:
            self.currentIndex+=1
            channel.gameid=self.currentIndex
            self.queue=Game(channel, self.currentIndex)
            
        else:
            channel.gameid=self.currentIndex
            self.queue.player1=channel
            self.queue.player0.Send({"action": "startgame","player":0, "gameid": self.queue.gameid})
            self.queue.player1.Send({"action": "startgame","player":1, "gameid": self.queue.gameid})
            self.games.append(self.queue)
            self.queue=None
            
    def placeLine(self, startP_i, startP_x, startP_y, endP_i, endP_x, endP_y, data, gameid, num):
        print 'Server.placeLine'
        game = [a for a in self.games if a.gameid==gameid]
        if len(game)==1:
            game[0].placeLine(startP_i, startP_x, startP_y, endP_i, endP_x, endP_y, data, num)
            
    def close(self, gameid):
        try:
            game = [a for a in self.games if a.gameid==gameid][0]
            game.player0.Send({"action":"close"})
            game.player1.Send({"action":"close"})
        except:
            pass
        
    def tick(self):
        # Check for any wins
        # Loop through all of the squares
        index=0
        for game in self.games:
            game.player1.Send({"action":"yourturn", "turn":True if self.games[index].turn==1 else False})
            game.player0.Send({"action":"yourturn", "turn":True if self.games[index].turn==0 else False})
            index+=1
        self.Pump()

        
class Game:
    
    def __init__(self, player0, currentIndex):
        
        self.turn = 0
        self.player0 = player0
        self.player1 = None
        self.gameid = currentIndex
        
    def placeLine(self, startP_i, startP_x, startP_y, endP_i, endP_x, endP_y, data, num):
        print 'Game.placeLine'
    
        if num == self.turn:            
            self.turn = 0 if self.turn else 1
            self.player1.Send({"action":"yourturn", "turn":True if self.turn==1 else False})
            self.player0.Send({"action":"yourturn", "turn":True if self.turn==0 else False})
            self.player0.Send(data)
            self.player1.Send(data)
print "STARTING SERVER ON LOCALHOST"

# try:
address=raw_input("Host:Port (localhost:8000): ")
if not address:
    host, port="localhost", 8000
    
else:
    host,port=address.split(":")
gameServe = GameServer(localaddr=(host, int(port)))

while True:
    gameServe.tick()
    sleep(0.01)
