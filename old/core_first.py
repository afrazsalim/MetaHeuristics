from math import sqrt
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
import random
import copy


N_POP = 200
N_GEN = 100
N_OFF = N_POP
TOUR_SIZE = 4
P_MUT = 5 #i don't know how to generate random double in python
P_CROSS = 0.2
MAX_TEMP = 2
TOURNAMENT_SIZE = 10

def extract(filename):
    city_locations = []
    process_time_per_unit = []
    with open(filename,'r') as f:
        for line in f:
            city_loc = line.strip().split(" ")
            city_locations.append((float(city_loc[0]), float(city_loc[1])))
            process_time_per_unit.append(float(city_loc[2]))
    return (city_locations,process_time_per_unit)



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
    plt.show(block=False)
    plt.pause(2)




def main_loop():
    city_locs,process_time_per_unit = extract("../test_cases/belgium.txt")
    distances = compute_distances(city_locs)
   # n_cities = len(city_locs)
    node_List = []
    for i in range(len(process_time_per_unit)):
        city = process_time_per_unit[i]
        for j in range(int(city)):
            node_List.append(i)
    population,current_time_of_each_chrom = generate_population(node_List,city_locs,N_POP) #Current time list maintains how many units a specific node has been processed
    current_gen = 0
    while not is_stopping(current_gen):
         time = update_processing_time(population,city_locs)
         fitness_of_population = assign_fitness(population,time,distances,current_gen)
         best_individual_index = find_best_solution(fitness_of_population)
         print('best individual')
         print(population[best_individual_index])
         print('fitness')
         print(fitness_of_population[best_individual_index])
         parents = select_parents(fitness_of_population,len(population))
         offsprings = order_crossover(parents,population)
         mutated_offsprings = mutate_offsprings(offsprings)
         time_offsprings = update_processing_time(mutated_offsprings,city_locs)
         offsprings_fitness = assign_fitness(mutated_offsprings,time_offsprings,distances,current_gen)
         population = survivor_selection_mechanism(offsprings_fitness,fitness_of_population,population,mutated_offsprings)
         current_gen += 1


   # print(fitness_eval(best, distances))
   # print(best)
   # plot_path(best, city_locs)


def survivor_selection_mechanism(offsprings_f,pop_f,pop,offsprings):
    result = []
    first_copy = copy.deepcopy(offsprings_f)
    second_copy = copy.deepcopy(pop_f)
    first_copy.sort()
    second_copy.sort()
    for i in range(len(offsprings_f)):
        if first_copy[i] < second_copy[i]:
            result.append(offsprings[offsprings_f.index(first_copy[i])])
        else:
            result.append(pop[pop_f.index(second_copy[i])])
    return result

def find_best_solution(fitness):
    min = 0
    for i in range(1,len(fitness)):
        if fitness[i] < fitness[min]:
            min = i
    return min

def mutate_offsprings(pop):
    for i in range(len(pop)):
        individual = pop[i]
        random_number = random.randint(0,10)
        if random_number > P_MUT:
            random_first = random.randint(1,len(individual)-1)
            random_second = random.randint(1,len(individual)-1)
            individual[random_first], individual[random_second] = individual[random_second], individual[random_first]
    return pop

def order_crossover(parents_index,population):
    offsprings = []
    for i in range(len(parents_index)-1):
        first_parent = population[parents_index[i]]
        second_parent = population[parents_index[i+1]]
        random_first = random.randint(1,len(first_parent)-1)
        random_second = random.randint(1,len(second_parent)-1)
        child_first = copy_elements(0,random_first,first_parent,second_parent)
        child_second = copy_elements(0,random_second,second_parent,first_parent)
        offsprings.append(child_first)
        offsprings.append(child_second)
    return offsprings


def copy_elements(begin_index,final_index,first_parent,second_parent):
    value = []
    for i in range(final_index):
        value.append(first_parent[i])
    for j in range(final_index,len(first_parent)):
        value.append(second_parent[j])
    return value

def select_parents(fitness,n):
    parents = []
    while len(parents) < N_POP/2+1:
           my_randoms = random.sample(range(n), TOURNAMENT_SIZE)
           current_cost = my_randoms[0]
           for i in range(1,len(my_randoms)):
               if fitness[my_randoms[i]] < fitness[current_cost]:
                   current_cost = my_randoms[i]
           parents.append(current_cost) #pass the index back instead of sorting
    return parents


def update_processing_time(population,city_locs):
    final_time = []
    for i in range(len(population)):
        individual_time = [0]*len(city_locs)
        first_individual = population[i]
        individual_time[0] = 1
        for j in range(len(first_individual)-1):
             next = first_individual[j+1]
             previous = first_individual[j]
             if individual_time[previous] == 0:
                 individual_time[previous] = 1
             if next == previous:
                 individual_time[previous] = individual_time[previous] + 1
             for k in range(len(individual_time)):
                 if k != previous and individual_time[k] < MAX_TEMP:
                    individual_time[k] = max(0,individual_time[k]-1)
        sum = 0;
        for s in range(len(individual_time)):
            if individual_time[s] > MAX_TEMP:
               sum = sum + individual_time[s]
        final_time.append(sum)
    return final_time

def assign_fitness(population,costs,distances,gen):
    distance_values = []
    distance = 0
    for i in range(len(population)):
        current_individual = population[i]
        for j in range(len(current_individual)-1):
            distance = distance + distances [current_individual[j]] [current_individual[j+1]]
        #distance = distance + distances[current_individual[len(current_individual)]] [current_individual[0]]
        #Add penalty value
        cost = costs[i]
        alpha = 2
        const = 1
        penalty = cost*(const*gen)**alpha
        distance_values.append(distance+penalty)
    return distance_values




def generate_population(node_list,city_locs,size):
    pop = []
    time = []
    for i in range(size):
        random.shuffle(node_list)
        pop.append(copy.deepcopy(node_list))
        time.append([0]*len(city_locs))
    return pop,time

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


