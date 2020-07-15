from pygame import *
from random import *
from math import *
from sys import *

myClock = time.Clock()
font.init()

# INITIALIZING -----------------------------------------------------------------------------------------------------
paddle = transform.scale(image.load("images/paddle.png"),(100,20))
paddle_width = paddle.get_width()
ball_diameter = 12
ball_radius = ball_diameter//2
ball = transform.scale(image.load("images/ball.png"),(ball_diameter,ball_diameter))
brick1 = transform.scale(image.load("images/brickblue1.png"),(70,25)) # solid brick
brick2 = transform.scale(image.load("images/brickblue2.png"),(70,25)) # medium-solid brick
brick3 = transform.scale(image.load("images/brickblue3.png"),(70,25)) # weak brick
steelbrick = transform.scale(image.load("images/steelbrick.png"),(70,25))
bricklist = [brick1,brick2,brick3]

# CAPSULE SETTINGS
capsuletype = "None"
capsule_x,capsule_y = 0,0
capsule = transform.scale(image.load("images/capsule.png"),(40,15))
bullet = transform.scale(image.load("images/bullet.png"),(20,30))
gun1_y,gun2_y,gun3_y = 0,0,0
gun1_rect = Rect(0,0,20,30)
gun2_rect = Rect(0,0,20,30)
gun3_rect = Rect(0,0,20,30)
is_flipped = False
wrapped = False
catch = False
bomb = False
bombred = False
gunlaunch = False
bombballred = transform.scale(image.load("images/bombballred.png"),(ball_diameter,ball_diameter))
bombballyellow = transform.scale(image.load("images/bombballyellow.png"),(ball_diameter,ball_diameter))

# FONTS
gamefont = font.Font("RetroGaming.ttf",22)
gamefontsmall = font.Font("RetroGaming.ttf",20)
gamefonttiny = font.Font("RetroGaming.ttf",10)


screen = display.set_mode((500,650))
default_paddle_x,default_paddle_y = screen.get_width()//2-paddle_width//2,600
default_ball_x,default_ball_y = screen.get_width()//2-ball_radius,595-ball_diameter
paddle_x,paddle_y = screen.get_width()//2-paddle_width//2,600
ball_x,ball_y = screen.get_width()//2-ball_radius,paddle_y-ball_diameter
scorenum = 0
livesnum = 3
ammonum = 0
level = 1
y_hit = False
x_hit = False

#--------------------------------------------------------------------------------------------------------------------

# list showing the locations of the bricks (i[0] for i in lev1blocks), and the strength of the bricks (i[1] for i in lev1blocks)
lev1blocks = [[[150,100],1],[[75,130],1],[[75,190],1],[[75,220],1],[[150,250],1],[[350-70,100],1],[[425-70,130],1],[[425-70,190],1],[[425-70,220],1],[[350-70,250],1]]

def initialize(): # reverts to initial settings
    x_paddle_change = 0
    accel_paddle_x = 0
    paddle_x,paddle_y = screen.get_width()//2-paddle_width//2,600
    ball_x,ball_y = screen.get_width()//2-ball_radius,paddle_y-ball_diameter-5
    x_change = (4)*angle # x-component of ball's position changes by 2*angle every cycle
    y_change = (-4)*sin(acos(abs(angle))) # y-component of ball's position changes by (-2)*angle every cycle
    max_speed = 7
    return x_paddle_change,accel_paddle_x,ball_x,ball_y,paddle_x,paddle_y,x_change,y_change,max_speed

def newmax(name,scorenum,maxname,maxscore): # checks if current score beats high score, if so, it becomes the new high score
    fwrite = open("scores.txt","w")
    if scorenum >= maxscore:
        fwrite.write(str(name)+" "+str(scorenum))
    else:
        fwrite.write(str(maxname)+" "+str(maxscore))
    fwrite.close()

