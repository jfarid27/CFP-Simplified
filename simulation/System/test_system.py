import simulation.System as System
import simulation.Networks as Network
import simulation.Contagion as Contagion
import pytest

def nodeGenerator(rowIndex, colIndex):
    x = {'spin': 0}
    if rowIndex == 0:
        x['spin'] = 1
    else:
        x['spin'] = -1
    return x

def mockRandomIntGen(x, y):
    return 0

def mockRandomNumGen():
    return 0

@pytest.fixture(scope="function")
def mockIsingNetwork():
    mockNetwork = Network.Lattice2DNP(2, 2)
    mockNetwork.build(nodeGenerator)
    mockContagion = Contagion.WolffIsing(mockNetwork, 1, mockRandomNumGen)
    return System.WolffIsing(mockContagion, mockRandomIntGen)

class TestWolffIsing():
    def test_genPossibleState(self, mockIsingNetwork):
        s = mockIsingNetwork.genPossibleState()
        assert s.prob() == 1

    def test_transition(self, mockIsingNetwork):
        mockIsingNetwork.transition({})
        assert mockIsingNetwork.wolffIsing.network.nodes[0]['spin'] == -1
        assert mockIsingNetwork.wolffIsing.network.nodes[1]['spin'] == -1
        assert mockIsingNetwork.wolffIsing.network.nodes[2]['spin'] == -1
        assert mockIsingNetwork.wolffIsing.network.nodes[3]['spin'] == -1
