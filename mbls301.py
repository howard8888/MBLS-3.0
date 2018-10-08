#!/usr/bin/python3
#pylint: disable=too-many-lines
#pylint: disable=pointless-string-statement
#
#MBLS Simulation
#Meaningful Based Learning System implementation of the Meaningful-Based Cognitive Architecture
#Language: Python 3.6
#Lang Note October 2018: Due to testing under 3.6 will not upgrade to higher version for moment.
#CPU, GPU, OS: Independent unless noted below
#
#Person(s) working on this project: Howard Schneider
#howard.schneider@gmail.com
#License: https://github.com/howard8888/MBLS-3.0
#Wiki, ReadMe and other info: https://github.com/howard8888/MBLS-3.0/wiki
#
#


####################

#TABLE OF CONTENTS
#Software is (or should be) written for humans, not computers. The source code below
#should tell a story to you, dear reader, just as any good book would. The language thus
#chosen is English-like Python (with a smattering of optimized C++ at the readable level).
#We do not program aimlessly to add more features or this or that -- we program to tell
#you a story (and in the process create an AGI).
#
#  Table of Contents
#  -----------------
#  0. Preface: Version and Technical Notes
#  1. Introduction: Why Create this Program?
#  2. Sleep/Wake and Autonomic Functions
#  3. Lower-Level Assist Functions
#     2a. Main Module Lower-Level Assist Functions
#     2b. Imported Module
#  4. High-Level MBLS Architecture Visible Functions
#     3a. Main Module High-Level MBLS Architecture Visible Functions
#     3b. Imported Module
#  5. Main Program Code
#  6. Embedded Software/Hardware Management
#
#


####################

