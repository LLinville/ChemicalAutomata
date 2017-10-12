import random
from reactor.Reaction import Reaction

import networkx as nx

class Reactor(object):

    def __init__(self, size):
        self.chanceToMove = 0.5
        self.sizeX = size[0]
        self.sizeY = size[1]
        self.cells = [[None for x in range(self.sizeX)] for y in range(self.sizeY)]
        self.reactions = {}

        self.maxReactionDistance = 4
        self.maxBondLength = 4
        self.maxMoveDistance = 1
        self.maxBonds = 40

        self.numElements = 0
        self.numStates = 0

        self.nextAtomId = 0

        self.bondGraph = nx.Graph()
        self.atomsById = []

    def newAtomId(self):
        self.nextAtomId += 1
        return self.nextAtomId - 1

    def getAtomsById(self):
        return self.atomsById

    def getBondGraph(self):
        return self.bondGraph

    def getReactions(self):
        return self.reactions

    def getNumElements(self):
        return self.numElements
    
    def setNumElements(self, numElements):
        self.numElements = numElements

    def getNumStates(self):
        return self.numStates

    def setNumStates(self, numStates):
        self.numStates = numStates

    def getSize(self):
        return self.sizeX, self.sizeY

    def addAtom(self, atom, location):
        if self.cellAt(location[0], location[1]) is None:
            atom.setLocation(location)
            atom.setId(self.newAtomId())
            self.atomsById.append(atom)
            self.bondGraph.add_node(atom.getId())

            self.cells[location[1]][location[0]] = atom

    def cellAt(self, x, y):
        if x < 0 or x >= self.sizeX or y < 0 or y >= self.sizeY:
            return None
        return self.cells[y][x]

    def getCells(self):
        return self.cells

    def addReaction(self, reactants, products):
        wasBonded = reactants[2] is not " "
        shouldBond = products[2] is not " "
        for startState, endState in self.parseReaction(reactants, products):
            self.reactions[startState] = Reaction(endState[1], endState[-1], shouldBond)
            self.reactions[startState[-2:] + ("" if wasBonded else " ") + startState[:2]] = self.reactions[startState].getMirroredReaction()
            print(startState + " -> " + endState)
        print("-" * 20)

    def setReaction(self, reactants, reaction):
        self.reactions[reactants] = reaction

    def removeReaction(self, reactants):
        self.reactions.pop(reactants)

    def parseReaction(self, reactants, products):
        reactantAndProductOptions = []
        reactant1 = reactants[:2]
        reactant2 = reactants[-2:]
        wasBonded = reactants[2] is not " "

        product1 = products[:2]
        product2 = products[-2:]
        shouldBond = products[2] is not " "

        elementOptions = [element for element in "abcdefghijklmnopqrstuvwxyz"[:self.numElements]]
        validElements = []

        if reactant1[0] == "x":
            for element in elementOptions:
                validElements.append(element)
        else:
            validElements.append(reactant1[0])

        validElementPairs = []
        if reactant2[0] == "x":
            validElementPairs = [(element, element) for element in validElements]
        elif reactant2[0] == "y":
            validElementPairs = [(element1, element2) for element1 in validElements for element2 in validElements]
        elif reactant2[0] == "z":
            validElementPairs = [(element1, element2) for element1 in validElements for element2 in filter(lambda x: x is not element1, validElements)]
        else:
            validElementPairs = [(reactant1[0], reactant2[0])]

        for elementPair in validElementPairs:
            reactantAndProductOptions.append((elementPair[0] + reactant1[1] + ("" if wasBonded else " ") + elementPair[1] + reactant2[1],
                                              elementPair[0] + product1[1] + ("" if shouldBond else " ") + elementPair[1] + product2[1]))

        return reactantAndProductOptions

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

    # def removeBadBonds(self):
    #     for y, row in enumerate(self.cells):
    #         for x, cell in enumerate(row):
    #             if cell is None:
    #                 continue
    #             for bondedAtom in list(cell.getBonds()):
    #                 product = cell.getReactionKey() + bondedAtom.getReactionKey()
    #                 if product in self.antireactions.keys():
    #                     #Break bond
    #                     cell.getBonds().remove(bondedAtom)
    #                     cell.setState(int(self.antireactions[product][1]))
    #                     bondedAtom.getBonds().remove(cell)
    #                     bondedAtom.setState(int(self.antireactions[product][3]))
    #     validateAtomLocations(self.cells)

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

            # if potentialReactant in thisCell.getBonds():
            #     continue

            if potentialReactant is thisCell:
                print("Bonded with self!")

            if manhattanDist(thisCell.getLocation(), potentialReactant.getLocation()) > self.maxReactionDistance:
                print("reacting with something too far away!")
                continue

            if potentialReactant in thisCell.getBonds():
                reactionKey = thisCell.getReactionKey() + potentialReactant.getReactionKey()
            else:
                reactionKey = thisCell.getReactionKey() + " " + potentialReactant.getReactionKey()

            reaction = self.reactions.get(reactionKey)

            if reaction is not None:
                productStates = reaction.getProductStates()
                print(reactionKey + " -> " +
                      reactionKey[0] + str(productStates[0]) +
                      ("" if reaction.shouldBond() else " ") +
                      reactionKey[-2] + str(productStates[1]))

                thisCell.setState(int(productStates[0]))
                potentialReactant.setState(int(productStates[1]))

                if reaction.shouldBond() and \
                        not potentialReactant in thisCell.getBonds() and \
                        len(thisCell.getBonds()) <= self.maxBonds and \
                        len(potentialReactant.getBonds()) <= self.maxBonds:

                    thisCell.bondWith(potentialReactant)
                    self.bondGraph.add_edge(thisCell.getId(), potentialReactant.getId())
                elif not reaction.shouldBond() and potentialReactant in thisCell.getBonds():
                    thisCell.getBonds().remove(potentialReactant)
                    potentialReactant.getBonds().remove(thisCell)
                    self.bondGraph.remove_edge(thisCell.getId(), potentialReactant.getId())

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

    def printReactions(self):
        reactionStrings = []
        for start in self.reactions.keys():
            products = self.reactions[start].getProductStates()
            end = start[0] + products[0] + ("" if self.reactions[start].shouldBond() else " ") + start[-2] + products[1]
            reactionStrings.append((start + " -> " + end))
        print("\n".join(sorted(reactionStrings)))

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