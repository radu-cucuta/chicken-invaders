import pygame
import random
import os
import time
import pyautogui


#Frame per second
FPS=60

# Define some colors
WHITE = (255, 255, 255)
A_WHITE= (200,200,200)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREY=(18,38,128)
BRIGHT_GREY=(35,44,128)
GREEN_V2 = (25, 255, 50)

#size of window
width=800
height=600


#buttons positioning
rectangle=[150,40]
first_button=[width/2-rectangle[0]/2,height/3]
second_button=[width/2-rectangle[0]/2,height/3+rectangle[1]+20]
third_button=[width/2-rectangle[0]/2,height/3+2*rectangle[1]+40]
th4_button=[width/2-rectangle[0]/2,height/3+2*rectangle[1]+60]
quit_button=[width/2-rectangle[0]/2,height/3+4*rectangle[1]+80]

#position of future window
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (1920/2-width/2,1080/2-height/2)

clock = pygame.time.Clock()

# Call this function so the Pygame library can initialize itself
pygame.init()
 

screen = pygame.display.set_mode([width, height])
 
# This sets the name of the window
pygame.display.set_caption('Chicken Invaders')

 
# Set positions of graphics
background_position = [0, 0]
 
# Load and set up graphics.
background_image = pygame.image.load("assets/background2.png").convert()
player_image = pygame.image.load("assets/spaceship3.png").convert_alpha()
player_image_shrink = pygame.transform.scale(player_image, (50, 50))

player_image_revive = pygame.image.load("assets/revive.png").convert_alpha()
player_image_revive = pygame.transform.scale(player_image_revive, (85, 85))

icon=pygame.image.load("assets/icon.png")
pygame.display.set_icon(icon)


player_laser_green=pygame.image.load("assets/laser2.png").convert_alpha()
player_laser_green=pygame.transform.scale(player_laser_green,(30,30))

player_laser_blue=pygame.image.load("assets/laser_blue2.png").convert_alpha()
player_laser_blue=pygame.transform.scale(player_laser_blue,(40,30))

player_laser_red=pygame.image.load("assets/laser1.png").convert_alpha()
player_laser_red=pygame.transform.scale(player_laser_red,(15,30))

red_enemy_image=pygame.image.load("assets/enemy.png").convert_alpha()
red_enemy_image=pygame.transform.scale(red_enemy_image,(50,50))

egg=pygame.image.load("assets/egg.png").convert_alpha()
egg=pygame.transform.scale(egg,(10,10))

eggSplash=pygame.image.load("assets/eggSplash.png").convert_alpha()
eggSplash=pygame.transform.scale(eggSplash,(50,50))

explosion=pygame.image.load("assets/explosion.png").convert_alpha()
explosion=pygame.transform.scale(explosion,(100,100))

gift_image=pygame.image.load("assets/gift_red.png").convert_alpha()
gift_image=pygame.transform.scale(gift_image,(20,20))

gift_image_green=pygame.image.load("assets/gift_green.png").convert_alpha()
gift_image_green=pygame.transform.scale(gift_image_green,(20,20))

gift_image_blue=pygame.image.load("assets/gift_blue.png").convert_alpha()
gift_image_blue=pygame.transform.scale(gift_image_blue,(20,20))

gift_image_heart=pygame.image.load("assets/heart.png").convert_alpha()
gift_image_heart=pygame.transform.scale(gift_image_heart,(20,20))

gift_image_shield=pygame.image.load("assets/shield.png").convert_alpha()
gift_image_shield=pygame.transform.scale(gift_image_shield,(20,20))

gift_image_bomb=pygame.image.load("assets/bomb.png").convert_alpha()
gift_image_bomb=pygame.transform.scale(gift_image_bomb,(20,20))

bomb_image=pygame.transform.scale(gift_image_bomb,(50,50))

pygame.mixer.init()
def music_main():
   pygame.mixer.music.load("assets/Ci1maintheme.oga")
   pygame.mixer.music.play(-1,0.0)
def music_main_reload():
   pygame.mixer.music.queue("assets/Ci1maintheme.oga")
def music_collide(number):
    pygame.mixer.music.load("assets/Ci1playerhit.oga")
    pygame.mixer.music.play(number,0.0)


