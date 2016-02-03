import Actor

class TestFundamentalistActorPrices():
    
    def __init__(self):
        assumptions = {correctValue: 1, sensitivity: 1}
        self.fundamentalist = Actor.Fundamentalist(assumptions, mockNoiseGenerator)
    
    def mockNoiseGenerator():
        return 0
    
    def test_fundamentalist_pricing_one(self):
        data = {currentPrice: 1}
        assert self.fundamentalist.price(data) == 1
    
    def test_fundamentalist_pricing_one(self):
        data = {currentPrice: 4}
        assert self.fundamentalist.price(data) == 1
