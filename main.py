import pygame
import os
##import Tkinter
##import Image
from pygame.locals import *
from sys import exit
from PodSixNet.Connection import ConnectionListener, connection
from time import sleep
from Triangle import *
from Line import *
from Dot import *
from Text import *


''' 示意圖

   [0]  -  [1]  -  [2]
  /   \   /   \   /   \
[3] -  [4]  -  [5]  -  [6]
  \   /   \   /   \   / 
    [7] -  [8]  -  [9]

'''


class Game(ConnectionListener):

    global BLACK, WHITE, RED, BLUE, RED_TRI, BLUE_TRI, startP, endP
    
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    RED_TRI = (255, 128, 128)
    BLUE_TRI = (128, 128, 255)
    startP = None
    endP = None

    def Network_close(self, data):
        exit()
        
    def Network_yourturn(self, data):
        self.turn = data["turn"]
        
    def Network_startgame(self, data):
        self.running = True
        self.num = data["player"]
        self.gameid = data["gameid"]
        
    def Network_place(self, data):        
        startP_x = data["startP_x"]
        startP_y = data["startP_y"]  
        endP_x = data["endP_x"]
        endP_y = data["endP_y"]
        startP_i = data["startP_i"]
        endP_i = data["endP_i"]
        
##        try:
##            self.connected_dots[startP_i].remove(-1)        # 將起點之連接記錄的初始值(-1)移除
##            self.connected_dots[endP_i].remove(-1)          # 將終點之連接記錄的初始值(-1)移除
##            
##        except:
##            pass
        
        self.connected_dots[startP_i].append(endP_i)        # 記錄起點連接至終點
        self.connected_dots[endP_i].append(startP_i)        # 記錄終點連接至起點

        
        print(data)
        print(self.connected_dots[startP_i])

        global url, coord_temp
        
        if startP_y == endP_y:
            if startP_x < endP_x:
                if self.color_LN == BLUE:
                    url = pygame.image.load("image/blue_line.png")
                else:
                    url = pygame.image.load("image/red_line.png")
                coord_temp = [startP_x, startP_y-5]
            else:
                if self.color_LN == BLUE:
                    url = pygame.image.load("image/blue_line.png")
                else:
                    url = pygame.image.load("image/red_line.png")
                coord_temp = [endP_x, endP_y-5]
        
        elif startP_y < endP_y:
            if startP_x < endP_x:
                if self.color_LN == BLUE:
                    url = pygame.transform.rotate(pygame.image.load("image/blue_line.png"), -60)
                else:
                    url = pygame.transform.rotate(pygame.image.load("image/red_line.png"), -60)
                coord_temp = [startP_x-3, startP_y]
            else:
                if self.color_LN == BLUE:
                    url = pygame.transform.rotate(pygame.image.load("image/blue_line.png"), 60)
                else:
                    url = pygame.transform.rotate(pygame.image.load("image/red_line.png"), 60)
                coord_temp = [startP_x-105, startP_y]
            
        else:
            if startP_x < endP_x:
                if self.color_LN == BLUE:
                    url = pygame.transform.rotate(pygame.image.load("image/blue_line.png"), 60)
                else:
                    url = pygame.transform.rotate(pygame.image.load("image/red_line.png"), 60)
                coord_temp = [startP_x, startP_y-180]
            else:
                if self.color_LN == BLUE:
                    url = pygame.transform.rotate(pygame.image.load("image/blue_line.png"), -60)
                else:
                    url = pygame.transform.rotate(pygame.image.load("image/red_line.png"), -60)
                coord_temp = [startP_x-100, startP_y-171]

        startP = Dot(self.screen, startP_i, [startP_x, startP_y])
        endP = Dot(self.screen, endP_i, [endP_x, endP_y])
            
        new_line = Line(self.screen, startP, endP, coord_temp, self.color_LN, url, None)
        self.LINES.append(new_line)  
        
        self.score_blue, self.score_red = self.check_and_create_triangle(startP, endP)     #確認是並產生三角形

        self.isConnected = 1

        ### 一旦產生連線事件，畫面更新 ###                   
        if self.isConnected == 1:
            self.redraw()
            
            # line起點,終點重設預設值
            startP = endP = None
            self.turn_N += 1
            self.isConnected = 0
        
        pygame.display.flip()

        ### 根據回合數變換顏色 ###                    
        if self.turn_N % 2 == 0 :
            self.color_LN = BLUE
            self.color_TRI = BLUE_TRI
        else:
            self.color_LN = RED
            self.color_TRI = RED_TRI

    def __init__(self):
        
        ### Constent ###
        self.SCREEN_SIZE = [800, 600]       # 視窗解析度
        self.TITLE = "Dot to Dot"           # 視窗標題    
        self.points_TRI = 3                 # 產生三角形之得分數
        self.points_LN = 1                  # 線條變色之得分數

        ### Variable ###
        self.turn = True                    # 是否為你的回合
        self.turn_N = 0                     # 回合數
        self.color_LN = BLUE                # 該回合 Line 顏色
        self.color_TRI = BLUE_TRI           # 該回合 Triangle 顏色
        self.isConnected = 0 		    # 刷新畫面之開關
        self.status = "Theme"

        ### Lines ###
        self.LINES = []

        ### Triangle ###
        self.TRIANGLES = []

        ### background ###