music_main()
def blit(x,y,img,time):
    done=time*60
    while done!=0:
        screen.blit(img,(x,y))
        pygame.display.update()
        pygame.display.flip()
        done-=1
class Ship():
    COOLDOWN=30
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.laser_off_screen=0
        self.ship_image=None
        self.laser_image=None
        self.cool_down_counter=0 
        self.lasers=[]

    def move_lasers(self,vel,obj,lost):
        global revive_time
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.y>=height-5 and laser.y<=height:
                laser.eggSplashActive=self.x
            if laser.eggSplashActive:
                screen.blit(eggSplash,[self.x,height-40])
            if laser.off_screen():
                   self.lasers.remove(laser)
            elif laser.collision(obj):
                if revive_time==0:
                    self.lasers.remove(laser)
                if lost==0 and revive_time==0:
                    obj.lives-=1
                    revive_time=obj.revive()


    def draw(self):
        screen.blit(self.ship_image,[self.x,self.y])
        for laser in self.lasers:
            laser.draw()

    def cooldown(self):
        if self.cool_down_counter>=self.COOLDOWN:
            self.cool_down_counter=0
        elif self.cool_down_counter>0:
            self.cool_down_counter+=1
     

    def shoot(self):
        if self.cool_down_counter==0:
            laser=Laser(self.x,self.y,self.laser_image)
            self.lasers.append(laser)
            self.cool_down_counter=1

    def get_width(self):
        return self.ship_image.get_width()

    def get_height(self):
        return self.ship_image.get_height()

class Enemy(Ship):
    COLOR_MAP={
           "red":(red_enemy_image)
        }
    def __init__(self,x,y,color):
        super().__init__(x,y)
        self.ship_image=self.COLOR_MAP[color]
        self.laser_image=egg
        self.mask=pygame.mask.from_surface(self.ship_image)
    
    def move(self,enemy_vel):
        self.y+=enemy_vel

    def shoot(self):
        if self.cool_down_counter==0:
            laser=Laser(self.x+20,self.y+30,self.laser_image)
            self.lasers.append(laser)
            self.cool_down_counter=1
            

def collide(obj1,obj2):
    offsetX=obj2.x-obj1.x
    offsetY=obj2.y-obj1.y
    return obj1.mask.overlap(obj2.mask,(offsetX,offsetY)) != None
    
class Laser():
    def __init__(self,x,y,img):
        self.x=x
        self.y=y
        self.eggSplash=eggSplash
        self.eggSplashActive=0
        self.img=img
        self.laser_color=None 
        self.mask=pygame.mask.from_surface(self.img)

    def draw(self):
        screen.blit(self.img,(self.x,self.y))
        
    def move(self,vel):
        self.y-=vel

    def off_screen(self):
        return not(self.y<=height+300 and self.y>=0)
    def off_screen_down(self):
        return (self.y>=height)

    def collision(self,obj):
        return collide(self,obj)




