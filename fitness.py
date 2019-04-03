from params import *

class Evaluator:
    def __init__(self, max_temp, distances, requirements, decreasing_func, increasing_func, wait_func,delay_function):
        self.max_temp = max_temp
        self.distances = distances
        self.requirements = requirements
        self.dt = decreasing_func
        self.it = increasing_func
        self.wait_func = wait_func
        self.delay_time = 0
        self.c1_violations = 0
        self.c2_violations = 0
        self.avg_c1_violations = 0
        self.avg_c2_violations= 0
        self.time_dist = 0
        self.delay_function = delay_function
        self.time_penalty = 0
        self.process_time = 0
        self.wait_time = 0
        self.n_eval = 0
        self.avg_c1_weights = 0
        self.avg_c2_weights = 0
        self.avg_c1_violated_weights = 0
        self.avg_c2_violated_weights = 0

    def fitness_eval(self, nl, ptl, c1, c2):
        self.n_eval += 1
        self.c1_violations = 0
        self.c2_violations = 0
        self.avg_c1_violations = 0
        self.avg_c2_violations = 0
        self.process_time = 0
        self.wait_time = 0
        self.time_dist = 0
        self.avg_c1_weights = 0
        self.avg_c2_weights = 0
        self.avg_c1_violated_weights = 0
        self.avg_c2_violated_weights = 0
        city_process = [0 for _ in range(len(c1))]
        city_temp = [(0, 0) for _ in range(len(c1))]
        time = 0
        penalty = 0
        previous_city = nl[0]
        for i_visit in range(len(nl)):
            process_time = ptl[i_visit]
            self.process_time += process_time
            self.time_dist += self.distances[previous_city][nl[i_visit]]
            city_process[nl[i_visit]] += process_time
            time += self.distances[previous_city][nl[i_visit]]
            previous_temp, last_time = city_temp[nl[i_visit]]
            if Params.C2_ON:
                self.avg_c2_weights += c2[i_visit] / len(c2)
                temp = self.calculate_temp(previous_temp, (time-last_time), process_time)
                if temp > self.max_temp:
                    if Params.C_PROPORTIONAL:
                        penalty += c2[i_visit]*(temp-self.max_temp) # other solution is just do c2[i_visit]*1
                    else:
                        penalty += c2[i_visit]*1
                    self.avg_c2_violated_weights += c2[i_visit]
                    self.c2_violations += 1
                    self.avg_c2_violations += (temp-self.max_temp)/len(nl)

                time +=  process_time
            else:
                current_temp = self.dt(previous_temp, (time-last_time))
                wait = self.wait_func(process_time, current_temp)
                self.wait_time += wait
                temp = self.calculate_temp(previous_temp, (time + wait - last_time), process_time)
                time += process_time + wait
                if temp > self.max_temp + 1.1:
                    print("ouille")
                    print(temp, self.max_temp)

            previous_city = nl[i_visit]
            city_temp[nl[i_visit]] = (temp, time)

        bool_cond = self.C1_bool()
        for i in range(len(city_process)):
            self.avg_c1_weights += c1[i] / len(c1)
            if bool_cond(city_process[i], self.requirements[i]):
                self.c1_violations += 1
                self.avg_c1_violated_weights += c1[i]
                self.avg_c1_violations += abs(self.requirements[i] - city_process[i])/len(city_process)
                if Params.C_PROPORTIONAL:
                    penalty += c1[i]*(abs(self.requirements[i] - city_process[i])) # other solution is just c1[i] * 1
                else:
                    penalty += c1[i]*1

        self.time_penalty = penalty
        rescaled_time = 0;
        delay_time = 0
        if Params.DELAY_FUNCTION:
           for i in range(len(nl)-1):
               j = i+1
               delay_time = delay_time + self.delay_function.get_delay_from(nl[i],nl[j])
           rescaled_time = delay_time # add it at the same scale
        self.delay_time = delay_time
        if self.c2_violations != 0:
            self.avg_c2_violated_weights = self.avg_c2_violated_weights / self.c2_violations
        if self.c1_violations != 0:
            self.avg_c1_violated_weights = self.avg_c1_violated_weights / self.c1_violations
        return -(time + penalty + rescaled_time) # so the higher the better

    def calculate_temp(self, previous_temp, elapsed_time, processing_time):
        cooled_temp = self.dt(previous_temp, elapsed_time)
        return self.it(cooled_temp, processing_time)

    @staticmethod
    def C1_bool():
        if Params.C1_ALL:
            return lambda x, y: x!=y
        else:
            return lambda x, y: x < y

