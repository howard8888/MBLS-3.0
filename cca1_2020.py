#!/usr/bin/env python
#utf-8 usage auto default in Python3
#ok with colab
'''
Causal Cognitive Architecture 1 (CCA1)
2020 rewrite with architectural changes, clean up of old deprecated versions

main() routine of CCA1 simulation
Contributor(s): Howard Schneider
See GitHub page for licensing, wiki, other details


if __name__ == '__main__': main_eval():  while loop:
    main_mech.cycles(True)  #if nano siml'n chosen
    print_conscious_memory(sim_choice)
    if not run_again(): break loop and end
    -->else loops again for new mission --^

#Deprecation Transition Note
#April 2019 Version 3 of MBLS/MBCA is being transitioned to
#"nano"/"micro"/"milli"/"full" MBCA coarse/fine grain simulations
#deprecated code below left for scaffolding purposes
#Oct 2019 deprecated code into palimpsest.py module
#--> #H12 scaffolded version to replace previous scaffolded version
#--> April 17/19 origin of scaffolding code -- rebuild G12 versions from
# H12 version from this scaffolding
#November 2019 G12/H12 versions MBLS/MBCA being transitioned to a new
#architecture -- CCA1 -- Causal Cognitive Architecture1
#
'''

## START IMPORTS   START IMPORTS
#
##standard imports -- being used by this module
import pdb
import sys
import platform
import os.path
#
##PyPI imports -- being used by this module
try:
    pass
    #nb. none
except ImportError:
    print('\nprogram will end -- cca1.py module unable to import a PyPI module')
    sys.exit()
#
##non-PyPI third-party imports -- being used by this module
try:
    pass
    #justification/ Awesome/LibHunt ratings for non-pypi imports: n/a
    #nb. none
except ImportError:
    print('program will end -- cca1.py module unable to import a third-party module')
    sys.exit()
#
##CCA1 module imports -- being used by this module
try:
    #pass
    import ddata
    import main_mech
    #import eval_micro
    #import eval_milli
    #import palimpsest  #nb  without GPU will use excessive resources
except ImportError:
    print('program will end -- cca1.py module unable to import an CCA1 module')
    sys.exit()
#
##requirements.txt file  -- with reference to this module
#   -design_text.txt (descriptive text from deprecated version)
#   -CCA1 module imports (listed above)
#   -pypi imports (none for this module)
#   -non-pypi third-party imports (none for this module)
#
##END IMPORTS          END IMPORTS

##START PRAGMAS
#
#temporary pylint bypasses during deprecation/transition devpt work
#pylint: disable=invalid-name
#   prefer not to use snake_case style for very frequent data structure or
#   for small temp variables
#pylint: disable=bare-except
#   prefer to have in certain locations to allow more graceful failure
##END PRAGMAS

##START GLOBAL & SYST VARIABLES
#
#most of the global and system data variables are being held in ddata.py
# these will be used by cca1.py module via instantiation ('g') in main_eval()
# of 'Multiple_sessions_data'  (also some global constants copied to g as well)
#include here variables which will persist between missions:
# performance_metric, conscious_memory
#most other data variables are initiated at start of each mission (ie, each
# time main_mech.cycles() is called via instantiation ('d') of Mapdata
##END GLOBAL & SYST VARIABLES

##SANDBOX
#pseudo sandbox  -- please erase after try out some code


#input('\nsandbox code has finished....press a key to end program....')
#sys.exit()
##END SANDBOX


