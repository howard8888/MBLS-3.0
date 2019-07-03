#!/usr/bin/env python
#utf-8 usage auto default in Python3
#ok with colab

#Deprecation Transition Note
#April 2019 Version 3 of MBLS/MBCA is being transitioned to
#"nano"/"micro"/"mini"/"full" MBCA coarse/fine grain simulations
#deprecated code below left for scaffolding purposes -- will be
#removed in future & coarse/fine grain new code will be packaged
#--> #H3 scaffolded version to replace previous scaffolded version
#--> April 17/19 origin of scaffolding code -- rebuild G3 versions from
# H3 version from this scaffolding

#temporary pylint bypasses during deprecation/transition devpt work
#pylint: disable=line-too-long
#pylint settings
#pylint: disable=invalid-name
#prefer not to use snake_case style for small temp variables
#pylint: disable=unused-import
#pylint: disable=too-many-lines
#pylint: disable=unused-import
#pylint: disable=bare-except
#pylint: disable=fixme
#pylint: disable=too-many-function-args
#pylint: disable=redefined-outer-name
#pylint: disable=global-statement
#pylint: disable=unexpected-keyword-arg
#pylint: disable=too-many-branches
#pylint: disable=too-many-statements
#pylint: disable=too-many-arguments
#pylint: disable=too-many-return-statements
#pylint: disable=line-too-long
#pylint: disable=pointless-string-statement


'''
Meaningful-Based Cognitive Architecture
Nanosimulation of Microsimulation of Minisimulation of Full Simulation of MBCA
Simulation to focus on subsymbolic vs symbolic data streams

Python 3.6; Compatible with GPU CUDA usage for PyTorch
Verified for use with Google Colab Jupyter Notebook GPUs

"nano" simulation version:
PURPOSE: Provide a scaffolding, ie, an emulation of full MBCA, so that
         more authentic components can be dropped into "micro" and other
         finer-grain simulations of the MBCA
##
for indexing/layout aid:
forest_map = [['forest0', 'forest1', 'sh_rvr2', 'forest3'],
              ['lake 4 ', 'forest5-', 'forest6-', 'forest7'],
              ['forest8', 'forest9-', 'ww_rvr10-', 'forest11'],
              ['forest12', 'hiker13', 'forest14', 'forest15']]
mbca_map = <offset 1, 1 due to including edge cells>
#                               N               E               S                       W
visual_possible_inputs = [ 0[['10011000', ...], ['11000110'], ['11111111'], ['10011000']], forest, MBCA initial
                           1[['10011000'], ['00010001'], ['11000110'], ['11000110']], forest
                           2[['10011000'], ['11000110'], ['11000110'], ['11000110']], sh_rvr
                           3[['10011000'], ['10011000'], ['11000110'], ['00010001']], forest
                           4[['11000110'], ['11000110'], ['11000110'], ['10011000']], lake
                           5[['11000110'], ['11000110'], ['11000110'], ['11111111']], forest
                           6[['00010001'], ['11000110'], ['00011001'], ['11000110']], forest
                           7[['11000110'], ['10011000'], ['11000110'], ['11000110']], forest
                           8[['11111111'], ['11000110'], ['11000110'], ['10011000']], forest
                           9[['11000110'], ['00011001'], ['01010000'], ['11000110']], forest
                           10[['11000110'], ['11000110'], ['11000110'], ['11000110']], ww_rvr
                           11[['11000110'], ['10011000'], ['11000110'], ['00011001']], forest
                           12[['11000110'], ['01010000'], ['10011000'], ['10011000']], forest
                           13[['11000110'], ['11000110'], ['10011000'], ['11000110']], hiker
                           14[['00011001'], ['11000110'], ['10011000'], ['01010000']], forest
                           15[['11000110'], ['10011000'], ['10011000'], ['11000110']]  forest     ]
                           nb. ['10011000', ...<many possible for each cell and dirn>]

visual_actual_inputs = {'11111111':'lake', '01010000':'lost hiker visual', '10011000':'obstruction', '00010001':'shallow river', '00011001':'shallow ww rvr',
                        '11000110':'forest'}
##
'''
##standard imports -- being used
import pdb
import random
import math
import sys
import platform
import os.path
#standard imports -- not used at present
import time
import pickle
import threading
import logging
from io import StringIO
import numpy as np
import torch
#import schedule #--issues on colab
from pympler import summary, muppy


##nonstandard lib imports being used
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