#PREFACE: Version and Technical Notes
#
#Prerequisite Knowledge
#----------------------
'''
To make sense of this program you need have/acquire the following prerequisite knowledge-- all
doable and constituting a wonderful journey, for you dear reader. (Please ignore the parts you
have a background in.)

1. Be able to write some small Python programs.

You will not be able to read Python if you
have never written the code. You probably already have this skill, or a skill in a related
language, so not a big issue. However, if you don't, consider acquiring this skill. Allocate
200 hours to doing so. There are a myriad of available courses.

2. Understand at a basic level the landscape of data science and machine learning.

Again, you cannot just read this material -- you need to do some projects. You probably have
this skill (no one is expert in every aspect of data science/ machine learning -- it is too
large), but again, if you don't, consider acquiring this skill. If you have a math background
allocate 200 hours to doing so, if no math background (feel comfortable with matrices and partial
derivatives) then allocate an extra 200 hours, ie, 400 hours in total. Again, if you have
the motivation and time, very doable with a myriad of available courses.

3. Have an introductory background in computer theory and cognitive science.

This is essential to understand why we are doing the things we are doing. The large question
is why even write this program? Why not just use one of those deep learning neural networks
that already exist and seem to do magical "AI" things? There are some online courses that
cover these subjects (ie, computer theory subject, cognitive science subject), but to save
time, consider for computer theory working through the book Algorithmics by David Harel, about
40 hours of your time (this is introductory and you may already have this knowledge),
and for cognitive science consider allocating 20 hours to reading papers in the references below.
("Reading papers" -- you really should make notes in a notebook so
that you will better acquire this information if you are learning it on your own outside
of a classroom.)

4. Read some of the main references described below in the Introduction section.

5. When you are reading the code please do not use a word processor but use a programming
editor (eg, Notepad++ for Windows, or many others) which will show different parts of the code
in different colors.
'''
#Technical Notes
#---------------
'''
Technical notes placeholder
'''
#
#Programming Style
#-----------------
'''
The programming style is a very simple one in theory: "write for you, the reader, not the
computer."

For future (hopefully :) contributors to this project:

-We thus use an English-like language such as Python as much as possible.
-Instead of having a long style section/manual for this project, please download and install
Pylint. We use the arbitrary wisdom of Pylint to decide what style we should or shouldn't use,
plus the general (if not philosophical) rules below.
-We avoid showing the cleverness of the coder, eg, combining 7 actions in a single Python line
when multiple lines would make this more readable and understandable. We write for the person
who must read and understand the code; we don't write for ourselves nor for the computer. (With
the small exception of optimized code routines where necessary for essential functioning of
the program.)
-All the 'spaghetti code' of MBLS version 2 has been replaced (by virtue of necessity -- we are
simulating a search-and-rescue robot rather than the detection of numerical digits) or has been
refactored to meet current style.
-We increase the probability of the code being reliable by unit testing and functional testing.
In keeping with the philosophy above, we favor easy to use and to read testing frameworks (eg,
Pytest-like) versus more complex ones (eg, PyUnit/unittest-like). See below for details.
-We avoid short variable names but try to use names which allow the reader to follow what
the variable represents. (Hard to remember what a variable means after seeing a hundred other
variables.)
-We only use classes if really necessary to ensure a data structure is not abused by other
parts of the program. Otherwise we don't. (Yikes!! But.... this is brain friendly code, not
arbitrary OO friendly code). Again, with apologies to the OO world, the
class name is another piece of data for your brain to remember as you read through the code.
-Unfortunately, there is too much code to keep as a single 'Main' module and we do break up
the code into imported modules, so there is a requirement (albeit without the class
properties) to remember the module name, but we have tried to make this as
gentle as possible for the human brain. (For development we import the rather explicit
but long module names as a shortened abbreviation -- if we start accumulating too many
modules, ie, at the lower Ebbinghaus number of the human mind, then we will change the
abbreviations to the full module name.)
-We keep functions as small as possible and will break them up if they cover too much
new material.
-TODO comments are encouraged. Be creative and be responsible -- add TODO's.
(Note: While not all code editors track TODO's, Pylint will flag any TODO's.)
-Unsure if type 'checking' will make a significant difference in preventing serious errors,
ie, at the level of a static language, so at this time type annotations are 'encouraged' so in
the future code can be checked by a type checker. Extra work but no effect on readability.
At present mypy used (to install: pip install mypy-lang) (to run:eg, mypy mbls300.py)
-Ok to print error messages in interactive parts of the code, but in other areas consider more
formal logging of events and errors via Python logging module.
'''
#
#Biological Inspiration of Cognitive Architecture and Cognitive Functioning
#--------------------------------------------------------------------------
'''
With pride the MBLS implementation of the Meaningful-Based Cognitive Architecture is inspired by
biological neurological cognitive architectures and biological cognitive functioning. It is NOT
the goal of the MBLS to implement a simulation of a biological nervous system at a
spiking-neuron level. Actually it is NOT the intention of the MBLS to simulate a biological
nervous system at a higher level either. Rather, we are inspired by biology, and use the
valuable design nature has provided, to create the best possible artificial cognitive system.
In doing so, however, there may be useful reflections that allow us to better understand
the mammalian nervous system, albeit at the mesoscopic level and above. Again, we are
inspired by biology, and our simulations may help increase the understanding the latter,
but we design and program to create the best possible artificial cognitive functioning ==
best possible AGI (artificial general intelligence) == best possible HLAI (human level
artificial intelligence).
'''
#
#
#Safety
#------
'''
Safety seems irrelevant at this early point of design and implementation of the MBLS, but such
is the argument in the AI and AGI communities that for systems which grow to become
superintelligence systems it will be argued at their start that it is too early to spend time
on safety issues (ie, safety in preventing the system from becoming some unproven
superintelligent system that would exponentially improve itself and then be a danger to
humankind). However, we note one important difference of the MBLS versus other AGI potential
systems -- the MBLS not only has an intuitive physics and intuitive psychology but also has
among its intuitive systems an intuitive human culture system. Just as it knows at a very
basic level that objects are permanent, for example, it knows at a very basic level its
purpose is to benefit the humans it interacts with. (There are many arguments in the AGI
community why this or that safeguard is not adequate, and such arguments could also be applied
to the intuitive human culture of the MBLS, but we argue in return this is a very strong
safeguard for one, and and for two, at this point in the development of the MBLS we don't
have the resources to spend more effort on this issue.)

With regard to the potential for superintelligence, an honest answer would be "yes" -- if the
number of working memories in the MBLS is increased and the quasi-instruction set that
manipulates vectors in and to and from the working memories is made more sophisticated,
and the algorithmic section is ramped up, then yes, a superintelligence of sorts should
emerge. But, this is not the goal of the MBLS and no work is planned in this area.
'''
#
#pylint: disable=wrong-import-position
#pylint: disable=unused-import
#Import Python3 Standard Library Modules
#---------------------------------------
#-New Python programmer note: No need to install anything -- Python will automatically import.
#-Platform dependency note: Dependencies noted via inline comments.
import random
import sys          #Warning: DEPENDENCIES win64
import os.path      #Warning: DEPENDENCIES win64
import platform
import time
import threading    #Warning: platform DEPENDENCIES uncertain
import logging
#
#
#Import Third-Party Dependencies
#-------------------------------
#-Style note: It is ok to import well known packages such as numpy with an abbreviation,
#since to our brains, it is not really an abbreviation.
#-Platform dependency note: Will run on most platforms unless inline comment.
#-A requirements.txt file is on GitHub page with exact version numbers.
#-New Programmer note: >pip install -r requirements.txt  -- will install exact dependencies
#-New Programmer note: If you have multiple projects, to avoid a mixture of different versions
#of dependencies, use a virtual environment: 1. Use a new directory 2. >python -m venv mbls
# 3. Go to mbls/Scripts (in Win) 4. >activate  5. (mbls)>  -- you are now in virtual envr't
#-In future, if any module is not in PyPI for automatic pip installation, then installation
#instructions will be given, and a copy of the module will also be on the GitHub page.
#-Third-party dependencies can potentially wreak havoc. Thus, a justification note is required
#for every third-party dependency used (as well to ensure license allows use).
import numpy as np
#Justification note: Awesome Python/LibHunt: 9.6 popularity, 9.8 activity, >8000 stars
#code quality ?? (L1 patchwork does not make sense), programmed in C, BSD license
#"fundamental package needed for scientific computing with Python...."
import schedule
#Justification note: Awesome Python/LibHunt: 8.8 popularity, 4.8 activity, >5000 stars
#code quality L4 (lumnify scale), programmed in Python, MIT license
#"Python job scheduling for humans. An in-process scheduler for periodic jobs that uses the
#builder pattern for configuration. Schedule lets you run Python functions periodically at
#predetermined intervals using a simple, human-friendly syntax."
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
#
#Version Info
#------------
VERSION_NUMBER = 3.01
VERSION_FILE_NAME = 'mbls301.py'
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

