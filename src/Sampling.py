import random
import sys
from XMLBIFParser import XMLBIFParser
class Sampling:
    def rejSample(self, x, e, bayNet, n):
        counts = {}
        for i in bayNet.nodes[x].domain:
            counts[i] = 0
            
        bayNet.topolist = bayNet.topologicalSort()
        for j in range(n):
            sample = self.priorSample(bayNet)
            value = sample.pop(x)
            if sample.items() >= e.items():
                counts[value] += 1
        return bayNet.normalize(counts)
    
    def priorSample(self, bayNet):
        assign = {}
        for i in bayNet.topolist:
            var = bayNet.nodes[i]
            dist = var.condDist(assign)
            randVal = self.randAssign(dist)[0]
            assign[var.name] = randVal
        return assign

    def randAssign(self, dist):
        rand = random.random()
        total = 0
        last = None
        for k, v in dist.items():
            total += v
            last = k
            if rand <= total:
                return k
        # Floating-point rounding can leave `total` marginally below 1.0;
        # fall back to the final outcome instead of returning None.
        return last

    def LikelihoodWeight(self, x, assign, bayNet, n):
        counts = {}
        for i in bayNet.nodes[x].domain:
            counts[i] = 0
         
        bayNet.topolist = bayNet.topologicalSort()   
        for j in range(n):
            wSample = self.weightedSample(bayNet, assign)
            counts[wSample[0][x]] += wSample[1]
        return bayNet.normalize(counts)
            
        
    def weightedSample(self, bayNet, assign):
        w = 1.0
        x = {}
        for k, v in assign.items():
            x[k] = v
        for i in bayNet.topolist:
            if i in assign:
                w = w * bayNet.nodes[i].condDist(x)[(x[i],)]
            else:
                x[i] = self.randAssign(bayNet.nodes[i].condDist(x))[0]
        return x, w
    
    
    
    def gibbsSample(self, queryVar, assign, bayNet, n):
        counts = {}
        for i in bayNet.nodes[queryVar].domain:
            counts[i] = 0
        z = []
        for var in bayNet.topologicalSort():
            if var not in assign:
                z.append(var)
        x = {}
        for k, v in assign.items():
            x[k] = v
        for i in z:
            x[i] = self.randAssign(bayNet.nodes[i].condDist(x))[0]
            
        for j in range(n):
            for i in z:
                x[i] = self.randAssign(self.markovBlanket(bayNet, i, x))[0]
                counts[x[queryVar]] += 1
        return bayNet.normalize(counts)
    
    def markovBlanket(self, bayNet, var, x):
        assign= {}
        for key, val in x.items():
            assign[key] = val
        dist = {}
        for dom in bayNet.nodes[var].domain:
            assign[var] = dom
            prob = bayNet.nodes[var].condDist(assign)[(dom,)]
            for child in bayNet.nodes[var].children:
                prob *= child.condDist(assign)[(x[child.name],)]
            dist[(dom,)] = prob

        return bayNet.normalize(dist)
        
    
            
if __name__ == '__main__':
    try:
        n = int(sys.argv[1]) 
    except:
        print("Invalid Number of Samples")
        exit()
    parser = XMLBIFParser()
    
    try:
        bayNet = parser.xmlparse(sys.argv[2])
    except:
        print("Invalid Parsing File")
        exit()
        
    i = 5
    observedVars = {}
    while i < len(sys.argv):
        try:
            observedVars[sys.argv[i]] = sys.argv[i+1]
        except:
            print("Invalid Input")
            exit()
        i += 2
    try:
        sampler = Sampling()
        if sys.argv[3] == "rejection":
            print(sampler.rejSample(sys.argv[4], observedVars, bayNet, n))
        elif sys.argv[3] == "weighted":
            print(sampler.LikelihoodWeight(sys.argv[4], observedVars, bayNet, n))
        elif sys.argv[3] == "gibbs":
            print(sampler.gibbsSample(sys.argv[4], observedVars, bayNet, n))
        else:
            print("Invalid Sampling Type")
            exit()
    except:
        print("Invalid Input")
        exit()
        