import random
import numpy as np
from Maze import maze, agent, COLOR, textLabel

def q_learning(m, *h, start=None, episodes=1000, alpha=0.1, gamma=0.9, epsilon=0.1):
    if start is None:
        start = (m.rows, m.cols)

    # Create obstacles in the maze
    hurdles = [(i.position, i.cost) for i in h]

    # Initialize the Q-table
    Q = {}
    for cell in m.grid:
        Q[cell] = {d: 0 for d in 'EWNS'}

    # Define actions and corresponding movements
    actions = {
        'E': (0, 1),
        'W': (0, -1),
        'N': (-1, 0),
        'S': (1, 0)
    }

    # Train the agent over a number of episodes
    for _ in range(episodes):
        currCell = start
        while currCell != m._goal:
            if random.uniform(0, 1) < epsilon:
                # Explore: choose a random action
                action = random.choice(list(actions.keys()))
            else:
                # Exploit: choose the action with max Q-value
                action = max(Q[currCell], key=Q[currCell].get)

            if m.maze_map[currCell][action]:
                nextCell = (currCell[0] + actions[action][0], currCell[1] + actions[action][1])

                reward = -1  # Default reward for each step
                for hurdle in hurdles:
                    if hurdle[0] == nextCell:
                        reward -= hurdle[1]  # Add hurdle cost to the reward

                # Update Q-value
                old_q_value = Q[currCell][action]
                next_max = max(Q[nextCell].values())
                new_q_value = (1 - alpha) * old_q_value + alpha * (reward + gamma * next_max)
                Q[currCell][action] = new_q_value

                currCell = nextCell
            else:
                Q[currCell][action] = -1000  # Penalize invalid actions

    # Generate the forward path using the learned Q-values
    fwdPath = {}
    currCell = start
    while currCell != m._goal:
        action = max(Q[currCell], key=Q[currCell].get)
        nextCell = (currCell[0] + actions[action][0], currCell[1] + actions[action][1])
        fwdPath[currCell] = nextCell
        currCell = nextCell

    return fwdPath, Q[start][max(Q[start], key=Q[start].get)]

# Note: `m` should be an instance of the maze with necessary attributes like grid, maze_map, _goal, rows, and cols.
if __name__ == "__main__":
    m = maze(10, 10)
    m.CreateMaze()

    h1 = agent(m, 1, 4, color=COLOR.red)
    # h2=agent(DijMaze,4,6,color=COLOR.red)
    # h3=agent(DijMaze,4,1,color=COLOR.red)
    # h4=agent(DijMaze,4,2,color=COLOR.red)
    # h5=agent(DijMaze,4,3,color=COLOR.red)

    h1.cost = 100
    # h2.cost=100
    # h3.cost=100
    # h4.cost=100
    # h5.cost=100

    path, c = q_learning(m, h1, start=(10,10))
    textLabel(m, 'Total Cost', c)

    a = agent(m, 10, 10, color=COLOR.cyan, filled=True, footprints=True)
    m.tracePath({a: path})

    m.run()