####################

#INTRODUCTION: Why Create this Program?
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
#Constants used for Developer Purposes
#-------------------------------------
CHECKPOINT_ON = False
DEVELOPER_USER = False
STOP_SCROLLING_BETWEEN_INPUTS = True
DEPENDENCIES = ['python36', 'win64']
#
#Constants used for Program Specifications and Resources
#-------------------------------------------------------
RESET_CODE_CREATE_NEW_MBSL = '9999'
INPUT_WORD_LENGTH = 9
#
#Constants used for MultThreading and Embedded Development and Execution
#-----------------------------------------------------------------------
EMBEDDED_MBLS_MULTITHREAD_INTERVALS_SECONDS = 2
EMBEDDED_MBLS_PAUSE_MULTITHREAD_INTERVALS_SECONDS = 0.02
#
#Large Data Variables used in the Program
#----------------------------------------
#pylint: disable=invalid-name
input_vector_history = ['start']
#pylint: enable=invalid-name
#TODO placement data variables
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
#Unit and Functional Testing Configuration
#-----------------------------------------
#We increase the probability of the code being reliable by unit testing and functional testing.
#In keeping with the philosophy above, we favor easy to use and to read testing frameworks (eg,
#Pytest-like) versus more complex ones (eg, PyUnit/unittest-like).
#>pip install pytest
#In file test_mblsxxxx.py put your test_functionxxxx, ie, your unit and other test functions.
#>pytest test_mblsxxxx.py
#Style Note: Consider keeping a commented copy of the test function in the mblsxxxx.py file beside
#the actual function -- seeing both in the same field of vision can help create better tests.
#New Programmer note: Be aware >pytest without a file will automatically find all sorts of files
#with a "_test" in the name (sometimes even body) that you didn't even know existed leading to
#strange errors. Pay attention to what directory tree Pytest is operating on if this happens.
#
PYTEST_UNIT_FILENAME = "test_mbls301.py"
PYTEST_FIXTURES = None
PYTEST_FUNCTIONAL1 = None
PYTEST_FUNCTIONAL2 = None
PYTEST_DEPLOYMENT = None
PYTEST_MANUALIZED = None
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

   Use external 'pylint' for style, external 'pytest' (with a test_xxxx file) for unit testing,
