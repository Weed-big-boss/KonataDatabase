from collections import defaultdict, deque
from copy import deepcopy
import sys
import os
uuid={True:'id TEXT PRIMARY KEY',False:'id INTEGER PRIMARY KEY AUTOINCREMENT'}
def topological_sort(relations,tables):
    graph=deepcopy(relations)
    for table in tables:
        if table['name'] not in graph:
            graph[table['name']]=[]



    in_degree = defaultdict(int)
    for deps in graph.values():
        for dep in deps:
            in_degree[dep] += 1

    queue = deque([node for node in graph if in_degree[node] == 0])
    result = []

    while queue:
        node = queue.popleft()
        result.append(node)
        for dependent in graph[node]:
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)
    return result
def data_catcher():
 file_path = get_file_path("attribute_list.txt")
 with open(file_path,"r",encoding="utf-8") as f:
    data=f.read()
    data=data.split("\n")
    data.pop(-1)
    att_n_types={}
    for elem in data:
        pair=elem.split(" ")
        att_n_types[pair[0]]=pair[1]
    attribue_list=[]
    for elem in data:
        attribue_list.append(elem.split(" ")[0])
    return att_n_types, attribue_list

def get_file_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

