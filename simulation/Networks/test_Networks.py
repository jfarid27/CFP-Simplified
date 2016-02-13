import simulation.Networks as Networks
import pytest

mockUniformRandomNumber = lambda: 1

def newNodes():
    return {0: {"name": "foo"}, 1:{"name": "bar"}}

def newEdges():
    return {0: [1]}

@pytest.fixture(scope="function")
def mockNewNetwork():
    return Networks.Network(newNodes(), newEdges())

@pytest.fixture(scope="function")
def mockBarabasi():
    return Networks.BarabasiScaleFree(uniformRandomNumber=mockUniformRandomNumber)

@pytest.fixture(scope="function")
def mockLattice2DNP():
    return Networks.Lattice2DNP(2, 2)

##Instantiation Test
class TestNetwork():
    def test_network(self, mockNewNetwork):
        assert mockNewNetwork.nodes[0]["name"] == "foo"
        assert mockNewNetwork.nodes[1]["name"] == "bar"

    def test_addNode(self, mockNewNetwork):
        mockNewNetwork.addNode(2, {"name": "zed"})
        assert mockNewNetwork.nodes[2]["name"] == "zed"

    def test_addEdges(self, mockNewNetwork):
        mockNewNetwork.addNode(2, {"name": "zed"})
        mockNewNetwork.addEdge(2, 0)
        mockNewNetwork.addEdge(2, 1)
        assert 0 in mockNewNetwork.edges[2]
        assert 1 in mockNewNetwork.edges[2]

class TestLattice2DNP():
    def test_smallInstance(self, mockLattice2DNP):
        mockLattice2DNP.build(lambda x,y: {})
        #0
        assert 1 in mockLattice2DNP.edges[0]
        assert 2 in mockLattice2DNP.edges[0]
        assert len(mockLattice2DNP.edges[0]) == 2
        #1
        assert 0 in mockLattice2DNP.edges[1]
        assert 3 in mockLattice2DNP.edges[1]
        assert len(mockLattice2DNP.edges[1]) == 2
        #2
        assert 0 in mockLattice2DNP.edges[2]
        assert 3 in mockLattice2DNP.edges[2]
        assert len(mockLattice2DNP.edges[2]) == 2
        #3
        assert 1 in mockLattice2DNP.edges[3]
        assert 2 in mockLattice2DNP.edges[3]
        assert len(mockLattice2DNP.edges[3]) == 2

##Barabasi Network Tests
class TestBarabasi():
    def test_build(self, mockBarabasi):
        mockBarabasi.build(4, lambda n: {})
        assert len(list(mockBarabasi.nodes.keys())) == 4

    def test_attachProbabilityZero(self, mockBarabasi):
        """This is a test for when a node is selected with no edges
        """
        assert (mockBarabasi.attachProbability(0) - .5) < .01

    def test_attachProbability(self, mockBarabasi):
        mockBarabasi.numEdges = 4
        mockBarabasi.addEdge(1, 5)
        mockBarabasi.addEdge(1, 3)
        assert (mockBarabasi.attachProbability(1) - .5) < .01

    def test_preferentialAttachmentZero(self, mockBarabasi):
        assert mockBarabasi.attachPreferentially(0) == "No Change"

    def test_preferentialAttachmentNotZero(self, mockBarabasi):
        mockBarabasi.attachProbability = lambda x: 1
        mockBarabasi.attachPreferentially(2)
        assert 2 in mockBarabasi.edges[0] 
        assert 2 in mockBarabasi.edges[1] 
        assert 0 in mockBarabasi.edges[2] 
        assert 1 in mockBarabasi.edges[2] 
