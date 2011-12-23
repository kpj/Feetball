import os, random
from useful import *
s = keySet()

WINDOWW = 600
WINDOWH = 500
WINDOWCAPTION = "FeetBall"
BGCOL = (38, 255, 92)

GRAVITY = 0.00981
FRICTIONG = 0.9
FRICTIONA = 0.99

BALLSTARTV = 6
BALLSTARTX = WINDOWW/2
BALLSTARTY = 50
BALLACCEL = 50000
BALLMAXSPEEDX = 5
BALLMAXSPEEDY = 15
BALLIMG = os.path.join('img', 'ball.png')
BALLMASS = 8
BALLBOUNCE = 1.4

PLAYERACCEL = 50000
PLAYERMAXSPEEDX = 5
PLAYERMAXSPEEDY = 15
PLAYERJUMPSTREN = 6
PLAYERBOUNCE = 0.6

P1ID = random.randint(1000,100000)
P1NAME = "kpj"
P1STARTX = 150
P1STARTY = WINDOWH - 120
P1IMG = os.path.join('img', 'p1.png')
P1KEYS = s.getSet(0)
P1MASS = 10

P2ID = random.randint(1000,100000)
P2NAME = "Master"
P2STARTX = WINDOWW - 200
P2STARTY = WINDOWH - 120
P2IMG = os.path.join('img', 'p2.png')
P2KEYS = s.getSet(1)
P2MASS = 10
