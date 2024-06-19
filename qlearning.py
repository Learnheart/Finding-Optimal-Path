import random
import numpy as np
from Maze import maze, agent, COLOR, textLabel
import timeit
def q_learning(m, start=None, episodes=1000, alpha=0.1, gamma=0.9, epsilon=0.1, max_steps=1000):
    if start is None:
        start = (m.rows, m.cols)

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

    first_episode_Q = None
    last_episode_reward = 0  # Initialize reward for the last episode

    # Train the agent over a number of episodes
    for episode in range(episodes):
        currCell = start
        episode_reward = 0  # Initialize reward for the current episode
        steps = 0  # Count steps in each episode
        while currCell != m._goal and steps < max_steps:  # Avoid infinite loops
            steps += 1
            if random.uniform(0, 1) < epsilon:
                # Explore: choose a random action
                action = random.choice(list(actions.keys()))
            else:
                # Exploit: choose the action with max Q-value
                action = max(Q[currCell], key=Q[currCell].get)

            if m.maze_map[currCell][action]:
                nextCell = (currCell[0] + actions[action][0], currCell[1] + actions[action][1])

                reward = -1  # Default reward for each step
                if nextCell == m._goal:
                    reward += 100  # Reward for reaching the goal

                episode_reward += reward  # Accumulate the episode reward

                # Update Q-value
                old_q_value = Q[currCell][action]
                next_max = max(Q[nextCell].values())
                new_q_value = (1 - alpha) * old_q_value + alpha * (reward + gamma * next_max)
                Q[currCell][action] = new_q_value

                currCell = nextCell
            else:
                Q[currCell][action] = -100  # Penalize invalid actions

        if episode == 0:
            # Capture Q-values at the end of the first episode
            first_episode_Q = {k: v.copy() for k, v in Q.items()}

        if episode == episodes - 1:
            last_episode_reward = episode_reward  # Track the reward for the last episode

        # Logging
        if episode % 100 == 0:
            print(f"Episode {episode}: Last reward = {episode_reward}")

    # Generate the forward path using the learned Q-values
    fwdPath = {}
    currCell = start
    while currCell != m._goal:
        action = max(Q[currCell], key=Q[currCell].get)
        nextCell = (currCell[0] + actions[action][0], currCell[1] + actions[action][1])
        fwdPath[currCell] = nextCell
        currCell = nextCell

    return fwdPath, last_episode_reward, first_episode_Q, Q

# Note: `m` should be an instance of the maze with necessary attributes like grid, maze_map, _goal, rows, and cols.
if __name__ == "__main__":
    m = maze(15, 15)
    m.CreateMaze()

    path, last_episode_reward, first_episode_Q, last_episode_Q = q_learning(m, start=(15,15))
    textLabel(m,"Reward", last_episode_reward)
    textLabel(m, 'Q-learning optimal path length:', len(path) + 1)
    time = timeit.timeit(stmt='q_learning(m)', number=10, globals=globals())
    print(f"QLearning's algorithm average time over 10 runs: {time:.6f} seconds")

    # Print Q-values
    print("Q-values at the end of the first episode:")
    for state, actions in first_episode_Q.items():
        print(f"{state}: {actions}")

    print("\nQ-values at the end of the last episode:")
    for state, actions in last_episode_Q.items():
        print(f"{state}: {actions}")

    a = agent(m, 15, 15, color=COLOR.cyan, filled=True, footprints=True)
    m.tracePath({a: path})

    m.run()
