import pygame
from pygame.locals import *
import random
import math
from time import sleep



WHITE = (255, 255, 255)
RED = (255, 0 , 0)
pad_width = 360
pad_height = 640
background_height = 640
aircraft_width = 57
aircraft_height = 63
enemy_width = 57
enemy_height = 63
enemy_bullet_width = 10
enemy_bullet_height = 20
planet_width = 949
planet_height = 92

def drawScore(count):
    global gamepad

    font = pygame.font.SysFont(None, 25)
    text = font.render('LIFE: ' + count*"♥",True,WHITE)
    gamepad.blit(text,(0,0))

def drawScore2(count):
    global gamepad

    font = pygame.font.SysFont(None, 25)
    text = font.render('Score: ' + str(count),True,WHITE)
    gamepad.blit(text,(240, 0))

def gameOver(count):
    global gamepad, explosion_sound, retry
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(explosion_sound)
    drawObject(retry, 82.5, 560)
    font = pygame.font.SysFont(None, 25)
    text = font.render('Your Score',True,WHITE)
    gamepad.blit(text,((pad_width/2), (pad_height/2)+ 50))
    font = pygame.font.SysFont(None, 40)
    text = font.render(str(count),True,WHITE)
    gamepad.blit(text,((pad_width/2), (pad_height/2)+ 75))
    dispMessage('Game Over!')
    crashed = False
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True

            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos() 
                x = pos[0]
                y = pos[1]
                if(x> 82.5 and x< 277.5):
                    if(y> 560 and y< 630):
                        runGame()
    pygame.quit()
    quit()
    
    

def pause():
    global gamepad
    largeText = pygame.font.Font('freesansbold.ttf', 55)
    TextSurf, TextRect = textObj('Pause', largeText)
    TextRect.center = ((pad_width/2),(pad_height/2))
    gamepad.blit(TextSurf, TextRect)
    largeText = pygame.font.Font('freesansbold.ttf', 35)
    TextSurf, TextRect = textObj('for 5 seconds', largeText)
    TextRect.center = ((pad_width/2),(pad_height/2)+ 55)
    gamepad.blit(TextSurf, TextRect)
    pygame.display.update()
    sleep(5)
    
        


def textObj(text, font):
    textSurface = font.render(text, True, RED)
    return textSurface, textSurface.get_rect()

def dispMessage(text):
    global gamepad

    largeText = pygame.font.Font('freesansbold.ttf', 55)
    TextSurf, TextRect = textObj(text, largeText)
    TextRect.center = ((pad_width/2),(pad_height/2))
    gamepad.blit(TextSurf, TextRect)
    pygame.display.update()


def twopoint(x1, y1, x2, y2):
    answer = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    return answer
def drawObject(obj, x, y):
    global gamepad
    gamepad.blit(obj, (x, y))

