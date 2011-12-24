import os, random
from useful import *
s = keySet()

WINDOWW = 1000 # main-window's width
WINDOWH = 500 # main-window's height
WINDOWCAPTION = "FeetBall"	# main-window's caption
BGCOL = (38, 255, 92) # main-window's background-color

GRAVITY = 0.00981	# Gravity in this world
FRICTIONG = 0.9 # Friction on the ground
FRICTIONA = 0.99 # Friction in the air

SHOTSOUND = os.path.join('sound', 'shot.wav')

BALLSTARTV = 6 # Maximum of ball's random start velocity
BALLSTARTX = WINDOWW/2 # x-coordinate of ball's spawn point
BALLSTARTY = 50 # y-coordinate of ball's spawn point
BALLACCEL = 50000 # Useless, because ball won't accelerate on keypressure
BALLMAXSPEEDX = 20 # Ball's maximum speed on x-axis
BALLMAXSPEEDY = 15 # Ball's maximum speed on y-axis
BALLIMG = os.path.join('img', 'ball.png') # Ball's image
BALLMASS = 15 # Ball's mass
BALLBOUNCE = 1.4 # Factor to determine ball's bounciness

FOOTSPEED = 0.2 # How fast should the foot move, when triggered
FOOTMASS = 17 # Foot's mass

PLAYERACCEL = 50000 # Player's acceleration, on keypress
PLAYERMAXSPEEDX = 5 # Player's maximum speed on x-axis
PLAYERMAXSPEEDY = 15 # Player's maximum speed on y-axis
PLAYERJUMPSTREN = 6 # Player's velocity, when jumping (y-axis)
PLAYERBOUNCE = 0.6 # Factor to determine player's bounciness

P1ID = random.randint(1000,100000) # ID of first player
P1NAME = "kpj" # Name of first player
P1STARTX = 150 # X-coordinate of first player's spawn point
P1STARTY = WINDOWH - 120 # Y-coordinate of first player's spawn point
P1IMG = os.path.join('img', 'p1.png') # First player's image
P1KEYS = s.getSet(0) # First players key set
P1MASS = 20	# First player's mass

P2ID = random.randint(1000,100000) # vice versa...
P2NAME = "Master"
P2STARTX = WINDOWW - 200
P2STARTY = WINDOWH - 120
P2IMG = os.path.join('img', 'p2.png')
P2KEYS = s.getSet(1)
P2MASS = 20
