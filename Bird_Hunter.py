from cmath import sqrt
from errno import ENOTEMPTY
import pygame
import random
import math
from pygame import mixer

pygame.init()
icon = pygame.image.load('images\\shooting.png')
pygame.display.set_icon(icon)

width = 800
height = 400
screen = pygame.display.set_mode((width,height))

gplaymus = mixer.Sound("sound\\gameplay.mp3")
gplaymus.play(-1)
# govermus = mixer.Sound("sound\\gameover.mp3")
# titlemus = mixer.Sound("sound\\title.mp3")
# death = mixer.Sound("death.mp3")

#player
playerimg = pygame.image.load("images\\shooting.png")
playerX = 100
playerY = 270
U_playerY = 0.6
U_playerX = 0

def display_player(playerX,playerY):
    screen.blit(playerimg,(playerX,playerY))

# enemy
enemyimg = pygame.image.load("images\\bird.png")
enemyX = 0
enemyY = 0
U_enemyX = 1

enemy_state = False
def enemy(x,y):
    global enemy_state
    enemy_state = True
    screen.blit(enemyimg,(x,y))

# bullet
bulletimg = pygame.image.load("images\\bullet.png")
bulletX = 0
bulletY = 0
U_bulletX = 2

bullet_state = False
def bullet(x,y):
    global bullet_state
    bullet_state = True
    screen.blit(bulletimg,(x,y))

# background
backimg = pygame.image.load("images\\background.jpg")

# start
startimg = pygame.image.load("images\\start.png")

# gameover
goverimg = pygame.image.load("images\\gameover.png")

score = 0
# font =pygame.font.Font('freesansbold.ttf',32)

def display_score(x,y,r,b,g,sz):
    font = pygame.font.Font('font\\Stop Bullying.otf',sz)
    score_1 = font.render("Score : "+str(score),True,(r,b,g))
    screen.blit(score_1,(x,y))


def iscollide(eX,eY,bX,bY):
    dist = math.sqrt(math.pow(eX-bX,2) + math.pow(eY-bY,2))
    if dist < 27:
        return True
    return False

def isgameover(eX,eY,pX,pY):
    dist = math.sqrt(math.pow(eX-pX,2) + math.pow(eY-pY,2))
    if dist < 27:
        return True
    return False

if __name__=="__main__":
    running = False
    close = False

    jump = False
    relay = False
    enemy_state = False
    gameover = False

    while running == False and close == False and gameover == False:
        screen.fill((0,0,0))
        screen.blit(startimg,(0,0))
        # titlemus.set_volume(1)
        # titlemus.play()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    running = True
        
        pygame.display.update()
        
    while running == True and close == False:
        if gameover == False:
            screen.fill((0,0,0))
            screen.blit(backimg,(0,0))
            # titlemus.stop()
            # gplaymus.set_volume(40)
            # gplaymus.play(-1)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    close = True
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if jump == False and relay == False:
                            jumpmus = mixer.Sound("sound\\jump.wav")
                            jumpmus.play()
                            jump = True
                        
                    if event.key == pygame.K_RIGHT:
                        U_playerX = 0.2

                    if event.key == pygame.K_LEFT:
                        U_playerX = -0.2

                    if event.key == pygame.K_SPACE:
                        if bullet_state == False:
                            bulletmus = mixer.Sound("sound\\gun.mp3")
                            bulletmus.play()
                            bulletX = playerX + 32
                            bulletY = playerY - 5
                            bullet(bulletX,bulletY)
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        U_playerX = 0

                    if event.key == pygame.K_LEFT:
                        U_playerX = 0
                
            if bullet_state == True:
                bullet(bulletX,bulletY)
                bulletX += U_bulletX            
            if bulletX > 800:
                bullet_state = False
                
            if jump == True and relay == False:
                if playerY > 150:
                    playerY -= U_playerY
                elif playerY <= 150:
                    relay = True
                
            playerX += U_playerX
            if playerX > 600:
                playerX = 600
            if playerX < 10:
                playerX = 10 

            if jump == True and relay == True:
                if playerY < 270:
                    playerY += U_playerY
                elif playerY >= 270:
                    relay = False
                    jump = False

            if gameover == False:
                if enemy_state == False:
                    enemyX = 800
                    enemyY = random.randint(145,265)
                    enemy(enemyX,enemyY)
                elif enemy_state == True:
                    enemy(enemyX,enemyY)
                    enemyX -= U_enemyX
                if enemyX < 0:
                    enemy_state = False

            collision = iscollide(enemyX,enemyY,bulletX,bulletY)
            if collision == True:
                enemyhit = mixer.Sound("sound\\enemy-hit.mp3")
                enemyhit.play()
                enemy_state = False
                score +=1

            gameover = isgameover(enemyX,enemyY,playerX,playerY)

            display_score(10,10,255,0,0,12)

            display_player(playerX,playerY)
            pygame.display.update()

        if gameover == True:
            screen.fill((0,0,0))
            screen.blit(goverimg,(0,0))

            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        close = True
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            gameover = False
                            score = 0
                            enemy_state = False
            
            display_score(320,150,0,0,0,24)
            pygame.display.update()