##        bg = Image.open('image/background.jpg')  
##        new_bg = bg.resize(self.SCREEN_SIZE,Image.ANTIALIAS)
##        new_bg.save('image/background-new.jpg',quality=100)
        self.bg_pic = pygame.image.load('image/background-new.jpg')

        ### Theme and button ###
        self.title = pygame.image.load('image/title.png')        
        self.play_title_coord = [self.SCREEN_SIZE[0]/2 - 164, self.SCREEN_SIZE[1]/3 - 80]
        self.play_button = pygame.image.load('image/play.png')
        self.play_button_coord = [self.SCREEN_SIZE[0]/2 - 81.5, self.SCREEN_SIZE[1]/3 * 2 - 28]

        ### Initialize Pygame ###
        pygame.init()
        pygame.display.set_caption(self.TITLE)
        self.screen = pygame.display.set_mode(self.SCREEN_SIZE)
        self.screen.fill(WHITE)
        self.screen.blit(self.bg_pic, [0, 0])
        self.screen.blit(self.title, self.play_title_coord)        
        self.screen.blit(self.play_button, self.play_button_coord)

        ### Initialize Music and Sound###
        pygame.mixer.init()
        pygame.mixer.music.load('music/background.ogg')
        pygame.mixer.music.play(0)
        self.link_sound = pygame.mixer.Sound('sound/link.wav')


        ### Initialize  Clock ###
        self.clock = pygame.time.Clock()

        ### Input dots coord ###
        self.DOTS = []
        self.connected_dots = []
        dots_file = open("dots.txt")
        setting = dots_file.readline().strip()
        dot_id = 0
        while setting:
            coord = setting.split(",")
            new_dot = Dot(self.screen, dot_id, [int(coord[0]), int(coord[1])])
            self.DOTS.append(new_dot)
            setting = dots_file.readline().strip()
            self.connected_dots.append([])
            dot_id += 1

                                    ### draw field lines ###
                                    ##create_field_line(screen, BLACK, DOTS, F_LINES, connected_dots)
                                    ##for i in range(len(F_LINES)):
                                    ##    F_LINES[i].draw()
            
