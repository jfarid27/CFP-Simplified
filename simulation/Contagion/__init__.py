class Contagion():
    def __init__(self, network, canBeInfected, tryToInfect, infect):
        self.network = network 
        self.canBeInfected = canBeInfected
        self.tryToInfect = tryToInfect 
        self.infect = infect
    
    def spread(self, alreadyChecked, nodesLeft, conditions, receiverId):
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