class Player(Ship):
    LASER_MAP={
           "red":(player_laser_red),
           "green":(player_laser_green),
           "blue":(player_laser_blue)
        }
    GIFT_MAP={
            "red":(gift_image),
            "green":(gift_image_green),
            "blue":(gift_image_blue),
            "heart":(gift_image_heart),
            "shield":(gift_image_shield),
            "bomb":(gift_image_bomb)
        }
    
    def __init__(self,x,y,lives,laser_type,multi_shoot):
        super().__init__(x,y)
        # Get the current mouse position. This returns the position
        # as a list of two numbers.
        self.lives=lives
        self.ship_image=player_image_shrink
        self.multi_shoot=multi_shoot
        self.laser_type=laser_type
        self.laser_image=self.LASER_MAP[laser_type]
        self.mask=pygame.mask.from_surface(self.ship_image)
        self.colors=["red","green","blue","heart","shield","bomb"]
        self.image_laser_position=[18,10,5]
        self.highscore=0
        self.bomb=0

    def mouse_init(self):
        player_position = pygame.mouse.get_pos()
        self.x = player_position[0]
        self.y = player_position[1]
        if self.x>width-self.get_width():
           self.x=width-self.get_width()
        if self.y>height-self.get_height():
           self.y=height-self.get_height()

        # set mouse invisible
        pygame.mouse.set_visible(0)

    def move_laser(self,vel,objs,gifts,lost):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen():
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        if lost==0:
                            self.highscore+=10
                        if random.randrange(0,5)==1:

                            rand=random.randrange(0,6)
                            a=self.colors[rand]
                            gift=Laser(obj.x,obj.y+10,self.GIFT_MAP[a]) 
                            gift.laser_color=a
                            gifts.append(gift)
                        objs.remove(obj)
                        #obj.shoot()??
                        self.lasers.remove(laser)

    def shoot(self):
        if self.cool_down_counter==0:
            a=0
            if self.laser_type=="green":
                a=1
            elif self.laser_type=="red":
                a=0
            else:
                a=2
            for i in range(self.multi_shoot):
                    laser=Laser(self.x+self.image_laser_position[a]+i*10-int((self.multi_shoot/2))*10,self.y-20,self.laser_image)
                    self.lasers.append(laser)
            self.cool_down_counter=1

    def revive(self):
        x=self.x;y=self.y
        self.laser_type="green"
        self.laser_image=self.LASER_MAP[laser_type]
        self.multi_shoot=1
        pyautogui.moveRel(width/2-25-x,height-y)
        return 4*FPS
           
def pause():
    run=1

    main_font=pygame.font.SysFont("comicsans",50)
    pause_label=main_font.render("Press 'space' to continue ...",1,WHITE)
    pygame.mouse.set_visible(1)
    mouse_click=pygame.mouse.get_pressed()
    while run:
        screen.blit(pause_label,(width/2-pause_label.get_width()/2,250))
        pygame.display.update()

        do1=lambda x1:exit(0)
        label_button(quit_button[0],quit_button[1],150,40,do1,mouse_click,"Quit Game")

        do2=lambda x1:main_menu()
        label_button(th4_button[0],th4_button[1],150,40,do2,mouse_click,"Main Menu")

        for event in pygame.event.get():
           if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_click=pygame.mouse.get_pressed()
           if event.type == pygame.QUIT:
              run = False
           elif event.type == pygame.KEYDOWN:
              if event.key == pygame.K_SPACE:
                      run=0
        clock.tick(60)


bomb=0
def events(player_ship):
    global bomb,level
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                  pause()
            if event.key == pygame.K_b and player_ship.bomb>0:
                player_ship.bomb-=1
                bomb=6*FPS
            if event.key == pygame.K_w:
                level+=1
 
def transparent_surface(image,color4):
    alpha_img = pygame.Surface(image.get_size(), pygame.SRCALPHA)
    alpha_img.fill(color4)
    image.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    
def label_button(buttonX,buttonY,button_width,button_height,function,mouse_click,text,text_size=30):
    button=[buttonX,buttonY]
    rectangle=[button_width,button_height]

    main_font=pygame.font.SysFont("Arial",text_size)
    label=main_font.render(text,1,A_WHITE);

    mouse=pygame.mouse.get_pos()

    if button[0]+rectangle[0] > mouse[0] > button[0] and  button[1]+rectangle[1]> mouse[1] >button[1]:
            pygame.draw.rect(screen, BRIGHT_GREY,(button[0],button[1],rectangle[0],rectangle[1]))
            screen.blit(label,[button[0]+rectangle[0]/2-label.get_width()/2,button[1]])
            if mouse_click[0]:
                function(0)
    else:
       pygame.draw.rect(screen, GREY,(button[0],button[1],rectangle[0],rectangle[1]))
       screen.blit(label,[button[0]+rectangle[0]/2-label.get_width()/2,button[1]+5])


laser_type="green"
laser_number=1
revive_time=0
highscore=0         
level=0