def runGame():
    global gamepad, aircraft, clock, background1, background2
    global enemy, planets, bullet, boom, e_bullet, heals
    global shot_sound

    #배경음
    pygame.mixer.music.load('plane_bgm.mp3')
    pygame.mixer.music.play(-1)
    score = 0
    isShotenemy = False
    boom_count = 0
    crash = 0
    
    bullet_xy = []
                 
    x = pad_width * 0.5 - 28.5
    y = pad_height * 0.9 - 31.5
    x_change = 0
    y_change = 0

    background1_y = 0
    background2_y = -background_height

    enemy_x = random.randrange(0, pad_width)
    enemy_y = 0

    planet_x = random.randrange(0, pad_width)
    planet_y = 0
    random.shuffle(planets)
    planet = planets[0]

    enemy_bullet_x = enemy_x - 26
    enemy_bullet_y = enemy_y + 60
    random.shuffle(e_bullet)
    enemy_bullet = e_bullet[0]

    heal_x = random.randrange(0, pad_width)
    heal_y = 0
    random.shuffle(heals)
    heal = heals[0]
    
    crashed = False
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                elif event.key == pygame.K_RIGHT:
                    x_change = 5
                elif event.key == pygame.K_UP:
                    y_change = -5
                elif event.key == pygame.K_DOWN:
                    y_change = 5
                elif event.key == pygame.K_SPACE:
                    pygame.mixer.Sound.play(shot_sound)
                    bullet_x = x + aircraft_width - 31
                    bullet_y = y - aircraft_height + 60
                    bullet_xy.append([bullet_x, bullet_y])
                elif event.key == pygame.K_LCTRL:
                    pygame.mixer.music.pause()
                    pause()
                    pygame.mixer.music.unpause()
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_change = 0

        
        #빈화면
        gamepad.fill(WHITE)
        
        #배경화면
        background1_y += 0.5
        background2_y += 0.5
        if background1_y == background_height:
            background1_y = -background_height

        if background2_y == background_height:
            background2_y = -background_height

        drawObject(background1, 0, background1_y)
        drawObject(background2, 0, background2_y)
        
        #플레이어 위치
        x += x_change
        y += y_change
        if x < 0:
            x = 0
        elif x > pad_width- aircraft_width:
            x = pad_width- aircraft_width
        if y < 0:
            y = 0
        elif y > pad_height- aircraft_height:
            y = pad_height- aircraft_height
        #점수 및 통과한 적
        drawScore(5 -crash)
        drawScore2(score)
        

        #적 위치
        enemy_y +=  2
        if enemy_y >= 640:
            enemy_y = 0
            enemy_x = random.randrange(0, pad_width- enemy_width)
                 
        #행성 위치
        if planet == None:
            planet_y += 5
        else:
            planet_y += 1
        if planet_y >= 640:
            planet_y = 0
            planet_x = random.randrange(0, pad_width)
            random.shuffle(planets)
            planet = planets[0]
            
        #적 총알 위치
        if enemy_bullet == None:
                 enemy_bullet_y += 8
        else:
                 enemy_bullet_y += 12
        if enemy_bullet_y >= 640:
            enemy_bullet_x = enemy_x + 23
            enemy_bullet_y = enemy_y + 70
            random.shuffle(e_bullet)
            enemy_bullet = e_bullet[0]
        #힐팩 위치
        if heal == None:
            heal_y += 10 
        else:
            heal_y += 2
        if heal_y >= 640:
            heal_y = 0
            heal_x = random.randrange(0, pad_width)
            random.shuffle(heals)
            heal = heals[0]
        #총알 위치
        if len(bullet_xy) != 640:
            for i,bxy in enumerate(bullet_xy):
                bxy[1] -= 15
                bullet_xy[i][1] = bxy[1]

                if bxy[1] < enemy_y:
                    if bxy[0] > enemy_x and bxy[0] < enemy_x + enemy_height :
                        bullet_xy.remove(bxy)
                        score += 10
                        isShotenemy = True
                        
                if bxy[1] <= 0:
                    try:
                        bullet_xy.remove(bxy)
                    except:
                        pass
        #적과 플레이어의 상호작용       
        if twopoint(x+ 28.5, y + 45, enemy_x + 28.5, enemy_y + 18)< 40:
                isShotenemy = True
                crash += 1
                enemy_y = 0
                enemy_x = random.randrange(0, pad_width- enemy_width)
                if crash > 4:
                    gameOver(score)
        #적 총알과 플레이어의 상호작용 
        if enemy_bullet != None:
            if twopoint(x+ 28.5, y + 45, enemy_bullet_x + 5, enemy_bullet_y+ 20)< 20:
                    crash += 1
                    enemy_bullet_x = enemy_x + 23
                    enemy_bullet_y = enemy_y + 70
                    random.shuffle(e_bullet)
                    enemy_bullet = e_bullet[0]
                    if crash > 4:
                        gameOver(score)
        #행성과 플레이어의 상호작용
        if planet != None:
            p_x = planet_x + 45
            p_y = planet_y + 45
            if twopoint(x + 28.5, y + 31.5, p_x, p_y)< 42:
                    crash += 2
                    drawObject(boom, planet_x, planet_y)
                    boom_count += 1
                    if boom_count > 5:
                        boom_count = 0
                    planet_x = random.randrange(0, pad_width - enemy_width)
                    planet_y = 0
                    random.shuffle(planets)
                    planet = planets[0]
                    if crash > 4:
                        gameOver(score)
        #힐팩과 플레이어의 상호작용
        if heal != None:
            if twopoint(x + 28.5, y + 31.5, heal_x +9, heal_y + 13)< 25:
                    crash -= 2
                    heal_y = 0
                    heal_x = random.randrange(0, pad_width)
                    random.shuffle(heals)
                    heal = heals[0]
                    if crash < 0 :
                        crash = 0
                 

        drawObject(enemy, enemy_x, enemy_y)
        
            
        if planet != None:
            drawObject(planet, planet_x, planet_y)
        if enemy_bullet != None:
            drawObject(enemy_bullet, enemy_bullet_x, enemy_bullet_y)
        if heal != None:
            drawObject(heal, heal_x, heal_y)

        if len(bullet_xy) != 640:
            for bx, by in bullet_xy:
                drawObject(bullet, bx, by)

        if not isShotenemy:
            drawObject(enemy, enemy_x, enemy_y)
        else:
            
            drawObject(boom, enemy_x, enemy_y)
            boom_count += 1
            if boom_count > 5:
                boom_count = 0
                enemy_x = random.randrange(0, pad_width - enemy_width)
                enemy_y = 0
                isShotenemy = False
                
        drawObject(aircraft, x, y)
        
        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    quit()
