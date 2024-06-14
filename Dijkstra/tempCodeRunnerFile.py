def dijkstra(graph, start, end):
  unvisited = {n:float('inf') for n in graph.keys()}
  unvisited[start] = 0
  visited = {}
  
  # visit all nodes in graph
  while unvisited:
    minNode = min(unvisited, key=unvisited.get) #return the smallest value of unvisited
    visited[minNode] = unvisited[minNode] #mark node as visited
    
    for neighbor in graph.get(minNode):
      if neighbor in visited:
        continue
      tempDist = unvisited[minNode] + graph[minNode][neighbor]
      if tempDist < unvisited[minNode]:
        unvisited[minNode] = tempDist
    unvisited.pop(minNode)
  
  print(f'{visited=}')

myGraph = {
  'A': {'B': 2, 'C': 9, 'F': 4},
  'B': {'C':6, 'E':3, 'F':2},
  'C': {'D': 1},
  'D': {'C': 2},
  'E': {'C': 2, 'D': 5},
  'F': {'E': 3}
}

dijkstra(myGraph, 'A', 'D')