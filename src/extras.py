import sprites, time, random

#############################
# Deal with particle-system #
#############################

def checkForParticles(l, dur=5, num=10, col=(random.randint(0,255),random.randint(0,255),random.randint(0,255))):
	output = []
	for o in l:
		if o.wantsParticles:
			o.wantsParticles = False
			output.extend(createParticles(o.rect.centerx, o.rect.centery, dur, num, col))
	return output

def createParticles(x, y, dur=1, num=10, col=False):
	partics = []
	for i in range(num):
		partics.append(sprites.particle(x, y, dur, time.time(), col))
	return partics
