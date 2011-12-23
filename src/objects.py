from var import *

p = [
	[
		P1STARTX,
		P1STARTY,
		P1IMG,
		P1KEYS,
		P1MASS,
		True,
		P1ID,
		P1NAME,
		PLAYERBOUNCE
	],
	[
		P2STARTX,
		P2STARTY,
		P2IMG,
		P2KEYS,
		P2MASS,
		True,
		P2ID,
		P2NAME,
		PLAYERBOUNCE
	],
	[
		BALLSTARTX,
		BALLSTARTY,
		BALLIMG,
		None,
		BALLMASS,
		False,
		-1,
		"Hans",
		BALLBOUNCE
	]
]



w = [
	[
		50,
		WINDOWH - 50,
		os.path.join('img', 'bottom.png'),
		True,
		-1
	],
	[
		0,
		WINDOWH - 150,
		os.path.join('img', 'chest.png'),
		True,
		-1
	],
	[
		WINDOWW - 100,
		WINDOWH - 150,
		os.path.join('img', 'chest.png'),
		True,
		-1
	],
	[
		0,
		WINDOWH - 250,
		os.path.join('img', 'chest.png'),
		True,
		-1
	],
	[
		WINDOWW - 100,
		WINDOWH - 250,
		os.path.join('img', 'chest.png'),
		True,
		-1
	],
	[
		WINDOWW - 130,
		WINDOWH - 150,
		os.path.join('img', 'goal.png'),
		False,
		P1ID
	],
	[
		100,
		WINDOWH - 150,
		os.path.join('img', 'goal.png'),
		False,
		P2ID
	],
]
