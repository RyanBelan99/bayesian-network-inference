#Class definition for a graph stored in 2 different ways allowing for diverse ways to access it
class BayGraph:
    class Node:
        def __init__(self, name):
            self.name = name
            self.parents = []
            self.children = []
            self.domain = []
            self.dist = {}
            self.topolist = None

#         Finds the probability distribution of variable given parents
        def condDist(self, assignments):
            if self.parents == []:
                return self.dist
            givenAssign = []
            for parent in self.parents:
                for assign in assignments:
                    if assign == parent.name:
                        givenAssign.append(assignments[assign])
                        break           
            
            
            condAssign = {}
            for i in self.domain:
                tempAssign = [x for x in givenAssign]
                tempAssign.append(i)
                condAssign[(i,)] = self.dist[tuple(tempAssign)]
            
            return condAssign
                        
                
                
    
    def __init__(self, nodes):
        self.nodes = nodes
        self.roots = None
        self.edges = {}
       
        
#     A recursive function used by topologicalSort 
    def topologicalSortUtil(self,node,visited,stack): 
        visited[node] = True
        if node in self.edges:
            for i in self.edges[node]: 
                if visited[i] == False: 
                    self.topologicalSortUtil(i,visited,stack) 
  
        stack.insert(0,node) 
  
#     Function that returns a stack of topologically sorted vertexes
    def topologicalSort(self): 
        visited = {}
        for i in self.nodes:
            visited[i] = False
        stack =[]
        for node in self.nodes: 
            if visited[node] == False:
                self.topologicalSortUtil(node,visited,stack) 
        return stack
    
    def normalize(self, dict):
        total = 0
        for k, v in dict.items():
            total += v
        normalized = {}
        if total == 0:
            for k in dict:
                normalized[k] = 1.0/len(dict)
            return normalized
        for k, v in dict.items():
            normalized[k] = v/total
        return normalized
            
        
    
            