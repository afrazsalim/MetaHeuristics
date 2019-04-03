import numpy as np
import random
from math import sqrt
from params import *


def create_instance(tour, idx):
    city_locs = get_locs(tour)
    print(len(city_locs))
    dist_avg = get_average_distance(city_locs)
    mean_temp = assign_mean_temp(dist_avg)
    standard_dev = assign_standard_deviation(mean_temp)
    city_requirements = assign_city_requirements(len(city_locs), mean_temp, standard_dev)
    max_temp = assign_max_temp(mean_temp)

    write_instance(idx, city_locs, city_requirements, max_temp)

def assign_mean_temp(dist_avg):
    ratio = random.randint(10, 40)/100
    return ratio*dist_avg

def assign_standard_deviation(mean_temp):
    return (random.randint(2,8)/10)*mean_temp

def assign_city_requirements(n_city, mean_temp, standard_dev):
    x = lambda: max(round(np.random.normal(mean_temp, standard_dev)), 1)
    return [ x() for _ in range(n_city)]

def assign_max_temp(mean_temp):
    difficulty_ratio = [0.5, 1, 2]
    return max(round(mean_temp*random.choice(difficulty_ratio)),2)


def get_average_distance(city_locs):
    distance = 0
    for city1 in city_locs:
        for city2 in city_locs:
            distance += sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)
    return distance / (len(city_locs)**2)


def write_instance(idx, city_locs, city_requirements, max_temp):
    filename = "test_cases/test_case"+str(idx)+".itsp"
    with open(filename, 'w') as f:
        f.write(str(max_temp)+"\n")
        for idx in range(len(city_locs)):
            s = str(city_locs[idx][0])+" "+str(city_locs[idx][1])+ " "+str(city_requirements[idx])+"\n"
            f.write(s)


def get_locs(tour):
    city_locs = []
    with open(tour, "r") as f:
        lines = f.readlines()
        dim_line = lines[3].strip().split()
        if dim_line[1] == ":":
            n_cities = int(dim_line[2])
        else:
            n_cities = int(dim_line[1])

        if n_cities > 100:
            temp_indexes = [idx for idx in range(6, n_cities+6)]
            n_cities = random.randint(50,100)
            random.shuffle(temp_indexes)
            indexes = [temp_indexes[idx] for idx in range(n_cities)]
        else:
            indexes = [idx for idx in range(6, n_cities+6)]

        city_locs = get_locs_on_scale(indexes, lines)
    return city_locs

def get_locs_on_scale(indexes, lines):
    max_val = 0
    coef = 1
    city_locs = []
    for idx in indexes:
        line = lines[idx].strip().split()
        loc = (float(line[1]), float(line[2]))
        if loc[0] > max_val:
            max_val = loc[0]
        elif loc[1] > max_val:
            max_val = loc[1]

    while max_val > 100:
        coef *= 2
        max_val /= 2

    for idx in indexes:
        line = lines[idx].strip().split()
        loc = (float(line[1])/coef, float(line[2])/coef)
        city_locs.append(loc)

    return city_locs

def create_dataset():
    for i in range(Params.N_INSTANCES):
        print(i)
        filename = "tours/prob_"+str(i)+".tsp"
        create_instance(filename, i)


create_dataset()