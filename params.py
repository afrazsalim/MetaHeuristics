from enum import Enum

class TemperatureProfile(Enum):
    LINEAR = 1
    QUADRATIC = 2
    EXPONENTIAL = 3

class SearchProfile(Enum):
    FREE = 1
    FIXED = 2
    SL = 3

class Mutation(Enum):
    MUT_INV = 1
    SWAP = 2
    ADJ = 3

class Initialisation(Enum):
    RANDOM = 1
    GREEDY_SL = 2
    GREEDY_TOT = 3
    CLASSIC_SL = 4

class LocalSearch(Enum):
    NONE = 1
    OPT2 = 2
    HILL = 3

class Params:
    #FILE = "teso_rpz.itsp"
    #FILE = "itsp_test_pham.itsp2"
    FILE = "belgiumtour2.itsp"
    FUNCTION_ORDER = "functionsOrder/order1.txt"


    N_POP = 50
    N_GEN = 400
    N_OFF = round(N_POP/2)
    TOUR_SIZE = 4
    MIN_C_VALUE = 1
    MAX_C_VALUE = 50
    #MAX_TEMP = 10 ## OVERRIDDEN IN PARSING

    P_MUT_NL = 0.4
    P_MUT_PTL = 0.02
    P_MUT_C = 0.1
    P_MUT_SL = 0.01
    P_CROSS = 1

    SIZE_COEFF = 1.2
    SL_COEFF = 1.5
    MAX_DEPTH = 15
    MAX_NEIGHBOUR = 15

    DELAY_FUNCTION = True
    SIMPLE_MEASURE = False
    NUMBER_OF_BESTSOLUTIONS = 20
    MULTIPLICATOR = 0.0001
    ElISTISM_PERCENTAGE = 0.5
    INCREASING_FACTOR = 0.2
    MAX_CHANCES = 5
    isActivated = True

    C_PROPORTIONAL = True
    C2_ON = False
    C1_ALL = False

    TEMP_INCREASE = TemperatureProfile.LINEAR
    TEMP_DECREASE = TemperatureProfile.LINEAR
    PROFILE = SearchProfile.FIXED
    MUTATION = Mutation.SWAP
    INIT = Initialisation.GREEDY_TOT
    SEARCH = LocalSearch.NONE

    MAX_ATTEMPT = 10
    MAX_STEP = 3
    MAX_JUMP = 5


    # DATASET
    N_INSTANCES =30;
