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
-Every piece of code is unit tested or equivalently tested. Before testing we consider what
side effects a function could have, and we try to test reasonably for these. We try to test
sufficiently so that we don't litter our code with Exceptions and decrease readability and
possibly introduce errors in flow control. However, where necessary, of course error control
code is used.
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
import unittest
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
#(Win: use command line, not PowerShell. Can't use venv in PS until MBLS uses Python 3.8+.)
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
....
....