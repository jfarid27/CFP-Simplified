import random
import os
import sys
from math import sqrt

sys.path.insert(0, os.getcwd())

import simulation.Networks as Network
import simulation.Contagion as Contagion
import simulation.System as System
import simulation.MCMC as MCMC

sys.setrecursionlimit(100000)
random.seed(int("54e22d", 16))

steps = 1000000
numNodes = 100
meanPrice = 100


def observablesWrap(openedFile):
    def wrap(system, observations):
        observables(system, observations)
        data = str.format("{},{},{},{}", observations['lastEnergy'], \
            observations['lastSqEnergy'], observations['lastMag'],\
            observations['lastSqMag'])
        openedFile.write(data + '\n')
    return wrap

def observables(system, observations):
    E = 0.0
    M = 0.0
    aggP = 0.0
    S = system.wolffIsing.network.nodes
    for k in range(system.wolffIsing.network.numNodes):
        M += S[k]['spin']
        aggP += S[k]['price']
        E -=  S[k]['spin'] * sum([S[neighbor]['spin'] for neighbor in system.wolffIsing.network.edges[k]])
    observations['lastEnergy'] = E
    observations['lastSqEnergy'] = E ** 2
    observations['lastMag'] = M
    observations['lastSqMag'] = M ** 2
    observations['lastPrice'] = aggP / float(numNodes)
    observations['lastSqPrice'] = observations['lastPrice'] ** 2 
    
def randomSpin(n):
    return {'spin': random.choice([-1, 1]), 'price': meanPrice + meanPrice * random.random()}

def experimentSingleNetwork(network):
    def closure(temperature):
        return experiment(temperature, network)
    return closure

def experiment(temperature, network):
    print("starting temperature", temperature)
    filename = 'data/small-world.cfp.random.10000.' + \
        str.format("{}", temperature) + ".csv"
    openedFile = open(filename, 'w')
    contagion = Contagion.WolffIsingCFP(network, 1/float(temperature), random.random)
    system = System.WolffCFPSystem(contagion, random.randint)
    montecarlo = MCMC.MCMC(system, random.random)
    observations = {}
    observations['lastEnergy'] = 0
    observations['lastMag'] = 0
    observations['lastSqEnergy'] = 0
    observations['lastSqMag'] = 0
    observations['lastPrice'] = 0
    observations['lastSqPrice'] = 0
    montecarlo.simulate(observablesWrap(openedFile), observations, steps)
    openedFile.close()
    return observations

if __name__ == '__main__':
    network = Network.BarabasiScaleFree(random.random, {}, {})
    network.build(numNodes, randomSpin)
    quickTemps = [5, 4, 3, 2, 1]
    #temperatures = [5, 4, 3, 2, 1]
    #temperatures.extend([float(x)/10 for x in range(1, 50) if x not in quickTemps])
    temperatures = [2.5]
    temperatures.reverse()
    experiments = map(experimentSingleNetwork(network), temperatures)
    results = [result for result in experiments]
