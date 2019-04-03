from params import *
from core import load_file, main_loop

def benchmark(test_name):
    best_score = 0
    c1_violations = 0
    c2_violations = 0
    c1_avg = 0
    c2_avg = 0
    time_dist = 0
    process_time = 0
    wait_time = 0
    time_penalty = 0
    delay = 0
    n_eval = 0
    avg_c1_weights = 0
    avg_c2_weights = 0
    avg_c1_violated_weights = 0
    avg_c2_violated_weights = 0

    n_c1_violated = 0
    n_c2_violated = 0
    success_rate = 0

    for i in range(Params.N_INSTANCES):
        print(i , " Iteration")
        distances, city_requirements, max_temp, ncities = load_file("test_case"+str(i)+".itsp")
        best, evaluator = main_loop(distances, city_requirements, max_temp, ncities)
        eval_fit = lambda p: evaluator.fitness_eval(p.NL, p.PTL,
                                                    p.C1, p.C2)
        best_score += eval_fit(best) / Params.N_INSTANCES
        c1_violations += evaluator.c1_violations / Params.N_INSTANCES
        c2_violations += evaluator.c2_violations / Params.N_INSTANCES
        c1_avg += evaluator.avg_c1_violations / Params.N_INSTANCES
        c2_avg += evaluator.avg_c2_violations / Params.N_INSTANCES
        time_dist += evaluator.time_dist / Params.N_INSTANCES
        process_time += evaluator.process_time / Params.N_INSTANCES
        wait_time += evaluator.wait_time / Params.N_INSTANCES
        time_penalty += evaluator.time_penalty / Params.N_INSTANCES
        delay += evaluator.delay_time / Params.N_INSTANCES
        n_eval += evaluator.n_eval / Params.N_INSTANCES
        avg_c1_weights += evaluator.avg_c1_weights / Params.N_INSTANCES
        avg_c2_weights += evaluator.avg_c2_weights / Params.N_INSTANCES
        if evaluator.c1_violations != 0:
            n_c1_violated += 1
            avg_c1_violated_weights += evaluator.avg_c1_violated_weights
        if evaluator.c2_violations != 0:
            n_c2_violated += 1
            avg_c2_violated_weights += evaluator.avg_c2_violated_weights
        if evaluator.c2_violations == 0 and evaluator.c1_violations == 0:
            success_rate += 1 / Params.N_INSTANCES


    if n_c1_violated != 0:
        avg_c1_violated_weights = avg_c1_violated_weights / n_c1_violated
    if n_c2_violated != 0:
        avg_c2_violated_weights = avg_c2_violated_weights / n_c2_violated

    result ="Score: "+str(best_score)+ " violations, C1: "+str(c1_violations)+" C2: "+str(c2_violations)+"\n"+ \
            "avg violations, C1: " + str(c1_avg) + " C2: " + str(c2_avg) + "\n" + \
            "distance time: " + str(time_dist) + " processing time: " + \
            str(process_time) + " wait time: " + str(wait_time) + \
            " penalty time: " + str(time_penalty) + " delay time: " + str(delay) + "\n" + \
            "N eval: " + str(n_eval) + "\n" + \
            "avg c1 weights: " + str(avg_c1_weights) + " avg c1 violated weights: " + str(avg_c1_violated_weights) + "\n" + \
            "avg c2 weights: " + str(avg_c2_weights) + " avg c2 violated weights: " + str(avg_c2_violated_weights) + "\n" + \
            "success rate: "+str(success_rate) + "\n"


    writeResult(test_name, result)





