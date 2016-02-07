import simulation.Networks as Networks
import pytest

mockNodes = {1: {"name": "foo"}, 2:{"name": "bar"}}
mockEdges = {1: [2]}
mockUniformRandomNumber = lambda: 1

@pytest.fixture
def mockNewNetwork():
    return Networks.Network(mockNodes, mockEdges)

@pytest.fixture
def mockBarabasi():
    return Networks.BarabasiScaleFree(uniformRandomNumber=mockUniformRandomNumber)


##Instantiation Test
def test_network(mockNewNetwork):
    assert mockNewNetwork.nodes[1]["name"] == "foo"
    assert mockNewNetwork.nodes[2]["name"] == "bar"

def test_addNode(mockNewNetwork):
    mockNewNetwork.addNode(3, {"name": "zed"})
    assert mockNewNetwork.nodes[3]["name"] == "zed"

def test_addEdges(mockNewNetwork):
    mockNewNetwork.addNode(3, {"name": "zed"})
    mockNewNetwork.addEdge(3, 1)
    mockNewNetwork.addEdge(3, 2)
    assert 1 in mockNewNetwork.edges[3]
    assert 2 in mockNewNetwork.edges[3]

##Barabasi Network Tests
def test_build(mockBarabasi):
    mockBarabasi.build(4, lambda n: {})
    assert len(list(mockBarabasi.nodes.keys())) == 4

def test_attachProbabilityZero(mockBarabasi):
    """This is a test for when a node is selected with no edges
    """
    assert (mockBarabasi.attachProbability(0) - .5) < .01

def test_attachProbability(mockBarabasi):
    mockBarabasi.numEdges = 4
    mockBarabasi.addEdge(2, 5)
    mockBarabasi.addEdge(2, 3)
    assert (mockBarabasi.attachProbability(2) - .5) < .01

def test_preferentialAttachmentZero(mockBarabasi):
    assert mockBarabasi.attachPreferentially(0) == "No Change"

def test_preferentialAttachmentNotZero(mockBarabasi):
    mockBarabasi.attachProbability = lambda x: 1
    mockBarabasi.numNodes = 1
    mockBarabasi.attachPreferentially(1)
    assert mockBarabasi.numEdges == 1
    assert 0 in mockBarabasi.edges[1]
