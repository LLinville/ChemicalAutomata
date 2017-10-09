class Reaction(object):

    def __init__(self, state1, state2, bond):
        self.product1State = state1
        self.product2State = state2
        self.bond = bond

    def getMirroredReaction(self):
        return Reaction(self.product2State, self.product1State, self.bond)

    def getProductStates(self):
        return self.product1State, self.product2State

    def shouldBond(self):
        return self.bond

    def toString(self):
        return self.product1State, self.product2State