import pygame
import colorsys
import random

# initialize game engine
from reactor.Atom import Atom
from reactor.Reaction import Reaction
from reactor.Reactor import Reactor

pygame.init()
# set screen width/height and caption
size = [640, 480]
screen = pygame.display.set_mode(size)
pygame.display.set_caption('My Game')
# initialize clock. used later in the loop.
clock = pygame.time.Clock()

atomWidth = 7
atomBorder = 1
numElements = 2
numStates = 4
reactorScreenLocation = (20, 20)

reactor = Reactor((20, 20))

for x in range(10):
    for y in range(10):
        if random.random() < 0.3:
            reactor.addAtom(Atom(random.randrange(numElements), random.randrange(numStates)), (x,y))

# reactor.addAtom(Atom(0, 0), (5, 5))
# reactor.addAtom(Atom(0, 0), (7, 9))
# reactor.addAtom(Atom(0, 0), (9, 7))
# reactor.addAtom(Atom(0, 0), (9, 9))
for r in range(16):
    reactor.addReaction((random.randrange(numElements), random.randrange(numStates)),
                        (random.randrange(numElements), random.randrange(numStates)),
                        Reaction(random.randrange(numStates), random.randrange(numStates), random.choice([True, False])))
#reactor.addReaction((0,0), (0,0), Reaction(2, 2, True))

def incrementState(reactor):
    reactor.react()
    reactor.removeBadBonds()
    reactor.move()

def drawState():
    screen.fill((255, 255, 255))
    state = reactor.getCells()
    for y, row in enumerate(state):
        for x, cell in enumerate(row):
            if cell is not None:
                pygame.draw.rect(screen, stateColors[cell.getType()][cell.getState()], getCellBoundingBox(x, y))
    
def drawBonds():
    for y, row in enumerate(reactor.getCells()):
        for x, cell in enumerate(row):
            if cell is not None:
                for bond in cell.getBonds():
                    thisBox = getCellBoundingBox(x, y)
                    thisCenter = (thisBox[0] + thisBox[2] / 2, thisBox[1] + thisBox[3] / 2)
                    bondedBox = getCellBoundingBox(bond.getLocation()[0], bond.getLocation()[1])
                    bondedCenter = (bondedBox[0] + bondedBox[2] / 2, bondedBox[1] + bondedBox[3] / 2)
                    pygame.draw.line(screen, (0,0,0), thisCenter, bondedCenter)
                    if abs(cell.getLocation()[0] - bond.getLocation()[0]) + abs(cell.getLocation()[1] - bond.getLocation()[1]) > 5:
                        print("Giant bond")

def getCellBoundingBox(x, y):
    return (
        (atomWidth + atomBorder) * x + reactorScreenLocation[0],
        (atomWidth + atomBorder) * y + reactorScreenLocation[1],
        (atomWidth + atomBorder * 2),
        (atomWidth + atomBorder * 2)
    )

def colorWheel(hue, numberOfSaturations):
    saturations = [1.0 * n / (numberOfSaturations + 1) for n in range(numberOfSaturations + 1)]
    rgb = [colorsys.hsv_to_rgb(hue, saturation, 1) for saturation in saturations]
    return [(int(color[0] * 255), int(color[1] * 255), int(color[2] * 255)) for color in rgb[1:]]

stateColors = [colorWheel(1.0 * element / numElements, numStates) for element in range(numElements)]


# Loop until the user clicks close button
done = False
while done == False:
    # write event handlers here
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    # write game logic here

    # clear the screen before drawing
    incrementState(reactor)
    drawState()
    drawBonds()
    # write draw code here

    pygame.display.update()
    # run at 20 fps
    clock.tick(20)

# close the window and quit
pygame.quit()