def main_game(mode):
   
   score=0
   lives=5
   enemies=[]
   gifts=[]
   wave_length=5+mode
   enemy_vel=1+mode
   laser_vel=2+mode
   laser_vel_ship=4
   main_font=pygame.font.SysFont("comicsans",50)
   global l
   l=0

   lost=0
   lost_count=0 
   done = False
   
   global laser_type,laser_number

   player_ship=Player(0,0,lives,laser_type,laser_number)
   shield=Laser(0,0,player_image_revive)

   while not done:
    global level
    clock.tick(FPS)

    if wave_length%10==0 and lives<5:
        lives+=1
        laser_vel+=1
        enemy_vel+=1
    #define enemies 
    if len(enemies)==0 and bomb==0:
        level+=1
        wave_length+=1
        for i in range(wave_length):
            enemy=Enemy(random.randint(50,width-100),random.randint(-1500,- 300),"red")
            enemies.append(enemy)

    events(player_ship)

    if player_ship.lives==0:
        lost=1

    def redraw_window(player_ship):
         # blit image to screen:
        global laser_type,laser_number,revive_time,bomb
        
        screen.blit(background_image, background_position)

        if revive_time>0:
            revive_time-=1
            shield.x=player_ship.x-17
            shield.y=player_ship.y-16
            shield.draw()

        if bomb>0:
            bomb-=1
            screen.blit(explosion,[width/2-50,height/2-50])
            enemies.clear()

        for enemy in enemies:
            enemy.draw()


        level_label=main_font.render(f"LEVEL: {level}",1,WHITE)
        lives_label=main_font.render(f"LIVES: {player_ship.lives}",1,WHITE)
        score_label=main_font.render(f"Score: {player_ship.highscore}",1,WHITE)
        bomb_label=main_font.render(f"{player_ship.bomb} X",1,WHITE)

        if lost:

           global highscore
           if highscore<player_ship.highscore:
               highscore=player_ship.highscore

           lost_label=main_font.render("GAME OVER !!!",1,WHITE)
           transparent_surface(lost_label,(0,0,0,200))
           screen.blit(lost_label,(width/2-lost_label.get_width()/2,250))
           mouse_click=pygame.mouse.get_pressed()
           
           do1=lambda ex1:exit(0)
           label_button(quit_button[0],quit_button[1],150,40,do1,mouse_click,"Quit Game")
           do2=lambda ex1:main_menu()
           label_button(th4_button[0],th4_button[1],150,40,do2,mouse_click,"Main Menu")
           global l
           if l==FPS*20:
               main_menu()
           else:
               l+=1
        screen.blit(level_label,[10,10])
        screen.blit(lives_label,[width-level_label.get_width()-10,10])
        screen.blit(score_label,[width/2-score_label.get_width()/2,10])
        screen.blit(bomb_label,[10,height-60])
        screen.blit(bomb_image,[15+bomb_label.get_width(),height-50])

        

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(-laser_vel,player_ship,lost)

            if random.randrange(0,4*FPS)== 1:
                enemy.shoot()

            if enemy.y+enemy.get_height()>height:
                enemies.remove(enemy)
                if lost==0 and revive_time==0:
                     player_ship.lives-=1


            if collide(enemy,player_ship) and lost==0 and revive_time==0:
                enemies.remove(enemy)
                player_ship.lives-=1
                revive_time=player_ship.revive()

        player_ship.mouse_init()
        mouse_click=pygame.mouse.get_pressed()
        if mouse_click[0]==1:
            player_ship.shoot()
        player_ship.move_laser(laser_vel_ship,enemies,gifts,lost)
        player_ship.draw()

        for gift in gifts:
            gift.draw()
            gift.move(-laser_vel)
            if gift.collision(player_ship):
                if gift.laser_color=="heart" and lost==0:
                    player_ship.lives+=1
                elif gift.laser_color=="bomb":
                    if player_ship.bomb<3:
                        player_ship.bomb+=1
                elif gift.laser_color=="shield":
                    revive_time=6*FPS
                elif player_ship.laser_type==gift.laser_color:
                    player_ship.multi_shoot+=1
                else:
                    player_ship.laser_type=gift.laser_color
                    player_ship.laser_image=player_ship.LASER_MAP[gift.laser_color]
                    player_ship.multi_shoot=1

                gifts.remove(gift)

    
    redraw_window(player_ship)
    pygame.display.flip()




