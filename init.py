import temperature
from params import *
import numpy as np
import random
import math
from Individual import Individual


def deviate_sl(split_list):
    new_sl = [0 for _ in range(len(split_list))]
    for i  in range(len(split_list)):
        sign = random.choice([-1,1])
        deviation = random.randint(0, math.ceil(split_list[i]*(Params.SL_COEFF-1)))
        value  = max(0, round(split_list[i] + deviation * sign))
        new_sl[i] = value
    if sum(split_list) < 2:
        idx = random.randint(0, len(split_list)-1)
        split_list[idx] += 2
    return new_sl


def create_node_list(split_list):
    node_list = []
    for i in range(len(split_list)):
        node_list.extend(np.repeat(i, split_list[i]))
    random.shuffle(node_list)
    return node_list

def create_processing_time_list(node_list,split_list, max_pt, requirements):
    counter = [0 for _ in range(len(split_list))]
    ptl = [0 for _ in range(len(node_list))]
    for i in range(len(node_list)):
        value = node_list[i]
        counter[value] += 1
        if counter[value] == split_list[value]:
            ptl[i] = requirements[value] - max_pt * (counter[value] - 1)
            if ptl[i] > max_pt:
                print("aie")
        else:
            ptl[i] = max_pt
    return ptl

def init(city_requirements, max_pt):
    # TODO nearest vertex
    population = []
    sl = [math.ceil(city_load / max_pt) for city_load in city_requirements]
    for _ in range(Params.N_POP):
        individual = Individual()
        if Params.INIT == Initialisation.RANDOM:
            size = int(sum([math.ceil(city_load/max_pt) for city_load in city_requirements])*Params.SIZE_COEFF)
            individual.NL = [random.randint(0,Individual.ncity-1) for _ in range(size)]
            individual.SL = individual.compute_SL()
            individual.PTL = [random.randint(1, max_pt) for _ in range(len(individual.NL))]
        elif Params.INIT == Initialisation.GREEDY_SL:
            individual.NL = create_node_list(sl)
            individual.SL = sl[:]
            individual.PTL = [random.randint(1, max_pt) for _ in range(len(individual.NL))]
        elif Params.INIT == Initialisation.GREEDY_TOT:
            individual.NL = create_node_list(sl)
            individual.SL = sl[:]
            individual.PTL = create_processing_time_list(individual.NL, individual.SL, max_pt, city_requirements)
        elif Params.INIT == Initialisation.CLASSIC_SL:
            individual.SL = deviate_sl(sl)
            individual.NL = create_node_list(individual.SL)
            individual.PTL = [random.randint(1, max_pt) for _ in range(len(individual.NL))]

        individual.C1 = [random.randint(Params.MIN_C_VALUE,Params.MAX_C_VALUE) for _ in range(Individual.ncity)]
        if Params.C2_ON:
            individual.C2 = [random.randint(Params.MIN_C_VALUE, Params.MAX_C_VALUE) for _ in range(len(individual.NL))]
        population.append(individual)
    return population


def get_temp_increase_func():
    if Params.TEMP_INCREASE == TemperatureProfile.LINEAR:
        return temperature.lin_it
    elif Params.TEMP_INCREASE == TemperatureProfile.QUADRATIC:
        return temperature.q_it
    else:
        return temperature.e_it

def get_temp_decrease_func():
    if Params.TEMP_DECREASE == TemperatureProfile.LINEAR:
        return temperature.lin_dt
    elif Params.TEMP_DECREASE == TemperatureProfile.QUADRATIC:
        return temperature.q_dt
    else:
        return temperature.e_dt

def get_max_pt():
    if Params.TEMP_INCREASE == TemperatureProfile.LINEAR:
        return temperature.lin_max_pt
    elif Params.TEMP_INCREASE == TemperatureProfile.QUADRATIC:
        return temperature.q_max_pt
    else:
        return temperature.e_max_pt

def get_max_sl(city_loads, max_pt):
    return [max(math.ceil((city_load / max_pt)*Params.SL_COEFF), 2) for city_load in city_loads]

def get_wait_func(max_temp):
    if Params.TEMP_INCREASE == TemperatureProfile.LINEAR:
        if Params.TEMP_DECREASE == TemperatureProfile.LINEAR:
            return lambda tproc, temp: temperature.lin_wait(temperature.lin_dt(max_temp, tproc), temp)
        elif Params.TEMP_DECREASE == TemperatureProfile.QUADRATIC:
            return lambda tproc, temp: temperature.q_wait(temperature.lin_dt(max_temp, tproc), temp)
        else:
            return lambda tproc, temp: temperature.e_wait(temperature.lin_dt(max_temp, tproc), temp)
    elif Params.TEMP_INCREASE == TemperatureProfile.QUADRATIC:
        if Params.TEMP_DECREASE == TemperatureProfile.LINEAR:
            return lambda tproc, temp: temperature.lin_wait(temperature.q_dt(max_temp, tproc), temp)
        elif Params.TEMP_DECREASE == TemperatureProfile.QUADRATIC:
            return lambda tproc, temp: temperature.q_wait(temperature.q_dt(max_temp, tproc), temp)
        else:
            return lambda tproc, temp: temperature.e_wait(temperature.q_dt(max_temp, tproc), temp)
    else:
        if Params.TEMP_DECREASE == TemperatureProfile.LINEAR:
            return lambda tproc, temp: temperature.lin_wait(temperature.e_dt(max_temp, tproc), temp)
        elif Params.TEMP_DECREASE == TemperatureProfile.QUADRATIC:
            return lambda tproc, temp: temperature.q_wait(temperature.e_dt(max_temp, tproc), temp)
        else:
            return lambda tproc, temp: temperature.e_wait(temperature.e_dt(max_temp, tproc), temp)