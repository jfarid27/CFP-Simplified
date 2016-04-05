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
side = 100
spins = side * side

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
    S = system.wolffIsing.network.nodes
    for k in range(system.wolffIsing.network.numNodes):
        M += S[k]['spin']
        E -=  S[k]['spin'] * sum([S[neighbor]['spin'] for neighbor in system.wolffIsing.network.edges[k]])
    observations['lastEnergy'] = E
    observations['lastSqEnergy'] = E ** 2
    observations['lastMag'] = M
    observations['lastSqMag'] = M ** 2
    
def randomSpin(x, y):
    return {'spin': random.choice([-1, 1])}

def experimentSingleNetwork(network):
    def closure(temperature):
        return experiment(temperature, network)
    return closure

def experiment(temperature, network):
    print("starting temperature", temperature)
    filename = 'data/ising.random.periodic.100.' + \
        str.format("{}", temperature) + ".csv"
    openedFile = open(filename, 'w')
    contagion = Contagion.WolffIsing(network, 1/float(temperature), random.random)
    system = System.WolffIsing(contagion, random.randint)
    montecarlo = MCMC.MCMC(system, random.random)
    observations = {}
    observations['lastEnergy'] = 0
    observations['lastMag'] = 0
    observations['lastSqEnergy'] = 0
    observations['lastSqMag'] = 0
    montecarlo.simulate(observablesWrap(openedFile), observations, steps)
    openedFile.close()
    return observations

if __name__ == '__main__':
    network = Network.Lattice2DPeriodic(side, side, {}, {})
    network.build(randomSpin)
    temperatures = [float(x)/5 for x in range(1, 25)]
    temperatures.reverse()
    experiments = map(experimentSingleNetwork(network), temperatures)
    results = [result for result in experiments]
