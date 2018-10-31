#!/usr/bin/python3
#pylint: disable=too-many-lines
#justification: convenience during devp't of related code in one place; prod'n to module
#
#MBLS Simulation
#Meaningful Based Learning System implementation of the Meaningful-Based Cognitive Architecture
#Language: Python 3.6
#CPU, GPU, OS: Independent unless noted below
#
#Person(s) working on this project: Howard Schneider
#howard.schneider@gmail.com
#License: https://github.com/howard8888/MBLS-3.0
#Wiki, ReadMe and other info: https://github.com/howard8888/MBLS-3.0/wiki
#
#
#
####################

#TABLE OF CONTENTS
#Software is (or should be) written for humans, not computers. The source code below
#should tell a story to you, dear reader, just as any good book would. The language thus
#chosen is English-like Python. We do not program aimlessly to add more features or this or
#that -- we program to tell you a story (and in the process create an AGI).
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
To make sense of this program you need to have/acquire the following prerequisite knowledge-- all
doable and constituting a wonderful journey, for you dear reader. (Please ignore the parts you
have a background in.)

1. Be able to write some small Python programs.

You will not be able to read Python if you have never written the code. If no programming
experience, consider acquiring this skill. Allocate 200 hours. A myriad of online courses exist.

2. Understand at a basic level the landscape of data science and machine learning.

Again, you cannot just read this material -- you need to do some projects. You may have
this skill (no one is expert in every aspect of data science/ machine learning -- it is too
large), but again, if you don't, consider acquiring it. If you have a math background allocate
200 hours, if no math background (feel comfortable with matrices and partial derivatives) then
then allocate an extra 200 hours, ie, 400 hours in total. There are a myriad of available courses.

3. Have an introductory background in computer theory and cognitive science.

This is essential to understand why we are doing the things we are doing. The large question
is why even write this program? Why not just use one of those deep learning neural networks
that already exist and seem to do magical "AI" things?
To save time, consider working through the introductory book Algorithmics by David Harel, about
40 hours,and for cognitive science consider allocating 20 hours to reading reference papers listed
below. ("Reading papers" == making notes in a notebook so you learn the material.)

4. When you read the code please use one the many programming editors (use Windows? try Notepad++)
which will show different parts of the code in different colors.
'''
#pylint: disable=pointless-string-statement
#justification: in this first section of the 'code' there is much documentation and explanation
#
#
#Technical Notes
#---------------
'''
Technical notes placeholder
'''
#
#
#Programming Style
#-----------------
'''
The programming style is a very simple one in theory: "write for you, the reader, not the
computer."

For future (hopefully :) contributors to this project:

