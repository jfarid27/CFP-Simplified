import pandas as pd

import random
random.seed(int("54e22d", 16))

import analysis.Stats as Stats

stats = Stats.Stats()
bootstrapSteps = 100

cols = ['energy', 'sqEnergy', 'mag', 'sqMag']

def generateBootstrappedMeanForColumn(filename, data):
    def closure(col):
        dataFileName = str.format("{}.{}.csv", filename, col)
        dataFile = open(dataFileName, 'w')
        print(data[col])
        bootstraps = stats.bootstrapping(stats.mean, data[col], bootstrapSteps)
        for point in bootstraps:
            dataFile.write(str.format("{}\n", point))
        dataFile.close()
    return closure

def generateBootstrappedMean(filename):
    data = pd.read_csv('./data/' + filename, header=None)
    data.columns = cols
    for col in cols:
        generateBootstrappedMeanForColumn(filename, data)(col)

with open('fileNames.txt') as file:
    lines = [line.rstrip('\n') for line in file]
    for line in lines:
        generateBootstrappedMean(line)
