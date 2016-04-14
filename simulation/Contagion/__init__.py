from math import exp

class Contagion():
    def __init__(self, network, canBeInfected, tryToInfect, infect):
        self.network = network
        self.canBeInfected = canBeInfected
        self.tryToInfect = tryToInfect
        self.infect = infect

    def aggrSpread(self, alreadyChecked, nodesLeft, conditions, receiverId):
        """Automatically infects neighbors if receiver is infected"""
        if receiverId not in alreadyChecked:
            alreadyChecked[receiverId] = True
            receiver = self.network.nodes[receiverId]
            self.infect(conditions, receiver)
            for neighbor in self.network.edges[receiverId]:
                if self.canBeInfected(conditions, self.network.nodes[neighbor]):
                    if neighbor not in alreadyChecked:
                        nodesLeft.append(neighbor)
        if len(nodesLeft) < 1:
            return
        else:
            nextNode = nodesLeft.pop()
            return self.aggrSpread(alreadyChecked, nodesLeft, conditions, nextNode)

    def spread(self, alreadyChecked, nodesLeft, conditions, receiverId):
        """Infects neighbors using tryToInfect. Does not auto infect"""
        if receiverId not in alreadyChecked:
            receiver = self.network.nodes[receiverId]
            if self.tryToInfect(conditions, receiver):
                self.infect(conditions, receiver)
                for neighbor in self.network.edges[receiverId]:
                    if neighbor not in alreadyChecked:
                        if self.canBeInfected(conditions, self.network.nodes[neighbor]):
                            nodesLeft.append(neighbor)
            alreadyChecked[receiverId] = True
        if len(nodesLeft) < 1:
            return
        else:
            nextNode = nodesLeft.pop()
            return self.spread(alreadyChecked, nodesLeft, conditions, nextNode)

class WolffIsing(Contagion):
    """Used to create an infection model that matches the Wolff Ising program, flipping
       all matching neighbors spins using Wolff spread probability."""
    def __init__(self, network, beta, randomNumGen):
        self.beta = beta
        self.network = network
        self.randomNumGen = randomNumGen

    def infect(self, conditions, receiver):
        receiver['spin'] = conditions['spin']

    def canBeInfected(self, conditions, receiver):
        return receiver['spin'] != conditions['spin']

    def tryToInfect(self, transmitter, receiver):
        """Uses Wolff spread probability to transmit infection"""
        wolfSpreadProbability = 1 - exp( - 2 * self.beta)
        return self.randomNumGen() < wolfSpreadProbability

class WolffIsingCFP(WolffIsing):
    """A Wolff Ising spread model that also has a price"""
    def infect(self, conditions, receiver):
        receiver['spin'] = conditions['spin']
        receiver['price'] = conditions['price']
