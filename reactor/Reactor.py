import random
from reactor.Reaction import Reaction

class Reactor(object):

    def __init__(self, size):
        self.chanceToMove = 0.5
        self.sizeX = size[0]
        self.sizeY = size[1]
        self.cells = [[None for x in range(self.sizeX)] for y in range(self.sizeY)]
        self.reactions = {}
        self.antireactions = {}

        self.maxReactionDistance = 5
        self.maxBondLength = 5
        self.maxMoveDistance = 2
        self.maxBonds = 3

    def getSize(self):
        return self.sizeX, self.sizeY

    def addAtom(self, atom, location):
        if self.cellAt(location[0], location[1]) is None:
            atom.setLocation(location)
            self.cells[location[1]][location[0]] = atom

    def cellAt(self, x, y):
        if x < 0 or x >= self.sizeX or y < 0 or y >= self.sizeY:
            return None
        return self.cells[y][x]

    def getCells(self):
        return self.cells

    def addReaction(self, reactant1, reactant2, reaction):
        print(reactant1, reactant2, " -> ", reaction)
        shouldBond = reaction[2] == "X"
        self.reactions[reactant1 + reactant2] = Reaction(int(reaction[1]), int(reaction[4]), shouldBond)
        self.reactions[reactant2 + reactant1] = Reaction(int(reaction[4]), int(reaction[1]), shouldBond)


    def addAntireaction(self, key1, key2, product1, product2):
        print(key1 + " X " + key2)
        self.antireactions[key1 + key2] = product1 + product2
        self.antireactions[key2 + key1] = product2 + product1

    def react(self):
        hasReacted = [[False for x in range(self.sizeX)] for y in range(self.sizeY)]
        directions = getOffsetsForDist(self.maxReactionDistance)
        #directions = shuffled([(-1, 0), (1, 0), (0, -1), (0, 1)])
        for y, row in enumerate(self.cells):
            for x, cell in enumerate(row):
                potentialReactionLocation = self.reactWithRandomDirection(cell, x, y, hasReacted, directions)
                if potentialReactionLocation is not None:
                    hasReacted[y][x] = True
                    hasReacted[potentialReactionLocation[1]][potentialReactionLocation[0]] = True

    def removeBadBonds(self):
        for y, row in enumerate(self.cells):
            for x, cell in enumerate(row):
                if cell is None:
                    continue
                for bondedAtom in list(cell.getBonds()):
                    product = cell.getReactionKey() + bondedAtom.getReactionKey()
                    if product in self.antireactions.keys():
                        #Break bond
                        cell.getBonds().remove(bondedAtom)
                        cell.setState(int(self.antireactions[product][1]))
                        bondedAtom.getBonds().remove(cell)
                        bondedAtom.setState(int(self.antireactions[product][3]))
        validateAtomLocations(self.cells)

    def move(self):
        newCells = [[None for x in range(self.sizeX)] for y in range(self.sizeY)]
        for y in shuffled(list(range(self.sizeY))):
            row = self.cells[y]
            for x in shuffled(list(range(self.sizeX))):
                cell = row[x]
                if cell is None:
                    continue
                #validateAtomLocations(newCells)

                directionOrder = shuffled(getOffsetsForDist(2))

                potentialDestination = self.getPotentialDestination(cell, directionOrder, newCells)
                if potentialDestination is not None:
                    #potentialDestination = (potentialDestination[0] % self.sizeX, potentialDestination[1] % self.sizeY)
                    cell.setLocation(potentialDestination)
                    newCells[potentialDestination[1]][potentialDestination[0]] = cell
                else:
                    newCells[y][x] = cell
                #validateAtomLocations(newCells)


        validateAtomLocations(newCells)
        self.cells = newCells

    def reactWithRandomDirection(self, thisCell, x, y, cellsToIgnore, directions):
        if thisCell is None:
            return None
        for direction in directions:
            potentialLocation = (x + direction[0], y + direction[1])
            if not 0 <= potentialLocation[0] < self.sizeX or not 0 <= potentialLocation[1] < self.sizeY:
                continue

            if cellsToIgnore[potentialLocation[1]][potentialLocation[0]]:
                continue

            potentialReactant = self.cellAt(potentialLocation[0], potentialLocation[1])

            if potentialReactant is None:
                continue

            if potentialReactant in thisCell.getBonds():
                continue

            if potentialReactant is thisCell:
                print("Bonded with self!")

            if manhattanDist(thisCell.getLocation(), potentialReactant.getLocation()) > self.maxReactionDistance:
                print("reacting with something too far away!")
                continue

            reaction = self.reactions.get(thisCell.getReactionKey() + potentialReactant.getReactionKey())

            if reaction is not None:
                productStates = reaction.getProductStates()
                thisCell.setState(productStates[0])
                potentialReactant.setState(productStates[1])
                if reaction.shouldBond() and len(thisCell.getBonds()) <= self.maxBonds and len(potentialReactant.getBonds()) <= self.maxBonds:
                    thisCell.bondWith(potentialReactant)
                    potentialReactant.bondWith(thisCell)
                return potentialLocation
        return None

    def getPotentialDestination(self, cell, directionOrder, newCells):
        x, y = cell.getLocation()
        for direction in directionOrder:
            potentialNewLocation = (x + direction[0], y + direction[1])
            if not(0 <= potentialNewLocation[0] < self.sizeX and 0 <= potentialNewLocation[1] < self.sizeY):
                continue
            if self.cellAt(potentialNewLocation[0], potentialNewLocation[1]) is None and \
                            newCells[potentialNewLocation[1]][potentialNewLocation[0]] is None and \
                    not self.wouldOverstretchBonds(cell, potentialNewLocation):
                return potentialNewLocation
        return None

    def wouldOverstretchBonds(self, cell, potentialNewLocation):
        for bondedAtom in cell.getBonds():
            if potentialNewLocation in randomSearchOrder():
                continue
            if manhattanDist(bondedAtom.getLocation(), potentialNewLocation) > self.maxBondLength:
                return True
        return False

    def manhattanDist(self, point1, point2):
        if point1 is None or point2 is None:
            print("finding dist between Nones")
        return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

    def randomSearchOrder(self):
        directions = [(-1, -1),
                      (-1, 0),
                      (-1, 1),
                      (0, -1),
                      (0, 1),
                      (1, -1),
                      (1, 0),
                      (1, 1)]
        random.shuffle(directions)
        return directions

