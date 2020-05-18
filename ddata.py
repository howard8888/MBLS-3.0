'''
holds many of the data structures needed by CCA1
these will be used by cca1.py module via instantiation ('g') in main_eval()
    of 'Multiple_sessions_data'  (also some global constants copied to g as well)
    include here variables which will persist between missions:
    performance_metric, conscious_memory
most other data variables are initiated at start of each mission (ie, each
    time main_mech.cycles() is called via instantiation ('d') of 'Mapdata'
'''
##START PRAGMAS
#
#temporary pylint bypasses during deprecation/transition devpt work
#pylint: disable=invalid-name
#   prefer not to use snake_case style for very frequent data structure or
#   for small temp variables
#pylint: disable=line-too-long
#pylint: disable=too-many-instance-attributes
##END PRAGMAS

##START GLOBAL CONSTANTS
#
VERSION = 'not specified'
DISPLAY_SYSTEM = False
MEMORY_CHECKING_ON_TEMP = False
FULL_CAUSAL = False
DEBUG = True
FASTRUN = False #True causes skipping of many user inputs
AUTORUN = False #True will run whole session without user input
MOD_CYCLE_REEVALUATE = 5
MAX_CYCLES = 220
TOTAL_ROWS = 4
TOTAL_COLS = 4
GOAL_RANDOM_WALK = '00000000'
GOAL_SKEWED_WALK = '00000001'
GOAL_PRECAUSAL_FIND_HIKER = '11111111'
GOAL_CAUSAL_FIND_HIKER = '11110000'
TRIES_BEFORE_DECLARE_LOCAL_MINIMUM = 2
DEFAULT_VECTOR = '00000000'
DEFAULT_GOAL = GOAL_RANDOM_WALK
DEFAULT_HIPPOCAMPUS = 'HUMAN'
ESCAPE_LEFT = '11111111'
FILLER = '00000000'
REFLEX_ESCAPE = '10011001'
INITIATE_VALUE = 0
##END GLOBAL CONSTANTS


class Multiple_sessions_data:
    '''hold data here that should be kept between sessions
    '''
    def __init__(self):
        '''the following are initiated at program start via instant-
            iation of ddata.Multiple_sessions_data -- 'g' instance:
        '''
        self.performance_metric: list = []
        self.conscious_memory = [['start of conscious_memory']]
        self.sensory_buffer: list = []
        self.debug = DEBUG
        self.fastrun = FASTRUN #True causes skipping of many user inputs
        self.autorun = AUTORUN #True will run whole session without user input
        self.mod_cycle_reevaluate = MOD_CYCLE_REEVALUATE
        self.version = VERSION
        self.display_system = DISPLAY_SYSTEM #nb verbose, print_references in code
        self.memory_checking_on_temp = MEMORY_CHECKING_ON_TEMP
        self.max_cycles = MAX_CYCLES
        self.total_rows = TOTAL_ROWS
        self.total_cols = TOTAL_COLS
        self.goal_random_walk = GOAL_RANDOM_WALK
        self.goal_skewed_walk = GOAL_SKEWED_WALK
        self.goal_precausal_find_hiker = GOAL_PRECAUSAL_FIND_HIKER
        self.goal_causal_find_hiker = GOAL_CAUSAL_FIND_HIKER
        self.tries_before_declare_local_minimum = TRIES_BEFORE_DECLARE_LOCAL_MINIMUM
        #self.default_vector = DEFAULT_VECTOR
        #self.default_goal = DEFAULT_GOAL
        #self.default_hippocampus = DEFAULT_HIPPOCAMPUS
        self.escape_left = ESCAPE_LEFT
        self.filler = FILLER
        self.reflex_escape = REFLEX_ESCAPE
        #self.initiate_value = INITIATE_VALUE


    def __str__(self)-> str:
        '''
        for developmental purposes
        values of the instance.Multiple_sessions_data values
        '''
        print('*******dump: instance.Multiple_sessions_data variables*****\n')
        print('self.performance_metric  ', self.performance_metric)
        print('self.conscious_memory  ', self.conscious_memory)
        print('self.sensory_buffer  ', self.sensory_buffer)
        print('self.debug  ', self.debug)
        print('self.fastrun  ', self.fastrun)
        print('self.autorun', self.autorun)
        print('self.mod_cycle_reevaluate  ', self.mod_cycle_reevaluate)
        print('self.version  ', self.version)
        print('self.display_system  ', self.display_system)
        print('self.memory_checking_on_temp  ', self.memory_checking_on_temp)
        print('additional values -- please look at ddata.py')
        return '*******finished dump: instance.Multiple_sessions_data variables*****\n'


    def printout_conscious_memory(self)->bool:
        '''prints conscious memory and whatever analysis method provides
        '''
        print('\n', self.conscious_memory, '\n')
        return True


    def gconscious(self, item: str, verbose: bool = False)->bool:
        '''goal and conscious module interacts with the emotional and reward module as well
         as the entire CCA1 to provide some overall control of the CCA1’s behavior
         memories of operations occurring in the logic/working memory are temporarily
          kept in the conscious module, allowing improved problem solving as well as
          providing more transparency to CCA1 decision making
        '''
        if verbose:
            print('CHECKPOINT: in conscious method')
        #nano ver emulate with simple list
        #add conscious item to conscious memory
        self.conscious_memory.append(item)
        print('in gconscious')
        return True



