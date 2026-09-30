from xml.etree.ElementTree import parse
from BayGraph import BayGraph
import itertools
class XMLBIFParser:
    def xmlparse(self, file):
        nodes = {}
        alarmNet = parse(file)
        root = alarmNet.find('NETWORK')
        
#         Find each Node's name and domain
        for node in root.findall('VARIABLE'):
            name = node.find('NAME').text
            newNode = BayGraph.Node(name)
            for child in node.findall('OUTCOME'):
                newNode.domain.append(child.text)
            nodes[name] = newNode
        graph = BayGraph(nodes)    
            
#         Find each Node's parents and table
        for node in root.findall('DEFINITION'):
            curNode = graph.nodes[node.find('FOR').text]
            for child in node.findall('GIVEN'):
                curNode.parents.append(graph.nodes[child.text])
                
                edge = child.text
                if edge in graph.edges:
                    graph.edges[edge].append(curNode.name)
                else:
                    graph.edges[edge] = [curNode.name]  
                
            totalList = []
            for parent in curNode.parents:
                totalList.append(parent.domain)
            totalList.append(curNode.domain)
            combList = list(itertools.product(*totalList))
            
            tableDict = {} 
            cell = node.find('TABLE').text.split()
            celli = 0
            for comb in combList:
                tableDict[comb] = float(cell[celli])
                celli += 1
            curNode.dist = tableDict
                
                
#         Find each Node's children and which ones are roots
        roots = []
        for n in nodes.items():
            node = n[1]
            if len(node.parents) == 0:
                roots.append(node)
            for parent in node.parents:
                parent.children.append(node)
        graph.roots = roots
        return graph
            
                    
                    
            
                        
                                       
                    
    