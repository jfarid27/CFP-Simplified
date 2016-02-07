class Network():
    def __init__(self, nodes={}, edges={}):
        """Initializes a new network using a dictionary of nodes and edges"""
        self.nodes = nodes
        self.edges = edges
    
    def addNode(self, index, node):
        """Takes a given node and index and add it to the network"""
        self.nodes[index] = node
    
    def addEdge(self, index, indexTo):
        """Takes a given node index/indexTo pair and adds it to the network"""
        if index in self.edges:
            self.edges[index].append(indexTo)
        else:
            self.edges[index] = [indexTo]

class BarabasiScaleFree(Network):
    def __init__(self, uniformRandomNumber, nodes={}, edges={}):
        self.nodes = nodes
        self.edges = edges
        self.uniformRandomNumber = uniformRandomNumber
        self.numNodes = 0
        self.numEdges = 0
    
    def attachProbability(self, index):
        if index not in self.edges or (self.numEdges == 0):
            return .5
        return float(len(self.edges[index])) / self.numEdges

    def build(self, numNodes, nodeGenerator):
        for n in range(numNodes):
            self.attachPreferentially(n) 
            self.addNode(n, nodeGenerator(n))
            self.numNodes += 1
    
    def attachPreferentially(self, i):
        """Preferentially attaches node with index i to nodes with index < i.
           Note this assumes i = self.numNodes + 1.
        """
        if (i == 0):
            return "No Change"
        for n in range(self.numNodes):
            if (self.uniformRandomNumber() <= self.attachProbability(n)):
                self.addEdge(i, n)
                self.numEdges += 1