def ruleGame():
    global gamepad, aircraft, clock, background1, background2
    global enemy, planets, bullet, boom, e_bullet, heals
    global shot_sound, explosion_sound
    global gs, gr, ge, rule

    enemy_x = 61.5
    enemy_y = 100

    planet_x = 223
    planet_y = 100
    planet = planets[0]

    heal = heals[0]
    
    crashed = False
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True

            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos() 
                x = pos[0]
                y = pos[1]
                if(x> 82.5 and x< 277.5):
                    if(y> 560 and y< 630):
                        runGame()
                
        gamepad.fill(WHITE)
        background1_y = 0
        background2_y = -background_height
        background1_y += 0.5
        background2_y += 0.5
        if background1_y == background_height:
            background1_y = -background_height
            

        if background2_y == background_height:
            background2_y = -background_height

        drawObject(background1, 0, background1_y)
        drawObject(background2, 0, background2_y)

        x = pad_width * 0.5 - 28.5
        y = pad_height * 0.5 - 31.5
        drawObject(aircraft, x, y)

        drawObject(gs, 82.5, 560)
        drawObject(rule, 0, 210)
        drawObject(enemy, enemy_x, enemy_y)
        drawObject(planet, planet_x, planet_y)
        drawObject(heal, 171, 100)

        
        largeText = pygame.font.Font('freesansbold.ttf', 40)
        TextSurf, TextRect = textObj('Rule', largeText)
        TextRect.center = ((pad_width/2),40)
        gamepad.blit(TextSurf, TextRect)
        pygame.display.update()
        clock.tick(60)
    
def Menu():
    global gamepad, aircraft, clock, background1, background2
    global enemy, planets, bullet, boom, e_bullet
    global shot_sound, explosion_sound
    global gs, gr, ge
    
    crashed = False
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True

            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos() 
                x = pos[0]
                y = pos[1]
                if(x> 82.5 and x< 277.5):
                    if(y> 380 and y< 450):
                        runGame()
                    elif(y> 470 and y< 540):
                        ruleGame()
                    elif(y> 560 and y< 630):
                        crashed = True
                
        gamepad.fill(WHITE)
        background1_y = 0
        background2_y = -background_height
        background1_y += 0.5
        background2_y += 0.5
        if background1_y == background_height:
            background1_y = -background_height

        if background2_y == background_height:
            background2_y = -background_height

        drawObject(background1, 0, background1_y)
        drawObject(background2, 0, background2_y)

        x = pad_width * 0.5 - 28.5
        y = pad_height * 0.5 - 31.5
        drawObject(aircraft, x, y)

        drawObject(gs, 82.5, 380)
        drawObject(gr, 82.5, 470)
        drawObject(ge, 82.5, 560)
        

        largeText = pygame.font.Font('freesansbold.ttf', 55)
        TextSurf, TextRect = textObj('Spaceship', largeText)
        TextRect.center = ((pad_width/2),(pad_height/2)- 150)
        gamepad.blit(TextSurf, TextRect)
        pygame.display.update()
        clock.tick(60)
    pygame.quit()
    quit()
    
def initGame():
    global gamepad, aircraft, clock, background1, background2
    global enemy, planets, bullet, boom, e_bullet, heals
    global shot_sound, explosion_sound
    global gs, gr, ge, rule, retry

    planets = []
    e_bullet = []
    heals = []
    
    pygame.init()

    gamepad = pygame.display.set_mode((pad_width, pad_height))
    pygame.display.set_caption('Spaceship Game')
    gs = pygame.image.load("gamestart.png")
    gr = pygame.image.load("gamerule.png")
    ge = pygame.image.load("exit.png")
    rule = pygame.image.load("rule_1.png")
    retry = pygame.image.load("retry.png")
    aircraft = pygame.image.load("plane_num106.png")
    background1 = pygame.image.load("plane_bg.png")
    background2 = background1.copy()
    heals.append(pygame.image.load("healing.png"))
    for i in range(9):
        heals.append(None)
    enemy = pygame.image.load("plane_enemy.png")
    boom = pygame.image.load("boom.png")
    planets.append(pygame.image.load("planet.png"))              
    for i in range(5):
        planets.append(None)
    bullet = pygame.image.load("bullet.png")
    e_bullet.append(pygame.image.load("bullet_enemy.png"))
    for i in range(2):
        e_bullet.append(None)
    shot_sound = pygame.mixer.Sound('shot.wav')
    explosion_sound = pygame.mixer.Sound('gameover.wav')
    
    clock = pygame.time.Clock()
    Menu()

initGame()