def drawscene(angle,scorenum,livesnum,ammonum,ball_x,ball_y,paddle_x,paddle_y,angles): #blits everything onto the screens
    screen.fill((0,0,0))
    screen.blit(ball,(ball_x,ball_y))
    screen.blit(paddle,(paddle_x,paddle_y))

    scoretext = gamefont.render("SCORE:"+str(scorenum),True,(255,255,0))
    livestext = gamefont.render("LIVES:"+str(livesnum),True,(255,255,0))
    ammotext = gamefont.render("AMMO:"+str(ammonum),True,(255,255,0))
    highscoretext = gamefontsmall.render("HIGH SCORE:"+str(maxscore),True,(255,255,0))

    if angle != 0 and angles != 0: # if start() is called, a line is drawn showing the trajectory of the ball at different angles
        draw.line(screen,(255,0,0),(ball_x+6,paddle_y-ball_radius),(ball_x+6+70*angle,paddle_y-ball_radius-70*sin(acos(abs(angle)))))
        
    screen.blit(scoretext,(30,20))
    screen.blit(livestext,(200,20))
    screen.blit(ammotext,(360,20))
    screen.blit(highscoretext,(250-highscoretext.get_width()//2,0))
    draw.line(screen,(255,255,0),(0,50),(600,50))

def drawblocks(blocklist):
    for i in blocklist:
        if i[1] == 1:
            screen.blit(brick1,tuple(i[0]))
        elif i[1] == 2:
            screen.blit(brick2,tuple(i[0]))
        elif i[1] == 3:
            screen.blit(brick3,tuple(i[0]))
        elif i[1] == "steel":
            screen.blit(steelbrick,tuple(i[0]))

def menu():
    screen.fill((0,0,0))
    iconpic = transform.scale(image.load("images/menu.png"),(screen.get_width(),180)) # shows brick breaker logo
    enter_text = gamefontsmall.render("PRESS ENTER TO START",True,(255,255,0))
    name = ''
    f = open("scores.txt","r")
    fline = f.readline()

    maxname = fline.split()[0] # name of person w/ highest score
    maxscore = int(fline.split()[1])

    f.close()

    highscore_text = gamefontsmall.render("HIGH SCORE IS "+maxname+" WITH "+str(maxscore),True,(0,255,0))

    running = True

    while running:
        for evt in event.get():
            if evt.type == QUIT:
                exit()
            elif evt.type == KEYDOWN:
                if evt.key == K_RETURN:
                    return name,maxname,maxscore
                elif evt.key == K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += chr(evt.key) # builds name one character at a time

        draw.rect(screen,(0,0,0),(100,300,300,50))
        name_text = gamefontsmall.render("ENTER NAME: "+name,True,(255,0,0))
        screen.blit(name_text,(120,300))
        screen.blit(iconpic,(-5,100))
        screen.blit(highscore_text,(screen.get_width()//2-highscore_text.get_width()//2,350))
        screen.blit(enter_text,(screen.get_width()//2-enter_text.get_width()//2,400))

        display.flip()


def gameover():
    screen.fill((0,0,0))
    gameoverpic = transform.scale(image.load("images/gameover.png"),(screen.get_width(),300))
    gamefontsmall = font.Font("RetroGaming.ttf",18)
    score_text = gamefontsmall.render("SCORE:"+str(scorenum),True,(255,255,0))
    space_text = gamefontsmall.render("PRESS SPACE TO RESTART",True,(255,255,0))

    running = True
    while running:
        for evt in event.get():
            if evt.type == QUIT:
                newmax(name,scorenum,maxname,maxscore) # if the game is quit, the score is checked against the high score
                exit()
            if evt.type == KEYDOWN:
                if evt.key == K_SPACE:
                    running = False

        screen.blit(gameoverpic,(0,0))
        screen.blit(score_text,(screen.get_width()//2-score_text.get_width()//2,300))
        screen.blit(space_text,(screen.get_width()//2-space_text.get_width()//2,300+score_text.get_height()))

        display.flip()

def nextlevel(level):
    screen.fill((0,0,0))
    bricklist = []
    gamefontbig = font.Font("RetroGaming.ttf",24)
    gamefontsmall = font.Font("RetroGaming.ttf",18)
    levelup_text = gamefontbig.render("LEVEL UP",True,(34,255,71))
    nextlevel_text = gamefontsmall.render("NEXT LEVEL: "+str(level+1),True,(34,255,71))
    space_text = gamefontsmall.render("PRESS SPACE TO CONTINUE",True,(255,255,0))

    if level == 2:
        for i in range(3):
            # loads images of the coloured bricks in every level of strength to a list
            # using a list allows me to loop through and let the computer fill in the numbers, as I have them listed as brickcolour1.png,brickcolour2.png,brickcolour3.png
            bricklist.append(transform.scale(image.load("images/brickgreen"+str(i+1)+".png"),(70,25)))
        # blocklist changes, bc locations and strengths of the bricks change with each level
        blocklist = [[[55,100],2],[[55,125],3],[[125,100],3],[[125,125],3],[[55,175],2],[[55,200],3],[[125,175],3],[[125,200],3],[[55,250],2],[[125,250],3],[[55,275],3],[[125,275],3],
                     [[305,100],2],[[305,125],3],[[375,100],3],[[375,125],3],[[305,175],2],[[305,200],3],[[375,175],3],[[375,200],3],[[305,250],2],[[305,275],3],[[375,250],3],[[375,275],3]]
    elif level == 3:
        for i in range(3):
            bricklist.append(transform.scale(image.load("images/orangebrick"+str(i+1)+".png"),(70,25)))
        blocklist = [[[135,100],1],[[205,100],1],[[275,100],1],[[135,150],1],[[65,150],1],[[65,175],1],[[65,200],1],[[65,225],1],[[135,225],1],
                     [[275,150],1],[[345,150],1],[[345,175],1],[[345,200],1],[[345,225],1],[[275,225],1],[[135,275],1],[[205,275],2],[[275,275],"steel"]]
    elif level == 4:
        for i in range(3):
            bricklist.append(transform.scale(image.load("images/purplebrick"+str(i+1)+".png"),(70,25)))
        blocklist = [[[145,0],3],[[285,0],3],[[145,25],1],[[285,25],1],[[145,50],2],[[285,50],2],[[145,75],2],[[215,75],2],[[285,75],2],
                     [[75,100],3],[[145,100],3],[[215,100],3],[[285,100],3],[[355,100],3],[[5,100],3],[[425,100],3],[[285,125],1]]
        for i in blocklist:
            i[0][1] += 50 # forgot that the ball only travels below y=50, fixed it by adding 50 to every y
    elif level == 5:
        for i in range(3):
            bricklist.append(transform.scale(image.load("images/darkpurplebrick"+str(i+1)+".png"),(70,25)))
        blocklist = [[[75,25],2],[[355,25],2],[[75,50],3],[[355,50],3],[[75,75],1],[[145,75],1],[[215,75],1],[[285,75],1],[[355,75],1],
                     [[75,100],3],[[145,100],3],[[215,100],3],[[285,100],3],[[355,100],3],[[75,125],1],[[145,125],1],[[215,125],1],[[285,125],1],[[355,125],1],
                     [[145,150],3],[[285,150],3],[[145,175],3],[[285,175],3]]
        for i in blocklist:
            i[0][1] += 50 # forgot that the ball only travels below y=50, fixed it by adding 50 to every y
    elif level == 6:
        for i in range(3):
            bricklist.append(transform.scale(image.load("images/redbrick"+str(i+1)+".png"),(70,25)))
        blocklist = [[[80,25],"steel"],[[80,50],"steel"],[[80,75],"steel"],[[80,100],"steel"],[[80,125],"steel"],[[80,150],"steel"],[[80,175],"steel"],[[80,200],"steel"],[[150,200],"steel"],
                     [[220,200],"steel"],[[290,200],"steel"],[[360,200],"steel"],[[430,200],"steel"],[[150,125],3],[[220,100],3],[[220,125],2],[[220,150],3],[[290,75],3],[[290,100],2],[[290,125],1],
                     [[290,150],2],[[290,175],3],[[360,100],3],[[360,125],2],[[360,150],3],[[430,125],3]]
        for i in blocklist:
            i[0][1] += 50 # forgot that the ball only travels below y=50, fixed it by adding 50 to every y
    elif level == 7:
        for i in range(3):
            bricklist.append(transform.scale(image.load("images/yellowbrick"+str(i+1)+".png"),(70,25)))
        blocklist = [[[215,125],"steel"],[[145,125],"steel"],[[75,125],"steel"],[[285,125],"steel"],[[355,125],"steel"],[[215,100],"steel"],[[215,75],"steel"],[[215,50],"steel"],
                     [[215,25],"steel"],[[215,150],"steel"],[[215,175],"steel"],[[215,200],"steel"],[[215,225],"steel"],[[145,100],3],[[145,75],3],[[145,50],3],[[285,100],3],[[285,75],3],[[285,50],3],
                     [[145,150],3],[[145,175],3],[[145,200],3],[[285,150],3],[[285,175],3],[[285,200],3]]
        for i in blocklist:
            i[0][1] += 50 # forgot that the ball only travels below y=50, fixed it by adding 50 to every y
    elif level == 8:
        for i in range(3):
            bricklist.append(transform.scale(image.load("images/brickblue"+str(i+1)+".png"),(70,25)))
        blocklist = [[[0,0],3],[[70,0],2],[[140,0],3],[[0,25],3],[[70,25],2],[[140,25],3],[[0,50],3],[[70,50],2],[[140,50],3],[[0,75],"steel"],[[70,75],"steel"],[[140,75],"steel"],[[210,75],"steel"],[[280,75],"steel"],[[350,75],"steel"],
                     [[80,150],"steel"],[[150,150],"steel"],[[220,150],"steel"],[[290,150],"steel"],[[360,150],"steel"],[[430,150],"steel"],[[0,225],"steel"],[[70,225],"steel"],[[140,225],"steel"],[[210,225],"steel"],
                     [[280,225],"steel"],[[350,225],"steel"]]
        for i in blocklist:
            i[0][1] += 50 # forgot that the ball only travels below y=50, fixed it by adding 50 to every y
    elif level == 9:
        for i in range(3):
            bricklist.append(transform.scale(image.load("images/brickgreen"+str(i+1)+".png"),(70,25)))
        blocklist = [[[0,0],3],[[0,25],"steel"],[[70,25],"steel"],[[430,0],3],[[430,25],"steel"],[[360,25],"steel"],[[145,125],"steel"],[[215,125],"steel"],[[285,125],"steel"],[[215,100],3],[[0,200],"steel"],[[70,200],"steel"],[[140,200],"steel"],
                     [[430,200],"steel"],[[360,200],"steel"],[[290,200],"steel"],[[0,175],3],[[430,175],3]]
        for i in blocklist:
            i[0][1] += 50 # forgot that the ball only travels below y=50, fixed it by adding 50 to every y
    elif level == 10:
        for i in range(3):
            bricklist.append(transform.scale(image.load("images/orangebrick"+str(i+1)+".png"),(70,25)))
        blocklist = []
        for i in range(3): # follows a pattern of 6 blocks, three times. looping through was easier than typing it all out
            blocklist.extend([[[0,75+(75*i)],3-i],[[70,75+(75*i)],3-i],[[140,75+(75*i)],"steel"],[[0,100+(75*i)],"steel"],[[70,100+(75*i)],"steel"],[[140,100+(75*i)],"steel"],[[430,75+(75*i)],3-i],[[360,75+(75*i)],3-i],[[290,75+(75*i)],"steel"],[[430,100+(75*i)],"steel"],[[360,100+(75*i)],"steel"],[[290,100+(75*i)],"steel"]])

    # assigns each value in bricklist to its respective brick
    brick1 = bricklist[0]
    brick2 = bricklist[1]
    brick3 = bricklist[2]

    running = True
    while running:
        for evt in event.get():
            if evt.type == QUIT:
                newmax(name,scorenum,maxname,maxscore)
                exit()
            if evt.type == KEYDOWN:
                if evt.key == K_SPACE:
                    return blocklist,brick1,brick2,brick3

        screen.blit(levelup_text,(screen.get_width()//2-levelup_text.get_width()//2,300))
        screen.blit(nextlevel_text,(screen.get_width()//2-nextlevel_text.get_width()//2,400))
        screen.blit(space_text,(screen.get_width()//2-space_text.get_width()//2,500))

        display.flip()

def start(blocklist,paddle_x,paddle_y,ball_x,ball_y):
    gamefontsmall = font.Font("RetroGaming.ttf",18)
    launch_text = gamefontsmall.render("PRESS SPACE TO LAUNCH",True,(255,255,0))
    # angles available to the user 
    # there are duplicates bc the left half of angles correspond to the negative cos of that angle
    # the right half correspond to the positive cos of that angle
    angles = [pi/6,pi/4,pi/3,pi/3,pi/4,pi/6]
    index = 2 # index is the position in angles the user has currently chosen
    running = True

    while running:
        for evt in event.get():
            if evt.type == QUIT:
                newmax(name,scorenum,maxname,maxscore) # if the game is quit, the score is checked against the high score
                exit()
            if evt.type == KEYDOWN:
                # right and left key lets the user switch the index
                if evt.key == K_LEFT:
                    index -= 1
                    if index < 0:
                        index = 0
                elif evt.key == K_RIGHT:
                    index += 1
                    if index > 5:
                        index = 5
                elif evt.key == K_SPACE:
                    return angle

        if index<=2:
            angle = (-1)*cos(angles[index])
        else:
            angle = cos(angles[index])

        drawscene(angle,scorenum,livesnum,ammonum,ball_x,ball_y,paddle_x,paddle_y,angles)
        drawblocks(blocklist)
        screen.blit(launch_text,(250-(launch_text.get_width()//2),500))

        display.flip()

def probcapsule():
    dropprob = random()
    if dropprob > 0.999: # there is a 0.1% chance of a capsule dropping
        capsuleprob = random()
        # of the capsules dropping...
        if 0 < capsuleprob <= 0.15: # life has a 15% chance of being chosen
            return "life"
        elif 0.15 < capsuleprob <= 0.26: # gun has a 12% chance of being chosen
            return "gun"
        elif 0.26 < capsuleprob <= 0.42: # long has a 16% chance of being chosen
            return "long"
        elif 0.42 < capsuleprob <= 0.57: # wrap has a 15% chance of being chosen
            return "wrap"
        elif 0.57 < capsuleprob <= 0.72: # flip has a 15% chance of being chosen
            return "flip"
        elif 0.72 < capsuleprob <= 0.88: # catch has a 12% chance of being chosen
            return "catch"
        elif 0.88 < capsuleprob <= 1: # bomb has a 12% chance of being chosen
            return "bomb"
    else:
        return "None"

name,maxname,maxscore = menu()
angle = start(lev1blocks,paddle_x,paddle_y,ball_x,ball_y)
x_paddle_change,accel_paddle_x,ball_x,ball_y,paddle_x,paddle_y,x_change,y_change,max_speed = initialize()
blocklist = lev1blocks

running = True

while running:
    for evt in event.get():
        if evt.type == QUIT:
            newmax(name,scorenum,maxname,maxscore) # if the game is quit, the score is checked against the high score
            running = False
        if evt.type == KEYDOWN:
            if is_flipped: # if capsule "flip" has collided w/ the paddle, directions are switched
                if evt.key == K_LEFT:
                    accel_paddle_x += 0.2 # left key corresponds to rightward movement
                if evt.key == K_RIGHT:
                    accel_paddle_x -= 0.2 # right key corresponds to leftward movement
            else:
                if evt.key == K_LEFT:
                    accel_paddle_x -= 0.2
                if evt.key == K_RIGHT:
                    accel_paddle_x += 0.2
            if evt.key == K_RETURN and gun_on: # if return is pressed and the "gun" capsule is activated, the bullet is lauched
                gunlaunch = True
        elif evt.type == KEYUP:
            # makes deceleration much easier for the user
            accel_paddle_x = 0
            x_paddle_change = 0

    ball_x += x_change
    ball_y += y_change
    
    # by making two variables each affecting paddle_x, I give the appearance of acceleration
    x_paddle_change += accel_paddle_x
    paddle_x += x_paddle_change

    ballrect = Rect(ball_x,ball_y,12,12)

    if abs(x_paddle_change) >= max_speed:  # If max_speed is exceeded.
        # Normalize the x_paddle_change and multiply it with the max_speed.
        x_paddle_change = x_paddle_change/abs(x_paddle_change) * max_speed

    if wrapped: # if "wrap" capsule is activated
        # if accel_paddle_x is negative, it means that the left key is pressed
        if accel_paddle_x < 0 and paddle_x < 3-paddle_width: # if left key is pressed and the paddle is going through the left side, it reappears on the right side
            paddle_x = 497+paddle_width
        # if accel_paddle_x is positive, it means that the left key is pressed
        if accel_paddle_x > 0 and paddle_x > 497+paddle_width:  # if righr key is pressed and the paddle is going through the right side, it reappears on the left side
            paddle_x = 3-paddle_width
    else:
        #if paddle hits the left or right side, the paddle is suddenly stopped, making it seem like there is a barrier
        if paddle_x < 3:
            x_paddle_change = 0
            accel_paddle_x = 0
            paddle_x = 3
        elif paddle_x > 497-paddle_width:
            x_paddle_change = 0
            accel_paddle_x = 0
            paddle_x = 497-paddle_width
    
    x_hit = False # if the left or right side of a brick is hit by the ball
    y_hit = False # if the top or bottom side of a brick is hit by the ball

    for i in blocklist:
        brickrect = Rect(i[0][0],i[0][1],70,25)
        noX = Rect(ball_x-x_change,ball_y,ball_diameter,ball_diameter) # creates a rect at the position of the previous ball_x
        noY = Rect(ball_x,ball_y-y_change,ball_diameter,ball_diameter) # creates a rect at the position of the previous ball_y
        if gun1_rect.colliderect(brickrect): # if 1st bullet collides with a brick, it breaks no matter its strength
            blocklist.remove(i)
            gun1_rect = Rect(0,0,20,30)
        elif gun2_rect.colliderect(brickrect): # if 2nd bullet collides with a brick, it breaks no matter its strength
            blocklist.remove(i)
            gun2_rect = Rect(0,0,20,30)
        elif gun3_rect.colliderect(brickrect): # if 3rd bullet collides with a brick, it breaks no matter its strength
            blocklist.remove(i)
            gun3_rect = Rect(0,0,20,30)
            gun_on = False # if 3rd (aka last) bullet collides w/ a brick, "gun" is deactivated
        elif brickrect.colliderect(ballrect):
            if brickrect.colliderect(noX) == False: # if previous ball_x doesn't hit and the current ball_x does
                x_hit = True
            if brickrect.colliderect(noY) == False: # if previous ball_y doesn't hit and the current ball_y does
                y_hit = True

            if i[1] != "steel":
                if bomb: # if "bomb" is activated, the ball destroys the brick it collides with
                    blocklist.remove(i)
                    # reverts to settings before "bomb" was activated
                    ball = transform.scale(image.load("images/ball.png"),(ball_diameter,ball_diameter))
                    bomb = False
                else:
                    i[1] += 1 # brick becomes one level weaker
                    if i[1] == 4: # if the weakest type of brick is hit
                        blocklist.remove(i) # it is destroyed
                    scorenum += 10 # user gets 10 additional points for every brick hit
            break

    if x_hit:
        x_change = (-1)*x_change # ball reflects in x direction
    elif y_hit:
        y_change = (-1)*y_change # ball reflects in y direction

    normblockcount = 0 # count of bricks that aren't steel bricks
    
    for i in blocklist:
        if i[1] != "steel":
            normblockcount += 1

    if normblockcount == 0: # if no normal bricks are left, the user has completed the level
        newmax(name,scorenum,maxname,maxscore) # current score is checked against high score
        level += 1
        blocklist,brick1,brick2,brick3 = nextlevel(level) # next level
        # settings are reverted
        wrapped = False
        catch = False
        bomb = False
        bombred = False
        gunlaunch = False
        capsuletype = "None"
        if level == 11: # game has run out of levels
            newmax(name,scorenum,maxname,maxscore) # current score is checked against high score
            gameover()
            # if user chooses to continue playing, they are lead to the beginning of the game
            blocklist = [[[150,100],1],[[75,130],1],[[75,190],1],[[75,220],1],[[150,250],1],[[350-70,100],1],[[425-70,130],1],[[425-70,190],1],[[425-70,220],1],[[350-70,250],1]] # level 1 blocks
            livesnum = 3
            scorenum = 0
        angle = start(blocklist,default_paddle_x,default_paddle_y,default_ball_x,default_ball_y)
        x_paddle_change,accel_paddle_x,ball_x,ball_y,paddle_x,paddle_y,x_change,y_change,max_speed = initialize()

    if ball_x < 5 or ball_x+ball_diameter > screen.get_width()-5: # if ball hits the sides of the screen, the x is reflected
        x_change = (-1)*x_change

    if ball_y < 55: # if ball hits the top of the screen, the y is reflected
        y_change = (-1)*y_change
    elif paddle_y-5 < ball_y+ball_diameter: # if ball hits the bottom of the screen
        if paddle_x < ball_x+ball_radius < paddle_x+paddle_width: # if ball hits the paddle
            if catch: # catch lets user choose their desired angle everytime the ball hits the paddle
                angle = start(blocklist,paddle_x,paddle_y,ball_x,ball_y)
                x_change = (4)*angle
                y_change = (-4)*sin(acos(abs(angle)))
            else:
                if ball_x+ball_radius == paddle_x+(paddle_width//2): # if ball_x hits the center of the paddle
                    ball_x += choice(-2,2) # x_change theoretically becomes 0, but this is remedied by moving the ball 2 pixels away
                x_change = (-1)*(paddle_width//2-ball_x-ball_radius+paddle_x)/10
                y_change = (-1)*y_change
            maxy =  blocklist[0][0][1]
            for i in blocklist:
                if i[0][1] > maxy:
                    maxy = i[0][1] # y-value of the lowest brick
            if maxy < 550: # if maxy is higher that y=550
                for i in range(len(blocklist)):
                    blocklist[i] = [[blocklist[i][0][0],blocklist[i][0][1]+10],blocklist[i][1]] # each bricks shifts down by 10 pixels
        else: # if ball misses the paddle, a life is lost and settings are reverted
            livesnum -= 1
            wrapped = False
            catch = False
            bomb = False
            bombred = False
            gunlaunch = False
            if livesnum == 0: # user is sent to the beginning of the game
                brick1 = transform.scale(image.load("images/brickblue1.png"),(70,25))
                brick2 = transform.scale(image.load("images/brickblue2.png"),(70,25))
                brick3 = transform.scale(image.load("images/brickblue3.png"),(70,25))
                blocklist = [[[150,100],1],[[75,130],1],[[75,190],1],[[75,220],1],[[150,250],1],[[350-70,100],1],[[425-70,130],1],[[425-70,190],1],[[425-70,220],1],[[350-70,250],1]]
                livesnum = 3
                scorenum = 0
                gameover()
                level = 1
            capsuletype = "None"
            ammonum = 0
            paddle = transform.scale(image.load("images/paddle.png"),(100,20))
            paddle_width = paddle.get_width()
            gun1_y,gun2_y,gun3_y = 0,0,0
            gun1_rect = Rect(0,0,20,30)
            gun2_rect = Rect(0,0,20,30)
            gun3_rect = Rect(0,0,20,30)
            angle = start(blocklist,default_paddle_x,default_paddle_y,default_ball_x,ball_y)
            x_paddle_change,accel_paddle_x,ball_x,ball_y,paddle_x,paddle_y,x_change,y_change,max_speed = initialize()

    
    if x_change == 0:
        # another failsafe, if x_change is 0 the ball travels straight up and down
        # another random x_change is chosen
        x_change = choice([uniform(-0.5,-0.05),uniform(0.05,0.5)])

    drawscene(0,scorenum,livesnum,ammonum,ball_x,ball_y,paddle_x,paddle_y,0) # blits essential aspects of the game
    drawblocks(blocklist) # blits the bricks

    if ammonum == 3:
        screen.blit(enter_gun_text,(250-(enter_gun_text.get_width()//2),550)) # gives instructions to launch the bullet

    if gunlaunch: # if bullet is launched
        if ammonum == 3:
            gun1_x,gun1_y = paddle_x+paddle_width//2,580 # the first bullet is activated, and starts from the centre of the paddle
            gun1_rect = Rect(gun1_x,gun1_y,20,30)
        elif ammonum == 2:
            gun2_x,gun2_y = paddle_x+paddle_width//2,580 # the second bullet is activated, and starts from the centre of the paddle
            gun2_rect = Rect(gun2_x,gun2_y,20,30)
        elif ammonum == 1:
            gun3_x,gun3_y = paddle_x+paddle_width//2,580 # the third bullet is activated, and starts from the centre of the paddle
            gun3_rect = Rect(gun3_x,gun3_y,20,30)
        gunlaunch = False
        ammonum -= 1

    # if bullet settings are not the reverted ones (aka a bullet has been activated)
    if gun1_rect != Rect(0,0,20,30) or gun1_y<-30:
        gun1_y -= 1 # bullet moves upwards
        gun1_rect = Rect(gun1_x,gun1_y,20,30)
        screen.blit(bullet,(gun1_x,gun1_y))
    if gun2_rect != Rect(0,0,20,30) or gun2_y<-30:
        gun2_y -= 1
        gun2_rect = Rect(gun2_x,gun2_y,20,30)
        screen.blit(bullet,(gun2_x,gun2_y))
    if gun3_rect != Rect(0,0,20,30) or gun3_y<-30:
        gun3_y -= 1
        gun3_rect = Rect(gun3_x,gun3_y,20,30)
        screen.blit(bullet,(gun3_x,gun3_y))

    if capsuletype == "None": # if no capsule is dropping
        capsuletype = probcapsule()
        if capsuletype != "None": # catches the moment a capsule is released
            capsule_text = gamefonttiny.render(capsuletype,True,(255,255,0))
            capsule_x,capsule_y = randrange(50,430),randrange(50,200) # generates a random initial point
    else:
        if capsule_y+15 < paddle_y: # if capsule has not reached the level of the paddle
            # it blits the capsuletype and the capsule
            screen.blit(capsule,(capsule_x,capsule_y))
            screen.blit(capsule_text,(capsule_x-(capsule_text.get_width()),capsule_y))
            capsule_y += 1
        elif paddle_x<capsule_x+20<paddle_x+paddle_width: # if capsule collides with paddle
            
            if capsuletype == "life":
                livesnum += 1

            if capsuletype == "flip":
                is_flipped = True
            else:
                is_flipped = False

            if capsuletype == "long":
                paddle = transform.scale(image.load("images/paddle.png"),(140,20))
            else:
                paddle = transform.scale(image.load("images/paddle.png"),(100,20))
            paddle_width = paddle.get_width()

            if capsuletype == "wrap":
                wrapped = True
            else:
                wrapped = False

            if capsuletype == "catch":
                catch = True
            else:
                catch = False

            if capsuletype == "bomb":
                bomb = True
                ball = bombballred # ball changes colour so its more apparent that it becomes a bomb
            else:
                ball = transform.scale(image.load("images/ball.png"),(ball_diameter,ball_diameter))

            if capsuletype == "gun":
                gun_on = True
                ammonum = 3
                enter_gun_text = gamefonttiny.render("PRESS ENTER TO LAUNCH AMMO",True,(255,255,0))
            else:
                gun_on = False
                ammonum = 0

            capsuletype = "None"

        elif capsule_y > paddle_y+15: # if capsule has gotten below the level of the paddle and has not collided with it (aka missed the capsule)
            capsuletype = "None" # it goes back to looking for a capsule to drop
        else:
            # blits the capsuletype and the capsule
            screen.blit(capsule,(capsule_x,capsule_y))
            screen.blit(capsule_text,(capsule_x-(capsule_text.get_width()),capsule_y))
            capsule_y += 1

    display.flip()

quit()
