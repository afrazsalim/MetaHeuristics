from math import sqrt
from seperate_chaining import SeperateChaining
#import matplotlib as mpl
#mpl.use('TkAgg')
#import matplotlib.pyplot as plt
from params import *
from init import *
from fitness import Evaluator
from operators import *
from local_search import improvement

def extract_loc(filename):
    city_locations = []
    city_requirements = []
    with open(filename,'r') as f:
        lines = f.readlines()
        max_temp = int(lines[0].strip())
        for idx in range(2, len(lines)):
            city_loc = lines[idx].strip().split()
            city_locations.append((float(city_loc[0]), float(city_loc[1])))
            city_requirements.append(int(city_loc[2]))
    return city_locations, city_requirements, max_temp

def extract_distances(filename):
    distances = []
    with open(filename, "r") as f:
        lines = f.readlines()
        max_temp = int(lines[0].strip())
        city_requirements = [int(req) for req in lines[1].strip().split()]
        for idx in range(2, len(lines)):
            distances.append([float(dist) for dist in lines[idx].strip().split()])

    return distances, city_requirements, max_temp

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


def initialize_list():
    list = []
    for i in range(Params.NUMBER_OF_BESTSOLUTIONS):
        list.append(-1)
    return list


def getTotalRatio(list):
    sum  = 0
    for i in range(len(list)):
        sum = sum +  (list[i])
    return -(sum/len(list))

#It's very inefficient and as it is not need so i did not optimize it.
def sort_for_elitism(pool,eval_fit):
    for i in range(int(Params.ElISTISM_PERCENTAGE*(len(pool)))):
        min_index = i
        for j in range(i+1, len(pool)):
           if eval_fit(pool[min_index]) > eval_fit(pool[j]):
              min_index = j
        pool[i], pool[min_index] = pool[min_index], pool[i]
    return pool


def load_file(filename):
    if ''.join(filename.split(".")[-1]) == "itsp":
        city_locs, city_requirements, max_temp = extract_loc("test_cases/"+filename)
        distances = compute_distances(city_locs)
    else:
        distances, city_requirements, max_temp = extract_distances("test_cases/"+filename)

    return distances, city_requirements, max_temp,len(city_locs)

def main_loop(distances, city_requirements, max_temp,number_of_cities):


    Individual.ncity = len(city_requirements)
    max_pt = get_max_pt()(max_temp)
    max_sl = get_max_sl(city_requirements, max_pt)
    it = get_temp_increase_func()
    dt = get_temp_decrease_func()
    wait_func = get_wait_func(max_temp)
    delay = None
    if Params.DELAY_FUNCTION:
            delay = SeperateChaining(number_of_cities,distances)
        # check if possibility to use distance instead of locs
    evaluator = Evaluator(max_temp, distances, city_requirements, dt, it, wait_func,delay)
    current_gen = 0
    population = init(city_requirements, max_pt)
    eval_fit = lambda p: evaluator.fitness_eval(p.NL, p.PTL,
                                  p.C1, p.C2)
    number_of_best_values = initialize_list()
    current_entry_index = 0
    previous_best_fitness = 0
    counter = 0
    while not is_stopping(current_gen):
        parents = parent_selection(population, evaluator)
        offsprings = crossover(parents, max_pt, evaluator)
        final_offsprings = mutate(offsprings, max_pt, max_sl)
        population = survivor_selection(population, final_offsprings, evaluator)
        if Params.SEARCH == LocalSearch.OPT2:
            improvement(population, evaluator)
        best = max(population, key=eval_fit)
        fitness_of_best = eval_fit(best)
        """

       
        print(sum([eval_fit(p) for p in population])/len(population))
        print(fitness_of_best)
        print("violations, C1: "+str(evaluator.c1_violations)+" C2: "+str(evaluator.c2_violations))
        print("avg violations, C1: " + str(evaluator.avg_c1_violations) +\
              " C2: " + str(evaluator.avg_c2_violations))
        print("distance time: "+str(evaluator.time_dist)+ " processing time: "+str(evaluator.process_time)+\
              " wait time: "+str(evaluator.wait_time)+" penalty time: "+str(evaluator.time_penalty) + " delay time " + str(evaluator.delay_time))
        """
        if Params.SIMPLE_MEASURE and Params.isActivated and number_of_best_values[Params.NUMBER_OF_BESTSOLUTIONS-1] != -1 :
           if(current_entry_index >= Params.NUMBER_OF_BESTSOLUTIONS):
              current_entry_index = current_entry_index%Params.NUMBER_OF_BESTSOLUTIONS
              number_of_best_values[current_entry_index] = fitness_of_best
              total_sum = getTotalRatio(number_of_best_values)
              hyper_mutation = total_sum -int(total_sum)
              if(fitness_of_best == previous_best_fitness):
                 counter = counter +1
              if counter  >= Params.MAX_CHANCES:
                 counter = 0
                 hyper_mutation = min((hyper_mutation  + (hyper_mutation*Params.INCREASING_FACTOR)),1)
              Params.P_MUT_NL = hyper_mutation
              print("Mutation after chagning ", Params.P_MUT_NL)
        elif Params.SIMPLE_MEASURE and Params.isActivated:
                 number_of_best_values[current_entry_index] = fitness_of_best
        previous_best_fitness = fitness_of_best
        current_entry_index = current_entry_index + 1
        current_gen += 1

    best = max(population, key=eval_fit)
    print(best)
    print(eval_fit(best))
    print("violations, C1: " + str(evaluator.c1_violations) + " C2: " + str(evaluator.c2_violations))
    print("avg violations, C1: " + str(evaluator.avg_c1_violations) + \
          " C2: " + str(evaluator.avg_c2_violations))
    print("distance time: " + str(evaluator.time_dist) + " processing time: " + str(evaluator.process_time) + \
          " wait time: " + str(evaluator.wait_time) + " penalty time: " + str(
        evaluator.time_penalty) + " delay time " + str(evaluator.delay_time))
    return best, evaluator
    #plot_path(best, city_locs)

def is_stopping(gen):
    return gen >= Params.N_GEN

def fillFunctions():
    file = open(Params.FUNCTION_ORDER,'w')
    for i in range(20):
        for j in range(200):
            file.write(str(random.randint(0,20)))
            file.write(' ')
        file.write("\n")

if __name__ == "__main__":
    d, c, m, n = load_file(Params.FILE)
    #fillFunctions()
    main_loop(d, c, m, n)
