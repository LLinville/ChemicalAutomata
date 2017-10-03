import random
class Reactor(object):

    def __init__(self, size):
        self.chanceToMove = 0.5
        self.sizeX = size[0]
        self.sizeY = size[1]
        self.cells = [[None for x in range(self.sizeX)] for y in range(self.sizeY)]
        self.reactions = {}
        self.antireactions = set({})

    def cellAt(self, x, y):
        return self.cells[y % self.sizeY][x % self.sizeX]

    def addReaction(self, reactant1, reactant2, reaction):
        self.reactions[getReactionKey(reactant1, reactant2)] = reaction
        self.reactions[getReactionKey(reactant2, reactant1)] = reaction.getMirroredReaction()

    def addAntireaction(self, key1, key2):
        self.antireactions.add(key1 + key2)

    def react(self):
        hasReacted = [[False for x in range(self.sizeX)] for y in range(self.sizeY)]
        for y, row in enumerate(self.cells):
            for x, cell in enumerate(row):
                potentialReactionLocation = self.reactWithRandomDirection(cell, x, y, hasReacted)
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
        for y, row in enumerate(self.cells):
            for x, cell in enumerate(row):

    def reactWithRandomDirection(self, thisCell, x, y, cellsToIgnore):
        directions = randomSearchOrder()
        if thisCell is None:
            return None
        for direction in directions:
            if cellsToIgnore[y + direction[1]][x + direction[0]]:
                continue

            potentialReactant = self.cellAt(x + direction[0], y + direction[1])
            if potentialReactant is None:
                continue

            reaction = self.reactions.get(thisCell.getReactionKey() + potentialReactant.getReactionKey())
            if reaction is not None:
                productStates = reaction.getProductStates()
                thisCell.setState(productStates[0])
                potentialReactant.setState(productStates[1])
                if reaction.shouldBond():
                    thisCell.bondWith(potentialReactant)
                    potentialReactant.bondWith(thisCell)
                return x + direction[0], y + direction[1]
        return None


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


def getReactionKey(self, reactant1, reactant2):
    return str(reactant1.getType()) + str(reactant1.getState()) + str(reactant2.getType()) + str(reactant2.getState())])