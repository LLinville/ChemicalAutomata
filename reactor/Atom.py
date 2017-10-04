class Atom(object):
    def __init__(self, type, state, location):
        self.type = type
        self.state = state
        self.location = location
        self.bonds = set({})

    def getLocation(self):
        return self.location

    def getType(self):
        return self.type

    def setType(self, type):
        self.type = type

    def getState(self):
        return self.state

    def setType(self, type):
        self.type = type

    def getReactionKey(self):
        return str(self.type) + str(self.state)

    def getBonds(self):
        return self.bonds

    def bondWith(self, atom):
        self.bonds.add(atom)

