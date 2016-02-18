import random
import os
from math import sqrt
from multiprocessing import Pool

import simulation.Networks as Network
import simulation.Contagion as Contagion
import simulation.System as System
import simulation.MCMC as MCMC

random.seed(int("54e22d", 16))

steps = 1000000
side = 32
spins = side * side

def observablesWrap(openedFile):
    def wrap(system, observations):
        observables(system, observations)
        data = str.format("{},{},{},{}", observations['lastAbsEnergy'], \
            observations['lastSqAbsEnergy'], observations['lastAbsMag'],\
            observations['lastSqAbsMag'])
        openedFile.write(data + '\n')
    return wrap

def observables(system, observations):
    E = 0.0
    M = 0.0
    S = system.wolffIsing.network.nodes
    for k in range(system.wolffIsing.network.numNodes):
        M += S[k]['spin']
        E -=  S[k]['spin'] * sum([S[neighbor]['spin'] for neighbor in system.wolffIsing.network.edges[k]])
    observations['absSumEnergy'] += abs(E)
    observations['absSumSqEnergy'] += abs(E) ** 2
    observations['absSumMag'] += abs(M)
    observations['absSumSqMag'] += abs(M) ** 2
    observations['lastAbsEnergy'] = abs(E)
    observations['lastSqAbsEnergy'] = abs(E) ** 2
    observations['lastAbsMag'] = abs(M)
    observations['lastSqAbsMag'] = abs(M) ** 2
    
def randomSpin(x, y):
    return {'spin': random.choice([-1, 1])}

def experiment(temperature):
    print("starting temperature", temperature)
    filename = 'data/ising_lattice_energy_mag_' + \
        str.format("{}", temperature) + ".csv"
    openedFile = open(filename, 'w')
    network = Network.Lattice2DNP(side, side, {}, {})
    network.build(randomSpin)
    contagion = Contagion.WolffIsing(network, 1/float(temperature), random.random)
    system = System.WolffIsing(contagion, random.randint)
    montecarlo = MCMC.MCMC(system, random.random)
    observations = {}
    observations['absSumEnergy'] = 0
    observations['absSumSqEnergy'] = 0
    observations['absSumMag'] = 0
    observations['absSumSqMag'] = 0
    observations['lastAbsEnergy'] = 0
    observations['lastAbsMag'] = 0
    observations['lastSqAbsEnergy'] = 0
    observations['lastSqAbsMag'] = 0
    montecarlo.simulate(observablesWrap(openedFile), observations, steps)
    openedFile.close()
    return observations

if __name__ == '__main__':
    temperatures = [float(x)/10 for x in range(1, 50)]
    p = Pool(len(temperatures))
    p.map(experiment, temperatures)
