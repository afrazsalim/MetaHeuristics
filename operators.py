import random
from params import *
from Individual import Individual

def mutate(population, max_pt, max_sl=0):
    for individual in population:
        mutate_NL(individual.NL, individual.PTL)
        mutate_PTL(individual.PTL, max_pt)
        if Params.C2_ON:
            mutate_constraints(individual.C2)
        mutate_constraints(individual.C1)

        if Params.PROFILE == SearchProfile.SL:
            old_sl = individual.SL[:]
            mutate_SL(individual.SL, max_sl)
            enforce_changes(old_sl, individual.SL, individual, max_pt)
    return population

def mutate_NL(path, ptl):
    if random.random() <= Params.P_MUT_NL:
        if Params.MUTATION == Mutation.SWAP:
            first = random.randint(0,len(path)-1)
            l = [i for i in range(len(path))]
            l.remove(first)
            second = random.choice(l)
            #second = random.randint(first+1,len(path)-1)
            temp = path[first]
            path[first] = path[second]
            path[second] = temp


        elif Params.MUTATION == Mutation.ADJ:
            first = random.randint(1, len(path) - 2)
            second = first + random.choice([-1,1])
            temp = path[first]
            path[first] = path[second]
            path[second] = temp



        elif Params.MUTATION == Mutation.MUT_INV:
            first = random.randint(0, len(path) - 2)
            second = random.randint(first + 1, len(path) - 1)
            sub_path_NL = path[first:second + 1]
            path[first:second + 1] = reversed(sub_path_NL)


def mutate_PTL(ptl, max_pt):
    for i in range(len(ptl)):
        if random.random() <= Params.P_MUT_PTL:
            # TODO: consider if we should remove the current value of ptl[i] before sampling new value.
            ptl[i] = random.randint(0, max_pt)


def mutate_constraints(constraints):
    for i in range(len(constraints)):
        if random.random() <= Params.P_MUT_C:
            # TODO: consider if we should remove
            # the current value of constraints[i] before sampling new value.
            # maybe use kind of normal distribution centered on current value
            constraints[i] = random.randint(Params.MIN_C_VALUE, Params.MAX_C_VALUE)


def mutate_SL(sl, max_sl):
    for i in range(len(sl)):
        if random.random() <= Params.P_MUT_SL:
            # TODO: consider if we should remove
            # the current value of sl[i] before sampling new value.
            sl[i] = random.randint(1, max_sl[i])

def enforce_changes(old_sl, new_sl, individual, max_pt):
    differential = [new_sl[i] - old_sl[i] for i in range(len(old_sl))]
    for i in range(len(differential)):
        if differential[i] < 0 :
            decrease_pop(differential[i], i, individual)
        elif differential[i] > 0:
            increase_pop(differential[i], i, individual, max_pt)

def increase_pop(amount, city, individual, max_pt):
    for step in range(amount):
        idx = random.randint(0, len(individual.NL)-1)
        individual.NL.insert(idx, city)
        individual.PTL.insert(idx, random.randint(0, max_pt))
        if Params.C2_ON:
            individual.C2.insert(idx, random.randint(Params.MIN_C_VALUE, Params.MAX_C_VALUE))

def decrease_pop(amount, city, individual):
    city_idx = []
    for idx in range(len(individual.NL)):
        if individual.NL[idx] == city:
            city_idx.append(idx)
    random.shuffle(city_idx)
    city_idx = city_idx[0:abs(amount)]
    city_idx.sort()
    new_list_NL = []
    new_list_PTL = []
    new_list_C2 = []
    current_idx = 0
    for i in range(len(individual.NL)):
        if current_idx < len(city_idx) and i == city_idx[current_idx]:
            current_idx += 1
        else:
            new_list_NL.append(individual.NL[i])
            new_list_PTL.append(individual.PTL[i])
            if Params.C2_ON:
                new_list_C2.append(individual.C2[i])

    individual.NL = new_list_NL
    individual.PTL = new_list_PTL
    individual.C2 = new_list_C2

def parent_selection(population, evaluator):
    mating_pool = []
    for i in range(Params.N_OFF):
        #TODO WITH REPLACEMENT -> consider without
        contenders = [ random.choice(population) for _ in range(Params.TOUR_SIZE)]
        wmax_c1, wmax_c2 = create_max_weights(contenders)
        mating_pool.append(max(contenders,
                               key= lambda c : evaluator.fitness_eval(c.NL, c.PTL,
                                                            wmax_c1, wmax_c2)))
    return mating_pool



def survivor_selection(population, offsprings, evaluator):
    # based on delete worse
    pool = population + offsprings
    for i in range(Params.N_OFF):
        indexes = [random.randint(0, len(pool) - 1) for _ in range(Params.TOUR_SIZE)]
        contenders = [ pool[idx] for idx in indexes]
        wmax_c1, wmax_c2 = create_max_weights(contenders)
        del pool[min(indexes, key=
            lambda idx: evaluator.fitness_eval(
                pool[idx].NL, pool[idx].PTL,
                wmax_c1, wmax_c2))]

    # TODO think of a more efficient way to delete from population
    return pool