class Mapdata:
    '''most of the data variables are held here in Mapdata class
    '''
    def __init__(self):
        '''these data variables are initiated at start of each mission (ie,
                each time main_mech.cycles is called) -- 'd' instance
           be aware the following are initiated at program start via instant-
                iation of ddata.Multiple_sessions_data -- 'g' instance:
                    performance_metric: list = []
                    conscious_memory = [['start of conscious_memory']]
                    sensory_buffer: list = []
        '''
        self.meaningfulness = False
        self.performance_metric_unit = INITIATE_VALUE
        self.evaluation_cycles = INITIATE_VALUE
        self.age_autonomic_calls = INITIATE_VALUE
        self.current_autonomic = FILLER
        self.current_instinct = FILLER
        self.current_goal = DEFAULT_GOAL
        self.current_hippocampus = DEFAULT_HIPPOCAMPUS
        self.h_mem_dirn_goal = None
        self.h_mem_prev_dirn_goal = None
        self.local_minimum = INITIATE_VALUE
        self.cca1_position = (INITIATE_VALUE, INITIATE_VALUE)
        self.hiker_position = (INITIATE_VALUE, INITIATE_VALUE)

        self.forest_map = [['edge', 'edge', 'edge', 'edge', 'edge', 'edge'],
                           ['edge', 'forest', 'forest', 'sh_rvr', 'forest', 'edge'],
                           ['edge', 'lake  ', 'forest', 'forest', 'forest', 'edge'],
                           ['edge', 'forest', 'wtrfall', 'forest', 'forest', 'edge'],
                           ['edge', 'forest', 'forest', 'forest', 'forest', 'edge'],
                           ['edge', 'edge', 'edge', 'edge', 'edge', 'edge']]
        self.int_map = [['edge', '', '', '', '', 'edge'],
                        ['', '', '', '', '', ''],
                        ['', '', '', '', '', ''],
                        ['', '', '', '', '', ''],
                        ['', '', '', '', '', ''],
                        ['edge', '', '', '', '', 'edge']]
        #deprecation/transition note -- full clean up in "micro" version
        #devpt goal is real hardware in "milli" version
        #this emulation/simulation pretends that the 'sensory_inputs' lists below are
        #values received from a video camera/pre-processor, audio/pre-processor, etc

        #visual_inputs data structure is as follows:
        # [ [ possible vector inputs for square 0,0 i,e square 0],
        #    ....
        #  [ possible vector inputs for square 3,3 i,e square 15]  ]
        #data structure of possible vector inputs for any square, eg,#0, is:
        #  [ [possible values for North visual input],[possibles for E],[S],[W] ]
        #thus if the CCA1 is in square 0 right now, then possible values for its
        #video camera/pre-processor to pretend to receive from the North are:
        #['11111100', '11111101', '11011000', '10011100'] -- the software routines
        #will randomly select one of these values, eg, perhaps '11111101'
        #thus in this example when the CCA1 is in square 0 its camera reports
        #visual input '11111101' from the North
        #programmatically this is represented as visual_inputs[0][0][2]
        #ie, visual_inputs[square 0][North possible values][value 2 randomly selected]
        #(note that these visual inputs, the 8 bits of video input, are not random,
        #but are an emulation of what a video camera would produce if it was looking
        #at the squares around (ie, N,E,S,W -- 4 values) and looking at that moment
        #North of square 0, given the landscape features in forest_map (ie, these
        #values are a real emulation/simulation of what a video camera would be
        #reporting for that landscape of the gridworld being used)
        self.visual_inputs = [[['11111100', '11111101', '11011000', '10011100'], ['11000110', '11000111', '11010110', '11000010'], ['11000011', '11110111', '10011111', '01111111'], ['11111100', '11111101', '11011000', '10011100']],
                              [['11111100', '11111101', '11011000', '10011100'], ['00010001', '00010011', '10010001', '00010101'], ['11000110', '11000111', '11010110', '11000010'], ['11000110', '11000111', '11010110', '11000010']],
                              [['11111100', '11111101', '11011000', '10011100'], ['11000110', '11000111', '11010110', '11000010'], ['11000110', '11000111', '11010110', '11000010'], ['11000110', '11000111', '11010110', '11000010']],
                              [['11111100', '11111101', '11011000', '10011100'], ['11111100', '11111101', '11011000', '10011100'], ['11000110', '11000111', '11010110', '11000010'], ['00010001', '00010011', '10010001', '00010101']],
                              [['11100110', '11100111', '11110110', '11100010'], ['11000110', '11000111', '11010110', '11000010'], ['11000110', '11000111', '11010110', '11000010'], ['11111100', '11111101', '11011000', '10011100']],
                              [['11000110', '11000111', '11010110', '11000010'], ['11000110', '11000111', '11010110', '11000010'], ['11000110', '11000111', '11010110', '11000010'], ['11000011', '11110111', '10011111', '01111111']],
                              [['00010001', '00010011', '10010001', '00010101'], ['11000110', '11000111', '11010110', '11000010'], ['00011001', '00011011'], ['11000110', '11000111', '11010110', '11000010']],
                              [['11000110', '11000111', '11010110', '11000010'], ['11111100', '11111101', '11011000', '10011100'], ['11000110', '11000111', '11010110', '11000010'], ['11000110', '11000111', '11010110', '11000010']],
                              [['11000011', '11110111', '10011111', '01111111'], ['11000110', '11000111', '11010110', '11000010'], ['11000110', '11000111', '11010110', '11000010'], ['11111100', '11111101', '11011000', '10011100']],
                              [['11000110', '11000111', '11010110', '11000010'], ['00011001', '00011011'], ['01010000', '01110000', '01010001'], ['11000110', '11000111', '11010110', '11000010']],
                              [['11000110', '11000111', '11010110', '11000010'], ['11000110', '11000111', '11010110', '11000010'], ['11000110', '11000111', '11010110', '11000010'], ['11000110', '11000111', '11010110', '11000010']],
                              [['11000110', '11000111', '11010110', '11000010'], ['11111100', '11111101', '11011000', '10011100'], ['11000110', '11000111', '11010110', '11000010'], ['00011001', '00011011']],
                              [['11000110', '11000111', '11010110', '11000010'], ['01010000', '01110000', '01010001'], ['11111100', '11111101', '11011000', '10011100'], ['11111100', '11111101', '11011000', '10011100']],
                              [['11000110', '11000111', '11010110', '11000010'], ['11000110', '11000111', '11010110', '11000010'], ['11111100', '11111101', '11011000', '10011100'], ['11000110', '11000111', '11010110', '11000010']],
                              [['00011001', '00011011'], ['11000110', '11000111', '11010110', '11000010'], ['11111100', '11111101', '11011000', '10011100'], ['01010000', '01110000', '01010001']],
                              [['11000110', '11000111', '11010110', '11000010'], ['11111100', '11111101', '11011000', '10011100'], ['11111100', '11111101', '11011000', '10011100'], ['11000110', '11000111', '11010110', '11000010']]]
        #auditory_inputs same data structure as visual_inputs
        #(and applies to any other sensors used by the CCA1)
        self.auditory_inputs = [[['00000000', '00100000', '00000001', '00000010'], ['11000000', '11000001', '11000010', '11010000'], ['00010001', '00010011', '00010000', '00100000'], ['00000000', '00000010', '00000001', '00100000']],
                                [['00000000', '00100000', '00000001', '00000010'], ['00010001', '00010011', '00010000', '00100000'], ['11000000', '11000001', '11000010', '11010000'], ['11000000', '11000001', '11000010', '11010000']],
                                [['00000000', '00100000', '00000001', '00000010'], ['11000000', '11000001', '11000010', '11010000'], ['11000000', '11000001', '11000010', '11010000'], ['11000000', '11000001', '11000010', '11010000']],
                                [['00000000', '00100000', '00000001', '00000010'], ['00000000', '00100000', '00000001', '00000010'], ['11000000', '11000001', '11000010', '11010000'], ['00010001', '00010011', '00010000', '00100000']],
                                [['11000000', '11000001', '11000010', '11010000'], ['11000000', '11000001', '11000010', '11010000'], ['11000000', '11000001', '11000010', '11010000'], ['00000000', '00100000', '00000001', '00000010']],
                                [['11000000', '11000001', '11000010', '11010000'], ['11000000', '11000001', '11000010', '11010000'], ['11000000', '11000001', '11000010', '11010000'], ['00010001', '00010011', '00010000', '00100000']],
                                [['00010001', '00010011', '00010000', '00100000'], ['11000000', '11000001', '11000010', '11010000'], ['01010101', '01010111', '01010011', '01000011'], ['11000000', '11000001', '11000010', '11010000']],
                                [['11000000', '11000001', '11000010', '11010000'], ['00000000', '00100000', '00000001', '00000010'], ['11000000', '11000001', '11000010', '11010000'], ['11000000', '11000001', '11000010', '11010000']],
                                [['00010001', '00010011', '00010000', '00100000'], ['11000000', '11000001', '11000010', '11010000'], ['11000000', '11000001', '11000010', '11010000'], ['00000000', '00100000', '00000001', '00000010']],
                                [['11000000', '11000001', '11000010', '11010000'], ['01010101', '01010111', '01010011', '01000011'], ['11110000', '11110001', '11110010', '11110100'], ['11000000', '11000001', '11000010', '11010000']],
                                [['11000000', '11000001', '11000010', '11010000'], ['11000000', '11000001', '11000010', '11010000'], ['11000000', '11000001', '11000010', '11010000'], ['11000000', '11000001', '11000010', '11010000']],
                                [['11000000', '11000001', '11000010', '11010000'], ['00000000', '00100000', '00000001', '00000010'], ['11000000', '11000001', '11000010', '11010000'], ['01010101', '01010111', '01010011', '01000011']],
                                [['11000000', '11000001', '11000010', '11010000'], ['11110000', '11110001', '11110010', '11110100'], ['00000000', '00100000', '00000001', '00000010'], ['00000000', '00100000', '00000001', '00000010']],
                                [['11000000', '11000001', '11000010', '11010000'], ['11000000', '11000001', '11000010', '11010000'], ['00000000', '00100000', '00000001', '00000010'], ['11000000', '11000001', '11000010', '11010000']],
                                [['01010101', '01010111', '01010011', '01000011'], ['11000000', '11000001', '11000010', '11010000'], ['00000000', '00100000', '00000001', '00000010'], ['11110000', '11110001', '11110010', '11110100']],
                                [['11000000', '11000001', '11000010', '11010000'], ['00000000', '00100000', '00000001', '00000010'], ['00000000', '00100000', '00000001', '00000010'], ['11000000', '11000001', '11000010', '11010000']]]
        #
        self.visual_dict = {'11100011':'lake', '01010000':'lost hiker visual', '11111100':'obstruction', '00010001':'shallow river', '00011001':'shallow river + spraying water',
                            '11000110':'forest'}
        self.auditory_dict = {'00000000':'strange silence', '11000000':'forest_noise', '11110000':'human cry help', '00010001':'smooth water sound', '11100000':'bird mating call', '01010101':'water spray noise'}
        self.fused_dict = {'1110001100010001':'lake + smooth water sound -> lake', '1100011011000000':'forest + forest noise -> forest',
                           '0001000100010001':'shallow river + smooth water sound -> shallow_river', '0001100101010101':'shallow river + spraying water + water spray noise -> waterfall',
                           '0101000011110000':'lost hiker visual + human cry help -> hiker', '1111110000000000':'obstruction + strange silence -> edge',
                           '1001111110011111':'forest value used for causal demo case -> forest'}
        #instinct values are goal action values to shape output
        self.instinct_dict = {'10000000':'forward eat/goal', '11000000':'left avoid', '01000000':'right avoid', '00000000':'conserve energy'}
        #autonomic values will shape instinct value along with sensory input values
        self.autonomic_dict = {'00000000':'conserve energy', '00000001':'move to different area',
                               '00000010':'eat', '00000011':'reproduce'}
        #intuit_instinct values are procedural vectors triggered in intuitive logic/physics/psychology or goal plannig
        self.intuitive_instinct_dict = {'1111110000000000':'edge_logic',
                                        '1110001100010001':'water_everywhere_logic',
                                        '0001100101010101':'water_everywhere_logic'}
        #learned_instinct values are procedural vectors triggered in learned logic/physics/psychology or goal plannig
        self.learned_instinct_dict = {'0001000100010001':'test_case_learned'}
        #


    def __str__(self)-> str:
        '''
        for developmental purposes
        values of the instance.Mapdata values
        '''
        print('*******devpt - values of instance.Mapdata variables*****')
        print('self.meaningfulness ', self.meaningfulness)
        print('self.performance_metric_unit', self.performance_metric_unit)
        print('self.evaluation_cycles', self.evaluation_cycles)
        print('self.age_autonomic_calls', self.age_autonomic_calls)
        print('self.current_autonomic', self.current_autonomic)
        print('self.current_instinct', self.current_instinct)
        print('self.current_goal', self.current_goal)
        print('self.current_hippocampus', self.current_hippocampus)
        print('self.h_mem_dirn_goal', self.h_mem_dirn_goal)
        print('self.h_mem_prev_dirn_goal', self.h_mem_prev_dirn_goal)
        print('self.local_minimum', self.local_minimum)
        print('self.cca1_position', self.cca1_position)
        print('self.hiker_position', self.hiker_position)
        print('\nself.forest_map', self.forest_map)
        print('\nself.int_map', self.int_map)
        print('\nself.visual_inputs', self.visual_inputs)
        print('\nself.auditory_inputs', self.auditory_inputs)
        print('\nself.visual_dict', self.visual_dict)
        print('self.auditory_dict', self.auditory_dict)
        print('self.fused_dict', self.fused_dict)
        print('self.instinct', self.instinct_dict)
        print('self.autonomic', self.autonomic_dict)
        print('self.intuitive_instinct', self.intuitive_instinct_dict)
        print('self.learned_instinct', self.learned_instinct_dict)
        return '*******finished printing out instance.Mapdata variables*****\n'


    def print_int_map(self)-> bool:
        '''prints out bird's-eye view of forest which CCA1 has constructed
        from its explorations
        int_map is m x n coordinate system, start 0,0, offset -1,-1 vs forest_map
        -see deprecation note about emulation and replacement with more authentic
        components in finer grain simulations
        '''
        if self.current_goal in (GOAL_SKEWED_WALK, GOAL_RANDOM_WALK):
            print('CCA1 is functioning via random/skewed walk and no internal maps constructed\n')
            return False
        horizontals = "---------------------------------------------------------------------------------------"
        print("\nCCA1 Internal Map of Bird's-Eye View of Forest (* is position of CCA1 {})".format(self.cca1_position))
        print("nb. This is internal map *before* move is made by CCA1")
        print(horizontals + '-')
        m = -1
        for i in self.int_map:
            m = m + 1
            n = -1
            for j in i:
                n = n + 1
                if m in (1, 2, 3, 4) and n in (1, 2, 3, 4) and self.cca1_position == (m - 1, n - 1):
                    j = j + '*'
                print(j.ljust(10), end='  |  ')
            print('\n', horizontals)
        return True

    def print_forest_map(self)-> bool:
        '''prints out bird's-eye view of forest from system values
        CCA1 does not necessarily have this information
        forest_map is m x n coordinate system, start 0,0

        print("Bird's-Eye View of Forest (CCA1 does not have this view)")
        print("-----------------------------------------")
        for i in forest_map:
            for j in i:
                print(j, end='  |  ')
            print("\n-----------------------------------------")
        return True
        #new structure for forest_map making it more similar to int_map
        '''
        horizontals = "---------------------------------------------------------------------------------------"
        print("\nBird's-Eye View of Forest (CCA1 does not have this view)")
        print(horizontals + '-')
        m = -1
        for i in self.forest_map:
            m = m + 1
            n = -1
            for j in i:
                n = n + 1
                if m in (1, 2, 3, 4) and n in (1, 2, 3, 4) and self.cca1_position == (m - 1, n - 1):
                    j = j + '*'
                print(j.ljust(10), end='  |  ')
            print('\n', horizontals)
        return True


    def set_hiker(self, m: int, n: int)-> tuple:
        '''sets hiker position on the forest map
        m rows x n columns coordinates, start 0,0
        **development note: keep hiker set to (3, 1) until modify
        **  method to appropriately alter sensory data that is presented
        **  to the CCA1, ie, visual/auditory/olfactory_possible_inputs[]
        **  for the position of the hiker
        '''
        x = m + 1
        y = n + 1
        if x < 0:
            x = 0
            print('error in map coordinates -- please check code')
        if y < 0:
            y = 0
            print('error in map coordinates -- please check code')
        if x > len(self.forest_map[0])-1:
            x = len(self.forest_map[0]) - 2
            print('error in map coordinates -- please check code')
        if y > len(self.forest_map[0])-1:
            y = len(self.forest_map[0]) - 2
            print('error in map coordinates -- please check code')
        self.hiker_position = (x, y)
        if self.forest_map[x][y] == 'CCA1  ':
            self.forest_map[x][y] = 'RESCUE'
            print('\n**CCA1 has rescued lost hiker**')
        elif self.forest_map[x][y] == 'RESCUE':
            print('\n**CCA1 has already rescued lost hiker**')
        else:
            self.forest_map[x][y] = 'hiker '
            print('\nhiker position set to: ', x-1, y-1)
        self.print_forest_map()
        return x-1, y-1


    def set_CCA1(self, m: int, n: int)-> tuple:
        '''sets CCA1 position on the forest map
            m rows x n columns coordinates, start 0,0
            m,n -> x,y  & cca1_position = x, y
            if forest_map[x][y] == 'hiker ' -> forest_map[x][y] = 'RESCUE'
            if forest_map[x][y] == 'RESCUE' -> print....
            else forest_map[x][y] = 'CCA1  ' &  cca1_position = x, y
            print_forest()
            return x, y
        '''
        x = m + 1
        y = n + 1
        if x < 0:
            x = 0
            print('error in map coordinates -- please check code')
        if y < 0:
            y = 0
            print('error in map coordinates -- please check code')
        if x > len(self.forest_map[0])- 1:
            x = len(self.forest_map[0]) - 2
            print('error in map coordinates -- please check code')
        if y > len(self.forest_map[0]) - 1:
            y = len(self.forest_map[0]) - 2
            print('error in map coordinates -- please check code')
        if self.forest_map[x][y] == 'hiker ':
            self.forest_map[x][y] = 'RESCUE'
            self.cca1_position = x, y
            print('\n**CCA1 has rescued lost hiker**')
        elif self.forest_map[x][y] == 'RESCUE':
            print('\n**CCA1 has rescued lost hiker**')
        else:
            self.forest_map[x][y] = 'CCA1  '
            self.cca1_position = x, y
            print('\nCCA1 position set to: ', x-1, y-1)
        self.print_forest_map()
        return x-1, y-1
            