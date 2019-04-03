from math import sqrt
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
import random

N_POP = 100
N_GEN = 100
N_OFF = N_POP
TOUR_SIZE = 4
P_MUT = 0.2
P_CROSS = 1

def extract(filename):
    city_locations = []
    with open(filename,'r') as f:
        for line in f:
            city_loc = line.strip().split(" ")
            city_locations.append((float(city_loc[0]), float(city_loc[1])))
    return city_locations

def compute_distances(city_locations):
    n_cities = len(city_locations)
    distances = [[0 for _ in range(n_cities)] for _ in range(n_cities)]
    for city_idx1 in range(n_cities):
        for city_idx2 in range(n_cities):
            city1 = city_locations[city_idx1]
            city2 = city_locations[city_idx2]
            dist = sqrt((city1[0]-city2[0])**2 + (city1[1]-city2[1])**2)
            distances[city_idx1][city_idx2] = dist
    return distances

def plot_path(solution, locations):
    x = []
    y = []
    for city in solution:
        x.append(locations[city][0])
        y.append(locations[city][1])
    x.append(locations[solution[0]][0])
    y.append(locations[solution[0]][1])
    plt.plot(x, y, 'co')
    a_scale = float(max(x))/ float(100)

    for i in range(0,len(x)-1):
        plt.arrow(x[i], y[i], (x[i+1] - x[i]), (y[i+1] - y[i]), head_width = a_scale,
                color = 'g', length_includes_head = True)

    plt.xlim(min(x)*1.1, max(x)*1.1)
    plt.ylim(min(y)*1.1, max(y)*1.1)
    plt.show()



def main_loop():
    city_locs = extract("../test_cases/old_test_case0.txt")
    distances = compute_distances(city_locs)
    n_cities = len(city_locs)

    current_gen = 0
    population = init(n_cities, N_POP)
    while not is_stopping(current_gen):
        print(current_gen)
        parents = parent_selection(population, distances)
        offsprings = crossover(parents)
        final_offsprings = mutate(offsprings)
        population = survivor_selection(population, final_offsprings)
        current_gen += 1



    best = max(population, key= lambda p: fitness_eval(p, distances))
    print(fitness_eval(best, distances))
    print(best)
    plot_path(best, city_locs)


def is_stopping(gen):
    return gen >= N_GEN

def init(path_len, pop_size):
    path = [i for i in range(path_len)]
    pop = []
    for _ in range(pop_size):
        new_path = path[:]
        random.shuffle(new_path)
        pop.append(new_path)
    return pop

def fitness_eval(individual, distances):
    start = individual[0]
    dist = 0
    for i in range(1,len(individual)):
        dist += distances[individual[i-1]][individual[i]]
    dist+= distances[individual[len(individual)-1]][start] # Close the circle by going to the first city
    # taking the opposite so that the higher the fitness -> the better -2 > -5
    return -dist


def parent_selection(population, distances):
    mating_pool = []
    for i in range(N_OFF):
        # WITH REPLACEMENT
        contenders = [ random.choice(population) for _ in range(TOUR_SIZE)]
        mating_pool.append(max(contenders,key= lambda c : fitness_eval(c, distances)))
    return mating_pool

def survivor_selection(_, offsprings):
    # (mu, lambda) selection
    return offsprings

def mutate(population):
    for individual in population:
        if random.randint(0,1) <= P_MUT:
            first = random.randint(0,len(individual)-1)
            second = random.randint(0,len(individual)-1)
            temp = individual[first]
            individual[first] = individual[second]
            individual[second] = temp
    return population

def crossover(population):
    pool = population[:]
    random.shuffle(pool)
    offsprings = []
    start = 0
    if N_OFF%2 != 0:
        offsprings.append(pool[0])
        start = 1
    for i in range(start, N_OFF, 2):
        if random.randint(0,1) <= P_CROSS:
            offsprings.extend(cross_operator(pool[i], pool[i+1]))
    return offsprings

def cross_operator(p1, p2):
    x1 = random.randint(0, len(p1)-1)
    x2 = random.randint(0, len(p1)-1)
    first = min(x1,x2)
    second = max(x1,x2)
    offspring1 = [-1 for _ in range(len(p1))]
    offspring2 = [-1 for _ in range(len(p2))]
    offspring1[first:second+1] = p1[first:second+1]
    offspring2[first:second+1] = p2[first:second+1]
    inc = lambda c: c+1 if c != len(p1)-1 else 0
    idx_visit = inc(second)
    idx_add1 = inc(second)
    idx_add2 = inc(second)
    while idx_add1 != first or idx_add2 != first:
        if not p2[idx_visit] in offspring1:
            offspring1[idx_add1] = p2[idx_visit]
            idx_add1 = inc(idx_add1)
        if not p1[idx_visit] in offspring2:
            offspring2[idx_add2] = p1[idx_visit]
            idx_add2 = inc(idx_add2)
        idx_visit = inc(idx_visit)
    return [offspring1, offspring2]

main_loop()


