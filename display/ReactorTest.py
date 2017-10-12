import pygame
import colorsys
import random
import networkx.drawing.nx_pylab as nx
import matplotlib.pyplot as plt
import pylab
pylab.ion()

# initialize game engine
from reactor.Atom import Atom
from reactor.Reaction import Reaction
from reactor.Reactor import Reactor, validateAtomLocations

pygame.init()
# initialize clock. used later in the loop.
clock = pygame.time.Clock()

atomWidth = 8
atomBorder = 0

reactorScreenLocation = (0, 0)

reactor = Reactor((50, 50))

# set screen width/height and caption
size = [reactor.getSize()[0] * (atomWidth + atomBorder),
        reactor.getSize()[1] * (atomWidth + atomBorder)]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Jittery Atoms")

startingAtoms = []

# reactor.addReaction("a1 b1", "a0b0")
# reactor.addReaction("b0 b1", "b2b0")
# reactor.addReaction("c1 b2", "c0 b3")
# reactor.addReaction("b3b2", "b2 b0")



#for a in range(10):
    #reactor.addAtom(Atom(0, 1), (random.randrange(reactor.getSize()[0]), random.randrange(reactor.getSize()[1])))
    #reactor.addAtom(Atom(random.randrange(numElements), random.randrange(numStates)), (random.randrange(10),random.randrange(10)))