def manhattanDist(point1, point2):
    if point1 is None or point2 is None:
        print("finding dist between Nones")
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])


def randomSearchOrder():
    directions = [(-1, -1),
                   (-1, 0),
                   (-1, 1),
                   (0, -1),
                   (0, 1),
                   (1, -1),
                   (1, 0),
                   (1, 1)]
    random.shuffle(directions)
    return directions

def getOffsetsForDist(dist):
    largeOffsets = []
    for dx in range(-dist + 1, dist):
        for dy in range(-dist + 1, dist):
            if (dx, dy) not in [(0, 0)] and manhattanDist((0, 0), (dx, dy)) <= dist:
                largeOffsets.append((dx, dy))
    return largeOffsets

def randomSearchOrder5():
    offsets = getOffsetsForDist(2)
    random.shuffle(offsets)
    return offsets

def shuffled(input):
    output = input[:]
    random.shuffle(output)
    return output

def getReactionKey(reactant1, reactant2):
    return "abcdefghijklmnopqrstuvwxyz"[reactant1[0]] + str(reactant1[1]) + "abcdefghijklmnopqrstuvwxyz"[reactant2[0]] + str(reactant2[1])

def validateAtomLocations(cells):
    for y, row in enumerate(cells):
        for x, cell in enumerate(row):
            if cell is None:
                continue
            if cell.getLocation()[0] != x or cell.getLocation()[1] != y:
                print("locations don't match")
            for boundAtom in cell.getBonds():
                if cells[boundAtom.getLocation()[1]][boundAtom.getLocation()[0]] is not boundAtom:
                    print("Bound to the wrong place")