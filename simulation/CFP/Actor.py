class Actor():
    def __init__(self, assumptions, noiseGenerator, uniformNoiseGenerator):
        self.assumptions = assumptions
        self.noiseGenerator = noiseGenerator
        self.uniformNoiseGenerator = uniformNoiseGenerator

class Fundamentalist(Actor):
    def price(self, data):
        return data['currentPrice'] + \
            (self.assumptions['sensitivity'] * (self.assumptions['correctValue'] - data['currentPrice'])) + \
                self.noiseGenerator()

class Chartist(Actor):
    def price(self, data):
        average = data['aggregate'] / self.assumptions['pastSteps']
        return data['currentPrice'] + \
            (self.assumptions['sensitivity'] * ( data['currentPrice'] - average )) + \
                self.noiseGenerator()

class Random(Actor):
    def price(self, data):
        return self.uniformNoiseGenerator() * data['currentPrice']
