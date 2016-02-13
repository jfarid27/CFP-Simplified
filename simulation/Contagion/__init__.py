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
       all matching neighbors spins automatically. This class is meant to be used with the
       aggrSpread when a node is selected to be flipped.
    """
    def __init__(self, network):
        self.network = network
    
    def infect(self, conditions, receiver):
        receiver['spin'] = conditions['spin']
    
    def canBeInfected(self, conditions, receiver):
        return receiver['spin'] != conditions['spin']
