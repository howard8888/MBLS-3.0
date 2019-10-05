#!/usr/bin/env python
#utf-8 usage auto default in Python3
#ok with colab
'''
Meaningful-Based Cognitive Architecture (MBCA)
main() routine of MBCA simulation
can choose coarse grain ("nano") to finer grain("micro")
to finest grains ("mini" and "full") simulations

Contributor(s): Howard Schneider
See GitHub page for licensing, wiki, other details

#Deprecation Transition Note
#April 2019 Version 3 of MBLS/MBCA is being transitioned to
#"nano"/"micro"/"mini"/"full" MBCA coarse/fine grain simulations
#deprecated code below left for scaffolding purposes
#Oct 2019 deprecated code into palimpset.py module
#--> #H12 scaffolded version to replace previous scaffolded version
#--> April 17/19 origin of scaffolding code -- rebuild G12 versions from
# H12 version from this scaffolding
'''

## START IMPORTS   START IMPORTS
#
##standard imports -- being used by this module
import pdb
import sys
import platform
import os.path
#
##pypi imports -- being used by this module
try:
    pass
    #nb. none
except ImportError:
    print('debug: mbca_main.py module unable to import a pypi module')
    print('       please make sure needed modules,paths, etc installed and set up correctly')
    sys.exit()
#
##non-pypi third-party imports -- being used by this module
try:
    pass
    #-justification for non-pypi imports: n/a
    #Awesome Python/LibHunt ratings: n/a
    #nb. no third-party imports
except ImportError:
    print('debug: mbca_main.py module unable to import a third-party module')
    print('       please make sure needed modules,paths, etc installed and set up correctly')
    sys.exit()
#
##MBCA module imports -- being used by this module
try:
    import eval_nano
    #import eval_micro
    #import eval_mini
    #import palimpset  #nb  without GPU will use excessive resources
except ImportError:
    print('\ndebug: mbca_main.py module unable to import one or more mbca modules')
    print('         please make sure needed modules,paths, etc set up correctly')
    print('        (please look at mbca_main.py -- self-explanatory)')
    sys.exit()
#
##requirements.txt file  -- with reference to this module
#   -design_text.txt (descriptive text from deprecated version)
#   -MBCA module imports (listed above)
#   -pypi imports (none for this module)
#   -non-pypi third-party imports (none for this module)
#
##END IMPORTS          END IMPORTS


##START GLOBAL & SYST VARIABLES
#
GPU_ENABLED = False
##END GLOBAL & SYST VARIABLES


##SANDBOX
#pseudo sandbox here to quickly try out things in envr't -- please erase code afterwards


#input('\nsandbox code has finished....press a key to end program....')
#sys.exit()
##END SANDBOX


