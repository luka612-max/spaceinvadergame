import pygame
import math
import random
from pygame import mixer

#initialize the pygame
pygame.init()
#create the screen
screen=pygame.display.set_mode((800,600))
#title and icon
pygame.display.set_caption('space invaders')
icon=pygame.image.load('startup.png')
pygame.display.set_icon(icon)
#background
background=pygame.image.load('background.png')
#background music
mixer.music.load('background.wav')
mixer.music.play(-1)
#player
playerimg=pygame.image.load('player1.png')
playerx=370
playery=480
playerx_change=0
#bullet
bulletimg=pygame.image.load('bullet.png')
bulletx=playerx
bullety=playery
bullety_change=-1
bullet_state="ready"
#ready-you can,t see the bullet
#fire-you can see the bullet

#enemy
enemyimg=[]
enemyx=[]
enemyy=[]
enemyx_change=[]
no_of_enemies=6
for i in range(no_of_enemies):
    enemyimg.append(pygame.image.load('enemy.png'))
    enemyx.append(random.randint(0,736))
    enemyy.append(random.randint(50,150))
    enemyx_change.append(2)

def player():
    screen.blit(playerimg,(playerx,playery))
def enemy(i):
    screen.blit(enemyimg[i],(enemyx[i],enemyy[i]))
def fire_bullet(x,y):
    global bullet_state
    bullet_state="fire"
    screen.blit(bulletimg,(x+16,y+10))
def iscollision(bulletX,bulletY,enemyX,enemyY):
    distance=math.sqrt(math.pow(enemyX-bulletX,2)+math.pow(bulletY-enemyY,2))
    if distance<27:
        return True
    else:
        return False
    
#game loop
running =True
score_value=0
font=pygame.font.Font('freesansbold.ttf',32)
textx=10
texty=10
#game over text
over_font=pygame.font.Font('freesansbold.ttf',64)
def game_over_text():
    over_text=over_font.render("GAME OVER",True,(255,255,255))
    screen.blit(over_text,(200,250))
def show_score(x,y):
    score=font.render("score:"+str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))
while running:
     # RGB-(red,green,blue)
    screen.fill((0,2,0))
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        #if keystroke is pressed left or right 
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                  playerx_change-=0.8
            if event.key==pygame.K_RIGHT:
                 playerx_change+=0.8
            if event.key==pygame.K_SPACE: 
                if bullet_state is "ready":
                   bullet_sound=mixer.Sound('laser.wav')
                   bullet_sound.play()
                   bulletx=playerx
                   fire_bullet(playerx,bullety)
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_LEFT:
               playerx_change+=0.8
            if event.key==pygame.K_RIGHT:
                playerx_change-=0.8
    for i in range(no_of_enemies):
        #game over
        if enemyy[i]>440:
            for j in range(no_of_enemies):
                enemyy[j]=2000
            game_over_text()
            break
        #enemy does not go out of boundary
        if enemyx[i]<=0:
            enemyx[i]=0
            enemyy[i]+=40
            enemyx_change[i]=2
        elif enemyx[i]>=736:
                enemyx[i]=736
            #direction of enemy changes as it touches boundary
        if enemyx[i]==736:
            enemyy[i]+=40
            enemyx_change[i]=-2
        collision=iscollision(bulletx,bullety,enemyx[i],enemyy[i])
        if collision:
            explosion_sound=mixer.Sound('explosion.wav')
            explosion_sound.play()
            bullety=490
            bullet_state="ready"
            score_value+=1
            enemyx[i]=random.randint(0,800)
            enemyy[i]=random.randint(50,150)
            #bullet movement
        if bullet_state is "fire":
            fire_bullet(bulletx,bullety)
            bullety+=bullety_change
        #reloading the bullet
        if bullety<=0:
            bullet_state="ready"
            bullety=490          
        playerx+=playerx_change
        enemyx[i]+=enemyx_change[i]
        enemy(i)
    #player doesn't go out of boundary
    if playerx<=0:
     playerx=0
    elif playerx>=736:
        playerx=736
     
    
    player()
    show_score(textx,texty)
    pygame.display.update()