##global constants
FULL_CAUSAL = False
DEBUG = True
MOD_CYCLE_REEVALUATE = 5
CYCLES_TO_COMPLETE = 220
TOTAL_ROWS = 4
TOTAL_COLS = 4
GOAL_RANDOM_WALK = '00000000'
GOAL_SKEWED_WALK = '00000001'
GOAL_FIND_HIKER = '11111111'
TRIES_BEFORE_DECLARE_LOCAL_MINIMUM = 2
DEFAULT_VECTOR = '00000000'
DEFAULT_GOAL = GOAL_RANDOM_WALK
DEFAULT_HIPPOCAMPUS = 'LAMPREY'
ESCAPE_LEFT = '11111111'
FILLER = '00000000'
REFLEX_ESCAPE = '10011001'
INITIATE_VALUE = 0
MOVE_NORTH = '0000'
MOVE_EAST = '0001'
MOVE_SOUTH = '0010'
MOVE_WEST = '0011'
MOVE_STOP = '1111'
MOVE_JUMP = '1010'
#global constants -- hardware emulation
#deprecation/transition note -- full clean up in "micro" version
#devpt goal is actual hardware in "mini" version
visual_possible_inputs = [[['11111100', '11111101', '11011000', '10011100'], ['11000110', '11000111', '11010110', '11000010'], ['11000011', '11110111', '10011111', '01111111'], ['11111100', '11111101', '11011000', '10011100']],
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
#
auditory_possible_inputs = [[['00000000', '00100000', '00000001', '00000010'], ['11000000', '11000001', '11000010', '11010000'], ['00010001', '00010011', '00010000', '00100000'], ['00000000', '00000010', '00000001', '00100000']],
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
visual_actual_inputs = {'11100011':'lake', '01010000':'lost hiker visual', '11111100':'obstruction', '00010001':'shallow river', '00011001':'shallow river + spraying water',
                        '11000110':'forest'}
auditory_actual_inputs = {'00000000':'strange silence', '11000000':'forest_noise', '11110000':'human cry help', '00010001':'smooth water sound', '11100000':'bird mating call', '01010101':'water spray noise'}
fused_actual_inputs = {'1110001100010001':'lake + smooth water sound -> lake', '1100011011000000':'forest + forest noise -> forest',
                       '0001000100010001':'shallow river + smooth water sound -> shallow_river', '0001100101010101':'shallow river + spraying water + water spray noise -> whitewater river',
                       '0101000011110000':'lost hiker visual + human cry help -> hiker', '1111110000000000':'obstruction + strange silence -> edge'}
#
#forest values are fused sensory input values
forest = {'11111111':'lake E', '11110000':'human cry help N', '11110001':'human cry help E', '11110010':'human cry help S', '111100011':'human cry help W',
          '11100000':'bird mating call N', '11100001':'bird mating call E', '11100010':'bird mating call S', '11100011':'bird mating call W',
          '01010000':'lost hiker visual N', '01010001':'lost hiker visual E', '01010010':'lost hiker visual S', '01010011':'lost hiker visual W',
          '11000000':'forest_noise N', '11000001':'forest_noise E', '11000010':'forest_noise S', '11000011':'forest_noise W',
          '10000000':'perfume/cologne odor N', '10000001':'perfume/cologne odor E', '10000010':'perfume/cologne odor S', '10000011':'perfume/cologne odor W',
          '10011001':'lake S'
          }
#instinct values are goal action values to shape output
instinct = {'10000000':'forward eat/goal', '11000000':'left avoid', '01000000':'right avoid', '00000000':'conserve energy'}
#autonomic values will shape instinct value along with sensory input values
autonomic = {'00000000':'conserve energy', '00000001':'move to different area',
             '00000010':'eat', '00000011':'reproduce'}


##global variables
#intentional use of these globals for better understanding of program operation
#intentionally prefer not to pass these in/out of methods or put in OO framework
#
#global variables -- only initiated at start
performance_metric = []
conscious_memory = [['start of conscious_memory']]

#global variables -- initiated each run via initiate_global_variables()
performance_metric_unit = INITIATE_VALUE
evaluation_cycles = INITIATE_VALUE
age_autonomic_calls = INITIATE_VALUE
current_autonomic = FILLER
current_instinct = FILLER
current_goal = DEFAULT_GOAL
current_hippocampus = DEFAULT_HIPPOCAMPUS
h_mem_dirn_goal = None
h_mem_prev_dirn_goal = None
local_minimum = INITIATE_VALUE
MBCA_position = (INITIATE_VALUE, INITIATE_VALUE)
hiker_position = (INITIATE_VALUE, INITIATE_VALUE)
forest_map = [['forest', 'forest', 'sh_rvr', 'forest'],
              ['lake  ', 'forest', 'forest', 'forest'],
              ['forest', 'forest', 'ww_rvr', 'forest'],
              ['forest', 'forest', 'forest', 'forest']]
mbca_map = [['edge', '', '', '', '', 'edge'],
            ['', '', '', '', '', ''],
            ['', '', '', '', '', ''],
            ['', '', '', '', '', ''],
            ['', '', '', '', '', ''],
            ['edge', '', '', '', '', 'edge']]


#
#sandbox here to quickly try out things -- please erase code afterwards


#input('sandbox code has finished')
#


##START METHODS     START METHODS
def choose_simulation():
    '''before evaluation cycles of a simulation version start, user can choose which
    emulation/simulation to run
    returns an integer corresponding to simulation version chosen
    '''
    print('\nMBCA   Meaningful Based Cognitive Architecture\n')
    print('Welcome to the MBCA Emulator/Simulator\n')
    print('Simulation: Rescuing a Lost Hiker in a Wumpus World Uninhabited Forest\n')
    print('Please choose which version of the MBCA emulation/simulation you would like to')
    print('  run in the Wumpus World.')
    print('(You will then be prompted to choose characteristics of that version)')
    print('\nThe following choices are available: ')
    print('-1. Exit from program')
    print('1. MBCA nano version D')
    print('2. MBCA nano version G (default if hit ENTER)')
    print('3. MBCA micro version beta')
    print('4. MBCA full simulation version 2018 code')
    print('5. MBCA full simulation version beta')
    print('6. AlexNet PyTorch implementation in same Wumpus World')
    print('7. PyTorch RL (conv1-3&fc4-5 layers) in same Wumpus World')
    print('\n\nAPRIL 2019 DEPRECATION & FUNCTIONAL NOTE:')
    print('MBLS-3 simulations are being converted to coarse and fine grain simulations --')
    print('"nano", "micro", "mini" and "full" simulations')
    print('The "nano" version is more an emulation that provides scaffolding to insertion of')
    print('more authentic components in the "micro" and more fine grained simulations.')
    print('TO DO - REMOVE \n')
    try:
        simulation_version_choice = int(input('Please make a selection: '))
    except:
        print('ENTER or nonstandard choice, thus default nano version G selected')
        return 2
    if simulation_version_choice == -1:
        print('Exit choice....')
        return -1
    if simulation_version_choice not in (1, 2, 3, 4, 5, 6, 7):
        print('Choice not found, thus default nano version G selected')
        return 2
    return simulation_version_choice


def welcome(to_print, print_references=False, display_system=False):
    '''print welcome message
    optional print system and version information
    '''
    if to_print == '':
        to_print = 'SPECIFY SUBMODULE OR MODULE NAME'
    print('\n****', to_print, '****')
    print('\n##Start Nano Sim of Micro Sim of Mini-Sim of MBCA Simulation##')
    print('Test large scale algo idea #G1 (code rewrite in progress June 2019 -- compare')
    print('   different organisms, i.e., random walk to basic instinct to full causality)\n')
    print('The term "MBCA" is here used as an MBCA computational device + a legged robot.')
    print('The "MBCA" must decide how to proceed through a Wumpus World representing an')
    print('uninhabited forest where a hiker is lost, and reach and save the hiker, while')
    print('avoiding dangers along the way.\n')
    if print_references:
        print_globals_debug('inside welcome')
    if display_system:
        try:
            print('\n--> OPTION to display platform information:')
            print('MBLS Project: Python installed: ', os.path.dirname(sys.executable))
        except:
            print('Did not find where Python installed.')

        try:
            #print('Version {} of "{}" was last saved/modified {}.'
            #     .format(VERSION_NUMBER, VERSION_FILE_NAME, time.ctime(
            #         os.path.getmtime(VERSION_FILE_NAME))))
            print('Platform Info (via StdLib): \n  ',
                  'os.name:', os.name, ', sys.platform:', sys.platform,
                  ', platform.system:', platform.system(),
                  ', platform.release:', platform.release(),
                  '\n  ', 'platform.processor:', platform.processor(), '\n  ',
                  'sys.maxsize (9223372036854775807 for 64 bit Python): ', sys.maxsize)
            #pylint: disable=no-member
            device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
            #pylint: enable=no-member
            print('   CPU only or GPU device/service detected: ', device)
            MEMORY_CHECKING_ON_TEMP = False
            if MEMORY_CHECKING_ON_TEMP:
                print("   Verify memory -- create 10,000 x 10,000 Numpy matrix ....")
                print("   Interim:100x100")
                print(np.zeros((100, 100)))
            print("   Ok.... basic infrastructure in place for program to run....")
        except:
            print('Exception occurred in retrieving platform specifications.')
    return True


def setup_MBCA_wumpusworld(message="", verbose=True):
    '''set up MBCA Wumpus World, ie, position of the lost hiker, the MBCA,
    possibly lakes and shallow rivers and shallow whitewater rivers'''
    welcome('NANO SIM', print_references=False, display_system=False)
    print("Let's put the MBCA at the m x n origin (0,0): ")
    set_MBCA(0, 0)
    print("\nNow let's put the lost hiker at m x n position (3,1): ")
    set_hiker(3, 1)
    set_current_goal()
    sleep_wake('SLEEP/WAKE')
    print_globals_debug(message, verbose)


def initiate_global_variables():
    '''initiate global variables
    note that performance_metric is only initiated at program start
    forest_map, forest, instinct, autonomic
    '''
    #make global so can modify with initial values
    global performance_metric_unit
    global evaluation_cycles
    global age_autonomic_calls
    global current_autonomic
    global current_instinct
    global current_goal
    global current_hippocampus
    global h_mem_dirn_goal
    global h_mem_prev_dirn_goal
    global local_minimum
    global MBCA_position
    global hiker_position
    global forest_map
    global mbca_map
    #initiate
    performance_metric_unit = INITIATE_VALUE
    evaluation_cycles = INITIATE_VALUE
    age_autonomic_calls = INITIATE_VALUE
    current_autonomic = FILLER
    current_instinct = FILLER
    current_goal = DEFAULT_GOAL
    current_hippocampus = DEFAULT_HIPPOCAMPUS
    h_mem_dirn_goal = None
    h_mem_prev_dirn_goal = None
    local_minimum = 0
    MBCA_position = (INITIATE_VALUE, INITIATE_VALUE)
    hiker_position = (INITIATE_VALUE, INITIATE_VALUE)
    forest_map = [['forest', 'forest', 'sh_rvr', 'forest'],
                  ['lake  ', 'forest', 'forest', 'forest'],
                  ['forest', 'forest', 'ww_rvr', 'forest'],
                  ['forest', 'forest', 'forest', 'forest']]
    mbca_map = [['edge', '', '', '', '', 'edge'],
                ['', '', '', '', '', ''],
                ['', '', '', '', '', ''],
                ['', '', '', '', '', ''],
                ['', '', '', '', '', ''],
                ['edge', '', '', '', '', 'edge']]
    return True


def exit_program():
    '''orderly shutdown of program
    "nano" version no intermediate PyTorch structures to save
    '''
    print('Orderly shutdown of program via exit_program()')
    sys.exit()
    #pdb.set_trace()


def devpt_timer(all_goals, age_autonomic_calls):
    '''depending on the age of the MBCA different procedural vectors are
    returned from the instinctual core goals module
    -the instinctual core goals module, which is affected by the maturity stage of the MBCA via
     this developmental timer, feeds intuitive logic, intuitive physics,
     intuitive psychology and/or intuitive goals planning procedural vectors into the groups of
     HLNs configured as logic/working memory units.
    nano version -- emulation to allow drop insertion of more authentic
     components
    '''
    if age_autonomic_calls < 10000:
        return all_goals
    all_goals['GOAL_POST_MATURE'] = 'consider transfer of learned knowledge'
    return all_goals


def set_current_goal(goal_desired=''):
    '''at start of program the current goal of the instinctual core goals module must
    be set, for example to find a lost hiker or perhaps just to display a random walk
    in between periods when must find a lost hiker (yes....energy wasteful for random
    walk but purpose is to exercise the system)
    GOAL_RANDOM_WALK = '00000000'
    GOAL_SKEWED_WALK = '00000001'
    GOAL_FIND_HIKER = '11111111'
    DEFAULT_GOAL = GOAL_RANDOM_WALK
    '''
    global current_goal
    global current_hippocampus
    all_goals = {GOAL_RANDOM_WALK:'random walk',
                 GOAL_SKEWED_WALK:'skewed to S and E given 0 0 start(==navgn help)',
                 GOAL_FIND_HIKER:'find the hiker'}
    allowed_goals = devpt_timer(all_goals, age_autonomic_calls)
    if goal_desired in allowed_goals:
        current_goal = goal_desired
        return current_goal
    print('\nIn this version of the nano MBCA simulation, you pick what type of cognition to')
    print('  emulate in the Wumpus World.')
    print('The following choices are available: ')
    print('1. Completely random walk')
    print('2. Random walk with some non-specific broad directional instinctual help')
    print('3. Pre-causal find the hiker')
    print('4. Basic causal find the hiker')
    print('5. Full causal find the hiker')
    try:
        a_a = int(input('Please make a selection: '))
    except:
        print('Default goal of pre-causal find the hiker selected')
        a_a = 3
    if a_a  not in (1, 2, 3, 4, 5):
        print('Default goal of pre-causal find the hiker selected')
        a_a = 3
    #non-precausal/causal operation
    if a_a == 1:
        current_goal = GOAL_RANDOM_WALK
        current_hippocampus = 'LAMPREY'
    if a_a == 2:
        current_goal = GOAL_SKEWED_WALK
        current_hippocampus = 'LAMPREY'
    #choose hippocampus if precausal/causal operation
    if a_a in (3, 4, 5):
        current_goal = GOAL_FIND_HIKER
        if a_a in (4, 5):
            print('Software modification -- basic and full causal not available for moment')
            print('Reverting to Pre-Causal')
            current_goal = GOAL_FIND_HIKER
        print('\nPlease choose type of "hippocampus" which will encompass the structure')
        print(' and algorithms access used for spatial movements which will ultimately')
        print(' find (or not find and be damaged by a hazard or loss of energy) the hiker.')
        print('1. Lamprey hippocampal/pallium analogue')
        print('2. Fish hippocampal/pallium analogue')
        print('3. Reptile hippocampal/pallium analgoue')
        print('4. Mammalian hippocampus')
        print('5. Human hippocampus - note: will default to lower level in precausal mode')
        print('6. Superintelligence level 1 - note: will default to lower level in precausal mode')
        print('7. Superintelligence level 2 - note: will default to lower level in precausal mode')
        try:
            b_b = int(input('Please make a selection:'))
        except:
            print('Default reptile hippocampal/pallium analogue selected')
            b_b = 3
        if b_b not in (1, 2, 3, 4, 5, 6, 7):
            print('Default reptile hippocampal/pallium analogue selected')
            b_b = 3
        if b_b == 1:
            current_hippocampus = 'LAMPREY'
        if b_b == 2:
            current_hippocampus = 'FISH'
        if b_b == 3:
            current_hippocampus = 'REPTILE'
        if b_b == 4:
            current_hippocampus = 'MAMMAL'
        if b_b == 5:
            current_hippocampus = 'HUMAN'
        if b_b == 6:
            current_hippocampus = 'SUPERINTELLIGENCE'
        if b_b == 7:
            current_hippocampus = 'SUPERINTELLIGENCE2'
    print('\ncurrent_goal is set to {} {}'.format(current_goal, allowed_goals[current_goal]))
    print('current_hippocampus is set to {}'.format(current_hippocampus))

    return current_goal


def sleep_wake(to_print):
    '''sleep/wake and energy cycles
    this version created for nano sim
    please update docstring for more complex sleep/wake algos
    please consider using input values for more complex sleep/wake algos
    '''
    if to_print == '':
        to_print = 'SPECIFY SUBMODULE OR MODULE NAME'
    print('\n-->', to_print)
    print('Simplified nano simulation of sleep/wake cycle')
    print('Entity is now sleeping....')
    print('Entity has now woken up and remainder of simulation')
    print('until ending should be some daily activities for that day')
    print('before another sleep cycle starts....')
    return True


def print_globals_debug(message="", verbose=True):
    '''for debug purposes print all global variables except forest map array
    '''
    if DEBUG:
        if verbose:
            print('\n--------------------------------')
            if message:
                print(message)
            print('For debug global (abbreviated) variables (except forest_map) are as follows:')
            print('ev_cycles, age_a_calls, curr_auton, curr_inst, curr_goal, MBCA_pos, hik_pos')
        print(evaluation_cycles, '        ', age_autonomic_calls, '          ',
              current_autonomic, '   ', current_instinct, ' ', current_goal, ' ',
              MBCA_position, ' ', hiker_position)
        if verbose:
            print('--------------------------------\n')
            input('Press a key to continue')
        return 1
    return 0


def beep_secs(secs=1):
    '''beeps for time above
    '''
    try:
        import winsound
        duration = secs * 1000  # milliseconds
        freq = 440  # Hz
        winsound.Beep(freq, duration)
        return True
    except:
        print('Windows beeping sound via <import winsound> did not work')
        return False


def get_inp_vector(to_print, emulation_possibilities):
    '''get raw input from sensors via keyboard or emulation
    calls get_input(sensory_possibles) for the NESW emulation
    emulation_possibilities is the list of the possible sensory inputs
    return slightly processed input as NESW list of strings'''
    if to_print == '':
        to_print = 'SPECIFY SUBMODULE OR MODULE NAME'
    print('\n-->', to_print)
    #get input from sensors
    aa = input("Press ENTER for automatic emulation of North-E-S-W sensors, or m to enter manually:")
    if aa == '':
        aa = get_input(emulation_possibilities)
    else:
        aa = [0, 0, 0, 0]
        aa[0] = input('Enter NORTH direction sensory input (1 and 0s): ')
        aa[1] = input('Enter EAST direction sensory input (1 and 0s): ')
        aa[2] = input('Enter SOUTH direction sensory input (1 and 0s): ')
        aa[3] = input('Enter WEST direction sensory input (1 and 0s): ')
    #process raw input
    for i in range(4):
        aa[i] = str(aa[i])
        aa[i] = aa[i] + FILLER
        aa[i] = aa[i][0:8]
    print('finishing get_inp_vector (which may call get_input) and aa is: ', aa)
    return aa


def get_input(sensory_possibles):
    '''
    gets input sensory vector depending on position of MBCA
    MBCA_position = (0..3, 0..3)  (main global, not modifying thus no declare global)
    sensory_possibles is a list with possible sensory values for a particular position
    selector chooses which of these possible values to use, trying to emulate real world data input
    selector here is just expression 'random.randint(0, len(possibles[0])-1)'
    '''
    possibles = sensory_possibles[MBCA_position[0]*4 + MBCA_position[1]]
    directional_input = [possibles[0][random.randint(0, len(possibles[0])-1)],
                         possibles[1][random.randint(0, len(possibles[1])-1)],
                         possibles[2][random.randint(0, len(possibles[2])-1)],
                         possibles[3][random.randint(0, len(possibles[3])-1)]]
    #gives [N, E, S, W] == [0, 1, 2, 3] sensory input values
    return directional_input


def reflex(to_print, input_vector):
    '''
    autonomous modules as well as mbca internal reflex centers
    processing an input for reflex activity
    input_vector consists of list of 4 vectors N,E,S,W
    '''
    print('\n-->', to_print)
    if evaluation_cycles > CYCLES_TO_COMPLETE:
        print('Evaluation cycles indicate that program will leave at common point, thus no reflex.')
        return False
    for i in ('N', 'E', 'S', 'W'):
        input_position_dict = {'N':0, 'E':1, 'S':2, 'W':3}
        input_position = input_position_dict[i]
        if input_vector == REFLEX_ESCAPE:
            print('Escape motion to left triggered by vector {} in {} in input {}'.format(
                i, input_vector[input_position], input_vector))
            put_motor_output(ESCAPE_LEFT)
            return True
    print('Input {} did not trigger any reflexes'.format(input_vector))
    return False


def subsymbolic(to_print, sensory_input, actuals, HLN_feedback=None):
    '''subsymbolic identification of sensory inputs
    HLN_feedback affects identification choice
    '''
    print('\n-->', to_print)
    print('in subsymbolic--received sens_input and HLN_feed: ', sensory_input, HLN_feedback)
    north = prelim_match(sensory_input[0], actuals)
    east = prelim_match(sensory_input[1], actuals)
    south = prelim_match(sensory_input[2], actuals)
    west = prelim_match(sensory_input[3], actuals)
    return [north, east, south, west]


def prelim_match(sensory_input, actuals):
    '''fuzzy match in microsimulation to
    simulate NN in fuller simulation
    from fuzzywuzzy import fuzz
    from fuzzywuzzy import process'''
    print('\n --in prelim_match-- sensory_input is: ', sensory_input)
    top_matched_forest_keys = process.extract(sensory_input, actuals.keys(), limit=2)
    alpha_matches = {}
    for ii in top_matched_forest_keys:
        alpha_matches[ii[0]] = [ii[1], actuals[ii[0]]]
    print('in prelim_match --top matches: ', alpha_matches)
    return alpha_matches


def sensory_fuse(to_print, sensory1, sensory2, HLN_feedback=None):
    '''DEPRECATED
    fusion of processed sensory inputs
    simple Nano-level fusion -- adds values of top choices of two senses
    however this type of binding often causes false positives
    DEPRECATED
    '''
    if HLN_feedback:
        pass
    fused_senses = [{}, {}, {}, {}]
    print('\n-->', to_print)
    for j in range(4):
        fused_senses[j] = dict(sensory1[j])
        for i in sensory2[j]:
            if i in fused_senses[j]:
                fused_senses[j][i][0] = fused_senses[j][i][0] + sensory2[j][i][0]
            else:
                fused_senses[j][i] = sensory2[j][i][0:2]
    return fused_senses


def fused_select(fused_vector, HLN_feedback=None):
    '''DEPRECATED
    uses meaningfulness as well as hierarchical feedback to determine which of
    the sensory-binding sensory possibilities will be selected
    nb see note/print statements about Nano model
    USED AFTER SENSORY_FUSE -->  DEPRECATED
    '''
    fused_vector = fused_vector[0]
    if HLN_feedback:
        print('In current Nano model of MBCA the max value of all the possible')
        print(' sensory bindings is used. This is updated with MBCA-related')
        print(' mechanisms (meaningfulness as well as hierarchical feedback) in Micro model.')
    max_record = -1
    current_max = -1 #use for readability
    for i in fused_vector:
        if fused_vector[i][0] >= current_max:
            current_max = fused_vector[i][0]
            max_record = i
    return max_record, fused_vector[max_record]


def NESW_fused_select(fused_vector):
    '''DEPRECATED
    calls fused_select for each of the NESW components
    returns eg--  01010101 [100, 'lost hiker']
    USED AFTER FUSED_SELECT --> DEPRECATED
    '''
    NESW_max_record = [0, 0, 0, 0]
    NESW_fused_vector = [0, 0, 0, 0]
    for i in range(4):
        a, b = fused_select(fused_vector)
        NESW_max_record[i] = a
        NESW_fused_vector[i] = b
    return NESW_max_record, NESW_fused_vector


def sensory_fuse2(to_print, sensory1, sensory2, actual_values, HLN_feedback=None):
    '''fusion of processed sensory inputs
    simple Nano-level fusion
    eg, sensory1 is visual_input
    eg, sensory2 is auditory_input
    combine 8 bits of sensory1 (eg, visual) with 8 bits of sensory2
      (eg, auditory) to yield 16 bit vector: visual(8)+auditory(8)
    combine the various possible combinations sensory1 and sensory2 components
    then compare the 16 bit combos against {fused_actual_inputs} to see most
      likely matches
    can generate combos from matching outputs of each sense
    however in this version just concatenate the actual sensory output
    -for moment if HLN_feedback given value then print devpt info
    '''
    #same prelude as original sensory_fuse
    if HLN_feedback:
        pass
    combos = [[], [], [], []]
    fused_matches = [[], [], [], []]
    print('\n-->', to_print)
    #create combos of 16 bit words
    #this implementation just concatenates the raw auditory and visual inputs, thus,
    # we are not really taking advantage of the lower level processing
    for i in range(4):
        combos[i] = sensory1[i] + sensory2[i]
        if HLN_feedback:
            print('direction {} value of combo is: {}'.format(i, combos[i]))
    #now must look for best matches in concatenated actual inputs dictionary
    for i in range(4):
        top_matched_forest_keys = process.extract(combos[i], actual_values.keys(), limit=2)
        alpha_matches = {}
        for ii in top_matched_forest_keys:
            alpha_matches[ii[0]] = [ii[1], actual_values[ii[0]]]
        fused_matches[i] = alpha_matches
    #for devp't
    if HLN_feedback:
        fused = fused_matches
        print('\n>>fused sensory signal: ', fused)
        #eg, [{'1111110000000000': [94, 'obstruction + strange silence -> edge'],
        #      '1100011011000000': [..]},
        #       {..}, {..}, {..}]
        print('N : ', fused[0])
        print('E : ', fused[1])
        print('S : ', fused[2])
        print('W : ', fused[3], '\n')
    #[{'16 bit fused sensory (vis+aud)':[int score, 'str descrpn']}, {dict E}, {dict S}, {dict W}]
    return fused_matches


def NESW_fused_select2(fused_vector):
    '''calls fused_select for each of the NESW components
    returns eg--  01010101 [100, 'lost hiker']
    if HLN_feedback:
            print('In current Nano model of MBCA the max value of all the possible')
            print(' sensory bindings is used. This is updated with MBCA-related')
            print(' mechanisms (meaningfulness as well as hierarchical feedback) in Micro model.')
    '''
    #print('------------------', fused_vector[0], '\n\n\n')
    # {'0001000100010001': [81, 'shallow river + smooth water sound -> shallow_river'], '1100011011000000': [75, 'forest + forest noise -> forest']}
    #fused_vector = [{...}, {...}, {...}, {...}]
    NESW_max_record = [0, 0, 0, 0]
    NESW_fused_vector = [0, 0, 0, 0]
    for g in range(4):
        fused_vectorg = fused_vector[g]
        #print('------------------', g, '  ', fused_vectorg, '\n')
        max_record = -1
        current_max = -1 #use for readability
        for i in fused_vectorg:
            if fused_vectorg[i][0] >= current_max:
                current_max = fused_vectorg[i][0]
                max_record = i
        NESW_max_record[g] = max_record
        NESW_fused_vector[g] = fused_vectorg[max_record]
    return NESW_max_record, NESW_fused_vector



def get_current_autonomic(to_print, influence=None):
    '''returns current_autonomic
    Nano-level
    instincts are influenced by external sensory plus internal autonomic sensory
    'influence' allows caller to influence what autonomic result should be returned
    Micro-level and above really should interface with wake-sleep method
    each call increments age of system 'age_autonomic_calls'
    current_autonomic is global since can affect much of system
    '''
    print('\n-->', to_print)
    #autonomic, age, instinctual states can affect many parts of the system, and kept global
    global age_autonomic_calls
    global current_autonomic
    global current_instinct
    age_autonomic_calls += 1
    #
    #caller can specify autonomic by simply entering it as influence parameter
    if influence:
        aa = str(influence)
        aa = aa + FILLER
        aa = aa[0:8]  #Nano level
        print('current_autonomic is value is set by caller of method: ', aa)
        return aa
    #
    #duty cycle specifies how often to change current_autonomic in the simple Nano model
    DUTY_CYCLE_CHANGE_AUTONOMIC = 5
    duty_cycle_random = random.randint(1, DUTY_CYCLE_CHANGE_AUTONOMIC)
    #
    #randomly change, if duty cycle allows, current_autonomic in simple Nano model
    if age_autonomic_calls <= 1 or duty_cycle_random == 1:
        current_autonomic = random.choice(list(autonomic.keys()))
        print('current_autonomic value randomly changed to: ', current_autonomic,
              ' which corresponds to autonomic state of ', autonomic[current_autonomic])
        return current_autonomic
    #otherwise current_autonomic will not be changed
    print('current_autonomic remains as {} '.format(autonomic[current_autonomic]))
    return current_autonomic


def get_current_instinct(to_print, current_fused_sensory, current_autonomic):
    '''returns current_instinct from the instinctual core
    goals module
    Nano-level
    instincts are influenced by external sensory plus internal autonomic sensory
    #to help see what instinct and other values are keyed as
    #pylint: disable=line-too-long
    #pylint: disable=pointless-string-statement
    instinct = {'10000000':'forward eat/goal', '11000000':'left avoid', '01000000':'right avoid', '00000000':'conserve energy' }
    autonomic = {'00000000':'conserve energy', '00000001':'move to different area',
                 '00000010':'eat', '00000011':'reproduce'}
    forest = {'11110001':'human cry help', '11110010':'bird mating call',
              '01010101':'lost hiker', '11100011':'forest_noise'}
    #pylint: enable=line-too-long
    #pylint: enable=pointless-string-statement'''
    print('\n-->', to_print)
    print('nb. instinct value calculated here and can be used in subsequent methods as desired')
    #at Nano level consider very basic instinctual strategies
    #| current_autonomic + current_fused_sensory -> current_instinct |
    #these strategies can at Micro level be replaced by neural network or fuzzy implementation
    #
    #autonomic, age, instinctual states can affect many parts of the system, and kept global
    global age_autonomic_calls
    global current_instinct
    #
    #if human cry sensory input then search robot should move regardless of energy/other issues
    if current_fused_sensory == '11110001':
        print("'11110001' human cry help --thus return instinct '10000000' -- 'forward eat/goal'")
        return '10000000'
    #
    #if autonomic is conserve energy and no human cry then instinct to conserve energy also
    if current_autonomic == '00000000':
        print("current_autonomic is {} thus return instinct value: {}".format(
            current_autonomic, instinct['00000000']))
        #conserve energy
        return '00000000'
    #
    #for now, for other autonomic values, treat as MBCA is active and in process of
    #wanting to reach goal, thus, we will return an instinct value of 1000 0000 which
    #is 'forward eat/goal'
    print('instinct method note: despite other auton values will treat as MBCA is active')
    return '10000000'


def generate_random_direction():
    '''generates a random direction which may be needed by various
    hippocampal and other path finding algorithms
    '''
    random_direction = random.randint(1, 4)
    if random_direction in (1, 999):
        random_direction = '00'
    if random_direction in (2, 999):
        random_direction = '01'
    if random_direction in (3, 999):
        random_direction = '10'
    if random_direction in (4, 999):
        random_direction = '11'
    return random_direction


def gconscious(item, verbose=0):
    '''goal and conscious module interacts with the emotional and reward module as well
     as the entire MBCA to provide some overall control of the MBCA’s behavior
     memories of operations occurring in the logic/working memory are temporarily
      kept in the conscious module, allowing improved problem solving as well as
      providing more transparency to MBCA decision making
    '''
    if verbose:
        print('CHECKPOINT: in conscious method')
    #nano ver emulate with simple list
    global conscious_memory
    #add conscious item to conscious memory
    conscious_memory.append(item)
    print('in gconscious')
    return True


def pattern_memory(max_fused_index, verbose=0):
    '''additional memory area
    generally holds non-procedural information
    nano version -- scaffolding to drop in more authentic component
    '''
    if verbose:
        print('CHECKPOINT: in pattern memory method', max_fused_index)
    return True


def emotional(max_fused_index, verbose=0):
    '''influences moves and goals
    influences learning of new facts and procedures
    allows effective learning of infrequent events and obviates the
     class imbalance problem seen in conventional neural networks
    --> rare events can sometimes be very important events to learn
    nano version -- scaffolding to drop in more authentic component
    '''
    if verbose:
        print('CHECKPOINT: in emotional method', max_fused_index)
    return True


def seq_and_error(max_fused_index, verbose=0):
    '''sequential/error-correcting memory is an optional moduleand
    distinct from memories in MANNs or other NN
    useful for detecting changes in a spectrum of external and internal data,
    and storing learning sequences which can automatically be repeated later as needed
    nano version -- scaffolding to drop in more authentic component
    '''
    if verbose:
        print('CHECKPOINT: in sequential and error method', max_fused_index)
    return True


def hippocampus(fused_sensory, instinct, max_fused_index, max_fused_value,
                visual_processed, auditory_processed, m_verbose=False):
    '''spatial maps and positioning for MBCA
    #
    --quick review of what hippocampus in biology does (since otherwise literature confusing for
    non-bio background reader due to terminology):
    -mammals have left and right hippocampi
    -in mammals part of the 'allocortex'=='heterogenetic cortex' versus the 'neocortex'
    (neocortex 6 layers vs. 3-4 cell layers in allocortex; types of allocortex: paleocortex,
    archicortex and transitional (ie, to neocortex) periallocortex)
    olfactory system also part of the allocortex
    -considered part of 'limbic system' (=='paleomammalian cortex' midline structures
     on L and R of thalamus, below temporal lobe; involved in emotion, motivation,
     olfactory sense and memory; making memories affected by limibc system)
     (basic limbic system is really amygdala, mammillary bodies, stria medull, nuc Gudden,
     but also tightly connected to limbic thalamus, cingulate gyrus, hippocampus,
     nucleus accumbens, anterior hypothalamus, ventral tegmental area, raphe nuc,
     hebenular commissure, entorhinal cortex, olfactory bulbs)
    -hippocampus involved in spatial memory, in this MBCA simulation that is what similarly
    name method does
    -hippcampus also involved in putting together portions of memory throughout whole brain
    -given relation between learning and memory, not surprising to find that hippocampus involved
    in learning; in more advanced hippocampal methods, ie, beyond LAMPREY level
    these indeed are implemented in this method
    -hippocampus needed for consolidation of (certain types) of short-term memories
    into long-term memory, and for spatial navigation
    -above note that in primates hippocampus is in bottom part of medial temporal lobe
    -hippocampus = 'hippocampus proper'==Ammon's horn + dentate gyrus
    -hippocampus in all mammals; animals with better spatial memories are found to have
    larger hippocampal structures
    -in other vertebrates (ie, fish to reptiles) don't have an allocortex but vertebrates
    do have pallium which evolved to cortex in mammals
    -even lamprey and hagfish (ancient jawless fish) have a pallium
    -medial, lateral, dorsal pallium
    -medial pallium is precursor of hippocampus and is homologous in other vertebrates but does
    not look like hippocampus found in mammals
    -evidence that hippocampal-like homologues used for spatial navigation in fish,
    reptiles, and fish -- thus in MBCA we call all these 'hippocampus' have different
    levels of 'hippocampus' methods
    -insect brain mushroom bodies may have function like hippocampal-like structures in
    vertebrates, but homology uncertain, so we don't deal with in the MBCA
    #
    --documentation of behavior of hippocampus() method
    CURRENTLY BEING TRANSITIONED INTO NANO CODE FROM PREVIOUS MBLS3 MODELS
    '''
    return_value = None
    #
    if m_verbose:
        print('visual_processed: \n', visual_processed, '\nauditory_processed: \n',
              auditory_processed)
        print('fused_sensory, instinct, max_fused_index, max_fused_value: \n', fused_sensory, '\n', instinct, '\n', max_fused_index, '\n', max_fused_value)
        print('\n', hippo_map())
    #
    #hippocampal temporary memories
    global h_mem_dirn_goal #initial None
    global h_mem_prev_dirn_goal #initial None
    global local_minimum
    if current_hippocampus == 'LAMPREY':
        print('current_hippocampus is set to {} \n'.format(current_hippocampus))
    else:
        print('current_hippocampus is set to {} but these'.format(current_hippocampus))
        print('other hippocampal/equivalent structures not migrated over to new nano version.')
        print('....continue with LAMPREY level hippocampal-equivalent functioning\n')
    #
    #build internal hippo_map
    for i, j in ((0, '00'), (1, '01'), (2, '10'), (3, '11')):
        if max_fused_index[i] == '1100011011000000': #forest
            hippo_map(j, 'forest')
        if max_fused_index[i] == '0001000100010001': #sh_rvr
            hippo_map(j, 'sh_rvr')
        if max_fused_index[i] == '0001100101010101': #ww_rvr
            hippo_map(j, 'ww_rvr')
        if max_fused_index[i] == '0101000011110000': #lost hiker
            hippo_map(j, 'hiker')
        if max_fused_index[i] == '1111110000000000': #edge
            hippo_map(j, 'edge')
        if max_fused_index[i] == '1110001100010001': #lake
            hippo_map(j, 'lake')
    print_mbca_map()
    #
    #try to use hippocampal memory for direction
    #first must see if reason to update the hippocampal memory, ie, is there a goal direction?
    for i, j in ((0, '00'), (1, '01'), (2, '10'), (3, '11')):
        if max_fused_index[i] == '0101000011110000': #lost hiker
            h_mem_prev_dirn_goal = h_mem_dirn_goal
            h_mem_dirn_goal = str(j)
            print('CHECKPOINT: h_mem_dirn_goal was just set to {} and local_min is {}'.format(h_mem_dirn_goal, local_minimum))
            return_value = h_mem_dirn_goal
    #reason to avoid the hippocampal /goal direction?
    #(nb local_min only reset each run.... thus todo better reset after few cycles of no goal)
    if h_mem_dirn_goal and local_minimum < TRIES_BEFORE_DECLARE_LOCAL_MINIMUM:
        print('CHECKPOINT: h_mem_dirn_goal (ie, there is a goal) and local_minimum', h_mem_dirn_goal, local_minimum)
        local_minimum += 1
        print('CHECKPOINT: local_minimum tries now equal: ', local_minimum)
        print('CHECKPOINT: now evaluating if {} direction from h_mem_dirn_goal should be avoided'.format(h_mem_dirn_goal))
        #for i, j, k in ((0, '00', 'northward'), (1, '01', 'eastward'), (2, '10', 'southward'), (3, '11', 'westward')):
        #    if h_mem_dirn_goal == j and hippo_calc(max_fused_index, j):
        if hippo_calc(max_fused_index, h_mem_dirn_goal):
            return_value = h_mem_dirn_goal
            print('attempts to walk goal direction {}....'.format(h_mem_dirn_goal))
            if max_fused_index[{'00':0, '01':1, '10':2, '11':3}[h_mem_dirn_goal]] == '1111110000000000': #edge
                print('would like to move this direction but edge thus LAMPREY primitive algo is to use random dirn')
                local_minimum = 0
                h_mem_prev_dirn_goal = h_mem_dirn_goal
                h_mem_dirn_goal = None
                print('using random direction for return_value')
                return_value = generate_random_direction()
            if max_fused_index[{'00':0, '01':1, '10':2, '11':3}[h_mem_dirn_goal]] == '1110001100010001': #lake
                print('would like to move this direction but lake thus LAMPREY primitive algo is to use random dirn')
                local_minimum = 0
                h_mem_prev_dirn_goal = h_mem_dirn_goal
                h_mem_dirn_goal = None
                print('using random direction for return_value')
                return_value = generate_random_direction()
            #only returns at this point if h_mem_dirn_goal has value (and not exceeded tries) and hippocalc True
            #otherwise will continue below with randint
            print('CHECKPOINT: now returning a return_value via h_mem_dirn_goal ', return_value)
            return return_value
    #
    #if no goal direction to go to then use a reasonable random direction, if not reasonable then try again
    while True:
        print('CHECKPOINT: h_mem_dirn_goal and local_minimum, ie, no goal direction and using randint', h_mem_dirn_goal, local_minimum)
        gconscious(['CHECKPOINT: h_mem_dirn_goal and local_minimum, ie, no goal direction and using randint', h_mem_dirn_goal, local_minimum])
        direction = random.randint(1, 11)
        emotional(max_fused_index)
        pattern_memory(max_fused_index)
        seq_and_error(max_fused_index)
        local_minimum = 0 #in case has been set in previous moves
        h_mem_prev_dirn_goal = h_mem_dirn_goal
        h_mem_dirn_goal = None
        if direction in (1, 2):
            print('randint direction: attempts to walk northward....')
            if not hippo_calc(max_fused_index, '00'):
                print('....but on or low probability of success of goal in this direction')
                continue
            if max_fused_index[0] == '1111110000000000': #edge
                print('....but this is an edge thus try again navigation for this move')
                continue
            if max_fused_index[0] == '1110001100010001': #lake
                print('....but this is a lake thus try again navigation for this move')
                continue
            return '00'
        if direction in (3, 4, 10, 9):
            print('randint direction: attempts to walk eastward....')
            if not hippo_calc(max_fused_index, '01'):
                print('....but on or low probability of success of goal in this direction')
                continue
            if max_fused_index[1] == '1111110000000000': #edge
                print('....but this is an edge thus try again navigation for this move')
                continue
            if max_fused_index[1] == '1110001100010001': #lake
                print('....but this is a lake thus try again navigation for this move')
                continue
            return '01'
        if direction in (5, 6, 11):
            print('randint direction: attempts to walk southward....')
            if not hippo_calc(max_fused_index, '10'):
                print('....but on or low probability of success of goal in this direction')
                continue
            if max_fused_index[2] == '1111110000000000': #edge
                print('....but this is an edge thus try again navigation for this move')
                continue
            if max_fused_index[2] == '1110001100010001': #lake
                print('....but this is a lake thus try again navigation for this move')
                continue
            return '10'
        if direction in (7, 8):  #prevent westward
            print('randint direction: attempts to walk westward....')
            if not hippo_calc(max_fused_index, '11'):
                print('....but on or low probability of success of goal in this direction')
                continue
            if max_fused_index[3] == '1111110000000000': #edge
                print('....but this is an edge thus try again navigation for this move')
                continue
            if max_fused_index[3] == '1110001100010001': #lake
                print('....but this is a lake thus try again navigation for this move')
                continue
            return '11'
        if direction == 100: #will not occur if randint set to prevent
            print('randint direction: this move random pause....')
            put_motor_output('00', 0)
        else:
            print('randint direction: coding issue -- please check code for goal find hiker')
            return '00'


def hippo_map(direction='00', geo_feature='forest'):
    '''internal hippocampal spatial map constructed and used by the MBCA
    note: in "nano" version the philosophy is to emulate modules which are replaced
     by more authentic components in the finer grain simulations, thus very artificial
     cartesian map constructed here
    #global variable recap:
    h_mem_dirn_goal = None
    h_mem_prev_dirn_goal = None
    MBCA_position = (INITIATE_VALUE, INITIATE_VALUE)
    hiker_position = (INITIATE_VALUE, INITIATE_VALUE)
    forest_map = [['forest', 'forest', 'sh_rvr', 'forest'],
                  ['lake  ', 'forest', 'forest', 'forest'],
                  ['forest', 'forest', 'ww_rvr', 'forest'],
                  ['forest', 'forest', 'forest', 'forest']]
    nb. m rows x n columns coordinates, start 0,0 --
    forest_map coords superimposed on mbca_map below
    mbca_map = [['', '', '', '', '', ''],
                ['', 0,0'', '', '', 0,3'', ''],
                ['', 1,0'', '', '', '', ''],
                ['', 2,0'', '', '', '', ''],
                ['', 3,0'', '', '', 3,3'', ''],
                ['', '', '', '', '', '']]
    nb. start at 0,0 also, note includes edge squares which forest_map does not
    #
    see note about this being emulation level in "nano" version
    nonetheless, the function is to provide MBCA history of where this
    direction, this location leads to
    '''
    #convert MBCA_position from forest map into mbca_map coords
    MBCA_int_posn = (MBCA_position[0] + 1, MBCA_position[1]+ 1)
    #print('-----------------MBCA mbca_map position is: ', MBCA_int_posn)
    #flag that square as being one where MBCA was already if no geo_feature
    m = MBCA_int_posn[0]
    n = MBCA_int_posn[1]
    if mbca_map[m][n] == '':
        mbca_map[m][n] = 'explored'
    #now flag square to direction specified with geo_feature given
    #nb in this "nano" version just overwrite whatever is there, but in more
    # authentic finer grain simulations to consider validity of data better
    # (geo_feature 'uncertain' used for this purpose as well as expanded set of
    # geo_features)
    if direction == '00':
        m = m - 1
    elif direction == '10':
        m = m + 1
    elif direction == '01':
        n = n + 1
    elif direction == '11':
        n = n - 1
    else:
        print('coding issue -- direction not valid: ', direction)
        return False
    if geo_feature not in ('hiker', 'mbca', 'explored', 'forest', 'sh_rvr', 'lake', 'ww_rvr', 'edge', 'uncertain'):
        print('coding issue -- geo_feature not valid: ', geo_feature)
        return False
    mbca_map[m][n] = geo_feature
    #print_mbca_map()
    #gconscious([mbca_map])
    return True


def hippo_calc(max_fused_index, direction, verbose=0, silent=0):
    '''look at internal hippocampal spatial map mbca_map and decide if
    should go in this direction
    -parameter is direction are considering
    -returns True if should go in direction or False if not to
    -although output is binary, method is allowed to use random function
    to sometimes return False for paths which while possible are unlikely to
    lead to the goal
    -LAMPREY level algo if all squares in that direction already explored then
    return False
    '''
    idirection = {'00':0, '01':1, '10':2, '11':3}[direction]
    if verbose:
        print('CHECKPOINT: in hippocalc, direction is {} ({}) and h_mem_dirn_goal is {}'.format(direction, idirection, h_mem_dirn_goal))
    #input validity as well as forced outputs
    if direction not in ('00', '01', '10', '11', '99', '-1'):
        print('coding issue -- direction not valid -- return False ', direction, '-1', '99')
        #gconscious(['coding issue -- direction not valid -- return False ', direction, '-1', '99'])
        return False
    if direction == '99':
        print('hippo_calc forced to allow directional move due to 99 input')
        #gconscious(['hippo_calc forced to allow directional move due to 99 input'])
        return True
    if direction == '-1':
        print('hippo_calc forced to prevent directional move due to -1 input')
        #gconscious = (['hippo_calc forced to prevent directional move due to -1 input'])
        return False
    #consider if direction is recommended (returns True) or not (returns False)
    #first make sure immediate direction even possible
    if max_fused_index[idirection] == '1111110000000000': #edge
        #gconscious(['....but this is an edge thus hippo_calc will be False', direction])
        if not silent:
            print('....but this is an edge thus hippo_calc will be False')
        return False
    if max_fused_index[idirection] == '1110001100010001': #lake
        if not silent:
            print('....but this is a lake thus try again navigation for this move')
            #gconscious(['....but this is a lake thus try again navigation for this move', direction])
        return False
    if not silent:
        print('CHECKPOINT: in hippocalc and now checking to see if any unexplored cells in direction ', idirection)
        #gconscious(['CHECKPOINT: in hippocalc and now checking to see if any unexplored cells in direction ', idirection])
    #convert MBCA_position from forest map into mbca_map coords
    MBCA_int_posn = (MBCA_position[0] + 1, MBCA_position[1]+ 1)
    m = MBCA_int_posn[0]
    n = MBCA_int_posn[1]
    if verbose:
        print('CHECKPOINT: MBCA_position and MBCA_int_posn: ', MBCA_position, MBCA_int_posn)
        #gconscious(['CHECKPOINT: MBCA_position and MBCA_int_posn: ', MBCA_position, MBCA_int_posn])
    #now explore directions to see if mbca_calc will recommend the direction
    #current simple algo is to recommend, ie, True, if unexplored squares
    if idirection == 0:
        #m = TOTAL_ROWS
        n = TOTAL_COLS
        for i in range(m - 1):
            for j in range(TOTAL_COLS):
                if verbose:
                    print(i + 1, j + 1)
                if mbca_map[i + 1][j + 1] == '' or mbca_map[i + 1][j + 1] == 'hiker ':
                    if not silent:
                        print('returning True from hippocalc since unexplored cells beyond direction', idirection, 'ijmn', i, j, m, n)
                    #gconscious(['returning True from hippocalc since unexplored cells beyond direction', idirection, 'ijmn', i, j, m, n])
                    return True
    if idirection == 2:
        #m = TOTAL_ROWS
        n = TOTAL_COLS
        for i in range(TOTAL_ROWS - 1, m - 1, -1):
            for j in range(n):
                if verbose:
                    print(i + 1, j + 1)
                if mbca_map[i + 1][j + 1] == '' or mbca_map[i + 1][j + 1] == 'hiker ':
                    if not silent:
                        print('returning True from hippocalc since unexplored cells beyond direction', idirection, 'ijmn', i, j, m, n)
                    #gconscious(['returning True from hippocalc since unexplored cells beyond direction', idirection, 'ijmn', i, j, m, n])
                    return True
    if idirection == 1:
        m = TOTAL_ROWS
        #n = TOTAL_COLS
        for i in range(m):
            for j in range(TOTAL_COLS - 1, n - 1, -1):
                if verbose:
                    print(i + 1, j + 1)
                if mbca_map[i + 1][j + 1] == '' or mbca_map[i + 1][j + 1] == 'hiker ':
                    if not silent:
                        print('returning True from hippocalc since unexplored cells beyond direction', idirection, 'ijmn', i, j, m, n)
                    #gconscious(['returning True from hippocalc since unexplored cells beyond direction', idirection, 'ijmn', i, j, m, n])
                    return True
    if idirection == 3:
        m = TOTAL_ROWS
        #n = TOTAL_COLS
        for i in range(m):
            for j in range(0, n - 1):
                if verbose:
                    print(i + 1, j + 1)
                if mbca_map[i + 1][j + 1] == '' or mbca_map[i + 1][j + 1] == 'hiker ':
                    if not silent:
                        print('returning True from hippocalc since unexplored cells beyond direction', idirection, 'ijmn', i, j, m, n)
                    #gconscious(['returning True from hippocalc since unexplored cells beyond direction', idirection, 'ijmn', i, j, m, n])
                    return True
    #
    if not silent:
        print('no unexplored squares in direction {}, thus hippocalc returns False'.format(direction))
    #gconscious(['no unexplored squares in direction {}, thus hippocalc returns False'.format(direction)])
    return False


def precausal(to_print, fused_sensory, instinct, max_fused_index, max_fused_value,
              visual_processed, auditory_processed):
    '''fused_sensory signal plus instinct will
    causally generate an output
    Sensory + context generating the instinct + instinct representing rules
    == sensory + context + associations with context -->
    at pre-causal level
    calls put_motor_output which in turn calls
        move_MBCA(direction, steps) which returns:
                -if 'forest' square returns 'MBCA  '
                -if 'hiker ' square returns 'RESCUE'
                -if 'lake  ' square returns 'LOSS  '
                -if 'ww_rvr' square returns 'DAMAGE'
                -if 'sh_rvr' square returns 'CROSS '
                -if no move then    returns 'STOP  '
    if goal is GOAL_RANDOM_WALK then just feeding in random N,E,S,W or pauses to
      put_motor_output
    GOAL_RANDOM_WALK = '00000000'
    GOAL_SKEWED_WALK = '00000001'
    GOAL_FIND_HIKER = '11100011'
    DEFAULT_GOAL = GOAL_RANDOM_WALK
    ---------------
    #ok to walk puddle, shallow river, grass, trees
    #not ok go into lake -- water will damage articulations
    #if lake subsymbolic -> instinctual -> danger -> change path
    #if shallow river subsymbolic -> instinctual -> continue activities
    #instinctual ->motor activities to accomplish goal
    #white areas river -> no particular action
    #damage leg -> associative memory white areas and danger
    #GOAL_RANDOM_WALK = '00000000'
    #GOAL_FIND_HIKER = '11100011'

    ##move_MBCA(direction='00', steps=0)   <------unreachable code
    ##return DEFAULT_VECTOR
    ----------------
    '''
    global current_goal
    print('\n-->', to_print)
    print('at this point fused_sensory is {} and instinct is {}\n'.format(fused_sensory, instinct))
    print('maxed_fused_index: ', max_fused_index)
    print('maxed_fused_value: ', max_fused_value, '\n')
    print('current goal is: ', current_goal)

    #GOAL_FIND_HIKER
    if current_goal == GOAL_FIND_HIKER:
        put_motor_output(hippocampus(fused_sensory, instinct, max_fused_index, max_fused_value, visual_processed, auditory_processed), 1)
        return True

    #GOAL_SKEWED_WALK
    if current_goal == GOAL_SKEWED_WALK:
        direction = random.randint(1, 11)
        #since N and E are not possible at starting origin, skew random generation
        if direction in (1, 2):
            print('Goal is (skewed) random walk.... so walks northward....')
            put_motor_output('00', 1)
        elif direction in (3, 4, 10, 9):
            print('Goal is (skewed) random walk.... so walks eastward....')
            put_motor_output('01', 1)
        elif direction in (5, 6, 11):
            print('Goal is (skewed) random walk.... so walks southward....')
            put_motor_output('10', 1)
        elif direction in (7, 8):
            print('Goal is (skewed) random walk.... so walks westward....')
            put_motor_output('11', 1)
        elif direction == 100: #will not occur if randint set to prevent
            print('Goal is (skewed) random walk....this move random pause....')
            put_motor_output('00', 0)
        else:
            print('coding issue -- please check code for random walk')
        return True

    #GOAL_RANDOM_WALK
    if current_goal == GOAL_RANDOM_WALK:
        direction = random.randint(1, 4)
        #since N and E are not possible at starting origin, skew random generation
        if direction in (1, 999):
            print('Goal is random walk.... so walks northward....')
            put_motor_output('00', 1)
        elif direction in (2, 999):
            print('Goal is random walk.... so walks eastward....')
            put_motor_output('01', 1)
        elif direction in (3, 999):
            print('Goal is random walk.... so walks southward....')
            put_motor_output('10', 1)
        elif direction in (4, 999):
            print('Goal is random walk.... so walks westward....')
            put_motor_output('11', 1)
        elif direction == 5: #will not occur if randint set to prevent
            print('Goal is random walk....this move random pause....')
            put_motor_output('00', 0)
        else:
            print('coding issue -- please check code for random walk')
        return True

    #DEFAULT_GOAL
    print('current_goal:{} no logic- GOAL_RANDOM_WALK set for next move'.format(current_goal))
    current_goal = GOAL_RANDOM_WALK
    return False


def causal(to_print, fused_sensory, instinct):
    '''fused_sensory signal plus instinct will
    causally generate an output
    Sensory + context generating the instinct + instinct representing rules
    == sensory + context + rules about context -->
     -allow better interpretation than just sensory association
     -predict future outcome better
     -plan goal directed result better
     == beginnings of causal reasoning
    '''
    print('\n-->', to_print)
    print('at this point fused_sensory is {} and instinct is {}\n'.format(fused_sensory, instinct))
    #todo
    return DEFAULT_VECTOR


def put_motor_output(output_vector, steps_specified=1):
    ''' assume 4x4 grid, ie, from 0,0 to 3,3
    calls "move_MBCA(direction, steps)" which returns:
        -if 'forest' square returns 'MBCA  '
        -if 'hiker ' square returns 'RESCUE'
        -if 'lake  ' square returns 'LOSS  '
        -if 'ww_rvr' square returns 'DAMAGE'
        -if 'sh_rvr' square returns 'CROSS '
        -if no move then    returns 'STOP  '
    '''
    steps = steps_specified
    if steps == 0:
        move_MBCA('E', 0)
        #return from move_MBCA will be 'STOP  ' but don't use
    elif output_vector == ESCAPE_LEFT:
        if MBCA_position[1] == 0:
            print('MBCA already all the way left, thus will jump escape right')
            result_of_move = move_MBCA('E', steps)
            if result_of_move == 'RESCUE':
                rescue()
            if result_of_move == 'DAMAGE':
                mission_failure("whitewater spray damaged an articulation")
            if result_of_move == 'CROSS ':
                print("MBCA ok to cross a shallow river.... all is fine")
            if result_of_move == 'LOSS  ':
                mission_failure("walked into a deep lake")
        else:
            print('Escape motion to left occurred')
            result_of_move = move_MBCA('W', steps)
            if result_of_move == 'RESCUE':
                rescue()
            if result_of_move == 'DAMAGE':
                mission_failure("whitewater spray damaged an articulation")
            if result_of_move == 'CROSS ':
                print("MBCA ok to cross a shallow river.... all is fine")
            if result_of_move == 'LOSS  ':
                mission_failure("walked into a deep lake")
    elif output_vector in ('00', 'N', 'north'):
        #print('n', MBCA_position)
        if MBCA_position[0] == 0:
            print('Note: Already northernmost -- no motion this evaln cycle.')
        result_of_move = move_MBCA('00', steps)
        if result_of_move == 'RESCUE':
            rescue()
        if result_of_move == 'DAMAGE':
            mission_failure("whitewater spray damaged an articulation")
        if result_of_move == 'CROSS ':
            print("MBCA ok to cross a shallow river.... all is fine")
        if result_of_move == 'LOSS  ':
            mission_failure("walked into a deep lake")
    elif output_vector in ('01', 'E', 'east'):
        #print('e', MBCA_position)
        if MBCA_position[1] == 3:
            print('Note: Already easternmost -- no motion this evaln cycle.')
        result_of_move = move_MBCA('01', steps)
        if result_of_move == 'RESCUE':
            rescue()
        if result_of_move == 'DAMAGE':
            mission_failure("whitewater spray damaged an articulation")
        if result_of_move == 'CROSS ':
            print("MBCA ok to cross a shallow river.... all is fine")
        if result_of_move == 'LOSS  ':
            mission_failure("walked into a deep lake")
    elif output_vector in ('10', 'S', 'south'):
        #print('s', MBCA_position)
        if MBCA_position[0] == 3:
            print('Note: Already southernmost -- no motion this evaln cycle.')
        result_of_move = move_MBCA('10', steps)
        if result_of_move == 'RESCUE':
            rescue()
        if result_of_move == 'DAMAGE':
            mission_failure("whitewater spray damaged an articulation")
        if result_of_move == 'CROSS ':
            print("MBCA ok to cross a shallow river.... all is fine")
        if result_of_move == 'LOSS  ':
            mission_failure("walked into a deep lake")
    elif output_vector in ('11', 'W', 'west'):
        #print('w', MBCA_position)
        if MBCA_position[1] == 0:
            print('Note: Already westernmost -- no motion this evaln cycle.')
        result_of_move = move_MBCA('11', steps)
        if result_of_move == 'RESCUE':
            rescue()
        if result_of_move == 'DAMAGE':
            mission_failure("whitewater spray damaged an articulation")
        if result_of_move == 'CROSS ':
            print("MBCA ok to cross a shallow river.... all is fine")
        if result_of_move == 'LOSS  ':
            mission_failure("walked into a deep lake")
    else:
        print('coding issue -- please check code for output_vector sent to put_motor_output')
        return False
    return True


def rescue(secs=2):
    '''called when rescue goal is achieved
    '''
    global performance_metric
    global performance_metric_unit
    beep_secs(secs)
    performance_metric_unit = evaluation_cycles - performance_metric_unit
    performance_metric.append([current_goal, 'rescue', performance_metric_unit])
    print("\nA 'rescue' of the lost hiker has occurred.")
    print("When the MBCA moves to the square of the lost hiker this assumes")
    print("that the MBCA now follows routines to assist or carry the lost hiker")
    print("back to civilization and medical evaluation.")
    print("\nThis may be the only goal of the system or one of many goals it has.")
    print("At present, even if there are multiple goals, such as an autonomous rest")
    print("goal or perhaps a random walk goal, if a rescue occurs it will be considered")
    print("a valid rescue.")
    print("\nYou can accept the rescue and the program will end, or you can")
    print(" ignore it and continue in the program.")
    aa = input("Accept rescue and end program ('y','yes',ENTER) or no ('n','no') and continue: ")
    if aa not in ('n', 'N', 'no', 'No', 'NO', 'stop', 'break'):
        print("Rescue effected. The lost hiker has been returned to civilization,")
        print("undergone a successful medical evaluation and is now enjoying a meal")
        print("with friends and family.")
        print("'Good job MBCA !!'")
        print("\nProgram will end now (break out of main loop at common point)")
        exit_by_completing_evaluation_cycles_to_count()
        return True
    print('Ok...will continue to run.... performance_metric_unit for last rescue was {} cycles'.
          format(performance_metric_unit))
    return False


def mission_failure(reason="reason not specified"):
    '''called when MBCA + robot become incapacitated or
    mission fails for other reasons
    '''
    global performance_metric
    global performance_metric_unit
    beep_secs()
    performance_metric_unit = evaluation_cycles - performance_metric_unit
    performance_metric.append([current_goal, 'mission_failure', performance_metric_unit])
    print("\nA Mission finding the lost hiker has failed.")
    print("Reason: ", reason)
    print("\nYou can stop the rescue and the program will end, or you can")
    print(" ignore it and continue in the program.")
    aa = input("Accept mission stop and end program ('y','yes',ENTER) or no ('n','no'): ")
    if aa not in ('n', 'N', 'no', 'No', 'NO', 'stop', 'break'):
        print("Rescue mission stopped. Unfortunately not completed.")
        print("\nProgram will end now (break out of main loop at common point)")
        exit_by_completing_evaluation_cycles_to_count()
        return True
    print('Ok...will continue to run.... performance_metric_unit for last period was {} cycles'.
          format(performance_metric_unit))
    return False


def exit_by_completing_evaluation_cycles_to_count():
    '''to have common exit point from the main() method, ie, at the conditional at the
    bottom of the loop, we can force an exit by increasing the evaluation cycles beyond
    what the loop expected to count
    '''
    global evaluation_cycles
    evaluation_cycles = CYCLES_TO_COMPLETE + 1
    return evaluation_cycles


def set_hiker(m, n):
    '''sets hiker position on the forest map
    m rows x n columns coordinates, start 0,0
    **development note: keep hiker set to (3, 1) until modify
    **  method to appropriately alter sensory data that is presented
    **  to the MBCA, ie, visual/auditory/olfactory_possible_inputs[]
    **  for the position of the hiker
    '''
    x = m
    y = n
    global hiker_position
    global forest_map
    if x < 0:
        x = 0
        print('error in map coordinates -- please check code')
    if y < 0:
        y = 0
        print('error in map coordinates -- please check code')
    if x > len(forest_map[0]):
        x = len(forest_map[0]) - 1
        print('error in map coordinates -- please check code')
    if y > len(forest_map[0]):
        y = len(forest_map[0]) - 1
        print('error in map coordinates -- please check code')
    hiker_position = (x, y)
    if forest_map[x][y] == 'MBCA  ':
        forest_map[x][y] = 'RESCUE'
        print('\n**MBCA has rescued lost hiker**')
    elif forest_map[x][y] == 'RESCUE':
        print('\n**MBCA has already rescued lost hiker**')
    else:
        forest_map[x][y] = 'hiker '
        print('hiker position set to: ', x, y, '\n')
    print_forest()
    return x, y


def set_MBCA(m, n):
    '''sets MBCA position on the forest map
        m rows x n columns coordinates, start 0,0
    '''
    x = m
    y = n
    global MBCA_position
    global forest_map
    if x < 0:
        x = 0
        print('error in map coordinates -- please check code')
    if y < 0:
        y = 0
        print('error in map coordinates -- please check code')
    if x > len(forest_map[0]):
        x = len(forest_map[0]) - 1
        print('error in map coordinates -- please check code')
    if y > len(forest_map[0]):
        y = len(forest_map[0]) - 1
        print('error in map coordinates -- please check code')
    if forest_map[x][y] == 'hiker ':
        forest_map[x][y] = 'RESCUE'
        MBCA_position = x, y
        print('\n**MBCA has rescued lost hiker**')
    elif forest_map[x][y] == 'RESCUE':
        print('\n**MBCA has rescued lost hiker**')
    else:
        forest_map[x][y] = 'MBCA  '
        MBCA_position = x, y
    print_forest()
    return x, y


def move_MBCA(direction='00', steps=1):
    '''moves MBCA position on the forest map
    forest_map is m x n coordinate system, start 0,0
    move_MBCA(direction, steps) returns:
    -if 'forest' square returns 'MBCA  '
    -if 'hiker ' square returns 'RESCUE'
    -if 'lake  ' square returns 'LOSS  '
    -if 'ww_rvr' square returns 'DAMAGE'
    -if 'sh_rvr' square returns 'CROSS '
    -if no move then    returns 'STOP  '
    '''
    global MBCA_position
    global forest_map
    #calculate new position
    steps = int(steps)
    delta_x = 0
    delta_y = 0
    current_x = MBCA_position[0]
    current_y = MBCA_position[1]
    if steps < 0:
        print('MBCA did not move. MBCA remains in place this evaluation cycle.')
        print('coding issue -- steps should not be negative value')
        print_forest()
        return 'STOP  '
    if steps == 0:
        print('MBCA did not move. MBCA remains in place this evaluation cycle.')
        print_forest()
        return 'STOP  '
    # m x n coordinate system, so go down south means go to higher row m
    if direction in ('north', 'N', '00'):
        delta_x = -steps
    elif direction in ('south', 'S', '10'):
        delta_x = steps
    elif direction in ('east', 'E', '01'):
        delta_y = steps
    elif direction in ('west', 'W', '11'):
        delta_y = -steps
    else:
        print('coding issue -- direction not valid')
        print('south direction arbitrarily used for number of steps specified or by default')
        delta_y = steps
    current_x += delta_x
    current_y += delta_y
    if current_x < 0:
        current_x = 0
    if current_x > 3:
        current_x = 3
    if current_y < 0:
        current_y = 0
    if current_y > 3:
        current_y = 3
    #update MBCA_position
    print('\nMBCA moved from {}  {},{}'.format(MBCA_position, current_x, current_y))
    previous_x = MBCA_position[0]
    previous_y = MBCA_position[1]
    MBCA_position = current_x, current_y
    #update forest_map
    #change previous square
    if forest_map[previous_x][previous_y] == 'RESCUE':
        forest_map[previous_x][previous_y] = 'hiker '
    elif forest_map[previous_x][previous_y] == 'DAMAGE':
        forest_map[previous_x][previous_y] = 'ww_rvr'
    elif forest_map[previous_x][previous_y] == 'CROSS ':
        forest_map[previous_x][previous_y] = 'sh_rvr'
    elif forest_map[previous_x][previous_y] == 'LOSS  ':
        forest_map[previous_x][previous_y] = 'lake  '
    else:
        forest_map[previous_x][previous_y] = 'forest'
    #change new square
    if forest_map[current_x][current_y] == 'hiker ':
        forest_map[current_x][current_y] = 'RESCUE'
        print('\n**MBCA has rescued lost hiker**')
        print_forest()
        return 'RESCUE'
    if forest_map[current_x][current_y] == 'RESCUE':
        print('\n**MBCA has already rescued lost hiker**')
        print_forest()
        return 'RESCUE'
    if forest_map[current_x][current_y] == 'ww_rvr':
        forest_map[current_x][current_y] = 'DAMAGE'
        print('\n**MBCA has gone into a whitewater river and damaged an articulation**')
        print_forest()
        return 'DAMAGE'
    if forest_map[current_x][current_y] == 'DAMAGE':
        print('\n**MBCA has already been damaged in the lake**')
        print_forest()
        return 'DAMAGE'
    if forest_map[current_x][current_y] == 'sh_rvr':
        forest_map[current_x][current_y] = 'CROSS '
        print('\n**MBCA has gone into a shallow river which it can successfully cross**')
        print_forest()
        return 'CROSS '
    if forest_map[current_x][current_y] == 'CROSS ':
        print('\n**MBCA has successfully crossed a shallow river**')
        print_forest()
        return 'CROSS '
    if forest_map[current_x][current_y] == 'lake  ':
        forest_map[current_x][current_y] = 'LOSS  '
        print('\n**MBCA has gone into a lake and is completely lost**')
        print_forest()
        return 'LOSS  '
    if forest_map[current_x][current_y] == 'LOSS  ':
        print('\n**MBCA has already been lost in the lake**')
        print_forest()
        return 'LOSS  '
    forest_map[current_x][current_y] = 'MBCA  '
    print_forest()
    return 'MBCA  '


def print_forest():
    '''prints out bird's-eye view of forest from system values
    MBCA does not necessarily have this information
    forest_map is m x n coordinate system, start 0,0
    '''
    print("Bird's-Eye View of Forest (MBCA does not have this view)")
    print("-----------------------------------------")
    for i in forest_map:
        for j in i:
            print(j, end='  |  ')
        print("\n-----------------------------------------")
    return True


def print_conscious_memory():
    '''prints conscious memory and whatever analysis method provides
    '''
    print('\n', conscious_memory, '\n')
    return True


def print_mbca_map():
    '''prints out bird's-eye view of forest which MBCA has constructed
    from its explorations
    mbca_map is m x n coordinate system, start 0,0, offset -1,-1 vs forest_map
    -see deprecation note about emulation and replacement with more authentic
    components in finer grain simulations
    '''
    if current_goal in (GOAL_SKEWED_WALK, GOAL_RANDOM_WALK):
        print('MBCA is functioning via random/skewed walk and no internal maps constructed\n')
        return False
    horizontals = "---------------------------------------------------------------------------------------"
    print("\nMBCA Internal Map of Bird's-Eye View of Forest (* is position of MBCA {})".format(MBCA_position))
    print("nb. This is internal map *before* move is made by MBCA")
    print(horizontals + '-')
    m = -1
    for i in mbca_map:
        m = m + 1
        n = -1
        for j in i:
            n = n + 1
            if m in (1, 2, 3, 4) and n in (1, 2, 3, 4) and MBCA_position == (m - 1, n - 1):
                j = j + '*'
            print(j.ljust(10), end='  |  ')
        print('\n', horizontals)
    return True
#
##END METHODS     END METHODS


##START EVALUATION_CYCLES()     START EVALUATION_CYCLES()
#
def evaluation_cycles_nano1(interactive=False):
    '''evaluation cycle of MBCA looped to
    complete mission
    '''
    #sandbox here to quickly try out things -- please erase code afterwards
    #os.system('cls')


    #input('sandbox code has finished')
    #end sandbox

    if interactive:
        input('Click ENTER to start evaluation cycles....')
    global performance_metric_unit
    global performance_metric
    global age_autonomic_calls
    global current_autonomic
    global current_instinct
    global current_goal
    global MBCA_position
    global hiker_position
    global forest_map
    global evaluation_cycles
    evaluation_cycles = 0

    while True:
        #start of evaluation cycle
        evaluation_cycles += 1
        print('STARTING EVALUATION CYCLE # ', evaluation_cycles)
        if age_autonomic_calls == 0:
            setup_MBCA_wumpusworld(message="MBCA Wumpus World set up complete", verbose=True)
        elif age_autonomic_calls% MOD_CYCLE_REEVALUATE == 0:
            sleep_wake('AUTONOMIC: SLEEP/WAKE')
            #print_globals_debug("auton mod triggered at eval cycle sleep_wake just called")
        else:
            #print_globals_debug("**another evaluation cycle....")
            pass

        #propagate input sensory vectors through the subsymbolic processing'
        ##visual
        visual_input = get_inp_vector('INPUT VECTORS SHAP MOD: VISUAL', visual_possible_inputs)
        reflex('AUTONOMIC MODULES: REFLEX VISUAL', visual_input)
        visual_processed = subsymbolic('HLNs-NANO-EQUIVALENT RECEIVE SENSORY: VISUAL', visual_input, visual_actual_inputs)
        print('\nValue of visual_processed: ', visual_processed)

        ##auditory
        auditory_input = get_inp_vector('INPUT VECTORS SHAP MOD: AUDITORY', auditory_possible_inputs)
        reflex('AUTONOMIC MODULES: REFLEX AUDITORY', auditory_input)
        auditory_processed = subsymbolic('HLNs-NANO-EQUIVALENT RECEIVE SENSORY: AUDITORY', auditory_input, auditory_actual_inputs)
        print('\nValue of auditory_processed: ', auditory_processed)

        ##sensory fusion
        fused = sensory_fuse2('SENSORY FUSION', visual_input, auditory_input, fused_actual_inputs, None)
        #fused = sensory_fuse('SENSORY FUSION', auditory_processed, visual_processed)
        max_fused_index, max_fused_value = NESW_fused_select2(fused) #eg: 01010101 [100, 'lost hiker']
        #max_fused_index, max_fused_value = NESW_fused_select(fused) #eg: 01010101 [100, 'lost hiker']
        #print('max fused sensory: ', max_fused_index, '\n', max_fused_value, '\n')
        input('Press a key to continue')

        #evaluate autonomic (ie, energy, damage, etc) and current instinctual state of MBCA
        current_autonomic = get_current_autonomic('CURRENT AUTONOMIC STATUS MODULE')
        #print('returned current_autonomic: ', current_autonomic)
        current_instinct = get_current_instinct('GET CURRENT INSTINCT', max_fused_index, current_autonomic)
        #print('returned current instinct: ', current_instinct, ' --> ', instinct[current_instinct])
        #print_globals_debug("just finished calculating instinct")

        #do pre-causal or fully causal analysis of subsymbolic input information + current instinct
        precausal('PRE-CAUSAL MEMORY INTEGRATION', fused, current_instinct, max_fused_index, max_fused_value, visual_processed, auditory_processed)
        #print_globals_debug("finished precausal")


        #now loop for another evaluation cycle unless reason for main to exit ---------^
        if evaluation_cycles == CYCLES_TO_COMPLETE: #occurs via excess evaluation_cycles
            performance_metric_unit = evaluation_cycles - performance_metric_unit
            performance_metric.append([current_goal, 'cycles used up', performance_metric_unit])
        if evaluation_cycles >= CYCLES_TO_COMPLETE: #occurs via rescue() or mission_failure()
            break
#
##END EVALUATION_CYCLES()     END EVALUATION_CYCLES()



##START MAIN     START MAIN
#
def main_nano():
    '''
    main() of MBCA simulation
    will generally call a particular version of one of the
     nano, micro, mini or full simulation evaluation cycle
     over and over again until the mission is completed
    '''
    #set up platform
    os.system('cls')

    #run mission, repeat mission again or exit
    while True:
        initiate_global_variables()
        sim_choice = choose_simulation()

        #choose to exit program?
        if sim_choice == -1:
            exit_program()

        #call selected simulation
        if sim_choice == 2:
            print('\nMBCA simulation version chosen: "nano" G\n')
            evaluation_cycles_nano1(True)
        else:
            print('\nCurrent software rewrite defaulting to MBCA "nano" G\n')
            evaluation_cycles_nano1(True)
        #repeat mission again or exit?
        print('performance_metric since program started (in cyclesN):  {}\n\n'.format(performance_metric))
        if input('Print out raw conscious memory?') in ('Y', 'y', 'Yes', 'yes'):
            print_conscious_memory()
            print('\n')
        if input('Run again?') in ('N', 'n', 'NO', 'No', 'no', '0', 'stop', 'break'):
            exit_program()
#
##END MAIN      END MAIN
#

#
if __name__ == '__main__':
    main_nano()
else:
    embedded_main_pyboard()
#
#
##START PALIMPSET     START PALIMPSET
#
#pylint: disable=wrong-import-position

#
#Flags used for Development Purposes
#-----------------------------------
TEST_VERBOSITY = False
#More verbose output in various unit tests/POST tests/functional tests
#
FORCE_EMBEDDED_MAIN = False
#Useful to force execution of the Embedded Main version in development
#Will decide which embedded version to run depending on value of PYBOARD and other flags
#
PYBOARD = True
#MicroPython development for use with a PyBoard for which necessary libraries have been installed
#Do not set this flag unless appropriate hardware and appropriate libraries exist.
#
PYTORCH_EMULATION = False
#Will use PyTorch emulation of subsymbolic HLNs
#PyTorch is a deep learning library which we have used as an intermediary step to simulate
#the subsymbolic portions of the MBCA before a full simulation with custom built HLNs is
#working and yielding usable results
#
MEMORY_CHECKING_ON = False
#In testing module will analyze the memory behavior of the Python objects created
#
CHECKPOINT_ON = False
#Used in various points of the code for development debugging
#
DEVELOPER_USER = True
#Development runs versus production runs
#
STOP_SCROLLING_BETWEEN_INPUTS = True
#From version 2 of the MBLS, not actively used in version 3 of MBLS
#
DEVPT_SKIP = True
#Pieces of nonessential code can be skipped in development mode
#
#

#
#Import MBLS Code Modules
#------------------------
#Keeping all the MBLS code together here in this Main Module (ie, top-level script) would be
#nice, but the program is actually more readable by putting dependent functions into external
#modules which are imported here. As well, program loads faster by doing so.
#-New Programmer note: At this time, these modules are **not** listed in PyPI, etc. You must
#make sure these files are in the directory where your Python programs run (or else in path).
#-Style note: Small number of modules, therefore importing "as" to save coding time with the
#long but descriptive module name. If in future the number of modules reaches the lower
#Ebbinghaus number of the human mind, then we will replace the abbrev'ns with full name.
#-Platform dependency note: Will run on all platforms.
import mbls3_low_level_functions as mbll
import mbls_some_version2_low_level_functions as mbv2
#
if PYTORCH_EMULATION:
    import pytorch_hln_nn
#HOP NOTE: From 'Flags used for Development Purposes' at start of code
##PyTorch is a deep learning library which we have used as an intermediary step to simulate
#the subsymbolic portions of the MBCA before a full simulation with custom built HLNs is
#working and yielding usable results
#pylint: enable=unused-import
#
#
#Deprecation/Version3 Transition Upgrade Insertion of Code:
#----------------------------------------------------------
#pylint: disable=invalid-name
#pylint: disable=redefined-outer-name
#
#
#pylint: disable=wildcard-import
#pylint: disable=unused-wildcard-import
#pylint: disable=pointless-string-statement
from mbls_brain_arch_0001 import *
#from mbls_visual_propagation import *
#from mbls_auditory_propagation import *
#from mbls_olfactory_propagation import *
'''
(scope: all below treated as globals)
predefined default matrices to speed up code below:

MATRIX_784x22x0, MATRIX_2000x22x0, MATRIX_2000x22x1,
MATRIX_1000x22x0, MATRIX_1000x22x1

predefined HLN class plus predefined brain layers made up HLN objects:

class HLN()

print('start create hln units ----------------------------')
BRAIN LAYERS FOR ARCH_0001
create v1/k1/a1 layer 784 hlns, 22 line output to 2000 outnodes
create v2/k2/a2 layer 2000 hlns, 22 line output to 2,000 outnodes
create v3/k3/a3 layer 2,000 hlns, 22 line output to 1000.0 (associative) outnodes
create t1 ('t' for associative since 'a' already used and 's' may be for other things)
 layer 1000.0 hlns, 22 line output to 2000 causal outnodes, 2000 logic unit
'''
'''
from mbls_visual_propagation import *
from mbls_auditory_propagation import *
from mbls_olfactory_propagation import *
-sensory propagation levels are quite similar in propagation but any
differences for any particular sense, implemented in the sense's
propagation routines below
-visual must be run first since reset t1[].holding values here
-visual do not compute t1 triggering
-then run olfactory where do not reset t1[].holding nor compute t1 triggering
-then run auditory last where do not reset t1[].holding but
  do compute t1[] auto-associative triggering here
'''
#pylint: enable=wildcard-import
#pylint: enable=unused-wildcard-import
#pylint: enable=wrong-import-position
#
#
#Logging & Development Configuration
#-----------------------------------
#New Programmer note: LOG_FILE is a text file you can examine. It contains various checkpoints
#and debug information posted each time the program runs.
#LOG_FILE will become cumulatively larger. Please manually truncate or erase periodically.
#Research note: Do not truncate or erase any results used for research purposes. Please archive.
LOG_FILE = 'mbls_dump.log'
logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG)
logging.info(time.strftime("%c"))
#
#
#Unit and Functional Testing Configuration
#-----------------------------------------
#In keeping with the philosophy above, we favor easy to use and to read testing frameworks (eg,
#Pytest-like) versus more complex ones (eg, PyUnit/unittest-like).
#-- >pip install pytest
#-- 'test functions' with prefix 'test_' (eg, test_abcxxx) go into file PYTEST_UNIT_FILENAME
#-- >pytest test_mblsxxxx.py    (or whatever filename in PYTEST_UNIT_FILENAME is)
#Style Note:    Ok to keep a commented copy of the test function (or a working copy to use via
#in-program simulation of pytest) near the actual function -- helps you create better tests.
#New Programmer note: Be aware >pytest without a file will automatically find all sorts of files
#with "_test" in name. Pay attention to what directory tree Pytest is operating on if this happens.
#Specific exceptions always are better than general 'except' but for convenience
#development, the latter will be allowed for now.
#pylint: disable=bare-except
#justification: at this point in development general exceptions are adequate
#
#
PYTEST_UNIT_FILENAME = "test_mbls300.py"
PYTEST_FIXTURES = None
PYTEST_FUNCTIONAL1 = None
PYTEST_FUNCTIONAL2 = None
PYTEST_DEPLOYMENT = None
PYTEST_MANUALIZED = None
#
#
#'POST Unit and Functional Testing' -- Power On Self Test Configuration
#----------------------------------------------------------------------
#In keeping with the Human Oriented Programming paradigm, ie, it is hard for human memory to keep
#track of so many things at the same time, we consider using what we call 'POST' unit tests, ie,
#when the program starts up we make sure that some minimal level of unit testing built directly
#into the function, is functional -- the unit test is part of the function, not a separate
#test function and not outside of the main program, but rather, the unit test is part of the
#function and is activated via a simple mechanism such as the setting of a flag on program startup.
#Anecdotally from the HOP perspective, this testing does not have to be exhaustive (ie, some level
#of 'smoke testing' or 'build verification testing' has is fine to accomplish the HOP goal).
#
#
#New Programmer Development Setup Summary Note
#---------------------------------------------
#You're interested in gaining insight into the human mind and creating an AGI, you've read the
#above and are ready to take the plunge. Let's summarize what you need to do:
#1. Acquire the knowledge listed in the section higher above.
#2. You may have used a learning environment to learn Python. Please uninstall it.
#   Install Python with same version as listed above. ( https://www.python.org )
#3. Install a proper code editor. (eg, Windows?  https://notepad-plus-plus.org/ )
#4. Learn how use/setup GitHub (or equivalent git in future). ( https://github.com/ )
#5. Install Pylint. ((command line)> pip install pylint )
#6. Install mypy. ((command line)>pip install mypy-lang )
#7. Install third-party dependencies as explained in the section above. There is a requirements.txt
#   file (explained above) in the GitHub (or equiv) page -- use it.
#8. You need to make sure the MBLS code modules (also on same GitHub (or equiv) page) are in
#   the path of your program (tip- copy them to the directory you are using).
#9. Install latest Pytest ((command line)>pip install pytest )
#10.At the time of writing above is correct, but it will change, eg, in future perhaps we use a
#   a different unit testing utility than Pytest, etc. Please read the comments above and below.
#
#Version Info
#------------
VERSION_NUMBER = 3.04
VERSION_FILE_NAME = 'mbls304.py'
'''
Migration history:

    1.0 Pyth27 -> 2.0 Pyth36 -> 2.0x Basic MBLS
        -> goal 2.1x MBLS 5000 HLNs -> work prematurely stopped for transition to
		->MBLS 3.0:
			-details of MBLS 3.0 on GitHub page
            -simulation to be tailored with capabilities to handle simple case of MBLS
			search-and-rescue robot
			-no longer focus on recognizing digits but general sensory inputs
			-ramp up to 50,000 HLNs
'''
#
#
#Constants used for Program Specifications and Resources
#-------------------------------------------------------
RESET_CODE_CREATE_NEW_MBSL = '9999'
INPUT_WORD_LENGTH = 9
#
#
#Constants used for MultThreading and Embedded Development and Execution
#-----------------------------------------------------------------------
EMBEDDED_MBLS_MULTITHREAD_INTERVALS_SECONDS = 2
EMBEDDED_MBLS_PAUSE_MULTITHREAD_INTERVALS_SECONDS = 0.02
#
#
#Constants used for Managing & Storing Large Data Variables used in the Program
#------------------------------------------------------------------------------
IN_VECS_FILE = 'in_vecs.pkl'
IN_VECS_FILE_TEST = 'tester1.pkl'
START_VALUE = 'start'
END_VALUE = 'end'
SAMPLE_VALUE = 'sample'
TOO_MANY_BYTES_TO_DISPLAY = 1000
TOO_MANY_BYTES_FOR_NORMAL_STORAGE_ROUTINES = 1000000000
HLN_UNITS = 10000
#
#
#Global Variables
#----------------
#Deprecation note: Much of this to be removed in next sub-version.
#justification: will use simple 'g' rather than snake case style
#
#Note: To keep in compliance with OOP paradigm imposed by Python, variables which are
#effectively global variables are defined as objects of function 'g'
#Name change: in previous software versions "input_vector_history"
#
def g():
    '''use this function to store data items as objects
    effectively create global variables compliant with OOP'''
    pass
#Description: main data structure of MBLS system
#Justification: development convenience, avoid emergence of complexity of class implement'n,
#Warnings: survey memory usage, survey for potential side effects as use in devp't
#
#New Programmer note: "If a variable is assigned a value anywhere within the function’s body, it’s
#  assumed to be a local unless explicitly declared as global." -- python.org Programming FAQ
#
#
#Python Installation & Platform Specifications
#---------------------------------------------
#
#
#Note: This code block will run before main() or <alternative>_main() listed at bottom
if DEVELOPER_USER:
    #HOP NOTE: From 'Flags used for Development Purposes' at start of code
    try:
        print('MBLS-3 Project: Python installed: ', os.path.dirname(sys.executable))
    except:
        print('Did not find where Python installed.')

    try:
        print('Version {} of "{}" was last saved/modified {}.'
              .format(VERSION_NUMBER, VERSION_FILE_NAME, time.ctime(
                  os.path.getmtime(VERSION_FILE_NAME))))
        print('Platform Info (via StdLib): \n  ',
              'os.name:', os.name, ', sys.platform:', sys.platform,
              ', platform.system:', platform.system(),
              ', platform.release:', platform.release(),
              '\n  ', 'platform.processor:', platform.processor(), '\n  ',
              'sys.maxsize (9223372036854775807 for 64 bit Python): ', sys.maxsize,
              '\n   GPU resources: ', 'not determined at present')
        if MEMORY_CHECKING_ON:
            #HOP NOTE: From 'Flags used for Development Purposes' at start of code
            print("   Verify memory -- create 10,000 x 10,000 Numpy matrix ....")
            print("   Interim:100x100")
            print(np.zeros((100, 100)))
        print("Ok.... basic infrastructure in place for program to run....\n\n")
    except:
        print('Exception occurred in retrieving platform specifications.')
#
#
####################
#
#  Deprecation Note (Apology)
#  --------------------------
#The software below is a collage of version 1, version 2 and multiple version 3's
#of the MBLS. These earlier versions are of no use to anyone, and serve the sole
#purpose of scaffolding a newer version 3 of the MBLS into existence. We take
#ease-of-understanding to be a major responsibility, and as each new sub-version is
#release more of the scaffolding of older versions will be discarded.
#
#
####################
#
#  Table of Contents
#  -----------------
#  0.  Preface: Version and Technical Notes
#->1.  Introduction: Why Create this Program? <-
#  2.  Sleep/Wake and Autonomic Functions
#  3.  Lower-Level Assist Functions
#      2a. Main Module Lower-Level Assist Functions
#      2b. Imported Module
#  3A. Higher-Level Assist Functions
#  4.  High-Level MBLS Architecture Visible Functions
#      3a. Main Module High-Level MBLS Architecture Visible Functions
#      3b. Imported Module
#  5.  Main Program Code
#  6.  Embedded Software/Hardware Management
#
#

#1. INTRODUCTION: Why Create this Program?
#
#Introduction
#------------
'''At the time of this writing, despite the human-like performance of artificial neural networks
(ANNs) in sensory processing and reinforcement learning (Goodfellow, Bengio and Courville,
2016; Mnih, Kavukcuoglu, Silver, et al., 2015), such neural networks, trained with a very
small quantity of examples, cannot causally make sense of their environment or information
at the level a four-year old child can (Gopnik, Glymour, Sobel et al., 2004; Waismeyer,
Meltzoff, and Gopnik, 2015).  Recent successful work by Graves, Wayne, Reynolds and colleagues
(2016) helps to narrow the neural-symbolic gap. Their model involves an ANN which can read
and write to an external memory, i.e., a hybrid system. However, like the human brain, the
meaningful-based learning system (MBLS), introduced below, can perform the sensory
processing associated with ANNs and the efficient symbolic logic associated with human
cognition, without the use of an external memory, i.e., it is not a physically hybrid system.

Abstract from:
	2018 Annual International Conference on Biologically Inspired Cognitive Architectures
	Meaningful-Based Cognitive Architecture by Howard Schneider:

"An overview is given of the cognitive architecture of the biologically inspired
meaningful-based learning system (MBLS). The basic element of the MBLS is a reconfigurable
Hopfield-like network (HLN) which can rapidly connect to other HLNs depending on the level
of abstraction which yields a practical maximal “meaningfulness,” defined as the reciprocal
of the Shannon entropy of the HLNs. Without any external memory the MBLS synergistically
processes external data (and internal data – “thoughts”) with sensory processing abilities
found in neural networks and some of the symbolic logical abilities found in human cognition.
In practical applications the MBLS offers near-simultaneous pattern recognition and
comprehension. In modeling the development of psychotic disorders in humans, the MBLS
predicts that in many patients the etiology stems from the fragility of the working memory
and the integration of additional reasoning mechanisms during adolescence." '''
#
#Suggested References (last update: Sept 2018)
#---------------------------------------------

#pylint: disable=line-too-long
#justification: non-code area, not worth reformatting
'''
[1]   Goodfellow, I., Bengio, Y. and Courville, A. Deep Learning. Cambridge, MA: MIT Press; 2016.
[2]   Mnih, V., Kavukcuoglu, K., Silver, D. … Hassabis, D. Human-level control through deep reinforcement learning. Nature Feb 26;518(7540):529-33; 2015.
[3]   Gopnik, A., Glymour, C., Sobel, D.M. et al. A Theory of Causal Learning in Children. Psychol Rev 111(1), 3-32; 2004.
[4]   Waismeyer, A., Meltzoff, A.N. and Gopnik, A. Causal learning from probabilistic events in 24-month-olds: an action measure. Developmental Science 18:1, pp175-182; 2015.
[5]   Graves, A., Wayne, G., Reynolds, M., … Hassabis, D.  Hybrid computing using a neural network with dynamic external memory. Nature 538, pp 471-476; 2016.
[6]   Lyke, J.C., Christodoulou, C.G., et al. An introduction to reconfigurable systems. Proc of the IEEE 103(3) 291-317; 2015.
[7]   Rojas, R. The Hopfield Model. In Neural Networks – A Systematic Introduction. New York, NY: Springer-Verlag; 1996.
[8]   Maurer, A., Hersch, M. and Billard, A.G. Extended Hopfield Network for Sequence Learning: Application to Gesture Recognition. Proceedings of the 15th International Conference on Artificial Neural Networks (ICANN), pp. 493- 498; 2005.
[9]   Laird, J.E., Lebiere, C. and Rosenbloom, P.S.  A Standard Model of the Mind: Toward a Common Computational Framework across Artificial Intelligence, Cognitive Science, Neuroscience and Robotics. AI Magazine 38(4); 2017.
[10]  Anderson, J.R., Bothell, D., Byrne, M.D., et al. An Integrated Theory of Mind. Psychol. Rev. 111(4),1036-1060; 2004.
[11]  Lázaro-Gredilla, M., Liu, Y., Phoenix, D.S., and George, D.  Hierarchical compositional feature learning. arXiv preprint arXiv:1611.02252v2; 2017.
[12]  Hawkins, J. and Blakeslee, S.  On Intelligence. New York, NY: Times Books; 2004.
[13]  Kurzweil, R.  How to Create a Mind.  New York, NY: Viking Press; 2012.
[14]  Sabour, S., Frosst, N. and Hinton, G.E.  Dynamic Routing Between Capsules. arXiv preprint arXiv:1710.09829v2; 2017.
[15]  Bastos, A.M., Usrey, W.M., Adams, R.A., et al.  Canonical Microcircuits for Predictive Coding. Neuron 76:695- 711; 2012.
[16]  Schneider, H.  Non-Hybrid Meaningful-Based Learning System Using a Configurable Network of Neural Networks. Proceedings of the 2018 International Conference on Artificial Intelligence  pp 96-102; Aug 2018.
[17]  Mountcastle, V.B. The columnar organization of the neocortex. Brain Apr: 120 (Pt 4):701-22; 1997.
[18]  Buxhoeveden, D.P. and Casanova, M.F. The minicolumn hypothesis in neuroscience. Brain May:125 (Pt 5):935-51; 2002.
[19]  Varela, F.J.  The Specious Present: A Neurophenomenology of Time Consciousness. In: Naturalizing Phenomenology – Jean, Petitot, et al., editors. Chap. 9, pp. 266- 329. Stanford, CA: Stanford University Press; 2000.
[20]  Schwalger, T., Deger, M. and Gerstner, W.  Towards a theory of cortical columns. PLoS Comput. Biol. 13(4); 2017.
[21]  Eliasmith,C. and Trujillo,O.  The use and abuse of large-scale brain models. Curr Opin Neurobiology. Apr; 25:1-6; 2014.
[22]  Cohen, J.D. and Servan-Schreiber, D.  Context, Cortex and Dopamine: A Connectionist Approach to Behavior and Biology in Schizophrenia. Psychological Review 99(1):45-77; 1992.
[23]  Papanastasiou, E., Mouchlianitis, E., Joyce, D.W., et al. Examination of the Neural Basis of Psychoticlike Experiences in Adolescence During Reward Processing. JAMA Psychiatry. Aug 1, doi:10.1001/jamapsychiatry.2018.1973; 2018.
[24]  Muraven,M. and Baumeister,R.F.  Self-regulation and depletion of limited resources. Psychol. Bull. 126(2):247-59; 2000.
[25]  van Os, J., Hanssen, M., Bijil, R.V. et al.  Prevalence of psychotic disorder and community level psychotic symptoms: an urban-rural comparison. Arch. Gen. Psychiatry Jul;58(7):663-8; 2001.
[26]  Jones, C.A., Watson, D.J.G. and Fone, K.C.F.  Animal models of schizophrenia. British Journal of Pharmacology 164:1162-1194; 2011.
[27]  Zhang, R., Pichhioni, M., Allen, P et al. Working Memory in Unaffected Relatives of Patients with Schizophrenia: A Meta-Analysis of Functional Magnetic Resonance Imaging Studies. Schizophrenia Bulletin 42(4): 1068-1077, 2016.
[28]  Bechdolf, A., Wagner, M., Ruhrmann, S. et al.  Preventing progression to first-episode psychosis in early initial prodromal states. British Journal of Psychiatry Jan; 200(1):22-9; 2012.
[29]  Fisher, M., Loewy, R., Hardy, K. et al.  Cognitive interventions targeting brain plasticity in the prodromal and early phases of schizophrenia. Annu Rev Clin Psychol. 9:435-63; 2013.
[30]  Sommer, I.E., Bearden, C.E., van Dellen, E. et al.  Early interventions in risk groups for schizophrenia: what are we waiting for? npj Schizophrenia Mar 9; 2:16003; 2016.
'''
#pylint: enable=line-too-long
#
#
#Overview
#--------
'''
Scroll down to "MAIN PROGRAM CODE" section to see what program does at a
#higher level, and then calls lower level functions.
'''
#
#TL;DR
#-----
'''This code is a simulation of a learning system that tries to combine neural network-like
learning (eg, the way a deep learning network recognizes a photograph) with symbolic-like
learning (eg, if X=2 and Y=3 then X + Y should be 5). Scroll down to 'Main Program' section
to see what the code is doing.

We program to tell a clear story and at the same time create an AGI.
'''


####################

#
#  Table of Contents
#  -----------------
#  0.  Preface: Version and Technical Notes
#  1.  Introduction: Why Create this Program?
#->2.  Sleep/Wake and Autonomic Functions <-
#  3.  Lower-Level Assist Functions
#      2a. Main Module Lower-Level Assist Functions
#      2b. Imported Module
#  3A. Higher-Level Assist Functions
#  4.  High-Level MBLS Architecture Visible Functions
#      3a. Main Module High-Level MBLS Architecture Visible Functions
#      3b. Imported Module
#  5.  Main Program Code
#  6.  Embedded Software/Hardware Management
#
#2. SLEEP/WAKE AND AUTONOMIC FUNCTIONS

#The sleep/wake and autonomic functions are inspired by the analogous biological functions,
#but their purpose is not to mimic nature but provide a useful level of very high overall
#control of the MBLS with regard to the sleep/wake functions, and to provide
#"stimulus->action"=="reflex" == "reptilian-like neurological functioning" ie, no cortical-like
#functioning but more of stimulus-action functioning although the strong caveat is made
#here that reptiles and birds and have cortical-like portions of their pallium and the
#stimulus->action effect is actually much more involved and processed than say stimulus->action
#in a worm. Thus, really the autonomic functions should be thought of as providing
#invertebrate-like stimulus->action processing, or if the case of mammals is considered,
#basic reflexes and basic autonomic processing.
#
#
#This section will be divided in future as number of functions grow into separate sleep/wake
#section, separate reflex autonomic function section (useful for very fast decisions)
#and more processed autonomic function section.
#
#
#pylint: disable=undefined-variable
#justification: results from blocking pympler import
def memory_var_usage(post_test: bool = False)->bool:
    '''Uses pympler third-party dependency to: "to measure, monitor and analyze
    the memory behavior of Python objects in a running Python application."
        Useful dev tool as MBLS data structure grows very large.
    Args:
        --
    Style/use note:
        -Usually pympler is only imported and used for occasional dev work
    Returns:
        True/ False depending on successful run
    Raises:
        try/except
'''
    if post_test:
        #HOP NOTE: Power On Self Testing to ensure function working at minimal level
        return memory_var_usage_test()

    try:
        variable_memory = summary.summarize(muppy.get_objects())
        print('\n'.join(summary.format_(variable_memory)))
        return True
    except:
        print('Pympler not active. No memory map printed out.')
        return False


def memory_var_usage_test()-> bool:
    ''' Unit testing of above function (with a "_test" suffix added) (suffix allows ordering)
        -This function, with appropriate imported file prefixes to variables (since this program
        must be imported) is stored in the Pytest testing file specified by PYTEST_UNIT_FILENAME.
        -It can also used for testing directly within this program.
        Args:
            --
        Style/use note:
        -We stylistically allow keeping the unit test functions close to the actual functions, so
        both can be examined together, encouraging the developer to create the most useful tests.
        -Simple unit test to ensure basic existence and functioning of memory_var_usage()
        Returns:
            True if make it to end of test and no try/except error occurs in tested function
        Raises:
            --
    '''
    print('\n\n&START UNIT TEST: memory_var_usage()')
    logging.info('\n&START UNIT TEST: memory_var_usage()')
    if memory_var_usage():
        logging.info('&END UNIT TEST: memory_var_usage(): success\n')
        print('&END UNIT TEST: memory_var_usage(): success\n')
        return True
    print('MEMORY_CHECKING_ON is set as: ', MEMORY_CHECKING_ON)
    #HOP NOTE: From 'Flags used for Development Purposes' at start of code
    logging.info('&END UNIT TEST: memory_var_usage(): FAILURE\n')
    print('&END UNIT TEST: memory_var_usage(): FAILURE\n')
    return False


def in_vecs_erase(file_name: str = IN_VECS_FILE, verbose: int = 0)-> int:
    ''' Erases file IN_VECS_FILE
        -therefore when MBLS attempts next load operation a new MBLS will be created
            in_vecs is a list holding vector info about MBLS HLN connections.
            IN_VECS_FILE -- pickled file where store this variable
        Args:
            file_name: optional filename; default is IN_VECS_FILE specified above
            verbose: if nonzero -  more verbose print and log messages
        Style/use note: -For development convenience in_vecs kept as global for moment
                    -Works well as is with typical local hard/SSD storage; consider more fault-
                    tolerant coding in future for network storage and mod the bare exceptions
        Returns:
                0  unable to successfully run (expect 'success' even if file non-existent)
                +1 if  runs to end of routine but does not actually erase file
                +2 if  actually erased the file
        Raises:
                fault-tolerant operation: no
                try-except raised if any issue in calling os.remove(<file>)
    '''
    try:
        if os.path.isfile(file_name):
            os.remove(file_name)
            logging.info('in_vecs_erase: IN_VECS_FILE file erased')
            print('IN_VECS_FILE (MBLS data) erased. When restart/reload will act as new MBLS.')
            return_value = 2
        else:
            if verbose:
                print('{} does not exist. Nothing to erase....'.format(file_name))
            return_value = 1
    except:
        logging.info('in_vecs_erase: EXCEPTION in in_vecs_erase routine ')
        print('in_vecs_erase: EXCEPTION in in_vecs_erase routine ')
        return_value = 0
    return return_value


def in_vecs_load(file_name: str = IN_VECS_FILE, verbose: int = 0)-> int:
    ''' Loads file IN_VECS_FILE into "in_vecs" data variable
            in_vecs is a list holding vector info about MBLS HLN connections.
            IN_VECS_FILE -- pickled file where store this variable
        Args:
            file_name: optional filename; default is IN_VECS_FILE specified above
            verbose: if nonzero -  more verbose print and log messages
        Style/use note:-The 'with' statement will automatically close the file after each code block
                    -For development convenience in_vecs kept as global for moment
                    -Works well as is with typical local hard/SSD storage; consider more fault-
                    tolerant coding in future for network storage and mod the bare exceptions
        Returns:
                0  unable to successfully run
                +1 if  runs to end of routine
                IMPORTANT: Note that we clear global in_vecs (var, not file) and then attempt to
                    load in storage contents into the cleared in_vecs
                    if function fails, in_vecs still remains cleared
        Raises:
                fault-tolerant operation: no
                try-except raised if any issues
    '''
    try:
        if not os.path.isfile(file_name):
            print("New MBLS detected -- will create IN_VECS_FILE file to store data.")
            with open(file_name, 'wb') as f_l:
                pickle.dump([], f_l)
        in_vecs.clear()   #IMPORTANT: Note that we clear in_vecs here (var, not file)
        with open(file_name, 'rb') as f_l:
            contents = pickle.load(f_l)
        for value in contents:
            in_vecs.append(value)
        if verbose and sys.getsizeof(in_vecs) < TOO_MANY_BYTES_TO_DISPLAY:
            print('in_vecs loaded: ', in_vecs)
        return_value = 1
    except:
        print('Failed to open or load info from file {}'.format(file_name))
        logging.info('in_vecs_load: FAILED\n')
        return_value = 0
    return return_value


def in_vecs_save(file_name: str = IN_VECS_FILE, verbose: int = 0)-> int:
    ''' Save in_vecs variable into file IN_VECS_FILE
            in_vecs is a list holding vector info about MBLS HLN connections.
            IN_VECS_FILE -- pickled file where store this variable
        Args:
            file_name: optional filename; default is IN_VECS_FILE specified above
            verbose: if nonzero -  more verbose print and log messages
        Style/use note:-The 'with' statement will automatically close the file after each code block
                    -For development convenience in_vecs kept as global for moment
                    -Works well as is with typical local hard/SSD storage; consider more fault-
                    tolerant coding in future for network storage and mod the bare exceptions
        Returns:
                0  unable to successfully run
                +1 if  runs to end of routine
        Raises:
                fault-tolerant operation: no
                try-except raised if any issues
     '''
    try:
        with open(file_name, 'wb') as f_s:
            pickle.dump(in_vecs, f_s)
        if verbose:
            pass
        return_value = 1
    except:
        print('Failed to save into file {}'.format(file_name))
        logging.info('in_vecs_load: FAILED\n')
        return_value = 0
    return return_value


def in_vecs_load_test(file_name: str = IN_VECS_FILE_TEST, verbose: int = 0)-> bool:
    ''' Unit testing of above function (with a "_test" suffix added) (suffix allows ordering)
        NOTE: This unit test combines the in_vecs_load_test, in_vecs_save_test and
        in_vecs_erase_test into this single in_vecs_load_test. The other unit tests are now
        deprecated.
        -This function, with appropriate imported file prefixes to variables (since this program
        must be imported) is stored in the Pytest testing file specified by PYTEST_UNIT_FILENAME.
        -It can also used for testing directly within this program.
        Args:
            file_name: optional filename; default is IN_VECS_FILE specified above
            verbose: if nonzero -  more verbose print and log messages
        Style/use note:
        -We stylistically allow keeping the unit test functions close to the actual functions, so
        both can be examined together, encouraging the developer to create the most useful tests.
        -We allow in unit tests large functions created by their verbose mode if/print's.
        -Warning: Actual function is being called and may have side effects on program.
            (Safer to run in Pytest external file. However, attempt always made to restore values.)
                  "&" precedes all printed lines ("&&" if verbose test function print out)
        Returns:
            True if make it to end of test and no assert error occurs
        Raises:
            AssertionError -- see below
    '''
    #pylint: disable =invalid-name
    #pylint: disable =global-statement
    #pylint: disable =global-variable-undefined
    global in_vecs
    #justification: need to restore in_vecs after unit test is complete

    print('\n&START UNIT TEST: in_vecs_load/save/erase()')
    logging.info('\n&START UNIT TEST: in_vecs_load/save/erase()')
    if verbose and sys.getsizeof(in_vecs) < TOO_MANY_BYTES_TO_DISPLAY:
        if in_vecs == []:
            in_vecs.append(SAMPLE_VALUE)
        print('in_vecs before test starts: ', in_vecs)
    restore_later_in_vecs = list(in_vecs)
    in_vecs.clear()

    try:
        if PYTORCH_EMULATION:
            pytorch_hln_nn.emulation_cycle()
        else:
            in_vecs_erase(file_name, verbose)
            in_vecs_load(file_name, verbose)
            in_vecs.append(START_VALUE)
            in_vecs.append(END_VALUE)
            print('in_vecs with some entries now and save next: ', in_vecs)
            in_vecs_save(file_name, verbose)
            first_length = sys.getsizeof(in_vecs)
            in_vecs.clear()
            print('in_vecs after being cleared: ', in_vecs)
            in_vecs_load(file_name, verbose)
            print('in_vecs after being reloaded from file: ', in_vecs)
            second_length = sys.getsizeof(in_vecs)
            assert first_length == second_length
            assert in_vecs[0] == START_VALUE
            in_vecs = list(restore_later_in_vecs)
            restore_later_in_vecs.clear()
            if verbose and sys.getsizeof(in_vecs) < TOO_MANY_BYTES_TO_DISPLAY:
                print('in_vecs after test over: ', in_vecs)
            logging.info('&END UNIT TEST: in_vecs_load/save/erase(): success\n')
            print('&END UNIT TEST: in_vecs_load(): success\n')
            return True
    except:
        if PYTORCH_EMULATION:
            return False
        in_vecs = list(restore_later_in_vecs)
        restore_later_in_vecs.clear()
        if verbose and sys.getsizeof(in_vecs) < TOO_MANY_BYTES_TO_DISPLAY:
            print('in_vecs after test over: ', in_vecs)
        logging.info('&END UNIT TEST: in_vecs_load/save/erase(): FAILURE\n')
        print('&END UNIT TEST: in_vecs_load/save/erase(): FAILURE\n')
        return False
    return False
    #pylint: enable =invalid-name
    #pylint: enable =global-statement


def sleep_selection(sleep_phase: int) -> int:
    '''Allows setting of wake or sleep phase to another particular sleep phase.
    Args:
        sleep_phase: what sleep phase to switch the MBLS into
    0 -- awake
    1 - 3 -- normal sleep phases to accomplish various maintenance and energy
        conserving routines (light sleep can be useful for the embedded version of the code)
    4 causes hibernation of the MBLS,ie, it (optionally) saves data and program exits
        Interactive input requested: If user does not want to hibernate then  sleep phase = 3
        Interactive input requested: If user wants to hibernate then user asked if wants to
        save data (program can boot up with same data) or not (program boots up as new MBLS)
    5 is considered REM -- again a phase to accomplish various maintenance routines
    6 - 8 -- anesthetic states to allow system debug and repair operations
    9 -- runs all (or all of a set) existing internal unit tests and then exits
    Inspired by biology but goal is for MBLS to create a great AGI, not mimic the biological
        brain down to spiking neurons.
    Style/use note: (for this function near top of program): Written so human mind can easily follow
    assumptions and logic. While, for the sake of example, using a dictionary of functions to
    emulate a switch/case structure, instead of the if/then's below would operate faster (ie,
    jump to dict item rather than go through a sequence of if/then's, this is immaterial in this
    section of the code. Except in critical areas of the code, we write for the reader,
    not the computer
    Returns:
        0..9 :The sleep/wake/debug phase MBLS now switched to
        RESET_CODE_CREATE_NEW_MBSL: if hibernation == system exit(asked if want to save data)
        -1: An error occurred
    Raises:
        --
    '''
    logging.info(' '.join(['sleep_selection(): sleep_phase = ', str(sleep_phase)]))
    all_allowed_sleep_values = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    hibernation_value = 4
    avoid_hibernation_conversion_value = 3
    run_internal_tests_value = 9

    if sleep_phase == run_internal_tests_value:
        print('Triggered run of internal test. Verbose == 0 ')
        unit_testing_functions_that_can_be_called_within_the_code()
        sleep_phase = hibernation_value
    if sleep_phase == hibernation_value:
        print('Awake/Sleep Phase switching to "Hibernation/reset"')
        if 'y' in input('Would you like to leave the MBLS asleep and exit? (y/n): '):
            print('Hibernation treated as a system exit code -- program will stop running.')
            if 'y' in input('Would you like to save data? (y/n): '):
                logging.info('call to save data before system exit')
                in_vecs_save()
            else:
                in_vecs_erase()
            print('Thank you....system exit underway....')
            logging.info('hibernation sleep phase parameter, return value will trigger sys exit')
            return_value = int(RESET_CODE_CREATE_NEW_MBSL)
        else:
            sleep_phase = avoid_hibernation_conversion_value
            print('Hibernation canceled. New sleep phase is {}.'.format(sleep_phase))
    if sleep_phase in all_allowed_sleep_values and sleep_phase != hibernation_value:
        return_value = set_sleep_phase(sleep_phase)
    if sleep_phase not in all_allowed_sleep_values:
        print('Coding error: sleep_phase "{}" not valid. No effect.'.format(sleep_phase))
        return_value = -1
        logging.info('inappropriate sleep phase parameter detected....')
    logging.info(' '.join(['leaving sleep_selection, return value = ', str(return_value)]))
    return return_value


def test_sleep_selection()-> bool:
    ''' Unit testing of above function (with a "test_" prefix added)
        -This function, with appropriate imported file prefixes to variables (since this program
        must be imported) is stored in the Pytest testing file specified by PYTEST_UNIT_FILENAME.
        -It can also used for testing directly within this program via Pytest-like feature in
        development mode of the MBLS code.
        -We stylistically allow keeping the unit test functions close to the actual functions, so
        both can be examined together, encouraging the developer to create the most useful tests.
        -Warning: Do NOT execute as part of normal program -- actual function is being called and
        will have side effects on program. Run in external file or if within in special dev mode.
        Args:
            verbose:
                optional with default of 0
                within this function directly:
                    verbose mode of some prints of actions
                    prompts user for interactive sleep_phase 4 input
        Style/use note:
        -We stylistically allow keeping the unit test functions close to the actual functions, so
        both can be examined together, encouraging the developer to create the most useful tests.
        Returns:
        Raises:
            -
    '''
    print('&START UNIT TEST : test_sleep_selection')
    logging.info('&START UNIT TEST: sleep_selection()')
    print("#Interactive input required: !!Do NOT opt to exit program!!")
    try:
        for phase in [(-888, -1), (0, 0,), (1, 1), (2, 2), (3, 3), (4, 3),
                      (5, 5), (6, 6), (7, 7), (8, 8), (55, -1)]:
            assert sleep_selection(phase[0]) == phase[1]
        print('&UNIT TEST OVER : test_sleep_selection: success\n')
        logging.info('&END UNIT TEST: sleep_selection(): success')
        return True
    except:
        print('&UNIT TEST OVER : test_sleep_selection: FAILURE\n')
        logging.info('&END UNIT TEST: sleep_selection(): FAILURE')
        return False


def set_sleep_phase(sleep_phase: int)-> int:
    ''' Part of setting the sleep phase
        Called by sleep_selection(sleep_phase)
        Useful for future use in expanding functionality of each sleep phase
        Args:
            sleep_phase: what sleep phase MBLS has now been switched to
            see parent function for meanings of the sleep phase
        Style/use note:
            --
        Returns:
            0..9 :The sleep/wake/debug phase MBLS switched to
        Raises:
            --
    '''
    if sleep_phase in [1, 2, 3, 4, 5]:
        print('Future use: any necessary sleep routines called here')
        print('MBLS is asleep now in sleep phase ', sleep_phase, '.')
    elif sleep_phase == 9:
        print('Sleep code 9 will trigger internal testing now.')
    elif sleep_phase in [6, 7, 8]:
        print('Future use: any necessary sleep routines called here')
        print('Sleep code 6, 7 or 8 will trigger special debug states.')
    elif sleep_phase == 0:
        print('Future use: any necessary sleep routines called here')
        print('MBLS is now in awake state.')
    else:
        print('MBLS in other awake/sleep/maintenance/debug state.')
    return sleep_phase

def start_active_time(active_time: int = 0)->int:
    '''Keep track of active time main while loop has been
       running; used to decide when to switch to a sleep cycle
       Called by main program loop
       Args:
        active_time -- starting time
       Style/use note:
        --
       Returns:
        time in seconds rounded to integer value
       Raises:
        --
    '''
    #TODO -- complete active part of function (different one used in
    #deprecated version 2
    #TODO all time and sleep routines need fault tolerance so if failed
    #program does not stop at this point
    return active_time


def start_cumulative_time()->int:
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1



####################


#
#  Table of Contents
#  -----------------
#  0.  Preface: Version and Technical Notes
#  1.  Introduction: Why Create this Program?
#  2.  Sleep/Wake and Autonomic Functions
#->3.  Lower-Level Assist Functions<--
#      2a. Main Module Lower-Level Assist Functions
#      2b. Imported Module
#  3A. Higher-Level Assist Functions
#  4.  High-Level MBLS Architecture Visible Functions
#      3a. Main Module High-Level MBLS Architecture Visible Functions
#      3b. Imported Module
#  5.  Main Program Code
#  6.  Embedded Software/Hardware Management
#


#3. LOWER-LEVEL ASSIST FUNCTIONS

#The functions help other functions do their tasks
#(further below are the MBLS Architecture functions)
#Lower-level assist functions do one or a few lower-level tasks,
#while the higher-level assist functions do more of function calling
#to prevent too much code in the main code section
#
#


#def welcome function put into module extra_fcns.py
#





def set_debugging_level():
    '''set debugging level
    '''
    #pylint: disable=global-statement
    #justification: old version 2 code
    #ToDo -- needs to be updated to version 3 code
    global CHECKPOINT_ON
    #HOP NOTE: From 'Flags used for Development Purposes' at start of code
    if CHECKPOINT_ON is False:
        x_1 = input('Would you like to turn CHECKPOINT tracer on? (y/Y): ')
        if x_1 in ('y', 'Y'):
            CHECKPOINT_ON = True
            #pylint: enable=global-statement

def checkpoint_tracer(checkpoint_name, return_output):
    '''
    If CHECKPOINT_ON is True then any function or other part of program which
    contains this function, will display an execution of the checkpoint.
    (Useful at times for quick program execution checking.)
    (Use debugger for more extensive trace: python -m pdb *.py )
    '''
    if CHECKPOINT_ON:
    #HOP NOTE: From 'Flags used for Development Purposes' at start of code
        x_1 = input\
    ('Checkpoint: {}, Returns:{} -->ENTER....'.format(checkpoint_name, return_output))
        print('what happened to x -- check code', x_1)


def stop_scrolling_check():
    '''The processing of an input, and other possible program executions,
    can generate many lines of text on the monitor screen. Thus there are
    'scrolling checks' where the user is asked to press any key so that the
    user has a chance to see what was just displayed on the terminal screen.
    However, to avoid having to do this keystroke, eg, with each new input cycle,
    user can enter a code, eg, 99, to stop this.'''
    #pylint: disable=global-statement
    #justification: old version 2 code
    global STOP_SCROLLING_BETWEEN_INPUTS
    #HOP NOTE: From 'Flags used for Development Purposes' at start of code
    if STOP_SCROLLING_BETWEEN_INPUTS:
        if input("\n---->NEW INPUT CYCLE -- Press any key to continue "
                 "('s' to stop scroll prompts)") == 's':
            print('Prompt turned off....')
            STOP_SCROLLING_BETWEEN_INPUTS = False
            #pylint: enable=global-statement


def update_in_vecs(x_1):
    '''Keeps track of what input vectors
    sent into the MBLS.
    Useful for evaluation/debug use.
    '''
    #pylint: disable=invalid-name
    #pylint: disable=global-statement
    #pylint: disable =global-variable-undefined
    global in_vecs
    #justification: 'in_vecs' global justification given above
    #pylint: enable=global-statement
    #pylint: enable=invalid-name

    in_vecs.append(x_1)


def print_in_vecs():
    '''Prints what input vectors were
    sent into MBLS. No mods made here.
    Useful for evaluation/debug use.
    '''
    print(in_vecs)


#def display_8_segments(aa) is imported from mbls_some_version2_low_level_functions as mbv2


####################

#3A. HIGHER-LEVEL ASSIST FUNCTIONS

#(further below are the MBLS Architecture functions)
#Lower-level assist functions do one or a few lower-level tasks, while
#the higer-level assist functions do more of function calling to
#to prevent too much code in the main code section
#
#
#pylint: disable=line-too-long
#justification: old version 2 code
def start_simulation(message_x):
    '''consider if developer or user is using when start
    program
    '''
    if DEVELOPER_USER:
        #HOP NOTE: From 'Flags used for Development Purposes' at start of code
        print("System is running in Developer User Mode right now.")
        print('Version {} of "{}" was last modified {}.'.format(VERSION_NUMBER, VERSION_FILE_NAME, time.ctime(os.path.getmtime(VERSION_FILE_NAME))))
        print('Platform Info (warning: tend to get conflicting info from Python Standard Library routines -- verify if important): \n  ',
              '(note that conventional AMD and Intel CPUs are both functionally compatible with x86(_64) architecture) \n  ',
              'os.name:', os.name, '\n  ', 'sys.platform:', sys.platform, '\n  ', 'platform.system:', platform.system(), '\n  ',
              'platform.release:', platform.release(), '\n  ', 'platform.machine:', platform.machine(), '\n  ', 'platform.architecture:', platform.architecture(),
              '\n  ', 'platform.processor:', platform.processor(), '\n   sys.maxsize (9223372036854775807 for 64 bit Python): ', sys.maxsize,
              '\n   GPU resources: ', 'not determined at present')
        print("Verify no memory error from creating 10,000 x 10,000 Numpy matrix ....")
        print("Interim mod: 100 x 100 matrix for moment.... ")
        print(np.zeros((100, 100)))
        print("Ok.... basic infrastructure in place for program to run....")
        #set_debugging_level()
        print('\n')

    if not DEVELOPER_USER:
        #HOP NOTE: From 'Flags used for Development Purposes' at start of code
        print("Running in Normal User Mode (not Developer Mode)")

    mbll.welcome(message_x)
#pylint: enable=line-too-long

####################

#
#  Table of Contents
#  -----------------
#  0.  Preface: Version and Technical Notes
#  1.  Introduction: Why Create this Program?
#  2.  Sleep/Wake and Autonomic Functions <-
#  3.  Lower-Level Assist Functions
#      2a. Main Module Lower-Level Assist Functions
#      2b. Imported Module
#  3A. Higher-Level Assist Functions
#->4.  High-Level MBLS Architecture Visible Functions<-
#      3a. Main Module High-Level MBLS Architecture Visible Functions
#      3b. Imported Module
#  5.  Main Program Code
#  6.  Embedded Software/Hardware Management
#

#4. HIGH-LEVEL MBLS ARCHITECTURE VISIBLE FUNCTIONS

#Each of these functions corresponds to a high-level
#component of the MBLS Cognitive Architecture
#
#

#pylint: disable=too-many-statements
#pylint: disable=invalid-name
#justification: old version 2 code, needs to be updated

###########################################################

#
#Deprecation/Version3 Transition Upgrade Insertion of Code:
#----------------------------------------------------------
#
def apply_visual_inputs():
    '''applies visual input v0 vector to layer v1
    -layer 1 really is just holding input layer since it does not
     receive inputs diagonally, just directly from layer 0
    '''
    for i in range(784):
        v1[i].out = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for j in range(22):
            v1[i].out[j] = random.random()
    #print('v1[111]: ', v1[111].out)
    #print('v1[112]: ', v1[112].out)
    return 'no actual visual transducer detected, thus seeded input values'

def apply_v1_to_v2():
    '''feedforward v1 to v2
    -v1 is just holding inputs so we don't care if triggered
    -v1 propagates to all v2 via lines and weights to v2.holding
    -after all the v1's propagated to v2's, we then go through the v2.holding and
        see which v2's are triggered
    -v1 is 784 (0..783) hln's each going to (0..1999) 2000 v2's
    '''
    #pylint: disable=line-too-long
    print('entering apply_v1_to_v2 procedure')
    #ensure v2[0..1999].holding & .out are set up to 22 rows, and all values reset to 0
    for j in range(2000):
        v2[j].holding = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        v2[j].out = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    #ensure v1[0..783].out is correct size of 22 rows
    for i in range(784):
        if len(v1[i].out) < 22:
            print('v1.out shorter than 22 detected', i, v1[i].out)
            for k in range(22 - len(v1[i].out)):
                v1[i].append(0)
    #now feedforward each v1[0..783] to all the v2[0..1999] via weights connecting them
    for i in range(784):
        for j in range(2000):
            for k in range(22):
                v2[j].holding[k] = v2[j].holding[k] + (v1[i].out[k] * v1[i].wt[j][k] * v1[i].abstraction_addressor[j][k])
    #at this point v2.holding has all propagated values from v1
    #randomly seed some of v2's with associate values corresponding to inputs
    for j in range(2000):
        if random.randint(1, 8) == 3:
            v2[j].assoc_value = v2[j].holding
    #now we see if any of the v2's auto-association triggered
    #auto_associate returns a score, and normalize by length of assoc_value, and if large enough
    # then consider neuron as having auto-associatively triggered to assoc_value
    for j in range(2000):
        if v2[j].auto_associate(v2[j].holding, v2[j].assoc_value)/len(v2[j].assoc_value) > 0.35:
            #optional for now -- if triggered neuron, set assoc_value to holding
            #want to consider removing in future
            v2[j].assoc_value = v2[j].holding
            #since auto-assoc triggered, there is a v2[].out value now
            v2[j].out = v2[j].assoc_value
    #at this point, v2[].out is 0 if not triggered, or v2[].out==assoc_value if triggered
    #for i in range(20):
    #   print('v2[i].out :', v2[i].out)
    #pylint: enable=line-too-long
    return 'v1 to v2 feedforward done'


def apply_v2_to_v3():
    '''feedforward v2 to v3
    -v2[].out  is 0 if not triggered or holds auto-associative value if triggered
    -v2 propagates to all v3 via lines and weights to v3.holding
    -after all the v2's propagated to v3's, we then go through the v3.holding and
        see which v3's are triggered
    -v2 is 2000 (0..1999) hln's each going to (0..1999) 2000 v3's
    '''
    print('entering apply_v2_to_v3 procedure')
    #ensure v3[0..1999].holding & .out are set up to 22 rows, and all values reset to 0
    for j in range(2000):
        v3[j].holding = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        v3[j].out = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    #ensure v2[0..1999].out is correct size of 22 rows
    for i in range(1999):
        if len(v2[i].out) < 22:
            print('v2.out shorter than 22 detected', i, v2[i].out)
            for k in range(22 - len(v2[i].out)):
                v2[i].append(0)
    #now feedforward each v2[0..1999] to all the v3[0..1999] via weights connecting them
    #pylint: disable=line-too-long
    for i in range(2000):
        for j in range(2000):
            for k in range(22):
                v3[j].holding[k] = v3[j].holding[k] + (v2[i].out[k] * v2[i].wt[j][k] * v2[i].abstraction_addressor[j][k])
    #at this point v3.holding has all propagated values from v2
    #randomly seed some of v3's with associate values corresponding to inputs
    for j in range(2000):
        if random.randint(1, 40) == 3:
            v3[j].assoc_value = v3[j].holding
    #now we see if any of the v3's auto-association triggered
    #auto_associate returns a score, and normalize by length of assoc_value, and if large enough
    # then consider neuron as having auto-associatively triggered to assoc_value
    for j in range(2000):
        if v3[j].auto_associate(v3[j].holding, v3[j].assoc_value)/len(v3[j].assoc_value) > 0.35:
            #optional for now -- if triggered neuron, set assoc_value to holding
            #want to consider removing in future
            v3[j].assoc_value = v3[j].holding
            #since auto-assoc triggered, there is a v3[].out value now
            v3[j].out = v3[j].assoc_value
    #at this point, v3[].out is 0 if not triggered, or v3[].out==assoc_value if triggered
    temp = 0
    for i in range(2000):
        if v3[i].out[0] != 0:
            temp += 1
    print('total number of triggered v3[].outs: ', temp)
    return 'v2 to v3 feedforward done'


def apply_v3_to_t1():
    '''feedforward v3 to t1
    -v3[].out  is 0 if not triggered or holds auto-associative value if triggered
    -v3 propagates to all t1 via lines and weights to t1.holding
    -after all the v3's propagated to t1's, we then go through the t1.holding and
        see which t1's are triggered
    -v3 is 2000 (0..1999) hln's each going to (0..999) 1000 t1's
    '''
    #pylint: disable=line-too-long
    print('entering apply_v3_to_t1 procedure')
    print('should run this sensory propagation routine first since reset holding values')
    #ensure t1[0..999].holding & .out are set up to 22 rows, and all values reset to 0
    #make sure not to erase if propagating multiply senses to t1 area
    for j in range(1000):
        t1[j].holding = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        t1[j].out = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    #ensure v3[0..1999].out is correct size of 22 rows
    for i in range(1999):
        if len(v2[i].out) < 22:
            print('v3.out shorter than 22 detected', i, v3[i].out)
            for k in range(22 - len(v3[i].out)):
                v3[i].append(0)
    #now feedforward each v3[0..1999] to all the t1[0..999] via weights connecting them
    for i in range(2000):
        for j in range(1000):
            for k in range(22):
                t1[j].holding[k] = t1[j].holding[k] + (v3[i].out[k] * v3[i].wt[j][k] * v3[i].abstraction_addressor[j][k])
    #at this point t1.holding has all propagated values from v3
    #randomly seed some of t1's with associate values corresponding to inputs
    for j in range(1000):
        if random.randint(1, 3) == 3:
            if v3[j].out != [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
                t1[j].assoc_value = t1[j].holding
    #now we see if any of the v3's auto-association triggered
    #auto_associate returns a score, and normalize by length of assoc_value, and if large enough
    # then consider neuron as having auto-associatively triggered to assoc_value
    '''this will be done by last sensory propagation routines the auditory ones
    for j in range(1000):
        if t1[j].auto_associate(t1[j].holding, t1[j].assoc_value)/len(t1[j].assoc_value) > 0.35:
            #optional for now -- if triggered neuron, set assoc_value to holding
            #want to consider removing in future
            t1[j].assoc_value = t1[j].holding
            #since auto-assoc triggered, there is a v3[].out value now
            t1[j].out = t1[j].assoc_value
    #at this point, t1[].out is 0 if not triggered, or t1[].out==assoc_value if triggered
    temp = 0
    for i in range(1000):
        if t1[i].out[0] != 0:
            temp += 1
    print('total number of triggered t1[].outs: ', temp)
    #for i in range(1000):
    #   print(i, 't1[i].out :', t1[i].out)'''
    #pylint: enable=line-too-long
    return 'v3 to t1 feedforward done'

#olfactory sensory propagation
'''
from mbls_olfactory_propagation import *
-sensory propagation levels are quite similar in propagation but any
differences for any particular sense, implemented in the sense's 
propagation routines below
'''
def apply_olfactory_inputs():
    '''applies olfactory input a0 vector to layer a1
    (for convenience just use constants below)
    -layer 1 really is just holding input layer since it does not
     receive inputs diagonally, just directly from layer 0
    '''

    for i in range(784):
        k1[i].out = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for j in range(22):
            k1[i].out[j] = random.random()
    #print('k1[111]: ', k1[111].out)
    return 'no actual olfactory transducer detected, thus seeded input values'


def apply_k1_to_k2():
    '''feedforward k1 to k2
    -k1 is just holding inputs so we don't care if triggered
    -k1 propagates to all k2 via lines and weights to k2.holding
    -after all the k1's propagated to k2's, we then go through the k2.holding and
        see which k2's are triggered
    -k1 is 784 (0..783) hln's each going to (0..1999) 2000 k2's
    '''
    #pylint: disable=line-too-long
    print('entering apply_k1_to_k2 procedure')
    #ensure k2[0..1999].holding & .out are set up to 22 rows, and all values reset to 0
    for j in range(2000):
        k2[j].holding = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        k2[j].out = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    #ensure k1[0..783].out is correct size of 22 rows
    for i in range(784):
        if len(k1[i].out) < 22:
            print('k1.out shorter than 22 detected', i, k1[i].out)
            for k in range(22 - len(k1[i].out)):
                k1[i].append(0)
    #now feedforward each k1[0..783] to all the k2[0..1999] via weights connecting them
    for i in range(784):
        for j in range(2000):
            for k in range(22):
                k2[j].holding[k] = k2[j].holding[k] + (k1[i].out[k] * k1[i].wt[j][k] * k1[i].abstraction_addressor[j][k])
    #at this point k2.holding has all propagated values from k1
    #randomly seed some of k2's with associate values corresponding to inputs
    for j in range(2000):
        if random.randint(1, 8) == 3:
            k2[j].assoc_value = k2[j].holding
    #now we see if any of the k2's auto-association triggered
    #auto_associate returns a score, and normalize by length of assoc_value, and if large enough
    # then consider neuron as having auto-associatively triggered to assoc_value
    for j in range(2000):
        if k2[j].auto_associate(k2[j].holding, k2[j].assoc_value)/len(k2[j].assoc_value) > 0.35:
            #optional for now -- if triggered neuron, set assoc_value to holding
            #want to consider removing in future
            k2[j].assoc_value = k2[j].holding
            #since auto-assoc triggered, there is a k2[].out value now
            k2[j].out = k2[j].assoc_value
    #at this point, k2[].out is 0 if not triggered, or k2[].out==assoc_value if triggered
    #for i in range(20):
    #   print('k2[i].out :', k2[i].out)
    #pylint: enable=line-too-long
    return 'k1 to k2 feedforward done'


def apply_k2_to_k3():
    '''feedforward k2 to k3
    -k2[].out  is 0 if not triggered or holds auto-associative value if triggered
    -k2 propagates to all k3 via lines and weights to k3.holding
    -after all the k2's propagated to k3's, we then go through the k3.holding and
        see which k3's are triggered
    -k2 is 2000 (0..1999) hln's each going to (0..1999) 2000 k3's
    '''
    #pylint: disable=line-too-long
    print('entering apply_k2_to_k3 procedure')
    #ensure k3[0..1999].holding & .out are set up to 22 rows, and all values reset to 0
    for j in range(2000):
        k3[j].holding = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        k3[j].out = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    #ensure k2[0..1999].out is correct size of 22 rows
    for i in range(1999):
        if len(k2[i].out) < 22:
            print('k2.out shorter than 22 detected', i, k2[i].out)
            for k in range(22 - len(k2[i].out)):
                k2[i].append(0)
    #now feedforward each k2[0..1999] to all the k3[0..1999] via weights connecting them
    for i in range(2000):
        for j in range(2000):
            for k in range(22):
                k3[j].holding[k] = k3[j].holding[k] + (k2[i].out[k] * k2[i].wt[j][k] * v2[i].abstraction_addressor[j][k])
    #at this point k3.holding has all propagated values from v2
    #randomly seed some of k3's with associate values corresponding to inputs
    for j in range(2000):
        if random.randint(1, 40) == 3:
            k3[j].assoc_value = k3[j].holding
    #now we see if any of the k3's auto-association triggered
    #auto_associate returns a score, and normalize by length of assoc_value, and if large enough
    # then consider neuron as having auto-associatively triggered to assoc_value
    for j in range(2000):
        if k3[j].auto_associate(k3[j].holding, k3[j].assoc_value)/len(k3[j].assoc_value) > 0.35:
            #optional for now -- if triggered neuron, set assoc_value to holding
            #want to consider removing in future
            k3[j].assoc_value = k3[j].holding
            #since auto-assoc triggered, there is a k3[].out value now
            k3[j].out = k3[j].assoc_value
    #at this point, k3[].out is 0 if not triggered, or k3[].out==assoc_value if triggered
    temp = 0
    for i in range(2000):
        if k3[i].out[0] != 0:
            temp += 1
    print('total number of triggered k3[].outs: ', temp)
    #pylint: enable=line-too-long
    return 'v2 to k3 feedforward done'


def apply_k3_to_t1():
    '''feedforward k3 to t1
    -k3[].out  is 0 if not triggered or holds auto-associative value if triggered
    -k3 propagates to all t1 via lines and weights to t1.holding
    -after all the k3's propagated to t1's, we then go through the t1.holding and
        see which t1's are triggered
    -k3 is 2000 (0..1999) hln's each going to (0..999) 1000 t1's
    '''
    #pylint: disable=line-too-long
    print('entering apply_k3_to_t1 procedure')
    print('nb should be run after visual where holdings reset and before auditory where triggering computed')
    #ensure t1[0..999].holding & .out are set up to 22 rows, and all values reset to 0
    #make sure not to erase if propagating multiply senses to t1 area
    #for j in range(1000):
    #this already done in visual sensory propagation to t1
        #t1[j].holding = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        #t1[j].out = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    #ensure k3[0..1999].out is correct size of 22 rows
    for i in range(1999):
        if len(v2[i].out) < 22:
            print('k3.out shorter than 22 detected', i, k3[i].out)
            for k in range(22 - len(k3[i].out)):
                k3[i].append(0)
    #now feedforward each k3[0..1999] to all the t1[0..999] via weights connecting them
    for i in range(2000):
        for j in range(1000):
            for k in range(22):
                t1[j].holding[k] = t1[j].holding[k] + (k3[i].out[k] * k3[i].wt[j][k] * k3[i].abstraction_addressor[j][k])
    #at this point t1.holding has all propagated values from k3
    #randomly seed some of t1's with associate values corresponding to inputs
    for j in range(1000):
        if random.randint(1, 3) == 3:
            if k3[j].out != [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
                t1[j].assoc_value = t1[j].holding
    #now we see if any of the k3's auto-association triggered
    #auto_associate returns a score, and normalize by length of assoc_value, and if large enough
    # then consider neuron as having auto-associatively triggered to assoc_value
    #do not compute triggering since will do at end of auditory propagation
    '''for j in range(1000):
        if t1[j].auto_associate(t1[j].holding, t1[j].assoc_value)/len(t1[j].assoc_value) > 0.35:
            #optional for now -- if triggered neuron, set assoc_value to holding
            #want to consider removing in future
            t1[j].assoc_value = t1[j].holding
            #since auto-assoc triggered, there is a k3[].out value now
            t1[j].out = t1[j].assoc_value
    #at this point, t1[].out is 0 if not triggered, or t1[].out==assoc_value if triggered
    temp = 0
    for i in range(1000):
        if t1[i].out[0] != 0:
            temp += 1
    print('total number of triggered t1[].outs: ', temp)
    #for i in range(1000):
    #   print(i, 't1[i].out :', t1[i].out)'''
    #pylint: enable=line-too-long
    return 'k3 to t1 feedforward done'

#auditory sensory propagation

'''
from mbls_auditory_propagation import *
-sensory propagation levels are quite similar in propagation but any
differences for any particular sense, implemented in the sense's 
propagation routines below
'''


def apply_auditory_inputs():
    '''applies auditory input a0 vector to layer a1
    (for convenience just use constants below)
    -layer 1 really is just holding input layer since it does not
     receive inputs diagonally, just directly from layer 0
    '''
    for i in range(784):
        a1[i].out = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for j in range(22):
            a1[i].out[j] = random.random()
    #print('a1[111]: ', a1[111].out)
    #print('a1[112]: ', a1[112].out)
    return 'no actual auditory transducer detected, thus seeded input values'


def apply_a1_to_a2():
    '''feedforward a1 to a2
    -a1 is just holding inputs so we don't care if triggered
    -a1 propagates to all a2 via lines and weights to a2.holding
    -after all the a1's propagated to a2's, we then go through the a2.holding and
        see which a2's are triggered
    -a1 is 784 (0..783) hln's each going to (0..1999) 2000 a2's
    '''
    #pylint: disable=line-too-long
    print('entering apply_a1_to_a2 procedure')
    #ensure a2[0..1999].holding & .out are set up to 22 rows, and all values reset to 0
    for j in range(2000):
        a2[j].holding = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        a2[j].out = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    #ensure a1[0..783].out is correct size of 22 rows
    for i in range(784):
        if len(a1[i].out) < 22:
            print('a1.out shorter than 22 detected', i, a1[i].out)
            for k in range(22 - len(a1[i].out)):
                a1[i].append(0)
    #now feedforward each a1[0..783] to all the a2[0..1999] via weights connecting them
    for i in range(784):
        for j in range(2000):
            for k in range(22):
                a2[j].holding[k] = a2[j].holding[k] + (a1[i].out[k] * a1[i].wt[j][k] * a1[i].abstraction_addressor[j][k])
    #at this point a2.holding has all propagated values from a1
    #randomly seed some of a2's with associate values corresponding to inputs
    for j in range(2000):
        if random.randint(1, 8) == 3:
            a2[j].assoc_value = a2[j].holding
    #now we see if any of the a2's auto-association triggered
    #auto_associate returns a score, and normalize by length of assoc_value, and if large enough
    # then consider neuron as having auto-associatively triggered to assoc_value
    for j in range(2000):
        if a2[j].auto_associate(a2[j].holding, a2[j].assoc_value)/len(a2[j].assoc_value) > 0.35:
            #optional for now -- if triggered neuron, set assoc_value to holding
            #want to consider removing in future
            a2[j].assoc_value = a2[j].holding
            #since auto-assoc triggered, there is a a2[].out value now
            a2[j].out = a2[j].assoc_value
    #at this point, a2[].out is 0 if not triggered, or a2[].out==assoc_value if triggered
    #for i in range(20):
    #   print('a2[i].out :', a2[i].out)
    #pylint: enable=line-too-long
    return 'a1 to a2 feedforward done'


def apply_a2_to_a3():
    '''feedforward a2 to a3
    -a2[].out  is 0 if not triggered or holds auto-associative value if triggered
    -a2 propagates to all a3 via lines and weights to a3.holding
    -after all the a2's propagated to a3's, we then go through the a3.holding and
        see which a3's are triggered
    -a2 is 2000 (0..1999) hln's each going to (0..1999) 2000 a3's
    '''
    #pylint: disable=line-too-long
    print('entering apply_a2_to_a3 procedure')
    #ensure a3[0..1999].holding & .out are set up to 22 rows, and all values reset to 0
    for j in range(2000):
        a3[j].holding = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        a3[j].out = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    #ensure a2[0..1999].out is correct size of 22 rows
    for i in range(1999):
        if len(a2[i].out) < 22:
            print('a2.out shorter than 22 detected', i, a2[i].out)
            for k in range(22 - len(a2[i].out)):
                a2[i].append(0)
    #now feedforward each a2[0..1999] to all the a3[0..1999] via weights connecting them
    for i in range(2000):
        for j in range(2000):
            for k in range(22):
                a3[j].holding[k] = a3[j].holding[k] + (a2[i].out[k] * a2[i].wt[j][k] * a2[i].abstraction_addressor[j][k])
    #at this point a3.holding has all propagated values from a2
    #randomly seed some of a3's with associate values corresponding to inputs
    for j in range(2000):
        if random.randint(1, 40) == 3:
            a3[j].assoc_value = a3[j].holding
    #now we see if any of the a3's auto-association triggered
    #auto_associate returns a score, and normalize by length of assoc_value, and if large enough
    # then consider neuron as having auto-associatively triggered to assoc_value
    for j in range(2000):
        if a3[j].auto_associate(a3[j].holding, a3[j].assoc_value)/len(a3[j].assoc_value) > 0.35:
            #optional for now -- if triggered neuron, set assoc_value to holding
            #want to consider removing in future
            a3[j].assoc_value = a3[j].holding
            #since auto-assoc triggered, there is a a3[].out value now
            a3[j].out = a3[j].assoc_value
    #at this point, a3[].out is 0 if not triggered, or a3[].out==assoc_value if triggered
    temp = 0
    for i in range(2000):
        if a3[i].out[0] != 0:
            temp += 1
    print('total number of triggered a3[].outs: ', temp)
    #pylint: enable=line-too-long
    return 'a2 to a3 feedforward done'


def apply_a3_to_t1():
    '''feedforward a3 to t1
    -a3[].out  is 0 if not triggered or holds auto-associative value if triggered
    -a3 propagates to all t1 via lines and weights to t1.holding
    -after all the a3's propagated to t1's, we then go through the t1.holding and
        see which t1's are triggered
    -a3 is 2000 (0..1999) hln's each going to (0..999) 1000 t1's
    '''
    #pylint: disable=line-too-long
    print('entering apply_a3_to_t1 procedure')
    print('nb should be last sensory propagation run since will compute t1 auto-assoc triggering')
    #ensure t1[0..999].holding & .out are set up to 22 rows, and all values reset to 0
    #make sure not to erase if propagating multiply senses to t1 area
    for j in range(1000):
        #t1[].holding already reset in visual propagation routine run first
        #t1[j].holding = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        t1[j].out = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    #ensure a3[0..1999].out is correct size of 22 rows
    for i in range(1999):
        if len(a2[i].out) < 22:
            print('a3.out shorter than 22 detected', i, a3[i].out)
            for k in range(22 - len(a3[i].out)):
                a3[i].append(0)
    #now feedforward each a3[0..1999] to all the t1[0..999] via weights connecting them
    for i in range(2000):
        for j in range(1000):
            for k in range(22):
                t1[j].holding[k] = t1[j].holding[k] + (a3[i].out[k] * a3[i].wt[j][k] * a3[i].abstraction_addressor[j][k])
    #at this point t1.holding has all propagated values from a3
    #randomly seed some of t1's with associate values corresponding to inputs
    for j in range(1000):
        if random.randint(1, 3) == 3:
            if a3[j].out != [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
                t1[j].assoc_value = t1[j].holding
    #now we see if any of the t1's auto-association triggered
    #auto_associate returns a score, and normalize by length of assoc_value, and if large enough
    # then consider neuron as having auto-associatively triggered to assoc_value
    for j in range(1000):
        if t1[j].auto_associate(t1[j].holding, t1[j].assoc_value)/len(t1[j].assoc_value) > 0.35:
            #optional for now -- if triggered neuron, set assoc_value to holding
            #want to consider removing in future
            t1[j].assoc_value = t1[j].holding
            #since auto-assoc triggered, there is a a3[].out value now
            t1[j].out = t1[j].assoc_value
    #at this point, t1[].out is 0 if not triggered, or t1[].out==assoc_value if triggered
    temp = 0
    for i in range(1000):
        if t1[i].out[0] != 0:
            temp += 1
    print('total number of triggered t1[].outs: ', temp)
    #for i in range(1000):
    #   print(i, 't1[i].out :', t1[i].out)
    #pylint: enable=line-too-long
    return 'a3 to t1 feedforward done'


#apply input sensor data to reflex circuits
def reflex_apply_visual_inputs():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def reflex_apply_auditory_inputs():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def reflex_apply_olfactory_inputs():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


#meaningfulness shuffle
def meaningfulness_shuffle_v1():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def meaningfulness_shuffle_v2():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def meaningfulness_shuffle_v3():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def meaningfulness_shuffle_a1():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def meaningfulness_shuffle_a2():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def meaningfulness_shuffle_a3():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def meaningfulness_shuffle_k1():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def meaningfulness_shuffle_k2():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def meaningfulness_shuffle_k3():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


#do another feedforward
def apply_v3_to_t1_prime():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def apply_k3_to_t1_prime():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def apply_a3_to_t1_prime():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


#choose between previous t1 results or new t1_prime results
def choose_t1_prev_or_t1_prime():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


#feedback to adjust weights to better give desired results
#close to real-time adjustment in weights
def fast_backprop_t1_to_v3():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def fast_backprop_v3_to_v2():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def fast_backprop_v2_to_v1():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def fast_backprop_t1_to_a3():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def fast_backprop_a3_to_a2():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def fast_backprop_a2_to_a1():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def fast_backprop_t1_to_k3():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def fast_backprop_k3_to_k2():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def fast_backprop_k2_to_k1():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


#causal memory initial propagation
def apply_t1_to_c1():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def apply_c1_to_c2():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def apply_t1_to_world_view():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def apply_c2_to_world_view():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def apply_g1_to_world_view():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def apply_g2_to_world_view():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def apply_developmental_timer(cumu_time):
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return cumu_time


def apply_world_view_to_instinctual_goals():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def apply_world_view_to_instinctual_physics():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def apply_world_view_to_instinctual_psychology():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def apply_world_view_to_instinctual_scheduling():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


#sub-symbolic goals propagation
def apply_c1_to_instinctual_goals():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def apply_t1_to_instinctual_goals():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def apply_instinctual_goals_to_c2():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


#sub-symbolic physics world propagation
def apply_c1_to_instinctual_physics():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def apply_t1_to_instinctual_physics():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def apply_instinctual_physics_to_c2():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


#sub-symbolic psychology world propagation
def apply_c1_to_instinctual_psychology():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def apply_t1_to_instinctual_psychology():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def apply_instinctual_psychology_to_c2():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


#apply processed sensory to motor center
def apply_reflex_center_to_m1():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def apply_t1_to_m1():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def apply_c1_to_m1():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def apply_c2_to_m1():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def apply_m1_to_motor_actuator():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def apply_m1_to_m2():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def apply_m2_to_m3():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def apply_m3_to_motor_actuator():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def apply_somatic_sensory_to_m1():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def fast_backprop_m3_to_m2():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def fast_backprop_m2_to_m1():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


#apply symbolic logic
def apply_c2_to_pre_g1():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def convert_pre_g1_to_working_memory_g1():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def apply_c2_to_pre_g2():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def convert_pre_g2_to_working_memory_g2():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def apply_c2_to_instinctual_goals():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def apply_g1_to_instinctual_goals():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def apply_g2_to_instinctual_goals():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def apply_instinctual_goals_to_g1():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def apply_instinctual_goals_to_g2():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def apply_t1_to_goal_conscious():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def apply_c2_to_goal_conscious():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def apply_goal_conscious_to_g1():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def apply_goal_conscious_to_g2():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def apply_m3_to_g1():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def apply_m3_to_g2():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def apply_c2_to_instinctual_physics():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def apply_g1_to_instinctual_physics():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def apply_g2_to_instinctual_physics():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def apply_instinctual_physics_to_g1():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def apply_instinctual_physics_to_g2():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def apply_c2_to_instinctual_psychology():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def apply_g1_to_instinctual_psychology():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def apply_g2_to_instinctual_psychology():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def apply_instinctual_psychology_to_g1():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def apply_instinctual_psychology_to_g2():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def apply_t1_to_emotional_reward_module():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def apply_c2_to_emotional_reward_module():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def apply_g1_to_emotional_reward_module():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def apply_g2_to_emotional_reward_module():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def apply_emotional_reward_module_to_g1():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def apply_emotional_reward_module_to_g2():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def apply_g1_operations_to_g1_prime():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def apply_g2_operations_to_g2_prime():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def apply_g1_operations_to_g2():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def apply_g2_operations_to_g1():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def apply_g1_prime_to_v2():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def apply_g2_prime_to_v2():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def apply_g1_prime_to_goal_conscious():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


def apply_g2_prime_to_goal_conscious():
    '''
    deprecated version 2/
    code insertion version 3
    '''
    #TO DO version 3 transition
    return 1


#
#
###########################################################
def input_cam_vector():
    ''' Sensory Inputs
    MBLS ARCHITECTURE VISIBLE COMPONENT
    Inputs 8 lines segments of camera simulation as input vector
    Position 1- 8 correspond to the line segments
    Position 0 corresponds to any special command sequences entered,
    eg, command to erase memory and prepare MBLS for a new simulation
    Returns list[0..8] (or whatever INPUT_WORD_LENGTH is set as)
    '''
    checkpoint_name = 'input_cam_vector()'
    #pylint: disable=global-statement
    #pylint: disable =global-variable-undefined
    global in_vecs
    global STOP_SCROLLING_BETWEEN_INPUTS
    #HOP NOTE: From 'Flags used for Development Purposes' at start of code
    #pylint: enable=global-statement
    l = [0 for aa in list(range(INPUT_WORD_LENGTH))]

    #input vector -- posn 0 for control codes, posns 1-8 represent presence of line segment
    stop_scrolling_check()
    print('\nA simple camera that can detect the presence or absence of')
    print('8 different lines of pixels, sends an input into the MBLS.')
    mbv2.display_8_segments([0, 1, 1, 1, 1, 1, 1, 1, 1])
    print('The camera can also input special codes and error codes. If you')
    print('enter any valid such code at anytime it will be immediately recognized.')
    print('(code 10 -- creates a random input vector, 11 -- creates input with all segs ')
    print('33 -- history of input vectors,')
    print('99 will give hard exit of program, ____ will reset input vector history)\n')

    for i in range(1, 8+1):
        print('Is line segment {} there?'.format(i))
        x = input("Enter 'y' or 'Y' if line segment input, any other key if no line segment: ")

        #caution: no exception handling implemented
        #special codes input
        if x == '99': #exit
            print('\n---->System exit code entered -- program will stop execution.')
            x = input('Press ENTER and program will stop execution.....')
            sys.exit()
        if x == RESET_CODE_CREATE_NEW_MBSL: #reset input hx
            l[0] = int(RESET_CODE_CREATE_NEW_MBSL)
            print('\n---->Reset code was entered -- memory is now wiped out:', l, '\n')
            in_vecs = l['restart']
            print_in_vecs()
            x = input('Press ENTER to continue in program now (zero segment input will run).....')
            return l
        if x == '10':  #create random input
            print('\n---->Random input vector chosen and shown below:')
            l[0] = int(10)
            for t in range(1, 8+1):
                l[t] = random.randint(0, 1)
            update_in_vecs(l)
            mbv2.display_8_segments(l)
            checkpoint_tracer(checkpoint_name, l)
            return l
        if x == '11':  #create full seg input
            print('\n---->Input with all segments chosen and shown below:')
            l[0] = int(11)
            for t in range(1, 8+1):
                l[t] = 1
            update_in_vecs(l)
            mbv2.display_8_segments(l)
            checkpoint_tracer(checkpoint_name, l)
            return l
        if x == '33':  #display input hx
            print('\n---->History of Camera Input Vectors for this run :')
            print_in_vecs()
            print('\nNull input loop will now run -- ignore results:')
            l[0] = int(33)
            checkpoint_tracer(checkpoint_name, l)
            return l

        #user input of input vector
        #did the camera detect this particular line segment?
        if x in('y', x == 'Y', '1', x == 't', 'yy'):
            l[i] = int(1)
        else:
            l[i] = int(0)
    update_in_vecs(l)
    print('\n---->The input vector you entered is: {} '.format(l))
    mbv2.display_8_segments(l)
    checkpoint_tracer(checkpoint_name, l)
    return l
#pylint: enable=too-many-statements
#pylint: enable=invalid-name

def input_vectors(in_vector):
    ''' Input Vectors Shaping Module
    MBLS ARCHITECTURE VISIBLE COMPONENT
    Can take various sensory inputs simultaneously,
    and shapes them for use by the MBLS.
    (Early version only calls input_cam_vector function
    taking keystroke-simulated camera input, but
    this method allows combination of many different
    such input function to input into the MBLS.)
    Then feeds shaped vectors into various modules
    and groups of HLNs in the MBLS.
    '''
    checkpoint_name = 'input_vectors(in_vector)'
    #global in_vecs -- if need for processing

    #at present just regurgitates the input
    checkpoint_tracer(checkpoint_name, in_vector)
    return in_vector


def hln_sensory_input1(in_vector):
    '''HLNs AutoConfigured to Receive Sensory Input1
    MBLS ARCHITECTURE VISIBLE COMPONENT
    HLNs further shape and route input vectors.
    At present just passes sensory input vector unchanged.
    '''
    checkpoint_name = 'hln_sensory_input1(in_vector)'
    checkpoint_tracer(checkpoint_name, in_vector)
    return in_vector


def sensory_binding1(in_vector):
    '''
    HLNs Autoconfigured to Bind Sensory Inputs
    MBLS ARCHITECTURE VISIBLE COMPONENT
    At present just returns input
    '''
    checkpoint_name = 'sensory_binding1(in_vector)'
    checkpoint_tracer(checkpoint_name, in_vector)
    return in_vector


def causal_memory1(in_vector):
    '''
    HLNs Autoconfigured as Causal Memory1
    MBLS ARCHITECTURE VISIBLE COMPONENT
    At present just returns input
    #
    #
    Much of the MBLS memory, as shown in Figure 4, is represented by HLNs
    auto-configured into networks of causal memory, keeping track of which
    event follows another event, and what the interesting sensory data
    were at the time. The intrinsic connections in the brain between hierarchical
    cortical columns may by
    default establish Bayesian inference (Bastos, Usrey, Adams, et al., 2012),
    although it can informally be shown that such connections would not be sufficient
    to easily allow the higher-level inferences humans perform without groups of HLNs
    configured as working memory/logic units.  In a group of HLNs auto-configured as
    a ‘working memory/logic unit’ (or ‘working memory’ for short) there can be
    logical manipulation of the information held there.
    '''
    checkpoint_name = 'causal_memory1(in_vector)'
    checkpoint_tracer(checkpoint_name, in_vector)
    return in_vector

#pylint: disable=line-too-long
#justification: old version 2 code
def pattern_memory1(in_vector):
    '''HLNs Autoconfigured as Pattern Memory1
    MBLS ARCHITECTURE VISIBLE COMPONENT
    Hopfield automatching will occur but just
    rough approximation rather than actual Hopfield-like network.
    #
    #
    The basic functional unit of the MBLS is not an artificial neuron but a reconfigurable unit containing a
Hopfield-like network (HLN) (Lyke, Christodoulou, et al., 2015, Rojas, 1996). While Hopfield networks
are typically thought of as requiring stationary inputs they can be extended for sequential learning
(Maurer, Hersch, and Billard, 2005). The HLN contains a Hopfield-like network as well as the circuitry
allowing it to rapidly reconfigure its connections with other HLNs. The weights of the connections
within the HLNs change gradually as in a conventional ANN. The weights of the connections between
different HLNs can be adjusted gradually with learning as in a conventional ANN, can be adjusted more
abruptly to form a more discrete logical relation between two HLNs, and as well can rapidly be configured
to maximal or minimal values to allow fast and extreme reconfiguration of the HLNs with each other.
This rapid reconfiguration of the HLNs can be done by the HLNs themselves – no external logic processing
unit is required. In rapid reconfigurations, there is an attempt by the HLNs to maximize meaningfulness,
where this is defined as the reciprocal of the Shannon entropy, as described below.
	#
	#
	A simplified view of one of the Hopfield-like networks (HLNs) is shown in Figure 2. An input vector goes
to the auto-associative processor, and its pattern may or may not be recognized here, depending on the values
of this auto-associative processor’s internal weights which have been shaped by learning experiences in
collaboration with the signal from the feedback vector.  To seed the hierarchical organization of HLNs in a
new MBLS, the default values of many of the auto-associative processors will be to produce a non-zero vector
to the vector processing unit for most non-zero input vectors.
The vector output of the auto-associative processor feeds into the vector processing unit, and depending on
this vector’s values, a corresponding vector, which often may be of smaller size, then feeds into the
abstraction addressor. In response to the signal from the feedback vector, the abstraction addressor decides
which of many possible output vectors wired up as inputs to other HLNs will have non-zero outputs. The
abstraction addressor effectively allows a number of HLNs to rapidly reconfigure their connections to
each other.
	#
	#
	Another property of the MBLS that distinguishes it from other hierarchical pattern recognizer systems is
that via learning experiences and subsequent changes in weights, different HLNs’ outputs form stronger and
weaker connections with other HLNs, as occurs in other systems, but each HLN has multiple sets of outputs
wired/configured to different sets of HLNs. The entire MBLS can rapidly reconfigure itself to allow different
emergent output properties for a given set of inputs to the MBLS. A simple example of this is described
below and Sillustrated in Figure 3.
Applying statistical mechanics to neural networks, whether biological or artificial, is not new, indirectly
going back to Schrödinger (Ramstead, Badcock, and Friston, 2018).  However, there is a wide variety of ways
these principles can be applied, including at different levels of organization of the system (Ackley,
Hinton, and Sejnowski, 1985; Clark, Watson and Friston, 2018). The MBLS uses the property of what is
defined here as “meaningfulness” to guide its reconfigurations. Meaningfulness M is defined as the
reciprocal of the Shannon entropy (1,2):
H= -∑iP(xi)log2P(xi)      (1)
M=1/H       (2)
As can be seen above, if we were flipping a coin, and it landed almost every time tails, for example,
then this sequence of almost all tails, would be considered a high amount meaningfulness M. In the MBLS,
if a particular sensory input caused a larger number of HLNs and at higher levels of the hierarchy of HLNs
for a particular sensory input to find a match in the auto-associative processors of their HLNs, than another
sensory input, then this particular sensory input would be said to have a higher meaningfulness M. For a given
sensory input, the HLNs can rapidly be reconfigured in different combinations with each other, to see what
configuration (i.e., connections between HLNs) can give a maximal meaningfulness. The implication of the
reconfiguration is not only to detect a signal in the sensory input, but to change the context or level of
abstraction in which the detected signal is considered for maximal meaningfulness, which then can affect
detection of subsequent signals in subsequent sensory inputs, since there may be a new configuration of
the HLNs. Conversely, the level of abstraction of the MBLS may be set a higher meta level from a vector
input fed back from a logic/working memory unit (which is essentially a ‘thought’, as will be described
below), which will affect the detection of a particular signal in the subsequent sensory inputs.
	#
Figure 3 shows aspects of a simple simulation run. If the input vector [ ,  ,/, ¬—,|,|, ] occurs
(not shown in the figure), which is an incomplete “A”, then this would cause the auto-associative processor
of HLN(m-1,1) to recognize it as an “A” and connect to HLN(m-3,2) which also recognizes the “A”. Both
HLN(m-1,1) and HLN(m-3,2) match the input vector, and meaningfulness is easily maximized with this default
connection. (In the computer simulation the meaningfulness feedback vector is simply composed of the number
of HLNs which auto-associate, ie, match up, the input vector to the HLN. A myriad of more sophisticated
algorithms are possible, of course.)
	#
If the input vector [—, |, |,—, |, |, —,    ] occurs (not shown in figure), then this input can correspond,
at this low pixel input resolution, to a “B” or to an “8”. However, the weights of the MBLS have been adjusted
by learning such that when this input vector goes into the MBLS, the auto-associative processor of HLN(m,1)
recognizes it as a “B” and keeps the default connection to HLN(m-1,2) which also recognizes it as a “B”, and the
feedback vector registers a high meaningfulness, and so the input vector [—, |, |,—, |, |, —,    ] is recognized
as a “B”.
	#
If, as shown in Figure 3, there is then an input vector of [—, |, |,—, |, |, —,  |  ], since it is so close to the
previous example of the vector recognized as a “B”, it will also be recognized by HLN(m,1) as a “B” (or more correctly
as a vector which HLN(m,1) auto-associates and connects to the next HLN without really knowing what it is). Thus,
since HLN(m1,) is connected to HLN(m-1,2) which would recognize, ie, auto-associate the output from HLN(m,1), and thus
output a vector recognizing the input vector as a “B”. However, other HLNs in the MBLS (not shown in the very simplified
Figure 3) would cause the feedback vector to report a much lower meaningfulness than if during the evaluation cycle, HLN(m,1)
connects to HLN(m,2). That is, if one of the possible reconfigurations of HLN(m,1) to HLN(m,2) occurs, there will be much
high meaningfulness (not shown, but because of other HLNs activating in the MBLS, eg, perhaps previously other HLNs activated
from this particular input vector or features within it) and thus the input vector causes HLN(m,2) be activated and cause the
input vector to be recognized as an “8”.
	#
	#
	'''
    checkpoint_name = 'pattern_memory1(in_vector)'
    pattern_accept_1 = [[1, 1, 1, 1, 1, 1, 1, 1], [1, 0, 1, 1, 1, 1, 1, 1]]
    if in_vector[1:9] in pattern_accept_1:
        in_vector = in_vector[0:1]+ pattern_accept_1[0]
        checkpoint_name = checkpoint_name + ' -- pattern match -- '
    else:
        checkpoint_name = checkpoint_name + ' -- no pattern match -- '
    checkpoint_tracer(checkpoint_name, in_vector)
    return in_vector
#pylint: enable=line-too-long


#pylint: disable=line-too-long
#justification: old version 2 code
def logic_working_memory1(in_vector):
    '''
	HLNs Autoconfigured as Logic/Working Memory1
	MBLS ARCHITECTURE VISIBLE COMPONENT
	At present just returns input
	#
	#
	[Much of the MBLS memory, as shown in Figure 4, is represented by HLNs auto-configured into networks of
causal memory, keeping track of which event follows another event, and what the interesting sensory data
were at the time. The intrinsic connections in the brain between hierarchical cortical columns may by
default establish Bayesian inference (Bastos, Usrey, Adams, et al., 2012), although it can informally
be shown that such connections would not be sufficient to easily allow the higher-level inferences
humans perform without groups of HLNs configured as working memory/logic units.  In a group of HLNs
auto-configured as a ‘working memory/logic unit’ (or ‘working memory’ for short) there can be logical
manipulation of the information held there.]
	The MBLS can be designed (via default weights) such that while some of the HLNs can auto-configure
with each other to form various sensory-processing hierarchies and various causal memory networks,
other parts of the MBLS can auto-configure to set up a group(s) of HLNs which will act as a working
memory with varying degrees of logical processing operating on the contents of this memory (in theory,
ranging from acting as small automatons to Church-Turing complete logical sub-systems). It is important
to realize that the representation of data in the MBLS is already quite causal and has meaning through
the connections an HLN has via connections to other HLNs. The working memory need not convert the
vectors from the HLN into some abstract symbolic data for the working memory to produce symbolic
behavior, i.e., manipulation of the HLN vectors it receives suffices. In the simulation of the MBLS,
described below, it can be shown that HLNs auto-configured as relatively simple logic/working memory
units are able to compare properties of vectors they receive, are able to choose one vector over
another, are able to pattern match a vector from the entire MBLS memory, and are able to direct the
MBLS to output a vector.
	#
As noted above, the MBLS can be designed so that there are group(s) of HLNs which will act as a working memory
with varying degrees of logical processing operating on the contents of this memory. These groups of HLNs,
“logic/working memory units”, are able to compare properties of vectors they receive, are able to choose one
vector over another, are able to pattern match a vector from the entire MBLS memory, and are able to direct the
MBLS to output a vector. A typical MBLS cognitive architecture is shown in Figure 4 below. Every evaluation cycle,
not only does the MBLS look at the meaningfulness of the data in the sensory input and cycle through varying levels
of abstraction so as to reconfigure the HLNs in a way to maximize local and system meaningfulness (via a feedback
vector to all the HLNs), but the sensory input vector or the casual memory vector it triggers (or other vectors,
as shown in the architecture of Figure 4) also go to the logic/working memory unit. The logic at the time may be
to do nothing, or it may be, for example to compare this vector with another vector previously triggered, and if
enough of a match then trigger another vector, for example, into the logic/working memory unit, or perhaps as an
output vector, for example.
Thus every evaluation cycle, the MBLS looks at the meaningfulness of the data in the sensory input vectors (local
and system meaningfulness is fed back to the HLNs via the feedback vector to allow evaluation of meaningfulness),
and the results of any operations in the logic/working memory, i.e., essentially a symbolic logical operation on the
data. The evaluation cycle completes, connections within the auto-associative processors of the HLNs are strengthened
or weakened in relation to neural-level activity and the feedback vector, connections between HLNs are strengthened and
weakened in response to the feedback vector, and the next evaluation cycle starts again. The above occurs automatically,
over and over again.
	#
In an evaluation cycle, rather than evaluating an input vector from the sensory systems, the MBLS can instead
equally evaluate a data vector from the logic/working memory unit as the next input vector. Essentially a thought
occurs. The current data vector from the logic/working memory is treated as the next input vector, and fed back into
the logic/working memory unit while HLNs are reconfigured to maximize meaningfulness. The evaluation cycle completes,
synapses are (or are set to be) strengthened or weakened, and the next evaluation cycle starts again. In the next evaluation
cycle the newly processed data vector in the logic/working memory can again be considered as the next input vector to evaluate.
As such, thoughts can be processed sequentially in a fashion to extract maximum meaningfulness from them.
	#

Creativity in solving problems is possible for the MBLS via algorithms applied to the logic/working memory units, and also
intrinsically within the HLNs. The operation of the MBLS can be skewed so that alternative solutions emerge that would not normally
represent the extraction of the maximal meaningfulness from the input (or thoughts from the working memory subunits), by altering
the values of the external inputs so as to give more obscure aspects of the input data closer pattern matching and hence a higher
value of meaningfulness.

	'''
    checkpoint_name = 'logic_working_memory1(in_vector)'
    checkpoint_tracer(checkpoint_name, in_vector)
    return in_vector
#pylint: enable=line-too-long

def instinctual_core_goals(in_vector):
    #not used until version migration
    '''
    Circuits that create (Instinctual) Core Goals Module
    MBLS ARCHITECTURE VISIBLE COMPONENT
    At present just returns input
    '''
    checkpoint_name = 'instinctual_core_goals(in_vector)'
    checkpoint_tracer(checkpoint_name, in_vector)
    return in_vector


def developmental_timer(in_vector):
    #not used until version migration
    '''
    Circuits that create Developmental Timer Module
    MBLS ARCHITECTURE VISIBLE COMPONENT
    At present just returns input
    '''
    checkpoint_name = 'developmental_timer(in_vector)'
    checkpoint_tracer(checkpoint_name, in_vector)
    return in_vector


def emotional_and_reward(in_vector):
    #not used until version migration
    '''
    Circuits that create Emotional and Reward Module
    MBLS ARCHITECTURE VISIBLE COMPONENT
    At present just returns input
    '''
    checkpoint_name = 'emotional_and_reward(in_vector)'
    checkpoint_tracer(checkpoint_name, in_vector)
    return in_vector


def goal_and_conscious(in_vector):
    #not used until version migration
    '''
    HLNs Autoconfigured as Goal and Conscious Module
    MBLS ARCHITECTURE VISIBLE COMPONENT
    At present just returns input
    '''
    checkpoint_name = 'goal_and_conscious(in_vector)'
    checkpoint_tracer(checkpoint_name, in_vector)
    return in_vector


def sequential_error_correcting_memory(in_vector):
    #not used until version migration
    '''
    HLNs Autoconfigured as Sequential/ Error-Correcting Memory
    MBLS ARCHITECTURE VISIBLE COMPONENT
    At present just returns input
    '''
    checkpoint_name = 'sequential_error_correcting_memory(in_vector)'
    checkpoint_tracer(checkpoint_name, in_vector)
    return in_vector


def hln_motor_output1(in_vector):
    '''
    HLNs Autoconfigured to Output Motor Vectors
    MBLS ARCHITECTURE VISIBLE COMPONENT
    hln_motor_output1 converts output to motor representation
    of letters or words
    '''
    checkpoint_name = 'hln_motor_output1(in_vector)'
    in_vector = in_vector[1:9]
    #assume in_vector at this point processed for auto-association
    #and meaningfulness
    #also assume in_vector comes with other associated pattern and
    #causal memory into hln_motor_output groups
    if in_vector == [1, 1, 1, 1, 1, 1, 0, 0]:
        motor_output = ["motor output directed towards the letter 'A'"]
    elif in_vector == [1, 1, 1, 1, 1, 1, 1, 0]:
        motor_output = ["motor output directed towards the letter 'B'"]
    elif in_vector == [1, 1, 1, 1, 1, 1, 1, 1]:
        motor_output = ["motor output directed towards the number '8'"]
    else:
        motor_output = ["motor output directed towards an indeterminate symbol '?'"]
    checkpoint_tracer(checkpoint_name, motor_output)
    return motor_output


def output_vectors(in_vector):
    '''Output Vectors Shaping Module
    Circuits that shape and route the output vectors
    to various output transducers, including the
    system display via function output_transducer_display
    MBLS ARCHITECTURE VISIBLE COMPONENT
    '''
    checkpoint_name = 'output_vectors(in_vector)'
    final_motor_output = ['motor outputs directed towards tranducer system display', in_vector]
    checkpoint_tracer(checkpoint_name, final_motor_output[0][0:10])
    return final_motor_output


def output_transducer_system_display(in_vector):
    '''Receives an output motor vector
    from the Output Vectors Shaping Module, and
    effects its action, in this case, the
    transducer is the main system display, ie,
    displays output vector on the system display
    '''
    checkpoint_name = 'output_transducer_system_display(in_vector)'
    checkpoint_tracer(checkpoint_name, in_vector[0][0:10])
    string_display = ''
    for i in range(len(in_vector[1])):
        string_display = string_display + str(in_vector[1][i])
    print('\n', 'System display: ', string_display, '\n--------------------------------\n')


#pylint: disable=line-too-long
#justification: old version 2 code
def system_to_compare_with_deep_learning_architecture(in_vector):
    #not used again until version migration
    '''For use to compare the MBLS with other cognitive
    architectures and information systems.

    The MBLS architecture involves hierarchies of pattern recognizers
    (the HLNs) which gives it similarities but also different properties than deep learning
    systems (e.g., Lázaro-Gredilla et al., 2017; Goodfellow et al., 2016).  Work on hierarchies
    of pattern recognizers actually started many years ago with Mountcastle’s (1957) hypothesis
    concerning the columnar organization of the cerebral cortex, and continued strongly in the
    last two decades (e.g., George and Hawkins, 2009; Lázaro-Gredilla et al., 2017).
    The MBLS builds upon previous work in artificial neural networks and systems of
    hierarchies of pattern recognizers, but has a number of different learning mechanisms
    which can use common techniques from previous work (e.g., Hebbian-like learning and
    gradient descent-like algorithms within the HLNs and/or between the different HLNs)
    but also different ones too (e.g., discrete immediate strong connections between HLNs,
    only briefly touched upon above, e.g., extreme rapid reconfigurations of HLNs with each
    other depending on meaningfulness values). The MBLS has a number of different operational
    features than previous work, such as the extreme rapid reconfigurations it undergoes in
    an attempt to maximize meaningfulness. The MBLS has a number of different features in its
    architecture than previous work, such as for example, lack of sharp demarcation and structures
    for long-term procedural memory versus long-term declarative memory, but instead, it heavily
    relies on a long-term causal memory. As well, the MBLS incorporates from its elementary
    HLN units, without the aid of an external CPU or memory, regions that can symbolically process
    input vectors (as well as symbolically-processed data vectors fed back to itself as thoughts)
    in the context of the entire MBLS rather than independently as an external CPU would do.
    While recent works have started narrowing the neural-symbolic gap (e.g., Graves et al., 2016;
    Sabour et al., 2017), it is believed that the meaningful-based learning system (MBLS) can close
    it – the MBLS should be able to perform the sensory processing associated with artificial
    neural networks while retaining the efficiently learned causal symbolic processing of the
    human brain.
    '''
    checkpoint_name = 'system_to_compare_with_deep_learning_architecture(in_vector)'
    checkpoint_tracer(checkpoint_name, in_vector)
    return in_vector
#pylint: enable=line-too-long

def mbls201_code_stack():
    '''docstring here
    '''
    vector1 = input_cam_vector()
    vector2 = input_vectors(vector1)
    vector3 = hln_sensory_input1(vector2)
    vector4 = sensory_binding1(vector3)
    vector5 = causal_memory1(vector4)
    vector6 = pattern_memory1(vector5)
    vector7 = logic_working_memory1(vector6)
    vector8 = hln_motor_output1(vector7)
    vector9 = output_vectors(vector8)
    output_transducer_system_display(vector9)
    #return


####################

#
#  Table of Contents
#  -----------------
#  0.  Preface: Version and Technical Notes
#  1.  Introduction: Why Create this Program?
#  2.  Sleep/Wake and Autonomic Functions <-
#  3.  Lower-Level Assist Functions
#      2a. Main Module Lower-Level Assist Functions
#      2b. Imported Module
#  3A. Higher-Level Assist Functions
#  4.  High-Level MBLS Architecture Visible Functions
#      3a. Main Module High-Level MBLS Architecture Visible Functions
#      3b. Imported Module
#->5.  Main Program Code <-
#  6.  Embedded Software/Hardware Management
#

#5. MAIN PROGRAM CODE

#
#
#The above occurs automatically, over and over again. Every
#evaluation cycle, the MBLS looks at the meaningfulness of the
#data in the sensory input vectors with modulation by the external
#inputs, and cycles through varying levels of abstraction so as
#to reconfigure the HLNs in a way to maximize local and system
#meaningfulness, which also can include utilization of the HLNs
#connected to the HLNs forming the working memory subunits and logic
#subunits. The evaluation cycle completes, local and system meaningfulness
#is fed back to the HLNs via the feedback vector, and the next evaluation
#cycle starts again.


def unit_testing_functions_that_can_be_called_within_the_code():
    '''These unit testing functions should be in an external file which can be
    called by Pytest. However, at times it is convenient to call these functions
    informly from within this code in a specific dev mode. They should never be
    casually called as they can modify data structures.
    Args:
        --
    Style/use note:
        --
    Returns:
        True if all unit tests run successfully
        False if any unit test fails
    Raises:
        try/except
    '''
    verbose = TEST_VERBOSITY
    #HOP NOTE: From 'Flags used for Development Purposes' at start of code
    logging.info("ALL SELECTED INTERNAL UNIT TESTS START")
    print('\nINTERNAL UNIT TESTING FUNCTION WILL NOW RUN')
    print('-------------------------------------------')
    print('Verbosity is set as: ', verbose)
    print('Unit Testing normally runs in external {} or test_<name>.'.format(PYTEST_UNIT_FILENAME))
    print('However, some are modified to run internally within the actual program code.\n')
    success_of_all_unit_tests = True

    try:
        if MEMORY_CHECKING_ON:
        #HOP NOTE: From 'Flags used for Development Purposes' at start of code
            if not memory_var_usage_test():
                success_of_all_unit_tests = False
        else:
            print('BYPASS UNIT TEST: memory_var_usage: MEMORY_CHECKING_ON not set to True\n')
        if not test_sleep_selection():
            success_of_all_unit_tests = False
        if not in_vecs_load_test(IN_VECS_FILE_TEST, verbose):
            success_of_all_unit_tests = False
    except:
        print('unit_testing_functions_that_can_be_called_within_the_code() raised try/except')
        logging.info('unit_testing_functions_that_can_be_called_within_the_code() ->try/except')
        success_of_all_unit_tests = False
    if success_of_all_unit_tests:
        print('\nALL SELECTED UNIT TESTS OVER-- SUCCESS\n\n')
        logging.info("ALL SELECTED INTERNAL UNIT TESTS OVER -- SUCCESS")
        return True
    print('\nALL SELECTED UNIT TESTS OVER-- FAILURE OF ONE OR MORE TESTS\n\n')
    logging.info("ALL SELECTED INTERNAL UNIT TESTS OVER -- FAILURE OF ONE OR MORE TESTS")
    return False


def job():
    '''sample code to try out schedule
        Args: --
        Style/use note: placeholder code
        Returns: --
        Raises: --
    '''
    print("I'm working....")


def welcomexxxx()-> bool: #defined above in nano code
    ''' Provides welcome message at start of program.
        Will first test to see if 'pragma' set for a force of the embedded_main()
          (if so, then embedded_main() is run and then exit of the code)
        Args:
            --
        Style/use note:
            --
        Returns:
            True if continues to display message
            No return if embedded_main() run since will exit code before
            False if failed try for a forced run of embedded_main()
        Raises:
            try/except
    '''
    return_value = True
    try:
        if FORCE_EMBEDDED_MAIN:
            #HOP NOTE: From 'Flags used for Development Purposes' at start of code
            print('Now attempting to force run of embedded_main instead of main()')
            logging.info('Now attempting to force run of embedded_main instead of main()')
            print('Embedded flags: PYBOARD=', PYBOARD)
            logging.info('Embedded flags: PYBOARD=')
            logging.info(PYBOARD)
            if not PYBOARD:
                embedded_main()
            else:
                embedded_main_pyboard()
            sys.exit()
    except:
        print('Error occurred with forcing EMBEDDED MAIN from main()')
        print('Will continue with normal main()')
        logging.info('Error occurred with forcing EMBEDDED MAIN from main()')
        logging.info('Will continue with normal main()')
        return_value = False
    print('\nWelcome to the Meaningful-Based Learning System')
    print('  (Version number: {}, Filename: {})'.format(VERSION_NUMBER, VERSION_FILE_NAME))
    print('                     MBLS')
    print('                     ----\n')
    logging.info("welcome message done")
    return return_value


def mainxxxx():  #defined above in nano code
    '''
    Main Code -- sub-symbolic and symbolic cycles loop until a sleep cycle occurs
    '''
    #pylint: disable=too-many-statements
    logging.info('\n------MAIN()----------------------------------------------------\n\n\n\n')
    welcomexxxx()   #otherwise accesses different welcome function with different arg requirements
    if not DEVPT_SKIP:
        #HOP NOTE: From 'Flags used for Development Purposes' at start of code
        unit_testing_functions_that_can_be_called_within_the_code()



    alive = True
    print(start_cumulative_time())
    while alive:
        print(apply_developmental_timer(start_cumulative_time()))
        start_active_time(active_time=0)
        #allow 18 hours of sub-symbolic 100msec cycles and 2000msec approximate symbolic cycles
        while start_active_time() < 3600 * 18:
            #apply input sensor data to hln's
            print(apply_visual_inputs())
            print(apply_auditory_inputs())
            print(apply_olfactory_inputs())
            #apply input sensor data to reflex circuits
            print(reflex_apply_visual_inputs())
            print(reflex_apply_auditory_inputs())
            print(reflex_apply_olfactory_inputs())
            #first feedforward before meaningfulness shuffle
            print(apply_v1_to_v2())
            print(apply_v2_to_v3())
            print(apply_v3_to_t1())
            print(apply_k1_to_k2())
            print(apply_k2_to_k3())
            print(apply_k3_to_t1())
            print(apply_a1_to_a2())
            print(apply_a2_to_a3())
            print(apply_a3_to_t1())
            #meaningfulness shuffle
            print(meaningfulness_shuffle_v1())
            print(meaningfulness_shuffle_v2())
            print(meaningfulness_shuffle_v3())
            print(meaningfulness_shuffle_a1())
            print(meaningfulness_shuffle_a2())
            print(meaningfulness_shuffle_a3())
            print(meaningfulness_shuffle_k1())
            print(meaningfulness_shuffle_k2())
            print(meaningfulness_shuffle_k3())
            #do another feedforward
            print(apply_v1_to_v2())
            print(apply_v2_to_v3())
            print(apply_v3_to_t1_prime())
            print(apply_k1_to_k2())
            print(apply_k2_to_k3())
            print(apply_k3_to_t1_prime())
            print(apply_a1_to_a2())
            print(apply_a2_to_a3())
            print(apply_a3_to_t1_prime())
            #choose between previous t1 results or new t1_prime results
            print(choose_t1_prev_or_t1_prime())
            #feedback to adjust weights to better give desired results
            #close to real-time adjustment in weights
            print(fast_backprop_t1_to_v3())
            print(fast_backprop_v3_to_v2())
            print(fast_backprop_v2_to_v1())
            print(fast_backprop_t1_to_a3())
            print(fast_backprop_a3_to_a2())
            print(fast_backprop_a2_to_a1())
            print(fast_backprop_t1_to_k3())
            print(fast_backprop_k3_to_k2())
            print(fast_backprop_k2_to_k1())
            #causal memory initial propagation
            print(apply_t1_to_c1())
            print(apply_c1_to_c2())
            #sub-symbolic goals propagation
            print(apply_c1_to_instinctual_goals())
            print(apply_t1_to_instinctual_goals())
            print(apply_instinctual_goals_to_c2())
            #sub-symbolic physics world propagation
            print(apply_c1_to_instinctual_physics())
            print(apply_t1_to_instinctual_physics())
            print(apply_instinctual_physics_to_c2())
            #sub-symbolic psychology world propagation
            print(apply_c1_to_instinctual_psychology())
            print(apply_t1_to_instinctual_psychology())
            print(apply_instinctual_psychology_to_c2())
            #apply processed sensory to motor center
            print(apply_reflex_center_to_m1())
            print(apply_t1_to_m1())
            print(apply_c1_to_m1())
            print(apply_c2_to_m1())
            print(apply_m1_to_motor_actuator())
            print(apply_m1_to_m2())
            print(apply_m2_to_m3())
            print(apply_m3_to_motor_actuator())
            print(apply_somatic_sensory_to_m1())
            print(apply_reflex_center_to_m1())
            print(apply_t1_to_m1())
            print(apply_c1_to_m1())
            print(apply_c2_to_m1())
            print(apply_m1_to_m2())
            print(apply_m2_to_m3())
            print(apply_m3_to_motor_actuator())
            print(fast_backprop_m3_to_m2())
            print(fast_backprop_m2_to_m1())
            #apply symbolic logic
            print(apply_c2_to_pre_g1())
            print(convert_pre_g1_to_working_memory_g1())
            print(apply_c2_to_pre_g2())
            print(convert_pre_g2_to_working_memory_g2())
            print(apply_t1_to_instinctual_goals())
            print(apply_c2_to_instinctual_goals())
            print(apply_g1_to_instinctual_goals())
            print(apply_g2_to_instinctual_goals())
            print(apply_instinctual_goals_to_g1())
            print(apply_instinctual_goals_to_g2())
            print(apply_t1_to_goal_conscious())
            print(apply_c2_to_goal_conscious())
            print(apply_goal_conscious_to_g1())
            print(apply_goal_conscious_to_g2())
            print(apply_m3_to_g1())
            print(apply_m3_to_g2())
            print(apply_t1_to_world_view())
            print(apply_c2_to_world_view())
            print(apply_g1_to_world_view())
            print(apply_g2_to_world_view())
            print(apply_world_view_to_instinctual_goals())
            print(apply_world_view_to_instinctual_physics())
            print(apply_world_view_to_instinctual_psychology())
            print(apply_world_view_to_instinctual_scheduling())
            print(apply_t1_to_instinctual_physics())
            print(apply_c2_to_instinctual_physics())
            print(apply_g1_to_instinctual_physics())
            print(apply_g2_to_instinctual_physics())
            print(apply_instinctual_physics_to_g1())
            print(apply_instinctual_physics_to_g2())
            print(apply_t1_to_instinctual_psychology())
            print(apply_c2_to_instinctual_psychology())
            print(apply_g1_to_instinctual_psychology())
            print(apply_g2_to_instinctual_psychology())
            print(apply_instinctual_psychology_to_g1())
            print(apply_instinctual_psychology_to_g2())
            print(apply_t1_to_emotional_reward_module())
            print(apply_c2_to_emotional_reward_module())
            print(apply_g1_to_emotional_reward_module())
            print(apply_g2_to_emotional_reward_module())
            print(apply_emotional_reward_module_to_g1())
            print(apply_emotional_reward_module_to_g2())
            print(apply_g1_operations_to_g1_prime())
            print(apply_g2_operations_to_g2_prime())
            print(apply_g1_operations_to_g2())
            print(apply_g2_operations_to_g1())
            print(apply_g1_operations_to_g1_prime())
            print(apply_g2_operations_to_g2_prime())
            print(apply_g1_prime_to_v2())
            print(apply_g2_prime_to_v2())
            print(apply_g1_prime_to_goal_conscious())
            print(apply_g2_prime_to_goal_conscious())
        #after active time exceeded leave active time while loop and
        #move to this outer sleep/wake while loop
        print('switching to a sleep cycle now....')
        print('(can be overridden depending on sleep function inputs)')
        #response from sleep centers can determine issues with alive status
        #TODO: if sleep center response malfunctions program will stop here
        if sleep_selection(0):
            continue
        else:
            sys.exit()



#start_simulation('MBLS Simulation of Finding Lost Hiker in Forest')
#TODO: deprecate/version3: implement in instinctual goals rather than
#explicit code
#
#	while True:
#		sleep
#		#mbls201_code_stack()
#		sleep(5)
#
#		#wake_up()
#
#		break
#def wake_up():


####################

#
#  Table of Contents
#  -----------------
#  0.  Preface: Version and Technical Notes
#  1.  Introduction: Why Create this Program?
#  2.  Sleep/Wake and Autonomic Functions <-
#  3.  Lower-Level Assist Functions
#      2a. Main Module Lower-Level Assist Functions
#      2b. Imported Module
#  3A. Higher-Level Assist Functions
#  4.  High-Level MBLS Architecture Visible Functions
#      3a. Main Module High-Level MBLS Architecture Visible Functions
#      3b. Imported Module
#  5.  Main Program Code
#->6.  Embedded Software/Hardware Management <-
#      6a. MicroPython Implementation and Communication
#

#6. EMBEDDED SOFTWARE/HARDWARE MANAGEMENT

#Goal of MBLS-3.0 Implementation is to use the Meaningful-Based Cognitive Architecture to
#control a Search-and-Rescue Robot, with the simulation of finding a lost hiker in a forest
#filled with a host of sensory noise and other irrelevant sensory signals.
#
#
#Many of the key embedded and multi-threading functions for this purpose are at this time
#implemented as inner functions encapsulated away from the non-embedded MBLS code.
#
#

def embedded_main():
    '''While run different portions of the MBLS in multiple threads for
    use with an embedded version of the MBLS-3.0 in, for example, a Search-and-
    Rescue Robot.
    '''
    logging.info('\n------EMBEDDED_MAIN()--------------------------------------\n\n\n\n')
    print('Reserved for running MBLS search-and-rescue robot version of Main() now.')

    def mbls_job1():
        '''MBLS functions running a job on a separate thread.
        Note: At this time not extensively tested on different hardware
        and operating system platforms. On Windows platform executes but
        a single core appears to be utilized only.
        '''
        print("Executing MBLS job1 thread now.")


    def mbls_job2():
        '''MBLS functions running a job on a separate thread.
        Note: At this time not extensively tested on different hardware
        and operating system platforms. On Windows platform executes but
        a single core appears to be utilized only.
        '''
        print("Executing MBLS job2 thread now.")


    def run_mbls_thread(mbls_job):
        '''Run each of the MBLS job functions in its own thread.
        Note: At this time not extensively tested on different hardware
        and operating system platforms. On Windows platform executes but
        a single core appears to be utilized only.
        '''
        mbls_jobjob_thread = threading.Thread(target=mbls_job)
        mbls_jobjob_thread.start()

    #pylint: disable=line-too-long
    #todo & temporary justification: need to apply to MBLS robot example
    schedule.every(EMBEDDED_MBLS_MULTITHREAD_INTERVALS_SECONDS).seconds.do(run_mbls_thread, mbls_job1)
    schedule.every(EMBEDDED_MBLS_MULTITHREAD_INTERVALS_SECONDS + 4).seconds.do(run_mbls_thread, mbls_job2)
    #pylint: enable=line-too-long

    while True:
        schedule.run_pending()
        time.sleep(EMBEDDED_MBLS_PAUSE_MULTITHREAD_INTERVALS_SECONDS)

####################

#
#  Table of Contents
#  -----------------
#  0.  Preface: Version and Technical Notes
#  1.  Introduction: Why Create this Program?
#  2.  Sleep/Wake and Autonomic Functions <-
#  3.  Lower-Level Assist Functions
#      2a. Main Module Lower-Level Assist Functions
#      2b. Imported Module
#  3A. Higher-Level Assist Functions
#  4.  High-Level MBLS Architecture Visible Functions
#      3a. Main Module High-Level MBLS Architecture Visible Functions
#      3b. Imported Module
#  5.  Main Program Code
#  6.  Embedded Software/Hardware Management <-
#->    6a. MicroPython Implementation and Communication
#
#6a. MicroPython Implementation and Communication
#------------------------------------------------
#justification: Some minimal documentation is required about direction of hardware interfacing.
'''
The goal of the MBLS-3.0 Implementation is to use the Meaningful-Based Cognitive Architecture
to control a Search-and-Rescue Robot, with the simulation of finding a lost hiker in a forest
filled with a host of sensory noise and other irrelevant sensory signals. Thus, the code above
must be able to somehow interface with the electronics of such a Search-and-Rescue Robot. This
issue has not been resolved at the time of this writing.

If a completely self-contained Search-and-Rescue Robot exists with some sort of interface to
high level instructions and data, then the issue becomes more of a digital communication issue
bidirectionally (the MBLS requires data in as well, not just instructions out) between the
MBLS code above and the Robot. More likely there will be the need to interface at a lower level
to the electronic circuitry of the Robot. In either case, there is the need of physical
communication between the above MBLS code and the Robot. 

At this time, the use of a MicroPython board (or multiple MicroPython boards) is considered as
the approach to the issue of communication, and would be able to handle a wide spectrum of
requirements from abstracted to detailed communication requirements between the main code and
the Robot hardware implementation.

MicroPython is an implementation of Python3 optimized to run on a compatible
micro-controller board. MicroPython is a subset of the full Python 3 and its Standard Library.
As such the above MBLS code has to be refactored so that necessary parts dealing with the
hardware implementation can run in the MicroPython environment. At the time of
this writing, MicroPython requires 256K of code space and 16K of RAM.

Note: MicroPython is an open source software under the MIT license which at this time has over
two hundred contributors.

Note: Although in theory MicroPython can run on a variety of micro-controller boards, in practice
a 'PyBoard' or equivalent (eg, WiPy IoT platform) should be used since the PyBoard has been
designed to run MicroPython code. PyBoards are not as readily available as other micro-controller
boards, eg, Arduino's, but can be commercially purchased from several sources at time of writing.

Note: MicroPython was not able to be run on an unmodified Arduino in MBLS proof of concept trials.
'''
def embedded_main_pyboard():
    '''While run different portions of the MBLS in multiple threads for
    use with an embedded version of the MBLS-3.0 in, for example, a Search-and-
    Rescue Robot.
    '''
    if not PYBOARD:
        print('Embedded software is not set up for a particular hardware implementation')
        print('at this time. Program will now end and exit....')
        sys.exit()
    print('Will attempt hardware-based MicroPython PyBoard execution now....')
    #pylint: disable=import-error
    #pylint: disable=expression-not-assigned
    #justification: success of hardware-based imports depends on development setup
    import pyb
    for i in range(1, 4):
        pyb.LED(i).on()
        time.sleep(2)
        pyb.LED(i).off
    #pylint: enable=import-error
    #pylint: enable=expression-not-assigned


if __name__ == '__main__':
    main_nano()
else:
    if not PYBOARD:
        embedded_main()
    else:
        embedded_main_pyboard()
#
##END PALIMPSET     END PALIMPSET