##        ### Draw dots ###
##        for i in range(len(self.DOTS)):
##            self.DOTS[i].draw()

        ### Create and draw score texts ###
        self.SCORE_FONT = pygame.font.Font(None,40)        
        self.SCORE_COLOR = BLACK
        
        self.score_blue = 0
        self.score_red = 0
        
        self.score_me = 0        
        self.score_me_coord = [110,41]                
        self.score_me_text_coord = [280,50]
        self.MY_SCORE_PIC = pygame.image.load("image/my_score.png")
        self.SCORE_MY_TEXT = Text(self.screen, str(self.score_me), self.SCORE_COLOR, self.SCORE_FONT, self.score_me_text_coord)
        
        self.score_enemy = 0
        self.score_enemy_coord = [510,41]                
        self.score_enemy_text_coord = [680,50]        
        self.ENEMY_SCORE_PIC = pygame.image.load("image/enemy_score.png")
        self.SCORE_ENEMY_TEXT = Text(self.screen, str(self.score_enemy), self.SCORE_COLOR, self.SCORE_FONT, self.score_enemy_text_coord)
      
        while True:

            if self.status == "Connecting":
                
                self.screen.blit(self.bg_pic, [0, 0])
                loading_text = Text(self.screen, str("Waiting..."), self.SCORE_COLOR, pygame.font.Font(None,60) , [self.SCREEN_SIZE[0]/2-60, self.SCREEN_SIZE[1]/2-50])
                loading_text.draw()
                pygame.display.flip()
                
                ### 連接Server ###
                address = raw_input("Address of Server: ")
                try:
                    if not address:
                        host, port = "localhost", 8000
                    else:
                        host,port = address.split(":")
                    self.Connect((host, int(port)))
                except:
                    print "Error Connecting to Server"
                    print "Usage:", "host:port"
                    print "e.g.", "localhost:31425"
                    exit()
                print "Boxes client started"
            
                ### 等待對方連接Server成功 ###
                self.running = False
                while not self.running:
                    self.Pump()
                    connection.Pump()
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            exit()
                self.running = False

                ### 決定先後下棋順序 ###
                if self.num == 0:
                    self.turn = True
                    self.my_color = "B"
                    self.enemy_color = "R"
                else:
                    self.turn = False
                    self.my_color = "R"
                    self.enemy_color = "B"
                    
                self.status = "Gaming"                
                self.redraw()

            if self.status == "Gaming":
                self.clock.tick(60)
                connection.Pump()
                self.Pump()
            
                
            ### 滑鼠事件處理 ###  
            for event in pygame.event.get():
                
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                                
                elif event.type == MOUSEMOTION:
                    global pos
                    pos = pygame.mouse.get_pos()

                elif event.type == MOUSEBUTTONDOWN and self.status == "Theme":
                    
                    pos = pygame.mouse.get_pos()
                            
                    button_x1 = self.play_button_coord[0]
                    button_x2 = self.play_button_coord[0] + 163
                    button_y1 = self.play_button_coord[1]
                    button_y2 = self.play_button_coord[1] + 56
                    
                    if pos[0] >= button_x1 and  pos[0] <= button_x2 and pos[1] >= button_y1 and pos[1] <= button_y2:
                        self.status = "Connecting"
                    
                elif event.type == MOUSEBUTTONDOWN and self.turn and self.status == "Gaming":                
                    pos = pygame.mouse.get_pos()
                    
                    # Line起點與終點預設None
                    startP = endP = None

                    # 確認點擊位置有無Dot；若有，將起點座設為該Dot                
                    startP = self.clicked_dot(pos)
                    if startP != None:
                        self.target_connectable_dot(startP)                        
                        print(self.connected_dots[startP.i])
                    elif startP == None:
                        self.redraw()
                        pygame.display.flip()
                    
                elif event.type == MOUSEBUTTONUP and self.turn and self.status == "Gaming" :
                    pos = pygame.mouse.get_pos()

                    # 確認點擊位置有無Dot；若有，將終點設為該Dot 
                    endP = self.clicked_dot(pos)
                        
                    # 判斷是否兩點可連接(重複連接、距離過長、起點與終點為同一點，以上為無法連接的情況)
                    if self.connectable(startP, endP):
                        self.link_sound.play()               
                        self.Send({"action": "place", "startP_i":startP.i, "startP_x":startP.coord[0], "startP_y":startP.coord[1], "endP_i":endP.i, "endP_x":endP.coord[0], "endP_y":endP.coord[1], "num": self.num, "gameid": self.gameid})
                      
                    else:
                        self.redraw()
                        pygame.display.flip()  
                            
                pygame.display.flip()

                

    def target_connectable_dot(self, startP):
        TARGET_PIC = pygame.image.load("image/target.png")
        for k in range(len(self.DOTS)):
            if self.DOTS[k].i != startP.i:
                distance_squa = (startP.coord[0] - self.DOTS[k].coord[0]) ** 2 + (startP.coord[1] - self.DOTS[k].coord[1]) ** 2
                if distance_squa <= 44025 and distance_squa > 0:
                    check = 0
                    for j in range(len(self.connected_dots[startP.i])):
                        if self.connected_dots[startP.i][j] == self.DOTS[k].i :
                            check += 1
                    if check == 0: 
                        target_coord = [self.DOTS[k].coord[0]-19, self.DOTS[k].coord[1]-18.5]
                        self.screen.blit(TARGET_PIC, target_coord)
                        pygame.display.flip()
                

    def clicked_dot(self, pos):
        for i in range(len(self.DOTS)):
            if pos[0] >= self.DOTS[i].coord[0] - 20 and pos[0] <= self.DOTS[i].coord[0] + 20:
                if pos[1] >= self.DOTS[i].coord[1] - 20 and pos[1] <= self.DOTS[i].coord[1] + 20:
                    return self.DOTS[i]
        return None


    def connectable(self, startP, endP):
        if endP != None:
            distance_squa = (startP.coord[0] - endP.coord[0]) ** 2 + (startP.coord[1] - endP.coord[1]) ** 2
            if distance_squa <= 44025 and distance_squa > 0 :
                check = 0
                for j in range(len(self.connected_dots[startP.i])):
                    if self.connected_dots[startP.i][j] == endP.i:
                        return False
                for j in range(len(self.connected_dots[endP.i])):
                    if self.connected_dots[endP.i][j] == startP.i:
                        return False
                return True            
        return False

    def check_and_create_triangle(self, startP, endP):
        for i in range(len(self.connected_dots[startP.i])):
            for j in range(len(self.connected_dots[endP.i])):
                
                ### 檢查是否有Dot與起點、終點連接 ###
                if self.connected_dots[startP.i][i] == self.connected_dots[endP.i][j]:
                    dot3_id = self.connected_dots[startP.i][i]
                    
                    coord_x = startP.coord[0]
                    if endP.coord[0] < coord_x:
                            coord_x = endP.coord[0];
                    if self.DOTS[dot3_id].coord[0] < coord_x:
                            coord_x = self.DOTS[dot3_id].coord[0];
                            
                    coord_y = startP.coord[1]
                    if endP.coord[1] < coord_y:
                            coord_y = endP.coord[1];
                    if self.DOTS[dot3_id].coord[1] < coord_y:
                            coord_y = self.DOTS[dot3_id].coord[1];

                    global angle
                    angle = 0
                    
                    if (startP.coord[1] == endP.coord[1] and startP.coord[1] > self.DOTS[dot3_id].coord[1]) or (startP.coord[1] == self.DOTS[dot3_id].coord[1] and startP.coord[1] > endP.coord[1]) or (endP.coord[1] == self.DOTS[dot3_id].coord[1]and endP.coord[1] > startP.coord[1]):
                        angle = 60
                        
                    if self.color_LN == BLUE:
                        url = pygame.transform.rotate(pygame.image.load("image/blue_tri.png"), angle)
                    else:
                        url = pygame.transform.rotate(pygame.image.load("image/red_tri.png"), angle)
                    
                    new_triangle = Triangle(self.screen, startP, endP, self.DOTS[dot3_id], self.color_TRI, url, [coord_x, coord_y])
                    self.TRIANGLES.append(new_triangle)
                    self.score_blue, self.score_red = self.gain_points(self.points_TRI)
                    
                    ### 將三角形之異色邊轉為同色，每改變一條線+10分 ###
                    for k in range(len(self.LINES)):
                        global change_color
                        change_color = False
                        
                        ### 檢查 self.LINES[k]的兩端點 是否有與起點和終點連線 ###
                        if ((startP.i == self.LINES[k].startP.i or endP.i == self.LINES[k].startP.i) and (startP.i == self.LINES[k].endP.i or endP.i == self.LINES[k].endP.i)) and self.LINES[k].color != self.color_LN:
                            self.LINES[k].color = self.color_LN
                            self.score_blue, self.score_red = self.gain_points(self.points_LN)
                            change_color = True
                            
                        ### 檢查 self.LINES[k]的兩端點 是否有與起點和dot3連線 ###
                        elif ((startP.i == self.LINES[k].startP.i or dot3_id == self.LINES[k].startP.i) and (startP.i == self.LINES[k].endP.i or dot3_id == self.LINES[k].endP.i)) and self.LINES[k].color != self.color_LN:
                            self.LINES[k].color = self.color_LN
                            self.score_blue, self.score_red = self.gain_points(self.points_LN)
                            change_color = True
                            
                        ### 檢查 self.LINES[k]的兩端點 是否有與dot3和終點連線 ###
                        elif ((dot3_id == self.LINES[k].startP.i or endP.i == self.LINES[k].startP.i) and (dot3_id== self.LINES[k].endP.i or endP.i == self.LINES[k].endP.i)) and self.LINES[k].color != self.color_LN:
                            self.LINES[k].color = self.color_LN
                            self.score_blue, self.score_red = self.gain_points(self.points_LN)
                            change_color = True
                            
                        if self.LINES[k].startP.coord[1] == self.LINES[k].endP.coord[1] and change_color:
                            if self.LINES[k].color == BLUE:
                                self.LINES[k].url = pygame.image.load("image/blue_line.png")
                            else:
                                self.LINES[k].url = pygame.image.load("image/red_line.png")
                        
                        elif self.LINES[k].startP.coord[1] < self.LINES[k].endP.coord[1] and change_color:
                            if self.LINES[k].startP.coord[0] < self.LINES[k].endP.coord[0]:
                                if self.LINES[k].color == BLUE:
                                    self.LINES[k].url = pygame.transform.rotate(pygame.image.load("image/blue_line.png"), -60)
                                else:
                                    self.LINES[k].url = pygame.transform.rotate(pygame.image.load("image/red_line.png"), -60)
                            else:
                                if self.LINES[k].color == BLUE:
                                    self.LINES[k].url = pygame.transform.rotate(pygame.image.load("image/blue_line.png"), 60)
                                else:
                                    self.LINES[k].url = pygame.transform.rotate(pygame.image.load("image/red_line.png"), 60)
                        elif  change_color:
                            if self.LINES[k].startP.coord[0] < self.LINES[k].endP.coord[0]:
                                if self.LINES[k].color == BLUE:
                                    self.LINES[k].url = pygame.transform.rotate(pygame.image.load("image/blue_line.png"), 60)
                                else:
                                    self.LINES[k].url = pygame.transform.rotate(pygame.image.load("image/red_line.png"), 60)
                            else:
                                if self.LINES[k].color == BLUE:
                                    self.LINES[k].url = pygame.transform.rotate(pygame.image.load("image/blue_line.png"), -60)
                                else:
                                    self.LINES[k].url = pygame.transform.rotate(pygame.image.load("image/red_line.png"), -60)
                        change_color = False
                                
        return self.score_blue, self.score_red


    def redraw(self):
        self.screen.fill(WHITE)
        self.screen.blit(self.bg_pic, [0, 0])
        for i in range(len(self.TRIANGLES)):
            self.TRIANGLES[i].draw()
    ##    for i in range(len(F_LINES)):
    ##        F_LINES[i].draw()
        for i in range(len(self.LINES)):
            self.LINES[i].draw()
        for i in range(len(self.DOTS)):
            self.DOTS[i].draw()
            
        self.screen.blit(self.MY_SCORE_PIC, self.score_me_coord )
        self.screen.blit(self.ENEMY_SCORE_PIC, self.score_enemy_coord )
        
        if self.my_color == "B":            
            self.SCORE_MY_TEXT = Text(self.screen, str(self.score_blue), self.SCORE_COLOR, self.SCORE_FONT, self.score_me_text_coord)
            self.SCORE_ENEMY_TEXT = Text(self.screen, str(self.score_red), self.SCORE_COLOR, self.SCORE_FONT, self.score_enemy_text_coord)
        else:
            self.SCORE_MY_TEXT = Text(self.screen, str(self.score_red), self.SCORE_COLOR, self.SCORE_FONT, self.score_me_text_coord)
            self.SCORE_ENEMY_TEXT = Text(self.screen, str(self.score_blue), self.SCORE_COLOR, self.SCORE_FONT, self.score_enemy_text_coord)      
        self.SCORE_MY_TEXT.draw()
        self.SCORE_ENEMY_TEXT.draw()

    def gain_points(self, points):
        if self.color_LN == BLUE:
            self.score_blue += points
        else:
            self.score_red += points
        return self.score_blue, self.score_red

    def Network_win(self, data):
        pass
    
    def Network_lose(self, data):
        pass

        
if __name__ == "__main__":
    GAME_START = Game()
    GAME_START.update()


