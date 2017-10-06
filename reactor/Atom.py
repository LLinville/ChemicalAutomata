class Atom(object):
    def __init__(self, type, state, location=(0, 0)):
        self.type = type
        self.state = state
        self.location = location
        self.bonds = set({})
        self.pastLocations = [location]

    def getLocation(self):
        return self.location

    def setLocation(self, location):
        if manhattanDist(self.getLocation(), location) > 5 and self.getLocation()[0] != 0 and self.getLocation()[1] != 0:
            print "Invalid move"
        self.pastLocations.append(location)
        self.location = location

    def getType(self):
        return self.type

    def setType(self, type):
        self.type = type

    def getState(self):
        return self.state

    def setState(self, state):
        self.state = state

    def getReactionKey(self):
        return str(self.type) + str(self.state)

    def getBonds(self):
        return self.bonds

    def bondWith(self, atom):
        self.bonds.add(atom)

def manhattanDist(point1, point2):
    if point1 is None or point2 is None:
        print "finding dist between Nones"
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])