import pygame
import colorsys
import random

# initialize game engine
from reactor.Atom import Atom
from reactor.Reaction import Reaction
from reactor.Reactor import Reactor, validateAtomLocations

pygame.init()
# initialize clock. used later in the loop.
clock = pygame.time.Clock()

atomWidth = 8
atomBorder = 0
numElements = 4
numStates = 4
reactorScreenLocation = (0, 0)

reactor = Reactor((100, 100))

# set screen width/height and caption
size = [reactor.getSize()[0] * (atomWidth + atomBorder),
        reactor.getSize()[1] * (atomWidth + atomBorder)]
screen = pygame.display.set_mode(size)
pygame.display.set_caption('My Game')

startingAtoms = []
# reactor.addReaction("a1", "b1", "a0Xb0")
# reactor.addReaction("b0", "b1", "b2Xb0")
# reactor.addReaction("c1", "b2", "c0 b3")
# reactor.addReaction("a0", "b0", "a0Xb2")
#
# reactor.addAntireaction("b3", "b2", "b2", "b0")

# reactor.addReaction("a1", "a1", "a1Xa1")
# reactor.addReaction("a1", "b1", "a3 b0")
# reactor.addReaction("a1", "a3", "a3 a3")
# reactor.addAntireaction("a1", "a3", "a3", "a3")
# reactor.addAntireaction("a3", "a3", "a3", "a3")
#
# reactor.addReaction("c1", "a3", "c1 a2")
# reactor.addReaction("a2", "a3", "a1Xa1")



#for a in range(10):
    #reactor.addAtom(Atom(0, 1), (random.randrange(reactor.getSize()[0]), random.randrange(reactor.getSize()[1])))
    #reactor.addAtom(Atom(random.randrange(numElements), random.randrange(numStates)), (random.randrange(10),random.randrange(10)))



# reactor.addAtom(Atom(0, 0), (5, 5))
# reactor.addAtom(Atom(0, 0), (7, 9))
# reactor.addAtom(Atom(0, 0), (9, 7))
# reactor.addAtom(Atom(0, 0), (9, 9))
def initiateReactor(reactor):
    for reaction in range(random.randrange(15, 25)):
        reactant1 = random.choice("abcdefghijklmnopqrstuvwxyz"[:numElements]) + str(random.randrange(numStates))
        reactant2 = random.choice("abcdefghijklmnopqrstuvwxyz"[:numElements]) + str(random.randrange(numStates))
        reactor.addReaction(reactant1, reactant2, reactant1[0] + str(random.randrange(numStates)) + random.choice([" ", " ", "X"]) + reactant2[0] + str(random.randrange(numStates)))


    for antireaction in range(random.randrange(4, 8)):
        if random.random() < 0.5:
            continue
        reactant1 = random.choice("abcdefghijklmnopqrstuvwxyz"[:numElements]) + str(random.randrange(numStates))
        reactant2 = random.choice("abcdefghijklmnopqrstuvwxyz"[:numElements]) + str(random.randrange(numStates))
        reactor.addAntireaction(reactant1, reactant2,
                            reactant1[0] + str(random.randrange(numStates)),
                            reactant2[0] + str(random.randrange(numStates)))

    for atom in range(int(reactor.getSize()[0] * reactor.getSize()[1] / 15)):
        reactor.addAtom(Atom(random.randrange(numElements), random.randrange(numStates)),
                        (random.randrange(reactor.getSize()[0]), random.randrange(reactor.getSize()[1])))

def incrementState(reactor):
    validateAtomLocations(reactor.getCells())
    reactor.react()
    reactor.removeBadBonds()
    reactor.move()
    if sum([sum([0 if cell is None else 1 for cell in row]) for row in reactor.getCells()]) < reactor.getSize()[0] * reactor.getSize()[1] / 5:
        reactor.addAtom(Atom(random.randrange(numElements), random.randrange(numStates)),
                        (random.randrange(reactor.getSize()[0]), random.randrange(reactor.getSize()[1])))
    # if random.random() < 0.01:
    #     reactor.addAtom(Atom(2, 1), (random.randrange(reactor.getSize()[0]), random.randrange(reactor.getSize()[1])))
def drawState():
    screen.fill((0, 0, 0))
    state = reactor.getCells()
    for y, row in enumerate(state):
        for x, cell in enumerate(row):
            skipCell = False
            for borderingCell in [reactor.cellAt(x + dx, y + dy) for dx, dy in [(-1, 0), (0, -1), (0, 1), (1, 0)]]:
                if borderingCell is not None and borderingCell.getJustBonded() % 3 == 1:
                    pygame.draw.rect(screen, (255, 255, 255), getCellBoundingBox(x, y))
                    skipCell = True
            if cell is not None and not skipCell:
                if cell.getJustBonded() > 0:
                    cell.setJustBonded(cell.getJustBonded() - 1)
                    pygame.draw.rect(screen, (255, 255, 255), getCellBoundingBox(x, y))
                    continue

                try:
                    pygame.draw.rect(screen, stateColors[cell.getType()][cell.getState()], getCellBoundingBox(x, y))
                except Exception:
                    print("exception")

                # try:
                #     b = getCellBoundingBox(x, y)
                #     b = (b[0] + 1, b[1] + 1, b[2] - 2, b[3] - 2)
                #     pygame.draw.rect(screen, (0,0,0), b, 1)
                # except Exception:
                #     print("highlight exception")

def drawBonds():
    for y, row in enumerate(reactor.getCells()):
        for x, cell in enumerate(row):
            if cell is not None:
                for bond in cell.getBonds():
                    thisBox = getCellBoundingBox(x, y)
                    thisCenter = (thisBox[0] + thisBox[2] / 2, thisBox[1] + thisBox[3] / 2)
                    bondedBox = getCellBoundingBox(bond.getLocation()[0], bond.getLocation()[1])
                    bondedCenter = (bondedBox[0] + bondedBox[2] / 2, bondedBox[1] + bondedBox[3] / 2)
                    pygame.draw.line(screen, (150, 150, 150), thisCenter, bondedCenter, 2)

def getCellBoundingBox(x, y):
    return (
        (atomWidth + atomBorder) * x + reactorScreenLocation[0],
        (atomWidth + atomBorder) * y + reactorScreenLocation[1],
        (atomWidth + atomBorder * 2),
        (atomWidth + atomBorder * 2)
    )

def colorWheel(hue, numberOfSaturations):
    saturations = [1.0 * (n + 2) / (numberOfSaturations + 2) for n in range(numberOfSaturations + 2)]
    rgb = [colorsys.hsv_to_rgb(hue, saturation, 1) for saturation in saturations]
    return [(int(color[0] * 255), int(color[1] * 255), int(color[2] * 255)) for color in rgb]

def manhattanDist(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

stateColors = [colorWheel(1.0 * element / numElements, numStates) for element in range(numElements)]


# Loop until the user clicks close button
done = False
initiateReactor(reactor)
while done == False:
    # write event handlers here
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            reactor = Reactor((reactor.getSize()[0], reactor.getSize()[1]))
            initiateReactor(reactor)
    # write game logic here

    # clear the screen before drawing
    incrementState(reactor)
    drawState()
    drawBonds()
    # write draw code here

    pygame.display.update()
    # run at 20 fps
    #clock.tick(20)

# close the window and quit
pygame.quit()