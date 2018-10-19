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
#  0.  Preface: Version and Technical Notes
#  1.  Introduction: Why Create this Program?
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


####################

#0. PREFACE: Version and Technical Notes
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
(To avoid the need for C code in critical sections of the program, we attempt to ensure the code
 will run under PyPy, and as well, optimize such critical sections.)
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
import pickle
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
#Managing & Storing Large Data Variables used in the Program
#-----------------------------------------------------------
#pylint: disable=invalid-name
input_vector_history = ['debug note: not loaded yet', 'style note: global for convenience for now']
#pylint: enable=invalid-name
INPUT_VECTOR_HISTORY_FILE = 'input_vector_history.pk1'
INIATION_VALUE = 'start'
END_VALUE = 'end'
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
#In keeping with the philosophy above, we favor easy to use and to read testing frameworks (eg,
#Pytest-like) versus more complex ones (eg, PyUnit/unittest-like).
#-- >pip install pytest
#-- 'test functions' with prefix 'test_' (eg, test_abcxxx) go into file PYTEST_UNIT_FILENAME
#-- >pytest test_mblsxxxx.py    (or whatever filename in PYTEST_UNIT_FILENAME is)
#Style Note: Ok to keep a commented copy of the test function (or a working copy to use via
#in-program simulation of pytest)beside the actual function -- helps you create better tests.
#New Programmer note: Be aware >pytest without a file will automatically find all sorts of files
#with "_test" in name. Pay attention to what directory tree Pytest is operating on if this happens.
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
def mbls_data(item_to_process: str, verbose: int = 0)-> None:
    ''' Load, store and possibly modify "input_vector_history" mbls data variable
            input_vector_history is a list holding vector info about MBLS HLN connections.
            INPUT_VECTOR_HISTORY_FILE -- pickled file where store variable
            INIATION_VALUE -- first prefix value add onto list (eg, 'start' or whatever value is)
            END_VALUE -- last value add onto list (eg, 'end' or whatever value is)
        Args:
            verbose:
                optional with default of 0
                if non-zero value then function runs in verbose mode with prints of actions
                also will prompt user to enter another value to store in variable saving
            item_to_process:
                'load' -- usually on initiation load pickled file of data into variable
                  (if first time and file does not exist, then it will be automatically created)
                'save' -- save all data before exiting, therefore system not reset when restart
                'erase' -- delete the file, therefore new mbls when restart system
        Style note: The 'with' statement will automatically close the file after
                    each block of code.
                    For development convenience input_vector_history kept as global for moment
        Returns:
        Raises:
    '''
    #pylint: disable=invalid-name
    global input_vector_history
    #pylint: enable=invalid-name
    if verbose:
        print('*start of mbls_data fcn: input_vector_history is: ', input_vector_history)

    if item_to_process == 'load':
        if not os.path.isfile(INPUT_VECTOR_HISTORY_FILE):
            print("New MBLS detected -- will create file to store data.")
            with open(INPUT_VECTOR_HISTORY_FILE, 'wb') as mbls_open_file1:
                pickle.dump([INIATION_VALUE], mbls_open_file1)
        with open(INPUT_VECTOR_HISTORY_FILE, 'rb') as mbls_open_file1:
            print("Successfully opened MBLS's data structure from storage.")
            input_vector_history = pickle.load(mbls_open_file1)
            if verbose:
                print('*leaving mbls_data "load": input_vector_history is: ', input_vector_history)

    if item_to_process == 'save':
        input_vector_history.append(END_VALUE)
        print('verbose =', verbose)
        if verbose:
            input_vector_history.append(input('*enter another test value to append'))
        with open(INPUT_VECTOR_HISTORY_FILE, 'wb') as mbls_open_file1:
            pickle.dump(input_vector_history, mbls_open_file1)
            print('All MBLS data saved to storage ({}) .'.format(INPUT_VECTOR_HISTORY_FILE))
            if verbose:
                print('*leaving mbls_data "save": input_vector_history is: ', input_vector_history)

    if item_to_process == 'erase':
        if os.path.isfile(INPUT_VECTOR_HISTORY_FILE):
            os.remove(INPUT_VECTOR_HISTORY_FILE)
            print('All MBLS data has been erased. When restart program will act as new MBLS.')
        else:
            print('Coding error: Cannot erase file that does not exist')
        if verbose:
            print('*leaving mbls_data "erase": input_vector_history is: ', input_vector_history)
            print('*note that input_vector_history may or may not be erased at this point(depends')
            print('*source code version/wishes) but if make new mbls it gets reset there')


