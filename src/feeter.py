from init import *
from var import *

i=setupWindow(WINDOWW, WINDOWH)
i.init(WINDOWCAPTION)
i.setBG(BGCOL)
i.addSpheres()
i.addFeet()
i.addWalls()
i.game()
