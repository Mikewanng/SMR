from Link import *
from Node import *
import random,math
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
class Topo(object):#定义拓扑
    def __init__(self):
        self.node=[]
        self.edge=[]
        self.topo=[]

    def CreatTopo(self,node_edge_set):#输出邻接矩阵
        self.node=node_edge_set[0][0]
        self.edge=node_edge_set[1]
        #初始化拓扑,拓扑包含邻接表以及节点安全概率
        self.topo=[[],node_edge_set[0][1]]
        for i in range(len(self.node)):#初始化邻接表
            t=[]
            for j in range(len(self.node)):
                t.append(Link())
            self.topo[0].append(t)
        
        #节点与数字映射
        i=0
        dictnode={}
        for node in self.node:
            dictnode[node]=i
            i+=1
        
        
        for edge in self.edge:
            self.topo[0][dictnode.get(edge.fr)][dictnode.get(edge.to)]=Link(dictnode.get(edge.fr),dictnode.get(edge.to),edge.c)
            
        return self.topo
    def CreatNodeEdgeSet(self,basic_node_edge_set,c=50,TrustednodeNum=4,nodesp=0.9,option=0 ):#option=0默认为无向图
        newedge=[] #存储Link结构的边
        newnode=[] #存储节点以及节点安全概率
        
        #随机生成可信节点
        TrustedNode=[]
        while len(TrustedNode)<TrustednodeNum:
            t=random.randint(0,len(basic_node_edge_set[0])-1)
            if t not in TrustedNode:
                TrustedNode.append(t)

        NodeSecurityProbability=[] #节点安全概率
        for i in range(len(basic_node_edge_set[0])):
            if i not in TrustedNode:
                NodeSecurityProbability.append(nodesp)
            else:
                NodeSecurityProbability.append(1)

        newnode=[basic_node_edge_set[0],NodeSecurityProbability]
            
        for edge in basic_node_edge_set[1]:
            if option==1:
                newedge.append(Link(edge[0],edge[1],c))
            else:
                newedge.append(Link(edge[0],edge[1],c))
                newedge.append(Link(edge[1],edge[0],c))
        return [newnode,newedge]

    def TopoUpdate(self,g,path):#删去路径上的不可信节点及路径
        for i in range(len(path)-1):
            g[0][path[i]][path[i+1]].dellink()
            g[0][path[i+1]][path[i]].dellink()
        nodelist=path[1:-1]
        for i in range(len(g[0])):
            for j in range(len(g[0][i])):
                if i in  nodelist or j in nodelist:
                    if g[1][j]<1 and g[0][i][j].Is_connected==True:
                        g[0][i][j].dellink()
                        g[0][j][i].dellink()
                    
    def creattr(self,a,n,sd):
        count=0
        for i in a:
            if i==1:
                count+=1
        while count<n:
            t=random.randint(0,38)
            while a[t]==1 or t in sd:
                t=random.randint(0,38)
            a[t]=1
            count+=1
        return a

                        
    def TopoUpdater(self,g,path):#删去路径上的所有节点 对比算法。
        for i in range(len(path)-1):
            g[0][path[i]][path[i+1]].dellink()
            g[0][path[i+1]][path[i]].dellink()
        nodelist=path[1:-1]
        for i in range(len(g[0])):
            for j in range(len(g[0][i])):
                if i in  nodelist or j in nodelist:
                    if g[0][i][j].Is_connected==True:
                        g[0][i][j].dellink()
                        g[0][j][i].dellink()
    def Toporeduce(self,g):#将邻接矩阵化为邻接表
        tmptopo=[]
        for i in g[0]:
            t=[]
            for j in range(len(i)):
                if i[j].fr != None:
                    t.append([i[j].to,g[1][j]])
            tmptopo.append(t)
        return [tmptopo,g[1]]

    def Toporeducehop(self,g):#将邻接矩阵化为hop邻接表
        tmptopo=[]
        for i in g[0]:
            t=[]
            for j in range(len(i)):
                if i[j].fr != None:
                    t.append([i[j].to,1])
            tmptopo.append(t)
        return [tmptopo,g[1]]

    def Changenodesp(self,topo,v):
        for i in range(len(topo[1])):
            if topo[1][i]!=1:
                topo[1][i]=v


    def create_random_topology(self,nodes_num=50, a=0.3, b=3,flag=0):##a = alpha, b = beta
        nodes = []
        edges = []
        positions = []
        edges_cost = []
        degree=[0]*nodes_num
        topology = [[0 for i in range(110)] for j in range(110)]
        distance = [[0 for i in range(nodes_num)] for j in range(nodes_num)]
        for n in range(0, nodes_num):
            x = random.randint(0, 100)
            y = random.randint(0, 100)
            while topology[x][y] == 1:
                x = random.randint(0, 100)
                y = random.randint(0, 100)
            topology[x][y] = 1
            nodes.append(f"N{n}")
            positions.append([x, y])
        i = 0
        max_length = -1
        while i < nodes_num:
            j = i + 1
            while j < nodes_num:
                distance[i][j] = (abs(positions[i][0] - positions[j][0]) ** 2 + abs(
                    positions[i][1] - positions[j][1])) ** 0.5
                max_length = max(max_length, distance[i][j])
                j += 1
            i += 1
        i = 0
        while i < nodes_num:
            j = i + 1
            while j < nodes_num:
                p =5* b * math.exp(-distance[i][j] / (max_length * a))/nodes_num  ##a = alpha, b = beta
                if random.random() < p:
                    edges_cost.append(round(distance[i][j], 1))
                    degree[i]+=1
                    degree[j]+=1
                    edges.append((nodes[i], nodes[j]))
                    edges.append((nodes[j], nodes[i]))
                j += 1
            i += 1
        for i in range(nodes_num):
            if degree[i]<2:
                while degree[i]<2:
                    j=random.randint(0,nodes_num-1)
                    while i==j:
                        j=random.randint(0,nodes_num-1)
                    p =5* b * math.exp(-distance[i][j] / (max_length * a))/nodes_num  ##a = alpha, b = beta
                    if random.random() < p:
                        edges_cost.append(round(distance[i][j], 1))
                        degree[i]+=1
                        degree[j]+=1
                        edges.append((nodes[i], nodes[j]))
                        edges.append((nodes[j], nodes[i]))

        if flag==1:
            g = nx.Graph()  # create graph
            g.add_nodes_from(nodes)  # add nodes
            g.add_edges_from(edges)  # add edges
            nodes_position = dict(zip(nodes, positions))  #
            node_labels = dict(zip(nodes, nodes))  # label of nodes
            edge_labels = dict(zip(edges, edges_cost))  # label of edges
            nx.draw_networkx_nodes(g, nodes_position, node_size=100, node_color="#6CB6FF")  # draw nodes
            nx.draw_networkx_edges(g, nodes_position, edges)  # draw edges
            nx.draw_networkx_labels(g, nodes_position, node_labels)  # draw label of nodes
            
            plt.axis('off')
            plt.show()
        return [nodes, edges]