from itertools import cycle
import pygame as pg
import time
from resources_full import *
from tools import *
from Qtools import *
import matplotlib.pyplot as plt

# Use these libraries for classic random implementation
from random import randrange as rnd
from random import choice

# Use these libraries for quantum random implementation
# from quantumRandomFunctions import qrandrange as rnd
# from quantumRandomFunctions import qchoice as choice

pg.init()

qc = QuantumCircuit(1)
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
SCORE = 0
direction = 0
speed = 4
status = 0    #0 = Alive | 1 = Death | 2 = Superposition
height = (SCREEN_HEIGHT // 2)
if status == 2: 
    FPS = 90
else: 
    FPS = 160
alive_ast = player_w
death_ast = player_b

"""
///////////////////////////////////////////////////////////
   QUANTUM ENGINE
///////////////////////////////////////////////////////////
"""

class ItemManager():
    def __init__(self):
        global status

        self.items = [(notgatebit_w, notgatebit_b), (ygatebit_w, ygatebit_b), (zgatebit_w, zgatebit_b), (hgatebit_w, hgatebit_b), (swapgatebit_w, swapgatebit_b), (qubit_w_s, qubit_w_l)]
        self.obs_height = (SCREEN_HEIGHT//2 - 80, SCREEN_HEIGHT//2 + 55)

        if status == 2:
            item_ast = choice(self.items)
            self.side = rnd(0,2)
            self.item1 = (rnd(SCREEN_WIDTH, SCREEN_WIDTH+500), self.obs_height[self.side])
            self.item_ast1 = item_ast[self.side]
        else:
            self.item1 = (rnd(SCREEN_WIDTH, SCREEN_WIDTH+500), self.obs_height[status])
            self.item_ast1 = choice(self.items)[status]


    def update_items(self, screen, player_cub):
        global height
        global status
        self.player_cub = player_cub

        if status == 2:
            screen.blit(pg.image.fromstring(self.item_ast1.tobytes(), self.item_ast1.size, 'RGBA'), self.item1)

            if self.item1[0]<=-50:
                item_ast = choice(self.items)
                self.side = rnd(0,2)
                self.item1 = (rnd(SCREEN_WIDTH, SCREEN_WIDTH+500), self.obs_height[self.side])
                self.item_ast1 = item_ast[self.side]
        else:
            screen.blit(pg.image.fromstring(self.item_ast1.tobytes(), self.item_ast1.size, 'RGBA'), self.item1)  
            if self.item1[0]<=-50:
                self.item1 = (rnd(SCREEN_WIDTH, SCREEN_WIDTH+500), self.obs_height[status])
                self.item_ast1 = choice(self.items)[status]

    def display_item(self):
        global status
        
        if status == 2:
            self.item1 = (self.item1[0]-speed, self.item1[1])

            self.item1_cub = (self.item1[0], self.item1[1], self.item1[0] + self.item_ast1.size[0], self.item1[1] + self.item_ast1.size[1])

            if self.item1_cub[0]<=self.player_cub[2]-10<=self.item1_cub[2] and self.item1_cub[1]<=self.player_cub[3]-10<=self.item1_cub[3]-5:
                return False
        else:
            self.item1 = (self.item1[0]-speed, self.item1[1])
        
            self.item1_cub = (self.item1[0], self.item1[1], self.item1[0] + self.item_ast1.size[0], self.item1[1] + self.item_ast1.size[1])
       
            if self.item1_cub[0]<=self.player_cub[2]-10<=self.item1_cub[2] and self.item1_cub[1]<=self.player_cub[3]-10<=self.item1_cub[3]-5:
                return False

        return True

class GateManager():
    def __init__(self):
        self.gates = []
        self.qc = QuantumCircuit(1)

    def push_gates(self,gate):
        self.gates.append(gate)
        add_gate(self.qc,gate,0)
    
    def get_gates(self):
        return self.gates

    def get_qc(self):
        return self.qc.draw()

    def measure(self):
        self.qc.measure_all()
        sim = Aer.get_backend('aer_simulator')
        x = measuring(self.qc,sim,1)
        k = list(x.keys())
        self.gates.clear()
        self.qc = QuantumCircuit(1)
        if k[0]=='1':
            self.qc.x(0)
        return k[0]

class ObstacleManager():
    def __init__(self):
        self.obstacles = [(noise_w_s, noise_b_s), (noise_w_l, noise_b_l)]
        self.obs_height = ((SCREEN_HEIGHT // 2) - 40 , (SCREEN_HEIGHT // 2) + 15)
        if status == 2:
            self.obs1 = (rnd(SCREEN_WIDTH, SCREEN_WIDTH+500), self.obs_height[0]-10)
            self.obs2 = (rnd(SCREEN_WIDTH*2, SCREEN_WIDTH*2+500), self.obs_height[0]-10)
            self.obast1 = choice(self.obstacles)
            self.obast2 = choice(self.obstacles)

            self.obs3 = (self.obs1[0], self.obs_height[1])
            self.obs4 = (self.obs2[0], self.obs_height[1])
            self.obast3 = self.obast1[1]
            self.obast4 = self.obast2[1]
            self.obast1 = self.obast1[0]
            self.obast2 = self.obast2[0]

        else:
            if status == 0:
                self.obs1 = (rnd(SCREEN_WIDTH, SCREEN_WIDTH+500), self.obs_height[0])
                self.obs2 = (rnd(SCREEN_WIDTH*2, SCREEN_WIDTH*2+500), self.obs_height[0])
                self.obast1 = choice(self.obstacles)[0]
                self.obast2 = choice(self.obstacles)[0]
            else:
                self.obs1 = (rnd(SCREEN_WIDTH, SCREEN_WIDTH+500), self.obs_height[1])
                self.obs2 = (rnd(SCREEN_WIDTH*2, SCREEN_WIDTH*2+500), self.obs_height[1])
                self.obast1 = choice(self.obstacles)[1]
                self.obast2 = choice(self.obstacles)[1]

    def update_items(self, screen, player_cub):
        global height
        global status
        self.player_cub = player_cub
        if status == 2:
            screen.blit(pg.image.fromstring(self.obast1.tobytes(), self.obast1.size, 'RGBA'), self.obs1)
            screen.blit(pg.image.fromstring(self.obast2.tobytes(), self.obast2.size, 'RGBA'), self.obs2)
            screen.blit(pg.image.fromstring(self.obast3.tobytes(), self.obast3.size, 'RGBA'), self.obs3)
            screen.blit(pg.image.fromstring(self.obast4.tobytes(), self.obast4.size, 'RGBA'), self.obs4)

            if self.obs1[0]<=-50:
                self.obs1 = (rnd(SCREEN_WIDTH, SCREEN_WIDTH+500), self.obs_height[0])
                self.obast1_choice = choice(self.obstacles)
                self.obast1 = self.obast1_choice[0]
                
            if self.obs2[0]<=-50:
                self.obs2 = (rnd(SCREEN_WIDTH*2, SCREEN_WIDTH*2+500), self.obs_height[0])
                self.obast2_choice = choice(self.obstacles)
                self.obast2 = self.obast2_choice[0]
            
            if self.obs3[0]<=-50:
                self.obs3 = (self.obs1[0], self.obs_height[1])
                self.obast3 = self.obast1_choice[1]
                
            if self.obs4[0]<=-50:
                self.obs4 = (self.obs2[0], self.obs_height[1])
                self.obast4 = self.obast2_choice[1]

        else:
            screen.blit(pg.image.fromstring(self.obast1.tobytes(), self.obast1.size, 'RGBA'), self.obs1)
            screen.blit(pg.image.fromstring(self.obast2.tobytes(), self.obast2.size, 'RGBA'), self.obs2)

            if status == 0:
                if self.obs1[0]<=-50:
                    self.obs1 = (rnd(SCREEN_WIDTH, SCREEN_WIDTH+500), self.obs_height[0])
                    self.obast1 = choice(self.obstacles)[status]

                if self.obs2[0]<=-50:
                    self.obs2 = (rnd(SCREEN_WIDTH*2, SCREEN_WIDTH*2+500), self.obs_height[0])
                    self.obast2 = choice(self.obstacles)[0]

            else:
                if self.obs1[0]<=-50:
                    self.obs1 = (rnd(SCREEN_WIDTH, SCREEN_WIDTH+500), self.obs_height[1])
                    self.obast1 = choice(self.obstacles)[1]

                if self.obs2[0]<=-50:
                    self.obs2 = (rnd(SCREEN_WIDTH*2, SCREEN_WIDTH*2+500), self.obs_height[1])
                    self.obast2 = choice(self.obstacles)[1]


    def display_obstacle(self):
        global status
        if status == 2:
            self.obs1 = (self.obs1[0]-speed, self.obs1[1])
            self.obs2 = (self.obs2[0]-speed, self.obs2[1])
            self.obs3 = (self.obs3[0]-speed, self.obs3[1])
            self.obs4 = (self.obs4[0]-speed, self.obs4[1])
            
            self.obs1_cub = (self.obs1[0], self.obs1[1], self.obs1[0] + self.obast1.size[0], self.obs1[1] + self.obast1.size[1])
            self.obs2_cub = (self.obs2[0], self.obs2[1], self.obs2[0] + self.obast2.size[0], self.obs2[1] + self.obast2.size[1])
            self.obs3_cub = (self.obs3[0], self.obs3[1], self.obs3[0] - self.obast3.size[0], self.obs3[1] - self.obast3.size[1])
            self.obs4_cub = (self.obs4[0], self.obs4[1], self.obs4[0] - self.obast4.size[0], self.obs4[1] - self.obast4.size[1])
            
            if self.obs1_cub[0]<=self.player_cub[0]+10<=self.obs1_cub[2] and self.obs1_cub[1]<=self.player_cub[1]+10<=self.obs1_cub[3]+5:
                return False
            if self.obs2_cub[0]<=self.player_cub[0]+10<=self.obs2_cub[2] and self.obs2_cub[1]<=self.player_cub[1]+10<=self.obs2_cub[3]+5:
                return False
            if self.obs3_cub[0]<=self.player_cub[0]+10<=self.obs3_cub[2] and self.obs3_cub[1]<=self.player_cub[1]+10<=self.obs3_cub[3]+5:
                return False
            if self.obs4_cub[0]<=self.player_cub[0]+10<=self.obs4_cub[2] and self.obs4_cub[1]<=self.player_cub[1]+10<=self.obs4_cub[3]+5:
                return False

            return True
        else:
            self.obs1 = (self.obs1[0]-speed, self.obs1[1])
            self.obs2 = (self.obs2[0]-speed, self.obs2[1])
            
            if status == 0:
                self.obs1_cub = (self.obs1[0], self.obs1[1], self.obs1[0] + self.obast1.size[0], self.obs1[1] + self.obast1.size[1])
                self.obs2_cub = (self.obs2[0], self.obs2[1], self.obs2[0] + self.obast2.size[0], self.obs2[1] + self.obast2.size[1])
                
                if self.obs1_cub[0]<=self.player_cub[0]-10<=self.obs1_cub[2] and self.obs1_cub[1]<=self.player_cub[3]+10<=self.obs1_cub[3]-5:
                    return False
                if self.obs2_cub[0]<=self.player_cub[0]-10<=self.obs2_cub[2] and self.obs2_cub[1]<=self.player_cub[3]+10<=self.obs2_cub[3]-5:
                    return False
            else:
                self.obs1_cub = (self.obs1[0], self.obs1[1], self.obs1[0] - self.obast1.size[0], self.obs1[1] - self.obast1.size[1])
                self.obs2_cub = (self.obs2[0], self.obs2[1], self.obs2[0] - self.obast2.size[0], self.obs2[1] - self.obast2.size[1])
                
                if self.obs1_cub[0]<=self.player_cub[2]+10<=self.obs1_cub[2] and self.obs1_cub[1]<=self.player_cub[3]+10<=self.obs1_cub[3]+50:
                    return False
                if self.obs2_cub[0]<=self.player_cub[2]+10<=self.obs2_cub[2] and self.obs2_cub[1]<=self.player_cub[3]+10<=self.obs2_cub[3]+50:
                    return False

            return True



"""
///////////////////////////////////////////////////////////
   GAME ENGINE
///////////////////////////////////////////////////////////
"""
class Game(object):
    def __init__(self):
        self.start = False
        self.lock = False
        self.jumping = False

    def process_events(self):
        global height
        for event in pg.event.get():
            #Quit game
            if event.type == pg.QUIT:
                return True

            #Press a key
            if event.type==pg.KEYDOWN:
                self.start = True
                if event.key == pg.K_SPACE:
                    if height >= (SCREEN_HEIGHT // 2)-20:self.jumping = True
                return False

    def display_alive_state(self, screen, obstacles, items):
        global height
        bg = (0, SCREEN_HEIGHT//2 - 15)
        bg1 = (ground_w.size[0], SCREEN_HEIGHT//2 - 15)
        player_sprite = live_ast
        player = player_sprite
        
        #Floor
        screen.blit(pg.image.fromstring(ground_w.tobytes(), ground_w.size, 'RGBA'), bg)
        screen.blit(pg.image.fromstring(ground_w.tobytes(), ground_w.size, 'RGBA'), bg1)
        
        #Jump
        if self.jumping:
            if height >= (SCREEN_HEIGHT // 2 -50)-100:
                height -= 3
            if height <= (SCREEN_HEIGHT // 2) -50-100:
                self.jumping = False
        if height < ((SCREEN_HEIGHT // 2)) and not self.jumping:
            height += 3
        player = screen.blit(pg.image.fromstring(player.tobytes(), player.size, 'RGBA'), (5, height-50))
        player_cub = (5, height-50, 5 + player.size[0], height-50-player.size[1])
        
        obstacles.update_items(screen, player_cub)
        items.update_items(screen, player_cub)
        
        if height > ((SCREEN_HEIGHT // 2)):
            self.start=True
        if self.start:
            if not self.lock:
                bg = (bg[0]-speed, bg[1])
                if -(bg[0]) >= (ground_w.size[0] - SCREEN_WIDTH):
                    self.lock = True
            if -(bg[0]) >= (ground_w.size[0] - SCREEN_WIDTH) and self.lock:
                bg1 = (bg1[0]-speed, bg1[1])
                bg = (bg[0]-speed, bg[1])
                if -(bg1[0]) >= (ground_w.size[0] - SCREEN_WIDTH):
                    bg = (SCREEN_WIDTH, SCREEN_HEIGHT//2 - 15)

            if -(bg1[0]) >= (ground_w.size[0] - SCREEN_WIDTH) and self.lock:
                bg = (bg[0]-speed, bg1[1])
                bg1 = (bg1[0]-speed, bg1[1])
                if -(bg[0]) >= (ground_w.size[0] - SCREEN_WIDTH):
                    bg1 = (SCREEN_WIDTH, SCREEN_HEIGHT//2 - 15)

            player_sprite = player_w
            self.start = obstacles.display_obstacle(screen)
            if not items.display_item():
                print("item recolectado")
        else:
            player_sprite = player_b

    def display_death_state(self, screen, obstacles, items):
        global height
        bg = (0, SCREEN_HEIGHT//2 + 5)
        bg1 = (ground_w.size[0], SCREEN_HEIGHT//2 + 5)
        player_sprite = death_ast
        player = player_sprite
        
        #Floor
        screen.blit(pg.image.fromstring(ground_b.tobytes(), ground_b.size, 'RGBA'), bg)
        screen.blit(pg.image.fromstring(ground_b.tobytes(), ground_b.size, 'RGBA'), bg1)
        
        #Jump
        if self.jumping:
            if height >= (SCREEN_HEIGHT // 2 -50)-100:
                height -= 3
            if height <= (SCREEN_HEIGHT // 2) -50-100:
                self.jumping = False
        if height < ((SCREEN_HEIGHT // 2)) and not self.jumping:
            height += 3
        player = screen.blit(pg.image.fromstring(player.tobytes(), player.size, 'RGBA'), (5, height-10))
        player_cub = (5, height-10, 5 + player.size[0], height-10-player.size[1])
        
        obstacles.update_items(screen, player_cub)
        items.update_items(screen, player_cub)
        
        if height > ((SCREEN_HEIGHT // 2)):
            self.start=True
        if self.start:
            if not self.lock:
                bg = (bg[0]-speed, bg[1])
                if -(bg[0]) >= (ground_b.size[0] - SCREEN_WIDTH):
                    self.lock = True
            if -(bg[0]) >= (ground_w.size[0] - SCREEN_WIDTH) and self.lock:
                bg1 = (bg1[0]-speed, bg1[1])
                bg = (bg[0]-speed, bg[1])
                if -(bg1[0]) >= (ground_b.size[0] - SCREEN_WIDTH):
                    bg = (SCREEN_WIDTH, SCREEN_HEIGHT//2 - 15)

            if -(bg1[0]) >= (ground_b.size[0] - SCREEN_WIDTH) and self.lock:
                bg = (bg[0]-speed, bg1[1])
                bg1 = (bg1[0]-speed, bg1[1])
                if -(bg[0]) >= (ground_b.size[0] - SCREEN_WIDTH):
                    bg1 = (SCREEN_WIDTH, SCREEN_HEIGHT//2 - 15)

            player_sprite = player_w
            self.start = obstacles.display_obstacle()
            self.start = items.display_item()
        else:
            player_sprite = player_b

    def quantum_effects(self, gate):
        global status, FPS, direction, SCORE, alive_ast, death_ast
        ygate = False
        self.old_status = status
        if gate == "notgatebit_w" or gate == "notgatebit_b":
            if status == 0: status = 1
            else: status = 0
            
        if gate == "ygatebit_w" or gate == "ygatebit_b":
            if not ygate: 
                FPS = FPS//2
                ygate = not ygate
            else:
                FPS = FPS * 2

        if gate == "zgatebit_w" or gate == "zgatebit_b":
            if direction == 0: 
                direction = 1
                if alive_ast == player_w:
                    alive_ast = player_w_up_r
                    death_ast = player_b_dwn_r
                else:
                    alive_ast = player_b_up_r
                    death_ast = player_w_dwn_r
            else: 
                direction = 0
                if alive_ast == player_w_up_r:
                    alive_ast = player_w
                    death_ast = player_b
                else:
                    alive_ast = player_b_up_l
                    death_ast = player_w_dwn_l

        if gate == "hgatebit_w" or gate == "hgatebit_b":
            if status == 2: status = self.old_status
            else: status = 2

        if gate == "qubit_w_s" or gate == "qubit_w_l":
            SCORE += 1
        
        if gate == "swapgatebit_w" or gate == "swapgatebit_b":
            temp_ast = alive_ast
            alive_ast = death_ast
            death_ast = temp_ast



class Menu():
    def __init__(self, screen):
        self.screen = screen
        # self.start_btn = Button(start_btn,start_btn,(0,0),(205,190),"Start")
        # self.input_box1 = InputBox(100, 100, 140, 32)
        # self.input_boxes = []

        # self.input_boxes.append(self.input_box1)
        pg.display.set_caption('Stranger Ducks')

        # #Launch app
        # self.game_runtime()
        self.main_menu()


    def process_events(self,button_list):
        pos = pg.mouse.get_pos()

        for event in pg.event.get():
            #Quit game
            if event.type == pg.QUIT:
                pg.mixer.music.stop()
                return True
            
            #Click on screen
            #(Button implementation)
            if event.type == pg.MOUSEBUTTONDOWN:
                for button in button_list:
                    if button.isOver(pos):
                        self.menu_open(button)
            
            #Hover effects trigger
            if event.type == pg.MOUSEMOTION:
                for button in button_list:
                    if button.isOver(pos):
                        button.hover_effects()
            
            # #Input boxes
            # for box in self.input_boxes:
            #     box.handle_event(event)


    def main_menu(self):
        done = False

        button_list = []

        strt = pg.image.fromstring(start_btn.tobytes(), start_btn.size, 'RGBA')
        button_list.append(Button(strt,strt,(550,250),(205,190),"Start"))
        # button_list.append(Button(leaderboard, leaderboard_glow, (0,200),(350,80),'Leaderboard'))
        # button_list.append(Button(howtoplay, howtoplay_glow, (0,280),(300,65),'How to Play'))
        # button_list.append(Button(options, options_glow, (0,350),(200,65),'Options'))
        # button_list.append(Button(cred, cred_glow, (440,530),(150,80),'Credits'))

        while not done:
            done = self.process_events(button_list)
            
            #Display elements
            self.screen.fill(WHITE)
            title = pg.image.fromstring(title_img.tobytes(), title_img.size, 'RGBA')
            self.screen.blit(title,(0,50))
            message_to_screen(self.screen,"ENTER SUPERPOSITION",BLACK,(508,350),18)
            message_to_screen(self.screen,"INSTRUCTIONS: Collect enough qubits to reach scalability,",BLACK,(310,430),18)
            message_to_screen(self.screen,"in as little time as possible. Watch out for annihilators and noise!",BLACK,(310,457),18)
            message_to_screen(self.screen,"Different gates have different effects on your state and the game.",BLACK,(310,484),18)
            message_to_screen(self.screen,"Don't loose all your qubits; annihilation of the ground state will end the game.",BLACK,(310,511),18)
            #self.screen.blit(main_menu_bg,(0,0))
            for button in button_list:
                button.draw(self.screen)

            pg.display.flip()
    

    def game_runtime(self):
        global status
        clock = pg.time.Clock()
        done = False
        game = Game()
        obstacles = ObstacleManager()
        items = ItemManager()

        while not done:
            done = game.process_events()
            self.screen.fill(WHITE, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT//2))
            self.screen.fill(BLACK, (0, SCREEN_HEIGHT//2, SCREEN_WIDTH, SCREEN_HEIGHT//2))
            if status == 0:
                game.display_alive_state(self.screen, obstacles, items)
            elif status == 1:
                game.display_death_state(self.screen, obstacles, items)
            elif status == 2:
                game.display_alive_state(self.screen, obstacles, items)
                game.display_death_state(self.screen, obstacles, items)
            pg.display.flip()
            clock.tick(FPS)
            
        if SCORE == 8: self.win()
        elif SCORE <0: self.game_over()

    def howtoplay(self):
        done = False

        button_list = []
        
        button_list.append(self.back_btn)

        while not done:
            done = self.process_events(button_list) #or back_btn_Pressed()

            #Display elements
            self.screen.fill(BLACK)
            #self.screen.blit(credits_bg,(0,0))
            for button in button_list:
                button.draw(self.screen)

            pg.display.flip()

    def options(self):
        done = False

        button_list = []
        
        button_list.append(self.back_btn)

        while not done:
            done = self.process_events(button_list) #or back_btn_Pressed()

            #Display elements
            self.screen.fill(BLACK)
            #self.screen.blit(credits_bg,(0,0))
            for button in button_list:
                button.draw(self.screen)

            pg.display.flip()
    
    def game_over(self):
        done = False
        player_name = ""

        button_list = []
        
        button_list.append(self.back_btn)

        while not done:
            done = self.process_events(button_list)# or back_btn_Pressed()

            #Display elements
            self.screen.fill(WHITE)
            #self.screen.blit(credits_bg,(0,0))
            for button in button_list:
                button.draw(self.screen)
            for box in self.input_boxes:
                    box.update()

            for box in self.input_boxes:
                box.draw(self.screen)
                player_name = box.text

            message_to_screen(self.screen,"GAME OVER",BLACK,(300,50),80)
            #message_to_screen(self.screen,"SCORE: " + str(SCORE),WHITE,(300,500),80)

            pg.display.flip()

        
        return player_name

    def menu_open(self,button):
        callback = button.callback
        if callback == 'Start':
            self.game_runtime()
        elif callback == 'Leaderboard':
            self.leaderboard()
        elif callback == 'How to Play':
            self.howtoplay()
        elif callback == 'Options':
            self.options()
        elif callback == 'Credits':
            self.credits()
        elif callback == 'Back':
            self.main_menu()

"""
///////////////////////////////////////////////////////////
   RUN
///////////////////////////////////////////////////////////
"""

def main():
    pg.init()

    screen = pg.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])

    Menu(screen)

    pg.quit()


if __name__ == "__main__":
	main()