def writeResult(test_name, result):
    s_params = "------ PARAMS -----\n" +\
               "N GEN: " + str(Params.N_GEN) + " N POP: "+str(Params.N_POP) + " N OFF: "+str(Params.N_OFF) + "\n" + \
               "TOUR SIZE:" +str(Params.TOUR_SIZE)+ " MIN C VALUE: "+str(Params.MIN_C_VALUE)+ " MAX C VALUE: " +str(Params.MAX_C_VALUE)+ "\n" + \
               "P MUT NL: " +str(Params.P_MUT_NL)+ " P MUT PTL: "+str(Params.P_MUT_PTL) + " P MUT SL: "+str(Params.P_MUT_SL)+ \
               " P MUT C: " + str(Params.P_MUT_C) + " P CROSS: "+str(Params.P_CROSS)+ "\n" +\
               "C PROPORTIONAL: "+str(Params.C_PROPORTIONAL)+ " C2 ON: "+str(Params.C2_ON)+ " C1 ALL: "+str(Params.C1_ALL)+"\n"+\
               "TEMP INCREASE: "+str(Params.TEMP_INCREASE)+ " TEMP DECREASE: "+str(Params.TEMP_DECREASE)+"\n" +\
               "PROFILE: "+ str(Params.PROFILE)+ " SEARCH: "+str(Params.SEARCH)+ "\n" +\
               "MUTATION: "+str(Params.MUTATION)+ " INIT: "+str(Params.INIT) + "\n"+\
               "MAX ATTEMPTS: "+str(Params.MAX_ATTEMPT)+ " MAX STEPS: "+str(Params.MAX_STEP)+ " MAX JUMP: "+str(Params.MAX_JUMP)+"\n"+\
               "MAX DEPTH: "+str(Params.MAX_DEPTH)+ " MAX NEIGHBOURS: "+str(Params.MAX_NEIGHBOUR)+"\n"
    sep = "-------------------- \n"
    with open("results_1.txt", "a") as file:
        file.write("\n")
        file.write("##### "+test_name+" ######\n")
        file.write(s_params)
        file.write(sep)
        file.write(result)
        file.write(sep)




""""
Params.PROFILE = SearchProfile.FREE
Params.INIT = Initialisation.GREEDY_SL
benchmark("free+greedy_sl")

Params.PROFILE = SearchProfile.SL
Params.INIT = Initialisation.CLASSIC_SL
Params.C_PROPORTIONAL = True
Params.C1_ALL = True
Params.C2_ON = True
benchmark("sl+ classic_sl -> prop true all true c2 true ")

Params.PROFILE = SearchProfile.SL
Params.INIT = Initialisation.CLASSIC_SL
Params.C_PROPORTIONAL = True
Params.C1_ALL = True
Params.C2_ON = False
benchmark("sl+ classic_sl -> prop true all true c2 false ")

Params.PROFILE = SearchProfile.SL
Params.INIT = Initialisation.CLASSIC_SL
Params.C_PROPORTIONAL = True
Params.C1_ALL = False
Params.C2_ON = True
benchmark("sl+ classic_sl -> prop true all False c2 true ")

Params.PROFILE = SearchProfile.SL
Params.INIT = Initialisation.CLASSIC_SL
Params.C_PROPORTIONAL = True
Params.C1_ALL = False
Params.C2_ON = False
benchmark("sl+ classic_sl -> prop true all false c2 false ")

Params.PROFILE = SearchProfile.SL
Params.INIT = Initialisation.CLASSIC_SL
Params.C_PROPORTIONAL = False
Params.C1_ALL = True
Params.C2_ON = True
benchmark("sl+ classic_sl -> prop false all true c2 true ")


Params.PROFILE = SearchProfile.SL
Params.INIT = Initialisation.CLASSIC_SL
Params.C_PROPORTIONAL = False
Params.C1_ALL = True
Params.C2_ON = False
benchmark("sl+ classic_sl -> prop false all true c2 false ")

Params.PROFILE = SearchProfile.SL
Params.INIT = Initialisation.CLASSIC_SL
Params.C_PROPORTIONAL = False
Params.C1_ALL = False
Params.C2_ON = True
benchmark("sl+ classic_sl -> prop false all false c2 true ")

Params.PROFILE = SearchProfile.SL
Params.INIT = Initialisation.CLASSIC_SL
Params.C_PROPORTIONAL = False
Params.C1_ALL = False
Params.C2_ON = False
benchmark("sl+ classic_sl -> prop false all false c2 false ")


Params.PROFILE = SearchProfile.FIXED
Params.INIT = Initialisation.GREEDY_TOT
Params.C_PROPORTIONAL = True
Params.C1_ALL = True
Params.C2_ON = False
benchmark("fixed+ greedy_sl -> prop true all true c2 false ")


Params.PROFILE = SearchProfile.FIXED
Params.INIT = Initialisation.GREEDY_TOT
Params.C_PROPORTIONAL = True
Params.C1_ALL = False
Params.C2_ON = True
benchmark("fixed+ greedy_sl -> prop true all false c2 true ")


Params.PROFILE = SearchProfile.FIXED
Params.INIT = Initialisation.GREEDY_TOT
Params.C_PROPORTIONAL = True
Params.C1_ALL = False
Params.C2_ON = False
benchmark("fixed+ greedy_sl -> prop true all false c2 false ")


Params.PROFILE = SearchProfile.FIXED
Params.INIT = Initialisation.GREEDY_TOT
Params.C_PROPORTIONAL = True
Params.C1_ALL = True
Params.C2_ON = True
benchmark("fixed+ greedy_sl -> prop true all true c2 true ")


Params.PROFILE = SearchProfile.FIXED
Params.INIT = Initialisation.GREEDY_TOT
Params.C_PROPORTIONAL = False
Params.C1_ALL = True
Params.C2_ON = True
benchmark("fixed+ greedy_sl -> prop false all true c2 true ")


Params.PROFILE = SearchProfile.FIXED
Params.INIT = Initialisation.GREEDY_TOT
Params.C_PROPORTIONAL = False
Params.C1_ALL = True
Params.C2_ON = False
benchmark("fixed+ greedy_sl -> prop false all true c2 false ")


Params.PROFILE = SearchProfile.FIXED
Params.INIT = Initialisation.GREEDY_TOT
Params.C_PROPORTIONAL = False
Params.C1_ALL = False
Params.C2_ON = True
benchmark("fixed+ greedy_sl -> prop false all false c2 true ")
"""

