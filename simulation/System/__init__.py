class System():
    def __init__(self, prob, params):
        self.returnedProb = prob
        self.params = params
        return
    def prob(self):
        return self.returnedProb

class WolffIsing(System):
    """Wraps the Wolff Ising contagion network into a MCMC System.
       Assumes the contagion network already is set with a temperature.
    """
    def __init__(self, wolffIsing, randomIntGen):
        self.wolffIsing = wolffIsing
        self.randomIntGen = randomIntGen
        self.returnedProb = 0
    def genPossibleState(self):
        """This is a mock possible state since the Wolff program asserts direct
           sampling of a new state by spreading with the Wolff spread probability
        """
        return System(1, {})
    def transition(self, stateToTransitionTo):
        numNodes = self.wolffIsing.network.numRows + self.wolffIsing.network.numCols
        randomNodeId = self.randomIntGen(0, numNodes - 1)
        randomNode = self.wolffIsing.network.nodes[randomNodeId]
        conditions = {'spin': -randomNode['spin']}
        randomNode['spin'] *= -1
        neighbors = [x for x in self.wolffIsing.network.edges[randomNodeId]]
        alreadyChecked = {}
        alreadyChecked[randomNodeId] = True
        self.wolffIsing.spread(alreadyChecked, neighbors, \
            conditions, randomNodeId)
