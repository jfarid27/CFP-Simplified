import random
import numpy as np
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
        return reduce(lambda agg, x: agg + ( x * exp(- x / float(t))  ), samples, 0)

    def partitionF(self, t, data):
        """Generalized Z partition function"""
        return reduce(lambda agg, x: agg + ( exp(- x / float(t))  ), samples, 0)

    def specificHeat(self, data, sqData, temperature, n):
        Z2 = weightedMean(temperature, sqData) / partitionF(temperature, data)
        Z =  (weightedMean(temperature, data) ** 2) / partitionF(temperature, data)
        return ( Z2 - (Z ** 2) ) / ((temperature ** 2) * n)

    def computeLogReturns(self, back, ahead):
        return np.divide(back, ahead).map(log)

    def computeSpecificHeats(self, dataStrWithArbTemp, cols, temperatures):
        points = []
        for temperature in temperatures:
            location = str.format(dataStrWithArbTemp, temperature)
            data = pd.read_csv(location, header=None)
            data.columns = cols
            points.append(specificHeat(data['energy'], data['sqEnergy'], temperature, numIsingSpins))
        return points