Params.PROFILE = SearchProfile.FIXED
Params.INIT = Initialisation.GREEDY_TOT
Params.C_PROPORTIONAL = False
Params.C1_ALL = False
Params.C2_ON = False
benchmark("fixed+ greedy_sl -> prop false all false c2 false ")


"""

Params.PROFILE = SearchProfile.SL
Params.SEARCH = LocalSearch.OPT2
Params.INIT = Initialisation.CLASSIC_SL
benchmark("SL+2opt+classicSL")

#Params.PROFILE = SearchProfile.FIXED
#Params.SEARCH = LocalSearch.OPT2
#Params.INIT = Initialisation.GREEDY_TOT
#benchmark("fixed+2opt+greedy_sl")



#Params.PROFILE = SearchProfile.SL
#Params.SEARCH = LocalSearch.HILL
#Params.INIT = Initialisation.CLASSIC_SL
#benchmark("SL+hill+classicSL")


Params.PROFILE = SearchProfile.FIXED
Params.SEARCH = LocalSearch.HILL
Params.INIT = Initialisation.GREEDY_TOT
benchmark("Fixed+hill+greedy_sl")



Params.PROFILE = SearchProfile.SL
Params.INIT = Initialisation.CLASSIC_SL
Params.TEMP_INCREASE = TemperatureProfile.LINEAR
Params.TEMP_DECREASE = TemperatureProfile.LINEAR
benchmark("sl+classic sl + lin__lin")

Params.PROFILE = SearchProfile.SL
Params.INIT = Initialisation.CLASSIC_SL
Params.TEMP_INCREASE = TemperatureProfile.LINEAR
Params.TEMP_DECREASE = TemperatureProfile.QUADRATIC
benchmark("sl+classic sl + lin__quad")

Params.PROFILE = SearchProfile.SL
Params.INIT = Initialisation.CLASSIC_SL
Params.TEMP_INCREASE = TemperatureProfile.LINEAR
Params.TEMP_DECREASE = TemperatureProfile.EXPONENTIAL
benchmark("sl+classic sl + lin__exp")
"""

