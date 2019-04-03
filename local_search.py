from params import *
import random

def improvement(population, evaluator):
    for individual in population:
        opt_2(individual, evaluator)

def opt_2(individual, evaluator):
    stop = False
    d = 0
    fit = evaluator.fitness_eval(individual.NL, individual.PTL, individual.C1, individual.C2)
    while not stop and d < Params.MAX_DEPTH:
        stop = True
        count = 0
        while count < Params.MAX_NEIGHBOUR:
            first = random.randint(0, len(individual.NL) - 2)
            second = random.randint(first + 1, len(individual.NL) - 1)
            sub_path_NL = individual.NL[first:second + 1]
            path_NL = individual.NL[:first] + list(reversed(sub_path_NL)) + individual.NL[second + 1:]
            new_fit = evaluator.fitness_eval(path_NL, individual.PTL, individual.C1, individual.C2)
            if new_fit > fit:
                fit = new_fit
                individual.NL = path_NL
                stop = False
                break
            count += 1
        d += 1