external 'mypy' for optional type checking, imported 'logging' for error and checkpoint logging (to
xxxxx.log), imported 'threading' and 'schedule' for embedded real-time concurrent
operation of the code, external 'pdb' (and/or other utilities) for debugging and code creation,
and GitHub for version control -- all straightforward and open source resources. We program to
tell a clear story and at the same time create an AGI.
'''


####################

#SLEEP/WAKE AND AUTONOMIC FUNCTIONS

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
def sleep_selection(sleep_phase: int) -> int:
    '''Allows setting of wake or sleep phase to another particular sleep phase.

    Sleep phase 1 - 3 -- normal sleep phases to accomplish various maintenance and energy
        conserving routines.
    Sleep phase 4 causes hibernation of the MBLS,ie, it (optionally) saves data and program exits.
    Sleep phase 5 is considered REM -- again a phase to accomplish various maintenance routines.
    Inspired by biology but goal is for MBLS to create a great AGI, not mimic the biological
        brain down to spiking neurons.

    Args:
        sleep_phase: what sleep phase to switch the MBLS into

    Returns:
        The sleep phase which the MBLS has now been switched to. (At present these phases can
            be 1,2,3,4 or 5.
        -1 if an error occurred.

    Raises:
        --

    '''
    if sleep_phase == 4:
        print('Deep Sleep Phase 4 - Hibernation rather than Maintenance/Energy Conservation')
        if 'y' in input('Would you like to leave the MBLS asleep and exit? (y/n): '):
            print('Hibernation treated as a system exit code -- program will stop running.')
            if 'y' in input('Would you like to save data? (y/n): '):
                save_data()
            print('System exit will now end program.')
            return_value = int(RESET_CODE_CREATE_NEW_MBSL)
        else:
            sleep_phase = 3
            print('No hibernation will occur. Sleep phase 4 converted to sleep '
                  'phase {}.'.format(sleep_phase))
    if sleep_phase in (1, 2, 3, 5):
        return_value = set_sleep_phase(sleep_phase)
    if sleep_phase not in (1, 2, 3, 4, 5):
        print('Coding: sleep phase parameter {} entered is not a sleep inducing '
              'value -- no wake to sleep transition occurs.'.format(sleep_phase))
        return_value = -1
    return return_value

'''
def test_sleep_selection():
    Unit testing (via Pytest) of sleep_selection(sleep_phase)
    
    result = xx.sleep_selection(0)
    assert result == -1
    
    result = xx.sleep_selection(1)
    assert result == 1
    
    result = xx.sleep_selection(5)
    assert result == 5
    
    result = xx.sleep_selection(6)
    assert result == -1
    '''

'''
	if    (random.randint(0,1) * phase)	> 0.5 :
		print ('MBLS is asleep now in sleep phase now.\n')
		return 1
	else:
		return 1
'''

def set_sleep_phase(sleep_phase):
    '''set the sleep phase
    '''
    print('MBLS is asleep now in sleep phase ', sleep_phase, '.\n')
    return sleep_phase

def save_data():
    '''save all data before exiting, therefore system not reset when restart
    '''
    print('All data has been saved')



####################

#LOWER-LEVEL ASSIST FUNCTIONS -- help other functions do their tasks
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
    global CHECKPOINT_ON
    if CHECKPOINT_ON is False:
        x_1 = input('Would you like to turn CHECKPOINT tracer on? (y/Y): ')
        if x_1 in ('y', 'Y'):
            CHECKPOINT_ON = True


def checkpoint_tracer(checkpoint_name, return_output):
    '''
    If CHECKPOINT_ON is True then any function or other part of program which
    contains this function, will display an execution of the checkpoint.
    (Useful at times for quick program execution checking.)
    (Use debugger for more extensive trace: python -m pdb *.py )
    '''
    if CHECKPOINT_ON:
        x_1 = input\
    ('Checkpoint: {}, Returns:{} -->ENTER....'.format(checkpoint_name, return_output))
        print('what happened to x -- check code', x_1)
    #todo check code transition from version 2

def stop_scrolling_check():
    '''The processing of an input, and other possible program executions,
    can generate many lines of text on the monitor screen. Thus there are
    'scrolling checks' where the user is asked to press any key so that the
    user has a chance to see what was just displayed on the terminal screen.
    However, to avoid having to do this keystroke, eg, with each new input cycle,
    user can enter a code, eg, 99, to stop this.'''
    global STOP_SCROLLING_BETWEEN_INPUTS
    if STOP_SCROLLING_BETWEEN_INPUTS:
        if input("\n---->NEW INPUT CYCLE -- Press any key to continue "
                 "('s' to stop scroll prompts)") == 's':
            print('Prompt turned off....')
            STOP_SCROLLING_BETWEEN_INPUTS = False


def update_input_vector_history(x_1):
    '''Keeps track of what input vectors
    sent into the MBLS.
    Useful for evaluation/debug use.
    '''
    global input_vector_history  #pylint: disable=invalid-name
    input_vector_history.append(x_1)


def print_input_vector_history():
    '''Prints what input vectors were
    sent into MBLS. No mods made here.
    Useful for evaluation/debug use.
    '''
    print(input_vector_history)


#def display_8_segments(aa) is imported from mbls_some_version2_low_level_functions as mbv2


#HIGHER-LEVEL ASSIST FUNCTIONS
#(further below are the MBLS Architecture functions)
#Lower-level assist functions do one or a few lower-level tasks, while
#the higer-level assist functions do more of function calling to
#to prevent too much code in the main code section
#
#
#pylint: disable=line-too-long
def start_simulation(message_x):
    '''consider if developer or user is using when start
    program
    '''
    if DEVELOPER_USER:
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
        print("Running in Normal User Mode (not Developer Mode)")

    mbll.welcome(message_x)
#pylint: enable=line-too-long

####################

#HIGH-LEVEL MBLS ARCHITECTURE VISIBLE FUNCTIONS
#Each of these functions corresponds to a high-level
#component of the MBLS Cognitive Architecture
#
#

#pylint: disable=too-many-statements
#pylint: disable=invalid-name
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
    global input_vector_history
    global STOP_SCROLLING_BETWEEN_INPUTS
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
            input_vector_history = l['restart']
            print_input_vector_history()
            x = input('Press ENTER to continue in program now (zero segment input will run).....')
            return l
        if x == '10':  #create random input
            print('\n---->Random input vector chosen and shown below:')
            l[0] = int(10)
            for t in range(1, 8+1):
                l[t] = random.randint(0, 1)
            update_input_vector_history(l)
            mbv2.display_8_segments(l)
            checkpoint_tracer(checkpoint_name, l)
            return l
        if x == '11':  #create full seg input
            print('\n---->Input with all segments chosen and shown below:')
            l[0] = int(11)
            for t in range(1, 8+1):
                l[t] = 1
            update_input_vector_history(l)
            mbv2.display_8_segments(l)
            checkpoint_tracer(checkpoint_name, l)
            return l
        if x == '33':  #display input hx
            print('\n---->History of Camera Input Vectors for this run :')
            print_input_vector_history()
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
    update_input_vector_history(l)
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
    #global input_vector_history -- if need for processing

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
#Main Program Code
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


def job():
    '''sample code to try out schedule
    '''
    print("I'm working....")


def main():
    '''    doc to do
    Some workspace for Howard here to figure out what want to do in this simulation of MBLS-3.0.
    -Ability to switch from 'see what's going on phase' to 'goal phase'
    -Actually same phase just different parameter of the 'goal' in the 'see what's going on phase'
    -ok... so first thing must do is sort of wake up MBLS robot and give a goal phase
    -ok.... let's do this.....

    '''

    print('Main Module of MBLS Program has started to run....\n')

    x_1 = sleep_selection(4)
    print('sleep phase is:', x_1)
    print('end of main')
    if x_1 == int(RESET_CODE_CREATE_NEW_MBSL):
        print('system exit next line')
        sys.exit()
    print('did not do system exit but program over here...')



#start_simulation('MBLS Simulation of Finding Lost Hiker in Forest')
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
#EMBEDDED SOFTWARE MANAGEMENT
#
#
#Goal of MBLS-3.0 Implementation is to use the Meaningful-Based Cognitive Architecture to
#control a Search-and-Rescue Robot, with the simulation of finding a lost hiker in a forest
#filled with a host of sensory noise and other irrelevant sensory signals.
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
    schedule.every(EMBEDDED_MBLS_MULTITHREAD_INTERVALS_SECONDS).seconds.do(run_mbls_thread, mbls_job1)
    schedule.every(EMBEDDED_MBLS_MULTITHREAD_INTERVALS_SECONDS + 4).seconds.do(run_mbls_thread, mbls_job2)
    #TODO see source code for schedule import re typing of parameter
    #pylint: enable=line-too-long

    while True:
        schedule.run_pending()
        time.sleep(EMBEDDED_MBLS_PAUSE_MULTITHREAD_INTERVALS_SECONDS)




if __name__ == '__main__':
    main()
else:
    embedded_main()
