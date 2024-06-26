from queue import PriorityQueue
from Maze import maze, agent, COLOR, textLabel
import time

def h(cell1,cell2):
    x1,y1=cell1
    x2,y2=cell2

    return (abs(x1-x2) + abs(y1-y2))

def AStar(m,start=None):
    if start is None:
        start=(m.rows,m.cols)

    open=PriorityQueue()
    open.put((h(start,m._goal),h(start,m._goal),start))
    aPath={}
    g_score={row:float('inf') for row in m.grid}
    g_score[start]=0
    f_score={row:float('inf') for row in m.grid}
    f_score[start]=h(start,m._goal)
    searchPath = [start]

    while not open.empty():
        currCell=open.get()[2]
        searchPath.append(currCell)
        if currCell== m._goal:
            break
        for d in 'ESNW':
            if m.maze_map[currCell][d]==True:
                if d=='E':
                    childCell = (currCell[0],currCell[1]+1)
                if d == 'W':
                    childCell = (currCell[0],currCell[1]-1)
                if d == 'N':
                    childCell = (currCell[0]-1,currCell[1])
                if d == 'S':
                    childCell = (currCell[0]+1,currCell[1])

                temp_g_score = g_score[currCell]+1
                temp_f_score = temp_g_score +h(childCell,m._goal)

                if temp_f_score < f_score[childCell]:
                    aPath[childCell] = currCell
                    g_score[childCell] = temp_g_score
                    f_score[childCell] = temp_f_score
                    open.put((f_score[childCell],h(childCell,m._goal),childCell))

    fwdPath={}
    cell= m._goal
    while cell!=start:
        fwdPath[aPath[cell]] = cell
        cell = aPath[cell]
    return searchPath, aPath, fwdPath


if __name__ == '__main__':
    m = maze(5,5)
    m.CreateMaze(loadMaze='15x15.csv')
    # path = AStar(m)
    
    start_time = time.time()
    searchPath, aPath, fwdPath = AStar(m)
    end_time = time.time()
    elapsed_time = end_time - start_time

    a = agent (m,footprints=True, color=COLOR.blue,filled=True)
    b = agent (m,1,1,footprints=True,color=COLOR.yellow,filled=True,goal=(m.rows,m.cols))
    c = agent (m,footprints=True,color=COLOR.red)

    m.tracePath({a:searchPath},delay=50)
    m.tracePath({b:aPath},delay=50)
    m.tracePath({c:fwdPath},delay=50)
    
    l = textLabel(m,'AStar Path Length', len(fwdPath)+1)
    l=textLabel(m,'A Star Search Legth', len(searchPath))
    l = textLabel(m, 'A Star Execution Time (s)', round(elapsed_time, 4))

    m.run()
