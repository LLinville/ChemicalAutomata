class Atom(object):
    def __init__(self, type, state, location=(0, 0)):
        self.type = type
        self.state = state
        self.location = location
        self.bonds = set({})

    def getLocation(self):
        return self.location

    def setLocation(self, location):
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

