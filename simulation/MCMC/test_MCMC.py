import simulation.MCMC as MCMC
import pytest

def mockRandomGen():
    return float(3/4)

def mockObservable(system, observations):
    if (system.transitioned):
        observations['count'] += 1

class MockPossibleSystem():
    def __init__(self):
        return
    def prob(self):
        return 2

class MockSystem():
    def __init__(self):
        self.transitioned = False
    def genPossibleState(self):
        return MockPossibleSystem() 
    def prob(self):
        return 1
    def transition(self, transitionTo):
        self.transitioned = True

@pytest.fixture
def mockSimulation():
    mockSystem = MockSystem()
    return MCMC.MCMC(mockSystem, mockRandomGen)

def test_metropolis_1(mockSimulation):
    """This is the probB > probA branch"""
    assert mockSimulation.metropolis(1, 2) == True
    
def test_metropolis_2(mockSimulation):
    """Test for probA > probB"""
    assert mockSimulation.metropolis(4, 2) == False

def test_simulation(mockSimulation):
    observations = {'count': 1}
    mockSimulation.simulate(mockObservable, observations, 1)
    assert observations['count'] == 2
