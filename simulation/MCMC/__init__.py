class MCMC():
    def __init__(self, system, randomGen):
        self.system = system
        self.randomGen = randomGen
    
    def metropolis(self, probA, probB):
        """Metropolis-Hastings transition odds function"""
        if (probB > probA):
            return True
        else:
            return self.randomGen() < float(probB) / probA
    
    def simulate(self, observable, observations, nsteps=1000):
        """MCMC simulation"""
        for n in range(nsteps):
            possibleState = self.system.genPossibleState()
            shouldTransition = self.metropolis(self.system.prob(), possibleState.prob())
            if (shouldTransition):
                self.system.transition(possibleState)
            observable(self.system, observations) 
        return observations
