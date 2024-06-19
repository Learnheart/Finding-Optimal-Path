from Maze import maze, COLOR, agent
# define row & columns
m = maze(15, 15)
# point of goal
# save maze to save maze to csv file
m.CreateMaze(saveMaze=True)

# create agent
a = agent(m,footprints=True, filled=True)

m.run()