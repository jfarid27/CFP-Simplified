import simulation.Contagion as Contagion
import simulation.Networks as Networks
import pytest


mockNodes = {1: {"spin": 1}, 2:{"spin": -1}, 3:{"spin": 0}, 4: {"spin": -1}}
mockEdges = {1: [2], 2:[1,3], 3:[2, 4], 4:[3]}
mockNetwork = Networks.Network(mockNodes, mockEdges)

def canBeInfected(conditions, node):
    return True

def tryToInfect(conditions, node):
    return node["spin"] != 0

def mockInfect(conditions, node):
    node["spin"] = 1

@pytest.fixture
def mockContagionSystem():
    return Contagion.Contagion(mockNetwork, canBeInfected, tryToInfect, mockInfect)

def test_proper_spread(mockContagionSystem):
    mockContagionSystem.spread({}, [], {}, 1)
    assert mockNodes[1]["spin"] == 1
    assert mockNodes[2]["spin"] == 1
    assert mockNodes[3]["spin"] == 0
    assert mockNodes[4]["spin"] == -1
