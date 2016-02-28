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

class Lattice2D(Network):
    def __init__(self, numRows, numCols, nodes={}, edges={}):
        """Generate a 2D lattice"""
        self.numRows = numRows
        self.numCols = numCols
        self.nodes = nodes
        self.edges = edges
        self.numNodes = numRows * numCols
    
    def build(self, nodeGenerator):
        for j in range(self.numRows):
            for k in range(self.numCols):
                index = k + (self.numCols * j)
                self.addNode(index, nodeGenerator(j, k))
                self.attachHorizontalNeighbor(j, k)
                self.attachVerticalNeighbor(j, k)

class Lattice2DNP(Lattice2D):
    def attachHorizontalNeighbor(self, row, column): 
        if column != 0:
            index = column + (self.numCols * row)
            leftIndex = column + (self.numCols * row) - 1
            self.addEdge(leftIndex, index)
            self.addEdge(index, leftIndex)
    
    def attachVerticalNeighbor(self, row, column): 
        if row != 0:
            index = column + (self.numCols * row)
            topIndex = (column) + (self.numCols * (row - 1))
            self.addEdge(topIndex, index)
            self.addEdge(index, topIndex)

class BarabasiScaleFree(Network):
    def __init__(self, uniformRandomNumber, nodes={}, edges={}):
        """Generates the initial empty network to start generation of a scale-free
           network based on the Barabasi-Albert model
        """
        self.nodes = nodes
        self.edges = edges
        self.uniformRandomNumber = uniformRandomNumber
        self.numNodes = len(nodes.keys())
        self.numEdges = sum(len(edges[index]) for index in edges.keys())
    
    def attachProbability(self, index):
        """Barabasi-Albert growth rule for edge attachment probability based on the
           preferential attachment.
        """
        if index not in self.edges or (self.numEdges == 0):
            return .5
        return float(len(self.edges[index])) / self.numEdges

    def build(self, numNodes, nodeGenerator):
        """Generate a network with numNodes nodes using nodeGenerator, which takes
           a nodeId and should return a dictionary representing the node data.
        """
        for n in range(numNodes):
            self.edges[n] = []
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
                self.addEdge(n, i)
                self.numEdges += 1
