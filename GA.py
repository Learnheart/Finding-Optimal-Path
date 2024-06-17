from Maze import maze, agent, COLOR, textLabel
from random import randint
from sys import exit

invalid_steps, path_length, num_turns = [], [], []
population, direction, fitness = [], [], []

rows, columns = 10, 10
fitness_threshold = (0)
mutation_rate = (1)
pop_size = 500 
m = maze(rows, columns)
m.CreateMaze(loopPercent=100)
a = agent(m, footprints=True)
path_length_result = None

def main():
    generate_population()
    count = 0
    while count < 3000:
        create_path()
        find_fitness()
        parent_selection()
        print(count)
        index = check_sol()
        if index:
            break
        crossover()
        mutation()
        count += 1
    else:
        exit("Not Found")

    if direction[index]:
        path = generate_path1(population[index])
    else:
        path = generate_path2(population[index])
    
    l=textLabel(m,'GA Search Legth', len(path))
    m.tracePath({a: path}, showMarked=True)
    m.run()

def check_sol() -> int:
    if 0 in invalid_steps:
        ind = invalid_steps.index(0)
        return ind if fitness[ind] >= fitness_threshold else 0
    else:
        return 0

def find_fitness() -> None:
    fitness.clear()
    wl, wt, wf = 2, 2, 3
    Smin, Lmin, Tmin = min(invalid_steps), min(path_length), min(num_turns)
    Smax, Lmax, Tmax = max(invalid_steps), max(path_length), max(num_turns)
    for i in range(pop_size):
        S = invalid_steps[i]
        T = num_turns[i]
        L = path_length[i]
        ff = 1 - ((S - Smin) / (Smax - Smin))
        fl = 1 - ((L - Lmin) / (Lmax - Lmin))
        ft = 1 - ((T - Tmin) / (Tmax - Tmin))
        f = ((float)(100 * wf * ff) * ((wl * fl) + (wt * ft))) / (wl + wt)
        fitness.append(f)

def crossover() -> None:
    offset = pop_size // 2
    for i in range(0, offset, 2):
        crossover_pt = randint(2, columns - 2)
        population[i + offset] = (
            population[i][:crossover_pt] + population[i + 1][crossover_pt:]
        )
        population[i + offset + 1] = (
            population[i + 1][:crossover_pt] + population[i][crossover_pt:]
        )

def mutation() -> None:
    for i in range(0, pop_size, mutation_rate):
        population[i][randint(1, columns - 2)] = randint(0, rows - 1)
        direction[i] = randint(0, 1)

def parent_selection() -> None:
    global fitness, population, direction, invalid_steps, path_length, num_turns
    zipped = zip(fitness, population, direction, invalid_steps, path_length, num_turns)
    zipped = sorted(zipped, key=lambda x: (-x[0], x[3]))
    fitness, population, direction, invalid_steps, path_length, num_turns = zip(*zipped)
    fitness, population, direction = list(fitness), list(population), list(direction)
    invalid_steps, path_length, num_turns = (
        list(invalid_steps),
        list(path_length),
        list(num_turns),
    )

def create_path() -> None:
    invalid_steps.clear()
    path_length.clear()
    num_turns.clear()
    for i in range(pop_size):
        t = 0
        for k in range(columns - 1):
            if population[i][k] != population[i][k + 1]:
                t += 1
        num_turns.append(t)
        if direction[i]:
            path = generate_path1(population[i])
            count = 0
            for j in range(len(path) - 1):
                if not is_valid(path[j], path[j + 1]):
                    count += 1
            invalid_steps.append(count)
            path_length.append(len(path))
        else:
            path = generate_path2(population[i])
            count = 0
            for j in range(len(path) - 1):
                if not is_valid(path[j], path[j + 1]):
                    count += 1
            invalid_steps.append(count)
            path_length.append(len(path))

def generate_population() -> None:
    global population, direction
    population = [
        [0] + [randint(0, rows - 1) for _ in range(columns - 2)] + [rows - 1]
        for _ in range(pop_size)
    ]
    direction = [randint(0, 1) for _ in range(pop_size)]

def generate_path1(s) -> list:
    path = []
    j = 0
    for i in range(columns - 1):
        if j < s[i + 1]:
            while j < s[i + 1]:
                path.append((j + 1, i + 1))
                j += 1
            path.append((j + 1, i + 1))
        else:
            while j > s[i + 1]:
                path.append((j + 1, i + 1))
                j -= 1
            path.append((j + 1, i + 1))
    path.append((rows, columns))
    path.reverse()
    return path


def generate_path2(s) -> list:
    path = [(1, 1)]
    j = 0
    for i in range(1, columns):
        if j <= s[i]:
            while j < s[i]:
                path.append((j + 1, i + 1))
                j += 1
            path.append((j + 1, i + 1))
        else:
            while j > s[i]:
                path.append((j + 1, i + 1))
                j -= 1
            path.append((j + 1, i + 1))
    path.reverse()
    return path

def is_valid(p1, p2) -> bool:
    x = (p2[0] - p1[0], p2[1] - p1[1])
    if x == (1, 0):
        return True if m.maze_map[p1]["S"] else False
    if x == (-1, 0):
        return True if m.maze_map[p1]["N"] else False
    if x == (0, 1):
        return True if m.maze_map[p1]["E"] else False
    if x == (0, -1):
        return True if m.maze_map[p1]["W"] else False

if __name__ == "__main__":
    # print(len(list(path_length)))
    # l = textLabel(m, 'GA Path Length: ', len(list(path_length)))
    main()
