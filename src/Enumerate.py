from BayGraph import BayGraph
from XMLBIFParser import XMLBIFParser
import sys
class Enumerate:
    #Returns the distribution of query variable x given the observed variables e
    def enumeration_ask(self, x, e, bn):
        #distribution over x, the query variable
        q = {};
        for i in bn.nodes[x].domain:
            #ex is e extending X = x
            ex = {}
            for k, v in e.items():
                ex[k] = v
            ex[bn.nodes[x].name] = i
            #find each part of the conditional probability
            q[i] = self.enumerate_all(bn, bn.nodes, ex, 0)
        #return normalized conditional probability of x
        return bn.normalize(q)

    def enumerate_all(self, bn, nodes, e, stack_index):

        s = bn.topologicalSort()
        #stack empty
        if stack_index >= len(s):
            return 1.0
        var_name = s.pop(stack_index)
        #get first unobserved variable
        for n in nodes:
            if n == var_name:
                Y = n
        temp = []
        for n in nodes:
            for i in s:
                if i == n:
                    temp.append(n)
        #if Y has y in e
        if Y in e:
            return bn.nodes[Y].condDist(e)[(e[bn.nodes[Y].name],)] * self.enumerate_all(bn, temp, e, stack_index+1)
        else:
            sum = 0
            for y in bn.nodes[Y].domain:
                #ey is e extending Y = y
                ey = {}
                for k, v in e.items():
                    ey[k] = v
                ey[bn.nodes[Y].name] = y
                sum += bn.nodes[Y].condDist(ey)[(ey[bn.nodes[Y].name],)] * self.enumerate_all(bn, temp, ey, stack_index+1)
            return sum

if __name__ == '__main__':
    parser = XMLBIFParser()
    try:
        bn = parser.xmlparse(sys.argv[1])
    except:
        print("Invalid Parsing File")
        exit()

    i = 3
    observedVars = {}
    while i < len(sys.argv):
        try:
            observedVars[sys.argv[i]] = sys.argv[i+1]
        except:
            print("Invalid Input")
            exit()
        i += 2
    enum = Enumerate()
    try:
        print(enum.enumeration_ask(sys.argv[2], observedVars, bn))
    except:
        print("Invalid Input")
        exit()