from Maze import maze, agent, COLOR, textLabel
import random
from datetime import datetime

class ACO:
    def __init__(self,maze, start=None, alpha=1, beta=1, num_ants=20, num_iters=30, evaporation_rate=0.1):
        self.maze = maze
        self.alpha = alpha  # Pheromone importance
        self.beta = beta    # Distance priority
        self.num_ants= num_ants
        self.num_iters=num_iters
        self.evaporation_rate = evaporation_rate
        self.pheromone_table = {k: 0 for k in self.maze.maze_map}
        self.end = self.maze._goal

        if start is None:
            self.start=(self.maze.rows, self.maze.cols)
        
        self.is_visited = [[0] * self.maze.rows for temp in range(self.maze.cols)]
        self.aco_current_route = []
        self.aco_best_route = []

    def randomize_list(self, new_list, max_tau, min_tau, max_pheromone, min_pheromone):
        den = 0
        if max_pheromone == min_pheromone:
            max_pheromone, min_pheromone = 1, 0
        if max_tau == min_tau:
            max_tau, min_tau = 1, 0

        for t in new_list:
            pheromone = (1 + ((t[2] - min_pheromone) / (max_pheromone - min_pheromone)))
            tau = (1 + ((t[1] - min_tau) / (max_tau - min_tau))) * 100
            den += ((pheromone ** self.beta) * (tau ** self.alpha))
            
        prob_check = 0
        temp_list = []
        for t in new_list:
            pheromone = (1 + ((t[2] - min_pheromone) / (max_pheromone - min_pheromone)))
            tau = (1 + ((t[1] - min_tau) / (max_tau - min_tau))) * 100
            prob = ((pheromone ** self.beta) * (tau ** self.alpha)) / den
            prob_check += prob
            temp_list.append((t[0], prob))

        ret_list = []
        possibilities = random.choices(population=temp_list, weights=[i[1] for i in temp_list], k=10)

        for l2 in possibilities:
            if l2 not in ret_list:
                ret_list.append(l2)
        random.shuffle(temp_list)
        for t in temp_list:
            if t not in ret_list:
                ret_list.append(t)

        return ret_list
    
    def get_heuristic(self, startnode, endnode):
        x1 = abs(startnode[0] - endnode[0])
        y1 = abs(startnode[1] - endnode[1])
        return x1 + y1

    def sort_by_probabilities(self, keynode, adjacent_directs):
        new_list = []
        max_tau = float('-inf')
        max_pheromone = float("-inf")
        min_tau = float("inf")
        min_pheromone = float("inf")

        for direct in adjacent_directs:
            if adjacent_directs[direct] == 0:
                continue

            node = (keynode[0], keynode[1]+1) if direct == "E" \
                else (keynode[0], keynode[1]-1) if direct == "W" \
                else (keynode[0]-1, keynode[1]) if direct == "N" \
                else (keynode[0]+1, keynode[1]) # S
            
            pheromone = self.pheromone_table[node]
            tau = self.get_heuristic(node, self.end) 
            max_tau = max(max_tau, tau) 
            max_pheromone = max(max_pheromone, pheromone)
            min_tau = min(min_tau, tau)
            min_pheromone = min(min_pheromone, pheromone)
            new_list.append((node, tau, pheromone))

        new_list = self.randomize_list(new_list, max_tau, min_tau, max_pheromone, min_pheromone)
        return new_list # [((x2,y2),prob2) ,((x1,y1),prob1)]

    def find_route(self, node): # to find a route from start to end node [(x1,y1), (x2,y2), (x4,y4), (x5, y5)]
        adjacent_directs = self.maze.maze_map[node] 
        x = node[0]
        y = node[1]

        if (x,y) == self.maze._goal:
            return -1

        self.is_visited[x-1][y-1] = 1
        adjacent_nodes = self.sort_by_probabilities((x,y), adjacent_directs)
        for node_prob in adjacent_nodes:
            n = node_prob[0]
            if self.is_visited[n[0]-1][n[1]-1] == 0:
                ret_val = self.find_route((n[0], n[1]))
                if ret_val == -1:
                    self.aco_current_route.append((n[0], n[1]))
                    return -1
                
    def get_current_best_path(self, all_paths): #Get shortest path
        current_best_path = []
        for p in all_paths:
            if not current_best_path:
                current_best_path = p
            if len(current_best_path) > len(p):
                current_best_path = p
        return current_best_path
        
    def update_pheromone(self, paths):
        for p in paths:
            for node in p:
                self.pheromone_table[(node[0], node[1])] += (1 / len(p))

    def evaporation(self):
        for k in self.pheromone_table:
            self.pheromone_table[k] = self.pheromone_table[k] * (1 - self.evaporation_rate)

    def run(self):
        best_path = []
        for i in range(self.num_iters):
            all_paths = []
            for j in range(self.num_ants):
                self.find_route(self.start)
                self.aco_current_route.append((self.start))
                self.aco_current_route = self.aco_current_route[::-1]
                all_paths.append(self.aco_current_route)
                self.aco_current_route = []
                self.is_visited = [[0] * self.maze.rows for temp in range(self.maze.cols)]
            current_best_path = self.get_current_best_path(all_paths)
            self.evaporation() 
            self.update_pheromone(all_paths)
            best_path = current_best_path if not best_path \
                        else current_best_path if len(best_path) > len(current_best_path) \
                        else best_path
            if len(best_path) == 0:
                return
            self.aco_best_route = best_path

        return best_path
        

if __name__ == '__main__':
    m = maze(15,15)
    m.CreateMaze()
    # print(m.maze_map)

    start_time = datetime.now()
    start_timestamp = datetime.timestamp(start_time)

    model = ACO(m)
    # print(model.pheromone_table)
    
    shortest = model.run()
    end_time = datetime.now()
    end_timestamp = datetime.timestamp(end_time)
    compute_time = end_timestamp - start_timestamp
    print(compute_time)

    print(shortest)
    print(len(shortest))

    a = agent(m,color=COLOR.pink,filled=True,footprints=True)
    m.tracePath({a:shortest},delay=100)
    l = textLabel(m,'ACO Path Length: ', len(shortest))
    l = textLabel(m,'Computing time: ', compute_time)


    m.run()
