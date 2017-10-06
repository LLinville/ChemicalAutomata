import random
class Reactor(object):

    def __init__(self, size):
        self.chanceToMove = 0.5
        self.sizeX = size[0]
        self.sizeY = size[1]
        self.cells = [[None for x in range(self.sizeX)] for y in range(self.sizeY)]
        self.reactions = {}
        self.antireactions = set({})

    def addAtom(self, atom, location):
        if manhattanDist(atom.getLocation(), location) > 5 and atom.getLocation()[0] != 0 and atom.getLocation()[1] != 0:
            print "Invalid move"
        atom.setLocation(location)
        self.cells[location[1]][location[0]] = atom

    def cellAt(self, x, y):
        return self.cells[y % self.sizeY][x % self.sizeX]

    def getCells(self):
        return self.cells

    def addReaction(self, reactant1, reactant2, reaction):
        self.reactions[getReactionKey(reactant1, reactant2)] = reaction
        self.reactions[getReactionKey(reactant2, reactant1)] = reaction.getMirroredReaction()

    def addAntireaction(self, key1, key2):
        self.antireactions.add(key1 + key2)

    def react(self):
        hasReacted = [[False for x in range(self.sizeX)] for y in range(self.sizeY)]
        directions = randomSearchOrder()
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
                for bondedAtom in cell.getBonds():
                    if cell.getReactionKey() + bondedAtom.getReactionKey() in self.antireactions:
                        #Break bond
                        cell.getBonds().remove(bondedAtom)
                        bondedAtom.getBonds().remove(cell)

    def move(self):
        newCells = [[None for x in range(self.sizeX)] for y in range(self.sizeY)]
        for y, row in enumerate(shuffled(self.cells)):
            for x, cell in enumerate(shuffled(row)):
                if cell is None:
                    continue

                directionOrder = randomSearchOrder5()
                potentialDestination = self.getPotentialDestination(cell, directionOrder, newCells)
                if potentialDestination is not None:
                    #potentialDestination = (potentialDestination[0] % self.sizeX, potentialDestination[1] % self.sizeY)
                    cell.setLocation(potentialDestination)
                    newCells[potentialDestination[1]][potentialDestination[0]] = cell
                    if manhattanDist(cell.getLocation(), potentialDestination) > 4:
                        print "Moving too far"
                else:
                    newCells[y][x] = cell


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

            if potentialReactant is thisCell:
                print("Bonded with self!")

            reaction = self.reactions.get(thisCell.getReactionKey() + potentialReactant.getReactionKey())
            if manhattanDist(thisCell.getLocation(), potentialReactant.getLocation()) > 5:
                print "reacting with something too far away!"

            if reaction is not None:
                productStates = reaction.getProductStates()
                thisCell.setState(productStates[0])
                potentialReactant.setState(productStates[1])
                if reaction.shouldBond():
                    thisCell.bondWith(potentialReactant)
                    potentialReactant.bondWith(thisCell)
                return x + direction[0], y + direction[1]
        return None

    def getPotentialDestination(self, cell, directionOrder, newCells):
        x, y = cell.getLocation()
        for direction in directionOrder:
            potentialNewLocation = (x + direction[0], y + direction[1])
            if not 0 <= potentialNewLocation[0] < self.sizeX or not 0 <= potentialNewLocation[1] < self.sizeY:
                continue
            if self.cellAt(potentialNewLocation[0], potentialNewLocation[1]) is None and \
                            newCells[potentialNewLocation[1]][potentialNewLocation[0]] is None and \
                    not wouldOverstretchBonds(cell, potentialNewLocation):
                return potentialNewLocation
        return None

largeOffsets = []
for dx in [-2, -1, 0, 1, 2]:
    for dy in [-2, -2, 0, 1, 2]:
        if dx != 0 and dy != 0:
            largeOffsets.append((dx, dy))


def wouldOverstretchBonds(cell, potentialNewLocation):
    for bondedAtom in cell.getBonds():
        if abs(bondedAtom.getLocation()[0] - potentialNewLocation[0]) > 2 or abs(
                        bondedAtom.getLocation()[1] - potentialNewLocation[1]) > 2:
            return True
    return False

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

def randomSearchOrder5():
    offsets = largeOffsets[:]
    random.shuffle(offsets)
    return offsets

def shuffled(input):
    output = input[:]
    random.shuffle(output)
    return output

def getReactionKey(reactant1, reactant2):
    return str(reactant1[0]) + str(reactant1[1]) + str(reactant2[0]) + str(reactant2[1])

def manhattanDist(point1, point2):
    if point1 is None or point2 is None:
        print "finding dist between Nones"
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])