##START METHODS     START METHODS
#
def choose_simulation()-> str:
    '''before evaluation cycles of a simulation version start, user can choose which
    simulation to run
    returns a value corresponding to simulation version chosen
    default return value is "nanoG"
    '''
    default_ret_value = "nanoG"
    printline = """
    \nMBCA   Meaningful Based Cognitive Architecture\n
    Welcome to the MBCA Simulator\n
    Simulation: Rescuing a Lost Hiker in a Wumpus World Uninhabited Forest\n
    Please choose which version of the MBCA simulation you would like to
      run in the Wumpus World.')
    (You will then be prompted to choose characteristics of that version)
    \nThe following choices are available:
    1. MBCA nano version D
    2. MBCA nano version G (default if hit ENTER)
    3. MBCA nano version H
    4. MBCA micro version beta
    5. MBCA mini version beta
    6. MBCA full simulation version 2018 code
    7. MBCA full simulation version beta
    8. AlexNet PyTorch implementation in same Wumpus World
    9. PyTorch RL (conv1-3&fc4-5 layers) in same Wumpus World
    -1 Exit program
    -2 Design philosophy behind Simulation (then runs default)
    -3 Information about computing environment (then runs default)
    -4 n/c
    \n\nAPRIL 2019 DEPRECATION & FUNCTIONAL NOTE:
    MBLS-3 simulations are being converted to coarse and fine grain simulations --
    "nano", "micro", "mini" and "full" simulations
    The "nano" version is more a functional simulation that provides scaffolding to
    insert more authentic components in the "micro" and more fine grained simulations.
    """
    choices = {
        0: ('\nNot defined but will return standard G version\n', default_ret_value),
        1: ('\n"nano" version D or H converted to standard G version\n', default_ret_value),
        2: ('\n"nano" standard G version is selected\n', "nanoG"),
        3: ('\n"nano" version D or H converted to standard G version\n', default_ret_value),
        4: ('\n"micro" version selected\n', "micro"),
        5: ('\n"mini" version selected\n', "mini"),
        6: ('\n"full simulation" 2018 code selected\n', "full2018"),
        7: ('\n"full simulation" beta code selected\n', "2018"),
        8: ('\n"AlexNet" or PyTorch versions currently converted to "nano" G version\n', "nanoG"),
        9: ('\n"AlexNet" or PyTorch versions currently converted to "nano" G version\n', "nanoG")
        }

    print(printline)
    try:
        simulation_version_choice = int(input('\nPlease make a selection: '))
    except ValueError:
        print('Choice not found, thus default nano version G selected')
        return default_ret_value

    if simulation_version_choice == -1:
        exit_program()
    if simulation_version_choice == -2:
        design_philosophy("design_text.txt")
        return default_ret_value
    if simulation_version_choice == -3:
        computing_evnrt()
        return default_ret_value

    if simulation_version_choice in range(0, 10):
        print(choices[simulation_version_choice][0])
        return choices[simulation_version_choice][1]

    print('Choice not found, thus default nano version G selected\n')
    return default_ret_value


def exit_program()-> None:
    '''orderly shutdown of program
    "nano" version no intermediate PyTorch structures to save
    '''
    print('\nOrderly shutdown of program via exit_program()')
    print('Please ignore any messages now generated by main/pyboard/etc detection code....')
    input('leaving main() now.... press any key to continue....')
    sys.exit()


def run_again()-> bool:
    '''check what action to take at end of a mission, ie, run again?
    '''
    if input('\nRun again?') in ('N', 'n', 'NO', 'No', 'no', '0', 'stop', 'break'):
        exit_program()
    return True


def print_conscious_memory(sim_choice: str)-> bool:
    '''print out raw conscious memory for now
    possibly add more functionality in future versions
    via other methods inside the appropriate module
    '''
    #pylint: disable=undefined-variable
    if sim_choice == "nanoG":
        if input('Print out raw conscious memory?') in ('Y', 'y', 'Yes', 'yes'):
            eval_nano.print_conscious_memory()
        return True
    if sim_choice == "micro":
        if input('Print out raw conscious memory?') in ('Y', 'y', 'Yes', 'yes'):
            eval_micro.print_conscious_memory() # type: ignore
        return True
    if sim_choice == "mini":
        if input('Print out raw conscious memory?') in ('Y', 'y', 'Yes', 'yes'):
            eval_mini.print_conscious_memory() # type: ignore
        return True
    print("\ndebug: main_eval() called print_conscious_memory(sim_choice) but")
    input("       sim_choice is not recognized....press any key to continue....")
    return False
    #pylint: enable=undefined-variable


def design_philosophy(file_name: str)-> bool:
    '''Design Philosophy behind Simulation (descriptive, no running of code)
    Reads through file design_text.txt taken from older versions of the code
    '''
    try:
        f_f = open(file_name, "r")
        i = 0
        for j in f_f:
            i += 1
            if i%20 == 0:
                input('Press any key to continue....')
            print(j)
        print('\n\n\n\nFile reading complete\nDefault code to run....\n\n\n')
        return True
    except FileNotFoundError:
        print('\nCannot find the file {} -- verify path or its location'.format(file_name))
        print('Design philosophy will not be shown, but continue with default code.\n')
        return False


