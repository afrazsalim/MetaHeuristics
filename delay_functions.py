
class DelayFunction:

    def __init__(self):
        self.number_of_functions = 8
        self.list = []
        self.list.append(self.no_delay_function)
        self.list.append(self.constant_delay_function)
        self.list.append(self.first_bezier_cruve)
        self.list.append(self.second_bezier_curve)
        self.list.append(self.smooth_decreasing_curve)
        self.list.append(self.linear_delay_function)
        self.list.append(self.quadratic_delay)
        self.list.append(self.sublinear_delay)



    def get_function(self,val):
        return self.list[val]

    def get_number_of_functions(self):
        return (len(self.list))

    def no_delay_function(self,x):
        return 0

    def constant_delay_function(self,x):
        return 1

    def first_bezier_cruve(self,x):
        return (x**2/12)*(4-x)

    def second_bezier_curve(self,x):
        return (x/12)*(4-x)**2

    def smooth_decreasing_curve(self,x):
        return (1-x**2/15)

    def linear_delay_function(self,x):
        return x

    def quadratic_delay(self,x):
        return 2*x-(x**2)/2

    def sublinear_delay(self,x):
      return 0.1*x


