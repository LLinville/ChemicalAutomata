import pygame
import colorsys
import random

# initialize game engine
from reactor.Atom import Atom
from reactor.Reaction import Reaction
from reactor.Reactor import Reactor, validateAtomLocations

pygame.init()
# set screen width/height and caption
size = [640, 480]
screen = pygame.display.set_mode(size)
pygame.display.set_caption('My Game')
# initialize clock. used later in the loop.
clock = pygame.time.Clock()

atomWidth = 7
atomBorder = 2
numElements = 7
numStates = 4
reactorScreenLocation = (20, 20)

reactor = Reactor((20, 20))

startingAtoms = []
reactor.addReaction("a1", "b1", "a0Xb0")
reactor.addReaction("b0", "b1", "b2Xb0")
reactor.addReaction("c1", "b0", "c0 b3")

reactor.addAntireaction("b3", "b2", "b3", "b3")



for a in range(1):
    reactor.addAtom(Atom(0, 1), (random.randrange(reactor.getSize()[0]), random.randrange(reactor.getSize()[1])))
    #reactor.addAtom(Atom(random.randrange(numElements), random.randrange(numStates)), (random.randrange(10),random.randrange(10)))



# reactor.addAtom(Atom(0, 0), (5, 5))
# reactor.addAtom(Atom(0, 0), (7, 9))
# reactor.addAtom(Atom(0, 0), (9, 7))
# reactor.addAtom(Atom(0, 0), (9, 9))
# for reaction in range(26):
#     reactant1 = random.choice("abcdefghijklmnopqrstuvwxyz"[:numElements]) + str(random.randrange(numStates))
#     reactant2 = random.choice("abcdefghijklmnopqrstuvwxyz"[:numElements]) + str(random.randrange(numStates))
#     reactor.addReaction(reactant1, reactant2, Reaction(
#         reactant1[0] + str(random.randrange(numStates),
#         reactant2[0] + str(random.randrange(numStates))),
#         bond=random.choice([True, False])))
#
# for antireaction in range(5):
#     reactor.addAntireaction(random.choice("abcdefghijklmnopqrstuvwxyz"[:numElements]) + str(random.randrange(numStates)), random.choice("abcdefghijklmnopqrstuvwxyz"[:numElements]) + str(random.randrange(numStates)))

def incrementState(reactor):
    validateAtomLocations(reactor.getCells())
    reactor.react()
    reactor.removeBadBonds()
    reactor.move()
    if random.random() < 0.1:
        reactor.addAtom(Atom(1, 1),
                        (random.randrange(reactor.getSize()[0]), random.randrange(reactor.getSize()[1])))
    if random.random() < 0.01:
        reactor.addAtom(Atom(2, 1), (random.randrange(reactor.getSize()[0]), random.randrange(reactor.getSize()[1])))
def drawState():
    screen.fill((255, 255, 255))
    state = reactor.getCells()
    for y, row in enumerate(state):
        for x, cell in enumerate(row):
            if cell is not None:
                if manhattanDist(cell.getLocation(), (x,y)) > 0:
                    print("Cell isn't in the right place!")
                try:
                    pygame.draw.rect(screen, stateColors[cell.getType()][cell.getState()], getCellBoundingBox(x, y))
                except Exception:
                    print("exception")

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
                    if manhattanDist(cell.getLocation(), bond.getLocation()) > 5:
                        print("Giant bond")

def getCellBoundingBox(x, y):
    return (
        (atomWidth + atomBorder) * x + reactorScreenLocation[0],
        (atomWidth + atomBorder) * y + reactorScreenLocation[1],
        (atomWidth + atomBorder * 2),
        (atomWidth + atomBorder * 2)
    )

def colorWheel(hue, numberOfSaturations):
    saturations = [1.0 * (n + 1) / (numberOfSaturations + 1) for n in range(numberOfSaturations + 1)]
    rgb = [colorsys.hsv_to_rgb(hue, saturation, 1) for saturation in saturations]
    return [(int(color[0] * 255), int(color[1] * 255), int(color[2] * 255)) for color in rgb]

def manhattanDist(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

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