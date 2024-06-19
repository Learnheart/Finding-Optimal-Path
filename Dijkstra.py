from Maze import maze, agent, COLOR, textLabel
import timeit

def dijkstra(m, *h, start=None):
    if start is None:
        start = (m.rows, m.cols)
    
    # Create obstacles in the maze
    hurdles = [(i.position, i.cost) for i in h]
    
    # Set initial value of nodes to infinity
    unvisited = {n: float('inf') for n in m.grid}
    unvisited[start] = 0
    visited = {}
    revPath = {}
    
    while unvisited:
        currCell = min(unvisited, key=unvisited.get)
        visited[currCell] = unvisited[currCell]
        
        # Stop when reaching the endpoint
        if currCell == m._goal:
            break
        
        # Movement directions W(<-) N(|^) S(|) E(->)
        for d in 'EWNS':
            if m.maze_map[currCell][d] == True:
                if d == 'E':
                    childCell = (currCell[0], currCell[1] + 1)  # Move to the right
                elif d == 'W':
                    childCell = (currCell[0], currCell[1] - 1)  # Move to the left
                elif d == 'N':
                    childCell = (currCell[0] - 1, currCell[1])  # Move to the top
                elif d == 'S':
                    childCell = (currCell[0] + 1, currCell[1])  # Move to the bottom
                if childCell in visited:
                    continue
                tempDist = unvisited[currCell] + 1
                
                # Add cost if encountering an obstacle
                for hurdle in hurdles:
                    if hurdle[0] == currCell:
                        tempDist += hurdle[1]
                        
                if tempDist < unvisited[childCell]:
                    unvisited[childCell] = tempDist
                    revPath[childCell] = currCell

        unvisited.pop(currCell)
    
    # Extract the forward path from revPath
    fwdPath = {}
    cell = m._goal
    while cell != start:
        prev_cell = revPath.get(cell)
        if prev_cell is None:
            break
        fwdPath[prev_cell] = cell
        cell = prev_cell

    # Create the search path list
    searchPath = list(revPath.keys())

    return searchPath, revPath, fwdPath

if __name__ == "__main__":
    DijMaze = maze(15, 15)
    DijMaze.CreateMaze(loadMaze='15x15.csv')
    # DijMaze.CreateMaze()
    
    # Define hurdles
    # h1 = agent(DijMaze, 1, 4, color=COLOR.red)

    # h1.cost = 100
    
    time = timeit.timeit(stmt='dijkstra(DijMaze)', number=10, globals=globals())
    print(f"Dijkstra's algorithm average time over 10 runs: {time:.4f} seconds")
    
    searchPath, revPath, fwdPath = dijkstra(DijMaze)
    
    a = agent(DijMaze, color=COLOR.cyan, filled=True, footprints=True)
    c = agent(DijMaze, color=COLOR.red, footprints=True)
    
    # Trace paths as lists
    DijMaze.tracePath({a: searchPath}, delay=50)
    DijMaze.tracePath({c: list(fwdPath.keys())}, delay=50)
    
    textLabel(DijMaze, 'Dijkstra optimal path length:', len(fwdPath))
    textLabel(DijMaze, 'Dijkstra search path length:', len(searchPath))
    textLabel(DijMaze,'Dijkstra Time',time )
    DijMaze.run()