"""
Params.PROFILE = SearchProfile.SL
Params.INIT = Initialisation.CLASSIC_SL
Params.TEMP_INCREASE = TemperatureProfile.QUADRATIC
Params.TEMP_DECREASE = TemperatureProfile.LINEAR
benchmark("sl+classic sl + quad_lin")

Params.PROFILE = SearchProfile.SL
Params.INIT = Initialisation.CLASSIC_SL
Params.TEMP_INCREASE = TemperatureProfile.EXPONENTIAL
Params.TEMP_DECREASE = TemperatureProfile.LINEAR
benchmark("sl+classic sl + exp_lin")

Params.PROFILE = SearchProfile.SL
Params.INIT = Initialisation.CLASSIC_SL
Params.TEMP_INCREASE = TemperatureProfile.QUADRATIC
Params.TEMP_DECREASE = TemperatureProfile.QUADRATIC
benchmark("sl+classic sl + quad_quad")

Params.PROFILE = SearchProfile.SL
Params.INIT = Initialisation.CLASSIC_SL
Params.TEMP_INCREASE = TemperatureProfile.EXPONENTIAL
Params.TEMP_DECREASE = TemperatureProfile.QUADRATIC
benchmark("sl+classic sl + exp_quad")


Params.PROFILE = SearchProfile.SL
Params.INIT = Initialisation.CLASSIC_SL
Params.TEMP_INCREASE = TemperatureProfile.QUADRATIC
Params.TEMP_DECREASE = TemperatureProfile.EXPONENTIAL
benchmark("sl+classic sl + quad_exp")

Params.PROFILE = SearchProfile.SL
Params.INIT = Initialisation.CLASSIC_SL
Params.TEMP_INCREASE = TemperatureProfile.EXPONENTIAL
Params.TEMP_DECREASE = TemperatureProfile.EXPONENTIAL
benchmark("sl+classic sl + exp_exp")

Params.PROFILE = SearchProfile.SL
Params.INIT = Initialisation.CLASSIC_SL
Params.TEMP_INCREASE = TemperatureProfile.LINEAR
Params.TEMP_DECREASE = TemperatureProfile.LINEAR
Params.MUTATION = Mutation.ADJ
benchmark("classic sl + sl + adj")

Params.PROFILE = SearchProfile.SL
Params.INIT = Initialisation.CLASSIC_SL
Params.TEMP_INCREASE = TemperatureProfile.LINEAR
Params.TEMP_DECREASE = TemperatureProfile.LINEAR
Params.MUTATION = Mutation.MUT_INV
benchmark("classic sl + sl + mut_inv")

Params.PROFILE = SearchProfile.SL
Params.INIT = Initialisation.GREEDY_SL
Params.TEMP_INCREASE = TemperatureProfile.LINEAR
Params.TEMP_DECREASE = TemperatureProfile.LINEAR
Params.MUTATION = Mutation.SWAP
benchmark("greedy_sl + sl + swap")

Params.PROFILE = SearchProfile.SL
Params.INIT = Initialisation.GREEDY_TOT
Params.TEMP_INCREASE = TemperatureProfile.LINEAR
Params.TEMP_DECREASE = TemperatureProfile.LINEAR
Params.MUTATION = Mutation.SWAP
benchmark("greedy_tot + sl + swap")

Params.PROFILE = SearchProfile.SL
Params.INIT = Initialisation.RANDOM
Params.TEMP_INCREASE = TemperatureProfile.LINEAR
Params.TEMP_DECREASE = TemperatureProfile.LINEAR
Params.MUTATION = Mutation.SWAP
benchmark("random + sl + swap")



Params.PROFILE = SearchProfile.FIXED
Params.INIT = Initialisation.GREEDY_TOT
Params.TEMP_INCREASE = TemperatureProfile.LINEAR
Params.TEMP_DECREASE = TemperatureProfile.LINEAR
benchmark("fixed+greedy sl + lin__lin")






Params.PROFILE = SearchProfile.FIXED
Params.INIT = Initialisation.GREEDY_TOT
Params.TEMP_INCREASE = TemperatureProfile.LINEAR
Params.TEMP_DECREASE = TemperatureProfile.QUADRATIC
benchmark("fixed+ greedy_sl + lin__quad")

Params.PROFILE = SearchProfile.FIXED
Params.INIT = Initialisation.GREEDY_TOT
Params.TEMP_INCREASE = TemperatureProfile.LINEAR
Params.TEMP_DECREASE = TemperatureProfile.EXPONENTIAL
benchmark("fixed+ greedy_sl + lin__exp")

Params.PROFILE = SearchProfile.FIXED
Params.INIT = Initialisation.GREEDY_TOT
Params.TEMP_INCREASE = TemperatureProfile.QUADRATIC
Params.TEMP_DECREASE = TemperatureProfile.LINEAR
benchmark("fixed+ greedy_sl + quad_lin")

Params.PROFILE = SearchProfile.FIXED
Params.INIT = Initialisation.GREEDY_TOT
Params.TEMP_INCREASE = TemperatureProfile.EXPONENTIAL
Params.TEMP_DECREASE = TemperatureProfile.LINEAR
benchmark("fixed+ greedy_sl + exp_lin")
Params.PROFILE = SearchProfile.FIXED
Params.INIT = Initialisation.GREEDY_TOT
Params.TEMP_INCREASE = TemperatureProfile.QUADRATIC
Params.TEMP_DECREASE = TemperatureProfile.QUADRATIC
benchmark("fixed+ greedy_sl + quad_quad")

Params.PROFILE = SearchProfile.FIXED
Params.INIT = Initialisation.GREEDY_TOT
Params.TEMP_INCREASE = TemperatureProfile.EXPONENTIAL
Params.TEMP_DECREASE = TemperatureProfile.QUADRATIC
benchmark("fixed+ greedy_sl + exp_quad")


Params.PROFILE = SearchProfile.FIXED
Params.INIT = Initialisation.GREEDY_TOT
Params.TEMP_INCREASE = TemperatureProfile.QUADRATIC
Params.TEMP_DECREASE = TemperatureProfile.EXPONENTIAL
benchmark("fixed+ greedy_sl + quad_exp")

Params.PROFILE = SearchProfile.FIXED
Params.INIT = Initialisation.GREEDY_TOT
Params.TEMP_INCREASE = TemperatureProfile.EXPONENTIAL
Params.TEMP_DECREASE = TemperatureProfile.EXPONENTIAL
benchmark("fixed+ greedy_sl + exp_exp")

Params.PROFILE = SearchProfile.FIXED
Params.INIT = Initialisation.GREEDY_TOT
Params.TEMP_INCREASE = TemperatureProfile.LINEAR
Params.TEMP_DECREASE = TemperatureProfile.LINEAR
Params.MUTATION = Mutation.ADJ
benchmark("fixed+ greedy_sl + adj")

Params.PROFILE = SearchProfile.FIXED
Params.INIT = Initialisation.GREEDY_TOT
Params.TEMP_INCREASE = TemperatureProfile.LINEAR
Params.TEMP_DECREASE = TemperatureProfile.LINEAR
Params.MUTATION = Mutation.MUT_INV
benchmark("fixed+ greedy_sl + mut_inv")



Params.PROFILE = SearchProfile.FIXED
Params.INIT = Initialisation.GREEDY_SL
Params.TEMP_INCREASE = TemperatureProfile.LINEAR
Params.TEMP_DECREASE = TemperatureProfile.LINEAR
Params.MUTATION = Mutation.SWAP
benchmark("greedy_tot + fixed + swap")

Params.PROFILE = SearchProfile.FIXED
Params.INIT = Initialisation.RANDOM
Params.TEMP_INCREASE = TemperatureProfile.LINEAR
Params.TEMP_DECREASE = TemperatureProfile.LINEAR
Params.MUTATION = Mutation.SWAP
benchmark("random + fixed + swap")

Params.PROFILE = SearchProfile.FIXED
Params.INIT = Initialisation.CLASSIC_SL
Params.TEMP_INCREASE = TemperatureProfile.LINEAR
Params.TEMP_DECREASE = TemperatureProfile.LINEAR
Params.MUTATION = Mutation.SWAP
benchmark("classicl_sl + fixed + swap")

"""
