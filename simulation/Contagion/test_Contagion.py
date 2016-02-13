import simulation.Contagion as Contagion
import simulation.Networks as Networks
import pytest


mockNodes = {1: {"spin": 1}, 2:{"spin": -1}, 3:{"spin": 0}, 4: {"spin": -1}}
mockNodes2 = {1: {"spin": 1}, 2:{"spin": 1}, 3:{"spin": -1}, 4: {"spin": -1}, 5: {"spin": 1}}
mockEdges = {1: [2], 2:[1,3], 3:[2, 4], 4:[3, 5], 5: [4]}
mockNetwork = Networks.Network(mockNodes, mockEdges)
mockNetwork2 = Networks.Network(mockNodes2, mockEdges)

def canBeInfected(conditions, node):
    return True

def tryToInfect(conditions, node):
    return node["spin"] != 0

def mockInfect(conditions, node):
    node["spin"] = 1

@pytest.fixture
def mockContagionSystem():
    return Contagion.Contagion(mockNetwork, canBeInfected, tryToInfect, mockInfect)

@pytest.fixture
def mockWolffSystem():
    return Contagion.WolffIsing(mockNetwork2)

def test_spread(mockContagionSystem):
    mockContagionSystem.spread({}, [], {}, 1)
    assert mockNodes[1]["spin"] == 1
    assert mockNodes[2]["spin"] == 1
    assert mockNodes[3]["spin"] == 0
    assert mockNodes[4]["spin"] == -1

def test_wolff_spread(mockWolffSystem):
    mockWolffSystem.aggrSpread({}, [], {'spin': -1}, 1)
    assert mockNodes2[1]["spin"] == -1
    assert mockNodes2[2]["spin"] == -1
    assert mockNodes2[3]["spin"] == -1
    assert mockNodes2[4]["spin"] == -1
    assert mockNodes2[5]["spin"] == 1
