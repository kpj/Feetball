import sprites, time

#############################
# Deal with particle-system #
#############################

def checkForParticles(l):
	output = []
	for o in l:
		if o.wantsParticles:
			o.wantsParticles = False
			output.extend(createParticles(o.rect.centerx, o.rect.centery))
	return output

def createParticles(x, y):
	partics = []
	for i in range(10):
		partics.append(sprites.particle(x, y, 1, time.time()))
	return partics
