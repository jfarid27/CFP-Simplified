import random
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