#pylint: disable=too-many-statements
def test_mbls_data(verbose: int = 0)-> bool:
    ''' Unit testing of above function (with a "test_" prefix added)
        -This function, with appropriate imported file prefixes to variables (since this program
        must be imported) is stored in the Pytest testing file specified by PYTEST_UNIT_FILENAME.
        -It can also used for testing directly within this program via Pytest-like feature in
        development mode of the MBLS code.
        Args:
            verbose:
                optional with default of 0
                passed to mbls_data function which causes:
                    if non-zero value then function runs in verbose mode with prints of actions
                    also will prompt user to enter another value to store in variable saving
                within this function directly:
                    verbose mode of some prints of actions
                    prompts user to optionally check directory for files created
        Style note:
        -We stylistically allow keeping the unit test functions close to the actual functions, so
        both can be examined together, encouraging the developer to create the most useful tests.
        -The 'non-verbose' mode of this unit test is still quite verbose, albeit just print's
        which can be run in an automated fashion. We do this because so many places for system
        to fail (and trigger assert error) -- in opening and writing to storage, in the global
        variable scope changing inadvertently, etc -- easier for you to debug with the audit
        trail being printed out.
        -Warning: Do NOT execute as part of normal program -- actual function is being called and
        will have side effects on program. Run in external file or if within in special dev mode.
        Returns:
            True if make it to end of test and no assert error occurs
        Raises:
            -Oct 18 -- ok to run internally -- we have made safe (will not overwrite real data)
    '''
    print('\nSTART UNIT TEST: mbls_data()')
    print('\nRunning unit test to verify correct operation of mbls_data() function')
    print('---------------------------------------------------------------------\n')
    if verbose:
        print('Running in verbose mode which will require prompts from user.')
        print('* from mbls_data verbosity, # from test function verbosity\n')
    print('Changing global constants....restart code before use in non-testing mode\n')
    #pylint: disable=invalid-name
    global input_vector_history
    #pylint: enable=invalid-name
    global INPUT_VECTOR_HISTORY_FILE
    restore_value = INPUT_VECTOR_HISTORY_FILE
    INPUT_VECTOR_HISTORY_FILE = 'tester1.pkl'

    print('Check to see if erasing non-existant data (pkl) file causes problem.')
    print('Expect to see "coding error message" - this is not error but source message - ignore')
    mbls_data('erase', verbose)
    mbls_data('erase', verbose)

    print('Now should open new pickled file "tester1.pkl" and store init value in it')
    print('Value of input_vector_history: ', input_vector_history)
    mbls_data('load', verbose)
    print('Value of input_vector_history: ', input_vector_history)
    if verbose:
        input('#Chance for you to see which *.pkl files exist. Then click ENTER to continue.')
    mbls_data('save', verbose)
    print('Value of input_vector_history: ', input_vector_history)
    a_1 = input_vector_history
    print('Just saved end value to file.... let us reload and what it shows...')
    input_vector_history = ['erased values and this is a new value']
    print('First we will change input_vector_history to :', input_vector_history)
    print('Ok....now we will go ahead and load from file....')
    mbls_data('load', verbose)
    print('Value of input_vector_history: ', input_vector_history)
    b_1 = input_vector_history
    assert a_1 == b_1
    logging.info('passed first assert test : test_mbls_data')

    mbls_data('save', verbose)
    print('Value of input_vector_history: ', input_vector_history)
    mbls_data('load', verbose)
    print('Value of input_vector_history: ', input_vector_history)
    if verbose:
        input('#Chance for you to see which *.pkl files exist. Then click ENTER to continue.')
    mbls_data('save', verbose)
    print('Value of input_vector_history: ', input_vector_history)
    mbls_data('load', verbose)
    c_1 = input_vector_history
    print('Value of input_vector_history: ', input_vector_history)
    input_vector_history = ['erased values and this is a new value']
    print('Ok....let us change input_vector_history to :', input_vector_history)
    print('Ok....now we will go ahead and load from file....')
    mbls_data('load', verbose)
    print('Value of input_vector_history: ', input_vector_history)
    d_1 = input_vector_history
    assert c_1 == d_1
    logging.info('passed second assert test : test_mbls_data')

    print('ok now let us go do cleanup')
    mbls_data('erase', verbose)
    INPUT_VECTOR_HISTORY_FILE = restore_value
    print('Also, you really should restart before use for real MBLS work but in case you')
    print('do not, INPUT_VECTOR_HISTORY_FILE restored to : ', INPUT_VECTOR_HISTORY_FILE)
    print('nb. input_vector_history *variable* at this time is:', input_vector_history)
    print('(if you do another "load" it will be replaced by contents from file)')
    logging.info('UNIT TEST OVER : test_mbls_data')
    print('UNIT TEST OVER : test_mbls_data\n')
    return True
