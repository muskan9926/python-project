import random
import sys
# we us sys.exit to exit the program
import pygame
from pygame.locals import *
# basic pygame imports

# global variables for the game
#frame per second 1 second 32 images
FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
# display.set mode it is used to initilliase the screen gives size 289 by 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT*0.8


# 80 percent of screen is ground height
GAME_SPRITES = {}
# display image
# dispaly sound
GAME_SOUNDS = {}
PLAYER = 'gallery/sprites/bird.png'
BACKGROUND = 'gallery/sprites/background.png'
PIPE = 'gallery/sprites/pipe.png'

def welcomescreen():
    # where are player should be from side
    playerx = int(SCREENWIDTH/5)
    # for player in center
    playery = int((SCREENHEIGHT-GAME_SPRITES['player'].get_height())/2)
    # to print messeage in center
    messagey = int(SCREENHEIGHT*0.13)
    messagex = int((SCREENWIDTH - GAME_SPRITES['messages'].get_width())/2)
    basex = 0
    while True:
        # it tells the event keyboard mouse where you clicked which key
        for event in pygame.event.get():
#if user click on cross button key down means we have pressed any key k_escape is the key used for escape present in pygame lin
         if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
             pygame.quit()
             sys.exit()

#if  user press space bar or up arrow key start the game
         elif event.type==KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
             return
         else:
             # blit means chipkana the image we wante at particular pos
             SCREEN.blit(GAME_SPRITES['background'],(0,0))
             SCREEN.blit(GAME_SPRITES['player'], (playerx,playery))
             SCREEN.blit(GAME_SPRITES['messages'], (messagex,messagey))
             SCREEN.blit(GAME_SPRITES['base'], (basex,GROUNDY))
             pygame.display.update()
             FPSCLOCK.tick(FPS)


def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery > GROUNDY - 25 or playery < 0:
        GAME_SOUNDS['hit'].play()
        return True

    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if (playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) <GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

    return False


def maingame():
    score = 0
    # here bird is set at center
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/5)
    basex = 0
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()
    # creating two types for blitting on screen and list of upper pipes and lower pipe
    upperPipes=[{'x': SCREENWIDTH+200, 'y': newPipe1[0]['y']},
                {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y': newPipe2[0]['y']},
                ]
    #lower pipe

    lowerPipes=[{'x': SCREENWIDTH+200, 'y': newPipe1[1]['y']},
                {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y': newPipe1[1]['y']},
                ]
    pipevelx=-4
    playervely=-9
    playermaxvely=10
    playerminvely=-8
    playeracc=1
    # velocity while flappping
    playerflapaccv=-8
    playerflapped=False
    # true only when bird is flapping
    #game loop bliitering
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    # it means that the player is in screen
                    playervely=playerflapaccv
                    playerflapped=True
                    GAME_SOUNDS['wing'].play()

        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes)  # This function will return true if the player is crashed
        if crashTest:
            return
            # return true if crashed

        #check for score
        playermidpos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
              pipemidpos = pipe['x']+GAME_SPRITES['pipe'][0].get_width()/2
              if pipemidpos <= playermidpos < pipemidpos+4:
                score += 2
                print(f"your score is {score}")
                GAME_SOUNDS['point'].play()

              if playervely < playermaxvely and not playerflapped:
               playervely += playeracc
              if playerflapped:
                  playerflapped = False
              playerheight = GAME_SPRITES['player'].get_height()
              playery = playery+min(playervely, GROUNDY-playery-playerheight)

              for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
                  upperPipe['x'] += pipevelx
                  lowerPipe['x'] += pipevelx

              #     to add new pipe
              if 0 < upperPipes[0]['x'] < 5:
                newpipe = getRandomPipe()
                upperPipes.append(newpipe[0])
                lowerPipes.append(newpipe[1])

              if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
                  upperPipes.pop(0)
                  lowerPipes.pop(0)


              SCREEN.blit(GAME_SPRITES['background'], (0, 0))
              for upperpipe, lowerpipe in zip(upperPipes, lowerPipes):
                 SCREEN.blit(GAME_SPRITES['pipe'][0], (upperpipe['x'], upperpipe['y']))
                 SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerpipe['x'], lowerpipe['y']))

              SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
              SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
              myDigits = [int(x) for x in list(str(score))]
              width = 0
              for digit in myDigits:
                width += GAME_SPRITES['numbers'][digit].get_width()
              Xoffset=(SCREENWIDTH-width)/2
              for digit in myDigits:
                 SCREEN.blit(GAME_SPRITES['numbers'][digit],(Xoffset, SCREENHEIGHT*0.12))
                 Xoffset += GAME_SPRITES['numbers'][digit].get_width()
              pygame.display.update()
              FPSCLOCK.tick(FPS)
#get random pipe is function contains list under which exists dictionary  x and y value for upper pipe and for x y for lower popoe
#  first we will set lower pipe according to which we will put upper pipe we will make pipe 10+width for x then we wil move it to left
#  of set is the value which y should have we will add random no from offset and screenheight -base-1.2*offset so that  upper pipe dosent touches base lower base shoul also be there
# y1 is the the distance from origin to ending of pipe from above  suppose our height of pipe is ph now we want that the distance between  upper and lower pipe shoul be present
# so y1=ph-y2+ofset y2 is the distance from above to the lower pipe so our pipe will move above

def getRandomPipe():
    """
    Generate positions of two pipes(one bottom straight and one top rotated ) for blitting on the screen
    """
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2 * offset))
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1}, #upper Pipe
        {'x': pipeX, 'y': y2} #lower Pipe
    ]
    return pipe

if __name__ == '__main__':
 pygame.init()
 FPSCLOCK=pygame.time.Clock()
 # control game fps how many frames it will take
 pygame.display.set_caption("Flappy Bird By Muskan")
 #  convert alpha-used for faster blending
 GAME_SPRITES['numbers']=(pygame.image.load('gallery/sprites/0.png').convert_alpha(),
                          pygame.image.load('gallery/sprites/1.png').convert_alpha(),
                          pygame.image.load('gallery/sprites/2.png').convert_alpha(),
                          pygame.image.load('gallery/sprites/3.png').convert_alpha(),
                          pygame.image.load('gallery/sprites/4.png').convert_alpha(),
                          pygame.image.load('gallery/sprites/5.png').convert_alpha(),
                          pygame.image.load('gallery/sprites/6.png').convert_alpha(),
                          pygame.image.load('gallery/sprites/7.png').convert_alpha(),
                          pygame.image.load('gallery/sprites/8.png').convert_alpha(),
                          pygame.image.load('gallery/sprites/9.png').convert_alpha(),)
 GAME_SPRITES['messages']=pygame.image.load('gallery/sprites/bg.webp').convert_alpha()
 GAME_SPRITES['base'] = pygame.image.load('gallery/sprites/base.png').convert_alpha()
 GAME_SPRITES['pipe'] =(pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
                         pygame.image.load(PIPE).convert_alpha())

#  initiallising game sounds
GAME_SOUNDS['die']=pygame.mixer.Sound('gallery/audio/die.wav')
GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')

GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

while True:
    # shows welcome screen until clicked somewhere
    welcomescreen()
    # starts the game
    maingame()