# reactor.addAtom(Atom(0, 0), (5, 5))
# reactor.addAtom(Atom(0, 0), (7, 9))
# reactor.addAtom(Atom(0, 0), (9, 7))
# reactor.addAtom(Atom(0, 0), (9, 9))
def initiateReactorDuplicator(reactor):
    elementSequence = "cd"
    elementSequence = [ord(element) - ord("a") for element in elementSequence]

    # reactor.addReaction("a8 a0", "a4a3")
    # reactor.addReaction("x4y1", "x2y5")
    # reactor.addReaction("x5 x0", "x7x6")
    # reactor.addReaction("x3 y6", "x2y3")
    # reactor.addReaction("x7x3", "x4x3")
    # reactor.addReaction("x2y8", "x9y1")
    # reactor.addReaction("x9y9", "x8 y8")


    # reactor.addReaction("a1 a0", "a2a5")
    # reactor.addReaction("x2y1", "x2y2")
    # reactor.addReaction("x2 x0", "x3x4")
    # reactor.addReaction("x5 y4", "x6y7")
    # reactor.addReaction("x6x2", "x4x2")
    # reactor.addReaction("x7x4", "x")

    # 1 - ready to bond
    # 2 - just bonded
    # reactor.addReaction("x1 x5", "x2x2")
    # reactor.addReaction("a2a2", "a3a3")
    # reactor.addReaction("x3x6", "x3x3")
    # reactor.addReaction("x6x4", "x4x4")
    # reactor.addReaction("x3y4", "x0y0")
    # reactor.addReaction("x2 x2", "x6x6")
    # reactor.addReaction("x0y3", "x0y0")
    # reactor.addReaction("x0y4", "x0y0")
    # reactor.addReaction("x0x0", "x1 y1")
    # reactor.addReaction("e2e2", "e4e4")

    # reactor.addReaction("x1 x5", "x4x2")
    # reactor.addReaction("a3a3", "a6a6")
    # reactor.addReaction("x5x6", "x6x6")
    # reactor.addReaction("x5x7", "x7x7")
    # reactor.addReaction("x6x7", "x0y0")
    # reactor.addReaction("x2 x2", "x3x3")
    # reactor.addReaction("x2 y2", "x3y3")
    # reactor.addReaction("x2 y3", "x3x4")
    # for i in range(numStates):
    #     reactor.removeReaction("e" + str(i) + " e3")
    # reactor.addReaction("x3 y3", "x4x4")
    # reactor.addReaction("x0y5", "x0y0")
    # reactor.addReaction("x0y6", "x0y0")
    # reactor.addReaction("x0x0", "x1 y1")
    # reactor.addReaction("e4e4", "e7e7")
    #

    """
    0 - unpaired food
    1 - backbone ready to pair
    2 - paired but needs two neighbors
    3 - paired but needs one neighbor
    4 - paired and needs no neighbors
    5 - backbone paired
    6 - backbone done pairing
    7 - head unzip signal
    8 - unzipping from tail
    9 - unzipped waiting for head
    
    """
    reactor.addReaction("x1 x0", "x5x2")
    reactor.setReaction("a1 a0", Reaction(5, 3, True))
    reactor.setReaction("a0 a1", Reaction(3, 5, True))
    reactor.setReaction("b1 b0", Reaction(5, 3, True))
    reactor.setReaction("b0 b1", Reaction(3, 5, True))

    reactor.addReaction("x2 y2", "x3y3")
    reactor.addReaction("x2 y3", "x3y4")
    reactor.addReaction("x3 y3", "x4y4")
    reactor.addReaction("x5x4", "x6x4")

    reactor.addReaction("a6a4", "a7a4")

    reactor.addReaction("x7y6", "x7y7")
    reactor.addReaction("b7b4", "b8b4")
    reactor.addReaction("x8y7", "x8y8")
    reactor.addReaction("x8y4", "x8 y8")

    reactor.setReaction("a8a4", Reaction(1, 1, False))
    reactor.setReaction("a4a8", Reaction(1, 1, False))

    reactor.addReaction("x1y8", "x1y1")

    reactor.addReaction("a4b4", "a3 b3")


    numElements = 5
    reactor.setNumElements(numElements)
    numStates = 10
    reactor.setNumStates(numStates)


    # lastElement = "abcdefghijklmnopqrstuvw"[elementSequence[-1]]
    # reactor.addReaction(lastElement + "4" + lastElement + "3", lastElement + "8 " + lastElement + "8")

    # for i in range(10):
    #     reactor.addReaction("x10 y" + str(i), "x10y10")
    #     reactor.addReaction("x10y" + str(i), "x10y10")
    # reactor.addReaction("x10x10", "x0 x0")

    print("-" * 20)

    atoms = [Atom(0, 1)]
    for element in elementSequence:
        atoms.append(Atom(element, 1))
    atoms.append(Atom(1, 1))

    for i, atom in enumerate(atoms):
        reactor.addAtom(atom, (reactor.getSize()[0] // 2, reactor.getSize()[1] // 2 + 2 * i))
    for i in range(len(atoms) - 1):
        atoms[i].bondWith(atoms[i+1])
        reactor.getBondGraph().add_edge(atoms[i].getId(), atoms[i+1].getId())

    for atom in range(300):
        reactor.addAtom(Atom(random.randrange(reactor.getNumElements()), 0), (random.randrange(reactor.getSize()[0]), random.randrange(reactor.getSize()[1])))

def initiateReactor(reactor):
    initiateReactorDuplicator(reactor)

def incrementState(reactor):
    #validateAtomLocations(reactor.getCells())
    reactor.react()
    reactor.move()
    if random.random() < 0:
        return
    if sum([sum([0 if cell is None else 1 for cell in row]) for row in reactor.getCells()]) < reactor.getSize()[0] * reactor.getSize()[1] / 3:
        # reactor.addAtom(Atom(random.randrange(numElements), random.randrange(numStates)),
        #                 (random.randrange(reactor.getSize()[0]), random.randrange(reactor.getSize()[1])))
        reactor.addAtom(Atom(random.randrange(reactor.getNumElements()), 0),
                        (random.randrange(reactor.getSize()[0]), random.randrange(reactor.getSize()[1])))
    if random.random() < 0:
        reactor.addAtom(Atom(2, 5), (random.randrange(reactor.getSize()[0]), random.randrange(reactor.getSize()[1])))
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
                    if len(cell.getBonds()) == 0:
                        color = stateColors[cell.getType()][cell.getState()]
                        pygame.draw.rect(screen, (color[0]//3, color[1]//3, color[2]//3), getCellBoundingBox(x, y))
                    else:
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
    saturations = [1.0 * (n + 1) / (numberOfSaturations + 1) for n in range(numberOfSaturations + 1)]
    rgb = [colorsys.hsv_to_rgb(hue, saturation, 1) for saturation in saturations]
    return [(int(color[0] * 255), int(color[1] * 255), int(color[2] * 255)) for color in rgb[1:]]

def manhattanDist(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])



# Loop until the user clicks close button
done = False
initiateReactor(reactor)
stateColors = [colorWheel(1.0 * element / reactor.getNumElements(), reactor.getNumStates()) for element in range(reactor.getNumElements())]
stateColors01 = [[tuple([component / 255.0 for component in elementColor]) for elementColor in elementColors] for elementColors in stateColors]
pylab.show()
pylab.figure(figsize=(1, 1))
while not done:
    # write event handlers here
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            reactor = Reactor((reactor.getSize()[0], reactor.getSize()[1]))
            initiateReactor(reactor)
    keysdown = pygame.key.get_pressed()

    if not keysdown[pygame.K_SPACE]:
        incrementState(reactor)
        pylab.clf()
        nodeDegrees = reactor.getBondGraph().degree()
        nodeColors = [stateColors01[cell.getType()][cell.getState()] + (1,) for cell in reactor.atomsById]
        nodesToDraw = [nodeIndex for nodeIndex in nodeDegrees if nodeDegrees[nodeIndex] > 0]
        nx.draw_networkx(
            reactor.getBondGraph(),
            nodelist=nodesToDraw,
            labels=dict((atom.getId(), atom.getReactionKey()) for atom in reactor.getAtomsById() if atom.getId() in nodesToDraw),
            node_size=10,
            node_color=nodeColors)
        pylab.draw()
        #drawState()
        #drawBonds()

    pygame.display.update()
    # run at 20 fps
    #clock.tick(20)

# close the window and quit
pygame.quit()