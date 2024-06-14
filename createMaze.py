from Maze import maze, COLOR, agent
# define row & columns
m = maze(20, 30)
# point of goal
# save maze to save maze to csv file
m.CreateMaze()

# create agent
a = agent(m,footprints=True, filled=True)

m.run()