#pylint: enable=too-many-statements


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
    Returns:
        0..9 :The sleep/wake/debug phase MBLS now switched to
        RESET_CODE_CREATE_NEW_MBSL: if hibernation == system exit(asked if want to save data)
        -1: An error occurred
    Raises:
        --
    Style note: (for this function near top of program): Written so human mind can easily follow
    assumptions and logic. While, for the sake of example, using a dictionary of functions to
    emulate a switch/case structure, instead of the if/then's below would operate faster (ie,
    jump to dict item rather than go through a sequence of if/then's, this is immaterial in this
    section of the code. Except in critical areas of the code, we write for the reader,
    not the computer.
    '''
    logging.info(' '.join(['-in sleep_selection, sleep_phase = ', str(sleep_phase)]))
    all_allowed_sleep_values = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    hibernation_value = 4
    avoid_hibernation_conversion_value = 3
    run_internal_tests_value = 9

    if sleep_phase == run_internal_tests_value:
        print('Triggered run of internal test. Verbose == 0 ')
        unit_testing_functions_that_can_be_called_within_the_code(0)
        sleep_phase = hibernation_value
    if sleep_phase == hibernation_value:
        print('Awake/Sleep Phase switching to "Hibernation/reset"')
        if 'y' in input('Would you like to leave the MBLS asleep and exit? (y/n): '):
            print('Hibernation treated as a system exit code -- program will stop running.')
            if 'y' in input('Would you like to save data? (y/n): '):
                logging.info('call to save data before system exit')
                mbls_data('save')
            else:
                mbls_data('erase')
            print('Thank you....system exit underway....')
            logging.info('hibernation sleep phase parameter, return value will trigger sys exit')
            return_value = int(RESET_CODE_CREATE_NEW_MBSL)
        else:
            sleep_phase = avoid_hibernation_conversion_value
            print('Hibernation cancelled. New sleep phase is {}.'.format(sleep_phase))
    if sleep_phase in all_allowed_sleep_values and sleep_phase != hibernation_value:
        return_value = set_sleep_phase(sleep_phase)
    if sleep_phase not in all_allowed_sleep_values:
        print('Coding error: sleep_phase "{}" not valid. No effect.'.format(sleep_phase))
        return_value = -1
        logging.info('inappropriate sleep phase parameter detected....')
    logging.info(' '.join(['leaving sleep_selection, return value = ', str(return_value)]))
    return return_value


def test_sleep_selection(verbose: int = 0)-> bool:
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
        Style note:
        -We stylistically allow keeping the unit test functions close to the actual functions, so
        both can be examined together, encouraging the developer to create the most useful tests.
        Returns:
        Raises:
            -
    '''
    print('START UNIT TEST : test_sleep_selection\n')
    if verbose:
        print('Running in verbose mode which will require prompts from user.')
        print('# from test function verbosity\n')
    for phase in [(-888, -1), (0, 0,), (1, 1), (2, 2), (3, 3), (4, 3),
                  (5, 5), (6, 6), (7, 7), (8, 8), (55, -1)]:
        if phase[0] == 4:
            if verbose:
                print("#Interactive input required: !!Do NOT opt to exit program!!")
                assert sleep_selection(phase[0]) == phase[1]
    logging.info('just completed unit tests for sleep_selection')
    print('UNIT TEST OVER : test_sleep_selection\n')
    return True


def set_sleep_phase(sleep_phase: int)-> int:
    '''set the sleep phase
    '''
    if sleep_phase in [1, 2, 3, 4, 5]:
        print('MBLS is asleep now in sleep phase ', sleep_phase, '.\n')
    elif sleep_phase == 9:
        print('Sleep code 9 will trigger internal testing now.')
    elif sleep_phase in [6, 7, 8]:
        print('Sleep code 6, 7 or 8 will trigger special debug states.')
    elif sleep_phase == 0:
        print('MBLS is now in awake state.')
    else:
        print('MBLS in other awake/sleep/maintenance/debug state.')
    return sleep_phase
....
....