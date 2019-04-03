import random
from delay_functions import DelayFunction
from scipy.integrate import quad
from params import *


class SeperateChaining:

    def __init__(self,n,distances):
        self.list = [[] for i in range(n)]
        self.distances = distances
        self.function_domain = DelayFunction()
        self.evaluated_functions = [0 for i in range(self.function_domain.number_of_functions)]
        for i in range(n):
            for k in range(n):
                self.list[i].append([])
        self.insert_functions()
        self.evaluated_function()
        self.totalTimeSteps = self.getTotalTimeSteps()



    def evaluated_function(self):
        self.evaluated_functions[0] = self.compute_integral(self.function_domain.no_delay_function,4)
        self.evaluated_functions[1] = self.compute_integral(self.function_domain.constant_delay_function,4)
        self.evaluated_functions[2] = self.compute_integral(self.function_domain.first_bezier_cruve,4)
        self.evaluated_functions[3] = self.compute_integral(self.function_domain.second_bezier_curve,4)
        self.evaluated_functions[4] = self.compute_integral(self.function_domain.smooth_decreasing_curve,4)
        self.evaluated_functions[5] = self.compute_integral(self.function_domain.linear_delay_function,4)
        self.evaluated_functions[6] = self.compute_integral(self.function_domain.sublinear_delay,4)
        self.evaluated_functions[7] = self.compute_integral(self.function_domain.quadratic_delay,4)



    def printList(self):
        print(self.list)

    def insert_functions(self):
         file = Params.FUNCTION_ORDER
         current_index = 0
         with open(file,'r') as f:
              lines = f.readlines()
              total_lines = len(lines)
              for i in range(len(self.list)):
                  inner_list = self.list[i]
                  for k in range(len(self.list)):
                      to_fill_list = inner_list[k]
                      if i == k:
                           to_fill_list.append(0)
                      else:
                           function_position = lines[current_index].strip().split()
                           index  = 0
                           while len(to_fill_list)*4 < self.distances[i] [k]: #Function is defined on 4 units.(Integral will be taken on 4 units).
                                 to_fill_list.append(int(function_position[index])%self.function_domain.get_number_of_functions())
                                 index = index+ 1
                           current_index = current_index + 1
                           if current_index >= total_lines:
                               current_index = current_index % total_lines


    def getTotalTimeSteps(self):
        value = 0
        for i in range(len(self.list)):
            value = value + len(self.list[i])
        return value

    #This one is not used.
    def get_delay_froms(self,first_city,second_city):
        distance = self.distances[first_city][second_city]
        index = 0
        inner_list = self.list[first_city]
        delay_functions = inner_list[second_city]
        sum  = 0;
        index = 0;
        for i in range(len(delay_functions)):
            if distance - index >= 4:
             sum = sum + self.compute_integral(delay_functions[i],4)
            else:
              sum = sum + self.compute_integral(delay_functions[i],distance-index)
        return sum


    def get_delay_from(self,first_city,second_city):
        distance = self.distances[first_city][second_city]
        index = 0
        inner_list = self.list[first_city]
        delay_functions = inner_list[second_city]
        sum  = 0;
        index = 0;
        for i in range(len(delay_functions)):
            if distance - index >= 4:
             sum = sum + delay_functions[i]
            else:
              sum = sum + self.compute_integral(self.function_domain.first_bezier_cruve,distance-index)
        return sum


    def compute_integral(self,f,upper_bound):
        area,error = quad(f, 0, upper_bound, args=()) #Must lie in 0 -4 and we can take rieman-sum.
        return area


