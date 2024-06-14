from Maze import maze, agent, COLOR, textLabel

def dijsktra(m, *h, start=None):
  if start is None:
    start = (m.rows, m.cols)
    
  # create obstacle in maze
  hurdles = [(i.position, i.cost) for i in h]
  
  # set init value of node to infinity 
  unvisited = {n:float('inf') for n in m.grid}
  unvisited[start] = 0
  visited = {}
  revPath = {}
  
  while unvisited:
    currCell = min(unvisited, key = unvisited.get)
    visited[currCell] = unvisited[currCell]
    
    # stop when get endpoint
    if currCell==m._goal:
      break
    
    # movement direction W(<-) N(|^) S(|) E(->)
    for d in 'EWNS':
      if m.maze_map[currCell][d]==True:
        if d == 'E':
          childCell = (currCell[0], currCell[1] + 1) #move to the right
        elif d == 'W':
          childCell = (currCell[0], currCell[1] - 1) #move to left
        elif d == 'N':
          childCell = (currCell[0] - 1, currCell[1]) #top
        elif d == 'S':
          childCell = (currCell[0] + 1, currCell[1]) #bot
        if childCell in visited:
          continue
        tempDist = unvisited[currCell] + 1
        
        # + cost if encouter obstacle
        for hurdle in hurdles:
          if hurdle[0]==currCell:
            tempDist+=hurdle[1]
            
        if tempDist < unvisited[childCell]:
          unvisited[childCell]=tempDist
          revPath[childCell]=currCell

    unvisited.pop(currCell)
  # keep move forward til get the goal
  fwdPath = {}
  cell = m._goal
  while cell != start:
    fwdPath[revPath[cell]] = cell
    cell = revPath[cell]
  
  return fwdPath, visited[m._goal]

if __name__=="__main__":
  DijMaze = maze(10, 10)
  DijMaze.CreateMaze()
  
  h1=agent(DijMaze,1,4,color=COLOR.red)
  # h2=agent(DijMaze,4,6,color=COLOR.red)
  # h3=agent(DijMaze,4,1,color=COLOR.red)
  # h4=agent(DijMaze,4,2,color=COLOR.red)
  # h5=agent(DijMaze,4,3,color=COLOR.red)

  h1.cost=100
  # h2.cost=100
  # h3.cost=100
  # h4.cost=100
  # h5.cost=100

  path,c=dijsktra(DijMaze,h1,start=(6,1))
  textLabel(DijMaze,'Total Cost',c)
  
  a=agent(DijMaze,6,1,color=COLOR.cyan,filled=True,footprints=True)
  DijMaze.tracePath({a:path})
  
  DijMaze.run()