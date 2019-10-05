#!/usr/bin/env python
#utf-8 usage auto default in Python3
#ok with colab
'''
Meaningful-Based Cognitive Architecture (MBCA)
main() routine of MBCA simulation
can choose coarse grain ("nano") to finer grain("micro")
to finest grains ("mini" and "full") simulations


#Deprecation Transition Note
#April 2019 Version 3 of MBLS/MBCA is being transitioned to
#"nano"/"micro"/"mini"/"full" MBCA coarse/fine grain simulations
#deprecated code below left for scaffolding purposes
#Oct 2019 deprecated code into palimpset.py module
#--> #H12 scaffolded version to replace previous scaffolded version
#--> April 17/19 origin of scaffolding code -- rebuild G12 versions from
# H12 version from this scaffolding
'''


##standard imports -- being used by this module
import pdb
import sys
import os.path
#
##pypi imports
#   nb. none
try:
    pass
except ImportError:
    print('debug: mbca_main.py module unable to import a pypi module')
    input('\nPress any key to continue....')
#
##MBCA module imports -- being used by this module
try:
    import eval_nano
    #import eval_micro
    #import eval_mini
    #import palimpset
except ImportError:
    print('\ndebug: mbca_main.py module unable to import one or more mbca modules')
    print('       please make sure needed modules,paths, etc set up correctly')
    print('       (please look at mbca_main.py -- fairly self-explanatory)')
    input('\nPress any key to continue....')
#
##files and other resources required to run module
#"design_text.txt" -- descriptive text from deprecated version
#

#sandbox here to quickly try out things -- please erase code afterwards


#input('sandbox code has finished')
#
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
    -2 Design Philosophy behind Simulation (descriptive, no running of code)
    \n\nAPRIL 2019 DEPRECATION & FUNCTIONAL NOTE:
    MBLS-3 simulations are being converted to coarse and fine grain simulations --
    "nano", "micro", "mini" and "full" simulations
    The "nano" version is more a functional simulation that provides scaffolding to
    insert more authentic components in the "micro" and more fine grained simulations.
    """
    print(printline)
    try:
        simulation_version_choice = int(input('\nPlease make a selection: '))
    except ValueError:
        print('Choice not found, thus default nano version G selected')
        return default_ret_value
    if simulation_version_choice == -2:
        design_philosophy("design_text.txt")

    choices = {
        0: ('\nNot defined but will return standard G version\n', default_ret_value),
        1: ('\n"nano" version D or H converted to standard G version\n', default_ret_value),
        2: ('\n"nano" standard G version is selected\n', "nanoG"),
        3: ('\n"nano" version D or H converted to standard G version\n', default_ret_value),
        4: ('\n"micro" version selected\n', "micro"),
        5: ('\n"mini" version selected\n', "mini"),
        6: ('\n"full simulation" 2018 code selected\n', "full2018"),
        7: ('\n"full simulation" beta code selected\n', "2018"),
        8: ('\n"AlexNet or PyTorch versions currently converted to "nano" G version\n', "nanoG"),
        9: ('\n"AlexNet or PyTorch versions currently converted to "nano" G version\n', "nanoG"),
        -1:('\nExit choice....', "exit"),
        -2:('\nDesign Philosophy behind Simulation (descriptive, no running of code)\n', "design")
        }

    if simulation_version_choice in range(-1, 10):
        print(choices[simulation_version_choice][0])
        return choices[simulation_version_choice][1]
    print('Choice not found, thus default nano version G selected\n')
    return default_ret_value


def exit_program()-> bool:
    '''orderly shutdown of program
    "nano" version no intermediate PyTorch structures to save
    '''
    print('Orderly shutdown of program via exit_program()')
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
    if sim_choice == "mini":
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
        return True
    except FileNotFoundError:
        print('\nCannot find the file {} -- verify path or its location\n'.format(file_name))
    exit_program()
    return False #mypy insisted on boolean return


def embedded_main_pyboard()-> bool:
    '''check palimpset for embedded_main_pyboard()
    code
    '''
    print("'embedded_main_pyboard()' is currently part of deprecated code")
    input("Program will now be ended.... click any key to continue....")
    exit_program()
    return False #mypy insisted on boolean return
#
##END METHODS     END METHODS


##START MAIN     START MAIN
#
def main_eval()-> bool:
    '''
    essentially main() of MBCA simulation
    this method will generally call a particular version of one
     the nano, micro, mini or full simulation's evaluation cycle
     over and over again until the mission is completed
    '''
    #set up platform
    os.system('cls')

    #run mission, repeat mission again or exit
    while True:
        #pylint: disable=undefined-variable
        #chose simulation for this loop
        sim_choice = choose_simulation()

        #choose to exit loop
        if sim_choice == "exit":
            exit_program()

        #utilize coarse to fine grain simulation selected
        if sim_choice in ("full2018", "full"):
            print('At this point in deprecation/rewrite the full simulations are')
            print('being run instead as "nanoG", or if available, "mini" versions')
            sim_choice = "nanoG"

        if sim_choice == "nanoG":
            try:
                #use evaluation_cycles_nano1(True)
                eval_nano.initiate_global_variables()
                eval_nano.evaluation_cycles_nano1(True)
                #repeat mission again or exit?
                print_conscious_memory(sim_choice)
                run_again()
            except NameError:
                print('debug: eval_nano.py module not found by main_eval()')
                exit_program()

        if sim_choice == "micro":
            try:
                #evaluation_cycles_nano1(True)
                eval_micro.initiate_global_variables()  # type: ignore
                eval_micro.evaluation_cycles_micro1(True)  # type: ignore
                #repeat mission again or exit?
                print_conscious_memory(sim_choice)
                run_again()
            except NameError:
                print('debug: eval_micro.py module not found by main_eval()')
                exit_program()

        if sim_choice == "mini":
            try:
                #evaluation_cycles_nano1(True)
                eval_mini.initiate_global_variables()  # type: ignore
                eval_mini.evaluation_cycles_mini1(True)  # type: ignore
                #repeat mission again or exit?
                print_conscious_memory(sim_choice)
                run_again()
            except NameError:
                print('debug: eval_mini.py module not found by main_eval()')
                exit_program()

        if sim_choice not in ("nanoG", "micro", "mini"):
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
    embedded_main_pyboard()
sys.exit()
pdb.set_trace()


#
##START PALIMPSET     START PALIMPSET
# 3408 lines of deprecated code transferred to
# module palimpset.py (old lines 2615 - 6023 ver 23)
#
##END PALIMPSET     END PALIMPSET
