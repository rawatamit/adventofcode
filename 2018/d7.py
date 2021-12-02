import re
from collections import deque
from collections import defaultdict


class Graph:
    def __init__(self) -> None:
        self._vertices = set()
        self._inedges = defaultdict(list)
    
    def __str__(self) -> str:
        return str(self._inedges)
    
    def add_inedge(self, u, v):
        self._vertices.add(u)
        self._vertices.add(v)
        self._inedges[u].append(v)
    
    def nodes(self):
        return self._vertices
    
    def inedges(self, u):
        return self._inedges[u]


def toposort(G):
    Q = [u for u in G.nodes() if len(G.inedges(u)) == 0]
    indegree = {u: len(G.inedges(u)) for u in G.nodes()}
    sorted_order = []

    while Q:
        u = sorted(Q)[0]
        Q.remove(u)
        sorted_order.append(u)

        for v in G.nodes():
            if u in G.inedges(v):
                indegree[v] -= 1
                if indegree[v] == 0:
                    Q.append(v)
    
    return sorted_order


def task_time(u):
    return ord(u) - ord('A') + 1 + 60


def add_tasks(taskpool, workers):
    for task in workers:
        if taskpool and task['name'] is None:
            min_task = min(taskpool)
            task['name'] = min_task[0]
            task['time'] = min_task[1]
            taskpool.remove(min_task)


def part2(G, nworkers):
    indegree = {u: len(G.inedges(u)) for u in G.nodes()}
    taskpool = [(u, task_time(u))
                for u, deg in indegree.items()
                if deg == 0]
    output = []
 
    tick = 0
    workers = [{'time': 0, 'name': None} for _ in range(nworkers)]

    add_tasks(taskpool, workers)

    while True:
        all_done = all(task['time'] == 0 for task in workers)
        if len(taskpool) == 0 and all_done: break

        # one tick
        for task in workers:
            if task['time'] > 0:
                task['time'] -= 1
 
            if task['name'] is not None and task['time'] == 0:
                output.append((tick, task['name']))
                for u in G.nodes():
                    if task['name'] in G.inedges(u):
                        indegree[u] -= 1
                        if indegree[u] == 0:
                            taskpool.append((u, task_time(u)))

                task['name'] = None
       
        # assign task
        add_tasks(taskpool, workers)
         
        # update tick
        tick += 1
    
    return output


if __name__ == '__main__':
    G = Graph()
    regex = r'Step (\w) must be finished before step (\w) can begin.'

    with open('d7t.txt') as fin:
        for line in fin:
            if groups := re.search(regex, line):
                before = groups.group(1)
                after = groups.group(2)
                G.add_inedge(after, before)
    
    order = toposort(G)
    print(''.join(order))

    order = part2(G, 5)
    print(order[-1], order[-1][0]+1)