def computing_evnrt()-> bool:
    '''displays information about the computing environment
    '''
    #pylint: disable=bare-except
    print('\nInformation about computing environment:\n')
    try:
        print('MBCA Project: Python installed: ', os.path.dirname(sys.executable))
        print('Platform Info (via StdLib): \n  ',
              'os.name:', os.name, ', sys.platform:', sys.platform,
              'platform.system:', platform.system(),
              ', platform.release:', platform.release(),
              '\n  ', 'platform.processor:', platform.processor(), '\n  ',
              'sys.maxsize (9223372036854775807 for 64 bit Python): ', sys.maxsize)
        if not GPU_ENABLED:
            print('Local or cloud GPU not set up in this module.\n')
        return True
    except:
        print('Unable to obtain full computing envrt information\n')
        return False
        #pylint: enable=bare-except


def embedded_main_pyboard()-> None:
    '''check palimpset for embedded_main_pyboard()
    code
    '''
    print("'embedded_main_pyboard()' is currently part of deprecated code")
    input("Program will now be ended.... click any key to continue....")
    exit_program()
#
##END METHODS     END METHODS


##START MAIN     START MAIN
#
def main_eval()-> None:
    '''
    essentially main() of MBCA simulation
    this method will generally call a particular version of one
     the nano, micro, mini or full simulation's evaluation cycle
     (which runs until the mission is completed)
    after mission complete, control returns here and can decide if
      want to run another mission or exit from this main loop
    '''
    #set up platform
    os.system('cls')

    #run mission, repeat mission again or exit
    while True:
        #pylint: disable=undefined-variable
        sim_choice = choose_simulation()

        if sim_choice in ("nanoG", "full2018", "2018"):
            if sim_choice in ("full2018", "2018"):
                sim_choice = "nanoG"
                print('\nnb. at this point in deprecation/rewrite full simulations--> nanoG\n')
            try:
                eval_nano.initiate_global_variables()
                eval_nano.evaluation_cycles_nano1(True)
                print_conscious_memory(sim_choice)
                run_again()
            except NameError:
                #raise NameError  #for system debugging
                print('debug: eval_nano.py module not found by main_eval()')
                exit_program()

        if sim_choice == "micro":
            try:
                eval_micro.initiate_global_variables()  # type: ignore
                eval_micro.evaluation_cycles_micro1(True)  # type: ignore
                print_conscious_memory(sim_choice)
                run_again()
            except NameError:
                #raise NameError  #for system debugging
                print('debug: eval_micro.py module not found by main_eval()')
                exit_program()

        if sim_choice == "mini":
            try:
                eval_mini.initiate_global_variables()  # type: ignore
                eval_mini.evaluation_cycles_mini1(True)  # type: ignore
                print_conscious_memory(sim_choice)
                run_again()
            except NameError:
                #raise NameError  #for system debugging
                print('debug: eval_mini.py module not found by main_eval()')
                exit_program()

        if sim_choice not in ("nanoG", "micro", "mini", "full2018", "2018"):
            print('debug: choose_simulation() returning unknown value to main_eval()')
            input('Program will end. Press any key to continue....')
            exit_program()
        #pylint: enable=undefined-variable
        #if not exited, then new mission, with new version selection, repeats now again

#
##END MAIN      END MAIN


if __name__ == '__main__':
    main_eval()
else:
    print('\nModule is not named as __main__, thus pyboard version of main being called')
    embedded_main_pyboard()
sys.exit()
pdb.set_trace()


#
##START PALIMPSET     START PALIMPSET
# 3408 lines of deprecated code transferred to
# module palimpset.py (old lines 2615 - 6023 ver 23)
#
##END PALIMPSET     END PALIMPSET