def create_max_weights(contenders):
    w_max_c1 = [0 for _ in range(contenders[0].ncity)]
    max_visit = max([len(contender.NL) for contender in contenders])
    w_max_c2 = [0 for _ in range(max_visit)]
    idx = max(len(w_max_c1), len(w_max_c2))
    for contender in contenders:
        for i in range(idx):
            if i < len(w_max_c1) and i < len(contender.C1):
                w_max_c1[i] = max(w_max_c1[i], contender.C1[i])
            if Params.C2_ON and i < len(w_max_c2) and i < len(contender.C2) :
                w_max_c2[i] = max(w_max_c2[i], contender.C2[i])
    return w_max_c1, w_max_c2


def crossover(population, max_pt, evaluator):
    pool = population
    #pool = population[:] # Probably no need to copy
    #random.shuffle(pool) # / shuffle
    offsprings = []
    start = 0
    if Params.N_OFF%2 != 0:
        offsprings.append(pool[0])
        start = 1
    for i in range(start, Params.N_OFF, 2):
        if random.randint(0,1) <= Params.P_CROSS:
            if Params.SEARCH == LocalSearch.HILL:
                offsprings.extend(hill_climbing_crossover(pool[i], pool[i + 1], evaluator, max_pt, population))
            else:
                offsprings.extend(cross_operator(pool[i], pool[i+1], max_pt))
        else:
            offsprings.extend([pool[i],pool[i+1]])
    return offsprings

def cross_operator(p1, p2, max_pt):
    min_len = min(len(p1.NL), len(p2.NL))
    off1 = Individual()
    off2 = Individual()

    x = random.randint(0,min_len-1)
    cross_1 = lambda l1, l2: l1[:x] + l2[x:]
    off1.NL = cross_1(p1.NL, p2.NL)
    off2.NL = cross_1(p2.NL, p1.NL)
    off1.PTL = cross_1(p1.PTL, p2.PTL)
    off2.PTL = cross_1(p2.PTL, p1.PTL)
    if Params.C2_ON:
        off1.C2 = cross_1(p1.C2, p2.C2)
        off2.C2 = cross_1(p2.C2, p1.C2)

    x_city = random.randint(0, p1.ncity)
    off1.C1 = p1.C1[:x_city] + p2.C1[x_city:]
    off2.C1 = p2.C1[:x_city] + p1.C1[x_city:]

    if Params.PROFILE == SearchProfile.SL:
        old_sl_1 = off1.compute_SL()
        old_sl_2 = off2.compute_SL()
        off1.SL = p1.SL[:x_city] + p2.SL[x_city:]
        off2.SL = p2.SL[:x_city] + p1.SL[x_city:]
        enforce_changes(old_sl_1, off1.SL, off1, max_pt)
        enforce_changes(old_sl_2, off2.SL, off2, max_pt)

    elif Params.PROFILE == SearchProfile.FIXED:
        new_sl_1 = p1.SL
        old_sl_1 = off1.compute_SL()
        new_sl_2 = p2.SL
        old_sl_2 = off2.compute_SL()
        enforce_changes(old_sl_1, new_sl_1, off1, max_pt)
        enforce_changes(old_sl_2, new_sl_2, off2, max_pt)
        off1.SL = new_sl_1
        off2.SL = new_sl_2

    return [off1, off2]

def hill_climbing_crossover(individual1, individual2, evaluator, max_pt, population):
    eval = lambda p: evaluator.fitness_eval(p.NL, p.PTL,
                                  p.C1, p.C2)
    jump = 0
    while jump < Params.MAX_JUMP:
        step = 0
        stop_step = False
        while step < Params.MAX_STEP and not stop_step:
            stop_step = True
            attempt = 0
            stop_attempt = False
            indi_1 = Individual([*individual1.NL], [*individual1.SL], [*individual1.PTL], [*individual1.C1], [*individual1.C2])
            indi_2 = Individual([*individual2.NL], [*individual2.SL], [*individual2.PTL], [*individual2.C1], [*individual2.C2])
            while attempt < Params.MAX_ATTEMPT and not stop_attempt:
                indi_1, indi_2 = cross_operator(indi_1, indi_2, max_pt)
                attempt += 1
                if max(eval(indi_1), eval(indi_2)) > max(eval(individual1), eval(individual2)):
                    individual1 = indi_1
                    individual2 = indi_2
                    stop_attempt = True

            if stop_attempt:
                step += 1
                stop_step = False

        idx = random.randint(0, len(population) - 1)
        if jump < Params.MAX_JUMP - 1:
            if eval(individual1) < eval(individual2):
                individual1 = population[idx]
            else:
                individual2 = population[idx]
        jump += 1

    return individual1, individual2


