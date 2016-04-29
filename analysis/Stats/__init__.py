import random
import numpy as np
import pandas as pd
from math import log, floor, exp

random.seed(int("54e22d", 16))

class Stats():
    def bootstrapping(self, observable, dataset, samples=1000):
        observableDist = []
        sample = [x for x in dataset]
        for n in range(samples):
            replacePos = random.randint(0, len(sample)-1)
            selectedValue = random.randint(0, len(dataset)-1)
            sample[replacePos] = dataset[selectedValue]
            observableDist.append(observable(sample))
        return observableDist

    def mean(self, samples):
        return sum(samples) / float(len(samples))

    def weightedMean(self, t, data):
        """Computes weighted mean using exponential energy distribution"""
        M = 0
        for point in data:
            M += point * exp(- point / float(t))
        return M

    def weightedSqMean(self, t, data):
        M = 0
        for point in data:
            M += (point ** 2) * exp(- point / float(t))
        return M

    def partitionF(self, t, data):
        """Generalized Z partition function"""
        Z = 0
        for point in data:
            Z += exp(- point / float(t))
        return Z

    def specificHeat(self, data, temperature, n):
        min = 0
        for energy in data:
            if (energy < min):
                min = energy
        shiftedData = data.map(lambda x: x - min)
        P = self.partitionF(temperature, shiftedData)
        Z2 = self.weightedSqMean(temperature, shiftedData) / P
        Z =  self.weightedMean(temperature, shiftedData) / P
        return ( Z2 - (Z ** 2) ) / ((temperature ** 2) * n)

    def computeLogReturns(self, back, ahead):
        return np.divide(back, ahead).map(log)

    def computeSpecificHeats(self, dataStrWithArbTemp, cols, temperatures, numIsingSpins):
        points = []
        for temperature in temperatures:
            location = str.format(dataStrWithArbTemp, temperature)
            data = pd.read_csv(location, header=None)
            data.columns = cols
            points.append((self.specificHeat(data['energy'], temperature, numIsingSpins), temperature))
        return points

if __name__ == "__main__":
    stats = Stats()
    cols = ['energy', 'sqEnergy', 'mag', 'sqMag']
    swTemps = [float(x)/10 for x in range(33, 50)]
    periodicTemps = [float(x)/5 for x in range(5, 25)]
    periodicSpecificHeats = stats.computeSpecificHeats('./data/ising.random.periodic.100.{}.csv', cols, periodicTemps, 100 * 100)
    swSpecificHeats = stats.computeSpecificHeats('./data/small-world.random.10000.{}.csv', cols, swTemps, 100 * 100)
    periodicFile = open('data/p.specificheat.csv', 'w')
    swFile = open('data/sw.specificheat.csv', 'w')
    for (point,temp) in periodicSpecificHeats:
        data = str.format("{},{}\n", temp, point)
        periodicFile.write(data)
    for (point,temp) in swSpecificHeats:
        data = str.format("{},{}\n", temp, point)
        swFile.write(data)
    periodicFile.close()
    swFile.close()