def first_apperance():
    img_width=100
    img_height=100
    playerX1=width/2-img_width/2
    playerY1=-img_height
    playerY1_change=2
    d=height-img_height
    img_height_final=50
    pas=d/img_height_final
   
    
    main_font=pygame.font.SysFont("assets/futureforcescondital.ttf",60)
    wave_font=main_font.render("FIRST ATTACK",1,A_WHITE);
    

    while playerY1<=height-3*img_height:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                   playerY=0

        pygame.mouse.set_visible(0)
        screen.blit(background_image,[0,0])
        player = pygame.image.load("assets/spaceship3.png").convert_alpha()
        player=pygame.transform.scale(player,[img_width,img_height])
        screen.blit(wave_font,(width/2-150,height/2-100))
        screen.blit(player,[playerX1,playerY1])
        playerY1+=playerY1_change

        if abs(playerY1)%pas==0:
            img_width-=1
            img_height-=1
            
        pygame.display.update()
        clock.tick(60)

CI2logo=pygame.image.load("assets/logo.jpg").convert_alpha()
CI2logo=pygame.transform.scale(CI2logo,[width,height+1])

def cntdwn():
    i=0
    while i<100*FPS:
        i+=1

def mode_game():
    in_menu=1

    do1=lambda ex1:(first_apperance(),main_game(0))
    do2=lambda ex1:(first_apperance(),main_game(1))
    do3=lambda ex1:(first_apperance(),main_game(2))
    do4=lambda ex1:main_menu()
    while in_menu:
        clock.tick(60)
        screen.blit(background_image,[0,0])
        mouse_click=[0,0]
        for event in pygame.event.get():
          if event.type == pygame.MOUSEBUTTONDOWN:
               mouse_click=pygame.mouse.get_pressed()
          if event.type == pygame.QUIT:
             quit(0)
        #Label_Buttons
        label_button(first_button[0],first_button[1],150,40,do1,mouse_click,"EASY")
        label_button(second_button[0],second_button[1],150,40,do2,mouse_click,"NORMAL")
        label_button(third_button[0],third_button[1],150,40,do3,mouse_click,"HARD")
        label_button(quit_button[0],quit_button[1],150,40,do4,mouse_click,"Main menu")

        pygame.display.update()
        pygame.display.flip()


def Highscore():
    clock.tick(FPS)
    in_menu=1

    do1=lambda ex1:main_menu()
    do2=lambda ex1:exit(0)

    main_font=pygame.font.SysFont("comicsans",50)

    global highscore
    score_label=main_font.render(f"Your highscore is: {highscore}",1,GREEN)

    while in_menu:
        screen.blit(background_image,[0,0])
        mouse_click=[0,0]
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_click=pygame.mouse.get_pressed()
            if event.type == pygame.QUIT:
                quit(0)

        screen.blit(score_label,(width/2-score_label.get_width()/2,200))
        label_button(third_button[0],third_button[1]+50,150,40,do1,mouse_click,"Main Menu")
        label_button(quit_button[0],quit_button[1],150,40,do2,mouse_click,"Quit Game")

        pygame.display.update()
        pygame.display.flip()

def main_menu():
    in_menu=1


    do4=lambda ex1:exit(0)
    do3=lambda ex1:1
    do2=lambda ex1:Highscore()
    do1=lambda ex1:mode_game()
    pygame.mouse.set_visible(1)


    while in_menu:
        clock.tick(FPS)
        screen.blit(CI2logo,[0,0])
        mouse_click=[0,0]
        for event in pygame.event.get():
           if event.type == pygame.MOUSEBUTTONDOWN:
               mouse_click=pygame.mouse.get_pressed()
           if event.type == pygame.QUIT:
                quit(0)
        
        #Label_Buttons
        label_button(first_button[0],first_button[1]+50 ,150,40,do1,mouse_click,"Play")
        label_button(second_button[0],second_button[1]+50,150,40,do2,mouse_click,"Highscore");
        label_button(third_button[0],third_button[1]+50,150,40,do3,mouse_click,"Options")
        label_button(quit_button[0],quit_button[1]+50,150,40,do4,mouse_click,"Quit Game")

        
        pygame.display.update()
        pygame.display.flip()

    pygame.quit()


main_menu()