##START METHODS     START METHODS
#
def choose_simulation(g: ddata.Multiple_sessions_data)-> str:
    '''before evaluation cycles of a simulation version start, user can choose which
    simulation to run
    input parameters:
        g: instance of ddata.Multiple_sessions_data
           instantiated in main_eval() when program starts
    returns:
        value corresponding to simulation version chosen
        default return value is "nanoG"

    '''
    default_ret_value = "nanoG"
    printline = """
    \nCCA1  Causal Cognitive Architecture 1\n
    Welcome to the CCA1 Simulator\n
    Simulation: Rescuing a Lost Hiker in a Wumpus World Uninhabited Forest\n
    Please choose which version of the CCA1 simulation you would like to
      run in the Wumpus World.')
    (You will then be prompted to choose characteristics of that version)
    \nThe following choices are available:
    1. CCA1 nano version D
    2. CCA1 nano version G (default if hit ENTER)
    3. CCA1 nano version H
    4. CCA1 micro version beta
    5. CCA1 milli version beta
    6. CCA1 full simulation version 2018 code
    7. CCA1 full simulation version beta
    8. AlexNet PyTorch implementation in same Wumpus World
    9. PyTorch RL (conv1-3&fc4-5 layers) in same Wumpus World
    -1 Exit program
    -2 Design philosophy behind Simulation (then runs default)
    -3 Information about computing environment (then runs default)
    -4 n/c
    \n\nAPRIL 2020 DEPRECATION & FUNCTIONAL NOTE:
    MBLS-3 simulations are being converted to coarse and fine grain simulations --
    "nano", "micro", "milli" and "full" simulations
    The "nano" version is more a functional simulation that provides scaffolding to
    insert more authentic components in the "micro" and more fine grained simulations.
    Then G12/H12 versions MBLS/MBCA being transitioned to a new
    architecture -- CCA1 -- Causal Cognitive Architecture 1

    """
    if g.fastrun:
        print('\n\n-------------------------------------------')
        print('\nCCA1   Causal Based Cognitive Architecture 1\n')
        print('Welcome to the CCA1 Simulator\n')
        return default_ret_value

    choices = {
        0: ('\nNot defined but will return standard G version\n', default_ret_value),
        1: ('\n"nano" version D or H converted to standard G version\n', default_ret_value),
        2: ('\n"nano" standard G version is selected\n', "nanoG"),
        3: ('\n"nano" version D or H converted to standard G version\n', default_ret_value),
        4: ('\n"micro" version selected\n', "micro"),
        5: ('\n"milli" version selected\n', "milli"),
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
    if input('\nRun again?') in ('N', 'n', 'NO', 'No', 'nO', 'N0', 'no', '0', 'stop', 'break'):
        return False
    return True


def print_conscious_memory(g: ddata.Multiple_sessions_data, sim_choice: str)-> bool:
    '''print out raw conscious memory for now
    add more functionality in future versions via
    other methods inside the appropriate module
    '''
    if sim_choice == "nanoG":
        if input('Print out raw conscious memory?') in ('Y', 'y', 'Yes', 'yes'):
            g.printout_conscious_memory()
        return True
    if sim_choice == "micro":
        if input('Print out raw conscious memory?') in ('Y', 'y', 'Yes', 'yes'):
            g.printout_conscious_memory()# type: ignore
        return True
    if sim_choice == "milli":
        if input('Print out raw conscious memory?') in ('Y', 'y', 'Yes', 'yes'):
            g.printout_conscious_memory()# type: ignore
        return True
    print("\ndebug: main_eval() called print_conscious_memory(sim_choice) but")
    input("       sim_choice is not recognized....press any key to continue....")
    return False


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
    print('\nInformation about computing environment:\n')
    try:
        print('CCA1 Project: Python installed: ', os.path.dirname(sys.executable))
        print('Platform Info (via StdLib): \n  ',
              'Python version: ', sys.version,
              '\n   os.name:', os.name, ', sys.platform:', sys.platform,
              'platform.system:', platform.system(),
              ', platform.release:', platform.release(),
              '\n  ', 'platform.processor:', platform.processor(), '\n  ',
              'sys.maxsize (9223372036854775807 for 64 bit Python): ', sys.maxsize)
        try:
            #GPU appropriate library required
            print('   Local or cloud GPU checking not enabled at present')
        except:
            print('Unable to check correctly if GPU_ENABLED')
        input('Press any key to continue....')
        return True
    except:
        print('Unable to obtain full computing envrt information\n')
        input('Press any key to continue....')
        return False


def embedded_main_pyboard()-> None:
    '''check palimpsest for embedded_main_pyboard()
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
    essentially top level main() of CCA1 simulation
    this method will generally call a particular version of one
     the nano, micro, milli or full simulation's evaluation cycles
     (which runs until the mission (==simulation) is completed)
    after mission complete, control returns here and can decide if
      want to run another mission or exit from this main loop

    if __name__ == '__main__': main_eval():  while loop:
        main_mech.cycles(True)  #if nano siml'n chosen
        print_conscious_memory(sim_choice)
        if not run_again(): break loop and end
        -->else loops again for new mission --^

    '''
    #set up
    os.system('cls')
    g = ddata.Multiple_sessions_data()

    #run mission, repeat mission again or exit
    while True:
        #current_valid_choices = ("nanoG", "micro", "milli", "full2018", "2018")
        sim_choice = choose_simulation(g)
        if sim_choice in ("full2018", "2018"):
            sim_choice = "nanoG"
            print('\nnb. at this point in deprecation/rewrite full simulations--> nanoG\n')

        elif sim_choice == "nanoG":
            try:
                main_mech.cycles(g, True)  #  type: ignore
                print_conscious_memory(g, sim_choice)
                if not run_again():
                    break
            except:
                print('debug: main_mech.py module not found by main_eval()')
                break

        elif sim_choice == "micro":
            try:
                eval_micro.evaluation_cycles_micro1(g, True)  # type: ignore
                print_conscious_memory(g, sim_choice)
                if not run_again():
                    break
            except NameError:
                print('debug: eval_micro.py module not found by main_eval()')
                break

        elif sim_choice == "milli":
            try:
                eval_milli.evaluation_cycles_milli1(g, True)  # type: ignore
                print_conscious_memory(g, sim_choice)
                if not run_again():
                    break
            except NameError:
                print('debug: eval_milli.py module not found by main_eval()')
                #raise NameError  #for system debugging
                break

        else:
            print('debug: unknown value sent to main_eval..program will end..')
            break
        #if not exited, then new mission (and selection) repeats now again --^
    exit_program()

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
##START PALIMPSEST     START PALIMPSEST
# 3408 lines of deprecated code transferred to
# module palimpsest.py (old lines 2615 - 6023 ver 23)
#
##END PALIMPSEST     END PALIMPSEST
