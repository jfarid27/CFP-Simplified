import simulation.CFP.Actor as Actor
import pytest

@pytest.fixture
def mockNoiseGenerator():
    return 0

def mockUniformGenerator():
    return 1

##Random pricing tests
@pytest.fixture
def mockRandomActor():
    assumptions = {'correctValue': 1, 'sensitivity': 1}
    random = Actor.Random(assumptions, mockNoiseGenerator, mockUniformGenerator)
    return random 

def test_random_pricing_one(mockRandomActor):
    data = {'currentPrice': 1}
    assert mockRandomActor.price(data) == 1

def test_random_pricing_two(mockRandomActor):
    data = {'currentPrice': 4}
    assert mockRandomActor.price(data) == 4

##Fundamentalist pricing tests
@pytest.fixture
def mockFundamentalistActor():
    assumptions = {'correctValue': 1, 'sensitivity': 1}
    fundamentalist = Actor.Fundamentalist(assumptions, mockNoiseGenerator, mockNoiseGenerator)
    return fundamentalist

def test_fundamentalist_pricing_one(mockFundamentalistActor):
    data = {'currentPrice': 1}
    assert mockFundamentalistActor.price(data) == 1

def test_fundamentalist_pricing_two(mockFundamentalistActor):
    data = {'currentPrice': 4}
    assert mockFundamentalistActor.price(data) == 1

##Chartist Pricing Tests
@pytest.fixture
def mockChartistActor():
    assumptions = {'sensitivity': 1, 'pastSteps': 1}
    chartist = Actor.Chartist(assumptions, mockNoiseGenerator, mockNoiseGenerator)
    return chartist 

def test_chartist_pricing_one(mockChartistActor):
    data = {'currentPrice': 1, 'aggregate': 1}
    assert mockChartistActor.price(data) == 1

def test_chartist_pricing_two(mockChartistActor):
    data = {'currentPrice': 4, 'aggregate': 10}
    assert mockChartistActor.price(data) == -2