-We thus use an English-like language such as Python as much as possible.
-To avoid the need for C code in critical sections of the program, we attempt to ensure the code
will run under PyPy, and as well, optimize such critical sections.
-Instead of having a long style section/manual for this project, please download and install
Pylint. We use the arbitrary wisdom of Pylint to decide what style we should or shouldn't use,
plus the general (if not philosophical) rules below.
-We avoid showing the cleverness of the coder, eg, combining 7 actions in a single Python line
when multiple lines would make this more readable and understandable. We write for the person
who must read and understand the code; we don't write for ourselves nor for the computer. (With
the small exception of optimized code routines where necessary for essential functioning.)
-All the 'spaghetti code' of MBLS version 2 has been replaced (by virtue of necessity -- we are
simulating a search-and-rescue robot rather than the detection of numerical digits).
-We increase the reliability of the code by unit/functional testing. We favor easy to use/read
unit tests (eg, Pytest-like) versus more complex ones (eg, PyUnit/unittest-like).
-We catch the heisenbugs -- we create a 'verbose' mode in unit tests and as well do formal logging
of checkpoint events outside of unit tests in normal program running.
-We respect that humans have operating characteristics, to wit, the Ebbinghaus/Miller capacity of
the human mind to process information -- possibly 7 ± 2 items.
-We avoid short variable names but try to use names which allow the reader to follow what the
variable represents. (Hard to remember what a variable means after seeing a hundred other ones.)
-We avoid cargo cult programming -- no copying of code and no code that is not justified with
regards to this AGI project
-In keeping with the avoidance of cargo cult phenomena, we only use classes if really necessary
to ensure a data structure is not abused by other parts of the program. Otherwise we don't.
(Yikes!! But.... this is brain friendly code, not arbitrary OO friendly code). Again, with
apologies to the OO world, the class name is another piece of data for your brain to remember.
-Unfortunately, there is too much code to keep as a single 'Main' module and we do break up
the code into imported modules, so there are module names but we make as easy to remember.
-We keep functions as small as possible and will -- if appropriate -- break them up if they cover
too much new material (except verbose mode added for in/unit testing purposes).
-TODO comments are actually encouraged. (Pylint and some editors will track/flag TODO's.)
-Type annotations are 'encouraged' (but not mandatory as effectiveness uncertain).
At present mypy used (to install: pip install mypy-lang) (to run:eg, mypy mbls300.py)
-Ok to disable Pylint warnings but provide a justification and enable when appropriate
'''
#
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
#Reproducibility
#---------------
'''
The basis of the scientific method (of which just about all the scientific, medical, technological
wonders around you emerged from) is reproducibility -- the studies/experiments/work of others
must be able to be replicated by you (assuming appropriate knowledge and equipment, of course).
However, there is somewhat of a "reproducibility crisis" in science, particularly severe in the
cognitive sciences, eg, Science,2015 Aug 28;349(6251), "Estimating the reproducibility of
psychological science" -- a huge percentage of published work cannot be replicated. This issue
extends to neural networks and the whole field of artificial intelligence, eg, Science,2018 Feb 16
;359(6377):725-726, "Artificial intelligence faces reproducibility crisis."

Thus, in the MBLS project we make every effort to ensure that you, dear reader, can reproduce the
workings of the MBLS and reproduce our results. Without getting into the fringe areas of the
'Entscheidungsproblem' (eg, is the MBLS super-Turing because a person with paper and pen could not
reproduce certain operations of the MBLS(actually, according to CT thesis this should not occur)),
while results may vary from run to run, from overall simulation to simulation, we endeavor to show
the consistencies in patterns and findings. Most important, is that you can reproduce the MBLS and
you can reproduce these consistencies.
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
safeguard for one, and and for two, with apologies for the irony, at this point in the development
of the MBLS we don't have the resources to spend more effort on this issue.)

With regard to the potential for superintelligence, an honest answer would be "yes" -- if the
number of working memories in the MBLS is increased and the quasi-instruction set that
manipulates vectors in and to and from the working memories is made more sophisticated,
and the algorithmic section is ramped up, then yes, a superintelligence of sorts should
emerge. But, this is not the goal of the MBLS and no work is planned in this area.
'''
#
#
#
#Flags used for Development Purposes
#-----------------------------------
MEMORY_CHECKING_ON = True
TEST_VERBOSITY = True
FORCE_EMBEDDED_MAIN = False
CHECKPOINT_ON = False
DEVELOPER_USER = True
STOP_SCROLLING_BETWEEN_INPUTS = True
#
#
#pylint: disable=wrong-import-position
#pylint: disable=unused-import
#justification: better documentation of dependencies
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
from io import StringIO
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
#
import numpy as np
#Justification note: Awesome Python/LibHunt: 9.6 popularity, 9.8 activity, >8000 stars
#code quality ?? (L1 patchwork does not make sense), programmed in C, BSD license
#"fundamental package needed for scientific computing with Python...."
#
import schedule
#Justification note: Awesome Python/LibHunt: 8.8 popularity, 4.8 activity, >5000 stars
#code quality L4 (lumnify scale), programmed in Python, MIT license
#"Python job scheduling for humans. An in-process scheduler for periodic jobs that uses the
#builder pattern for configuration. Schedule lets you run Python functions periodically at
#predetermined intervals using a simple, human-friendly syntax."
#
if MEMORY_CHECKING_ON:
    from pympler import summary, muppy
#Justification note: No Awesome Python/Libhunt rating; GitHub - 15 contributors, 376 stars,
#programmed in Python , Apache License2.0
#"Development tool to measure, monitor and analyze the memory behavior of Python objects in
#a running Python application."
#Note: At present, normally not imported except for occasional development work.
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
#pylint: enable=wrong-import-position
#pylint: enable=unused-import
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
#               Specific exceptions always are better than general 'except' but for convenience
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
#
#Version Info
#------------
VERSION_NUMBER = 3.02
VERSION_FILE_NAME = 'mbls302.py'
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
#
#
#Global Variables
#----------------
#pylint: disable=invalid-name
#justification: separate justification for every global variable used
#
in_vecs = []
#Description: main data structure of MBLS system
#Justification: development convenience, avoid emergence of complexity of class implement'n,
#Warnings: survey memory usage, survey for potential side effects as use in devp't
#Name change: in previous software versions "input_vector_history"
#
#New Programmer note: "If a variable is assigned a value anywhere within the function’s body, it’s
#  assumed to be a local unless explicitly declared as global." -- python.org Programming FAQ
#pylint: enable=invalid-name
#
#
#Python Installation & Platform Specifications
#---------------------------------------------
#
#
#Note: This code block will run before main() or <alternative>_main() listed at bottom
if DEVELOPER_USER:
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
            print("   Verify memory -- create 10,000 x 10,000 Numpy matrix ....")
            print("   Interim:100x100")
            print(np.zeros((100, 100)))
        print("Ok.... basic infrastructure in place for program to run....\n\n")
    except:
        print('Exception occurred in retrieving platform specifications.')
#
#
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
#pylint: enable=pointless-string-statement


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
#pylint: disable=undefined-variable
#justification: results from blocking pympler import
def memory_var_usage()->bool:
    '''Uses pympler third-party dependency to: "to measure, monitor and analyze
    the memory behavior of Python objects in a running Python application."
        Useful dev tool as MBLS data structure grows very large.
    Args:
        --
    Style note:
        -No associated unit test
        -Usually pympler is only imported and used for occasional dev work
    Returns:
        True/ False depending on successful run
    Raises:
        try/except
'''
    try:
        variable_memory = summary.summarize(muppy.get_objects())
        print('\n'.join(summary.format_(variable_memory)))
        return True
    except:
        print('Pympler not active. No memory map printed out.')
        return False
#pylint:enable=undefined-variable


def memory_var_usage_test()-> bool:
    ''' Unit testing of above function (with a "_test" suffix added) (suffix allows ordering)
        -This function, with appropriate imported file prefixes to variables (since this program
        must be imported) is stored in the Pytest testing file specified by PYTEST_UNIT_FILENAME.
        -It can also used for testing directly within this program.
        Args:
            --
        Style note:
        -We stylistically allow keeping the unit test functions close to the actual functions, so
        both can be examined together, encouraging the developer to create the most useful tests.
        Returns:
            True if make it to end of test and no try/except error occurs
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
        Style note: -For development convenience in_vecs kept as global for moment
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
        Style note: -The 'with' statement will automatically close the file after each code block
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
        Style note: -The 'with' statement will automatically close the file after each code block
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
        Style note:
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
        in_vecs = list(restore_later_in_vecs)
        restore_later_in_vecs.clear()
        if verbose and sys.getsizeof(in_vecs) < TOO_MANY_BYTES_TO_DISPLAY:
            print('in_vecs after test over: ', in_vecs)
        logging.info('&END UNIT TEST: in_vecs_load/save/erase(): FAILURE\n')
        print('&END UNIT TEST: in_vecs_load/save/erase(): FAILURE\n')
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
    Style note: (for this function near top of program): Written so human mind can easily follow
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
            print('Hibernation cancelled. New sleep phase is {}.'.format(sleep_phase))
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
        Style note:
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
        Style note:
            --
        Returns:
            0..9 :The sleep/wake/debug phase MBLS switched to
        Raises:
            --
    '''
    if sleep_phase in [1, 2, 3, 4, 5]:
        print('MBLS is asleep now in sleep phase ', sleep_phase, '.')
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
