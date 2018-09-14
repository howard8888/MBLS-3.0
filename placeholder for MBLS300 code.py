#
#
#MBLS Simulation
#Meaningful Based Learning System implementation of the Meaningful-Based Cognitive Architecture
#Language: Python 3.6
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
#you a story.sleep
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
#Version Info
#------------
VERSION_NUMBER = 3.01
VERSION_FILE_NAME = 'mbls301.py'
'''
Migration history: 1.0 Pyth27 -> 2.0 Pyth36
	-> 2.0x Basic MBLS -> goal 2.1x MBLS 5000 HLNs -> work prematurely stopped for transition to
	->MBLS 3.0:
	-details of MBLS 3.0 on GitHub page
	-simulation to be tailored with capabilities to handle simple case of MBLS search-and-rescue robot
	-no longer focus on recognizing digits but general sensory inputs
	-ramp up to 50,000 HLNs
	'''
#Prerequisite Knowledge
#----------------------
'''To make sense of this program you need have/acquire the following prerequisite knowledge -- all doable
and constituting a wonderful journey, for you dear reader.
1. Be able to write some small Python programs. You will not be able to read Python if you have never 
written the code. You probably already have this skill, or a skill in a related language, so not a big
issue. However, if you don't, consider acquiring this skill. Allocate 200 hours to doing so. There are a 
myriad of available courses.
2. Understand at a basic level the landscape of data science and machine learning. Again, you cannot just
read this material -- you need to do some projects. You probably have this skill (no one is expert in 
every aspect of data science/ machine learning -- it is too large), but again, if you don't, consider
acquiring this skill. If you have a math background allocate 200 hours to doing so, if no math background
(feel comfortable with matrices and partial derivatives) then allocate an extra 200 hours, ie, 400 hours
in total. Again, if you have the motivation and time, very doable with a myriad of available courses.
3. Have an introductory background in computer theory and cognitive science. This is essential to understand
why we are doing the things we are doing. The large question is why even write this program? Why not just
use one of those deep learning neural networks that already exist and seem to do magical "AI" things?
There are some online courses that conver these subjects, but to save time, consider for computer theory
working through the book Algorithmics by David Harel, about 40 hours of your time (this is introductory and
you may already have this knowledge) and for cognitive science consider allocating 20 hours to reading 
papers in the references below -- a great way to acquire this knowledge. ("Reading papers" -- you really 
should make notes in a notebook so that you will better acquire this information if you are learning it on
your own outside of a classroom.)
4. Read some of the main references described below in the Introduction section.
'''
#Technical Notes
#---------------
'''
'''
#
#Programming Style
#-----------------
#The programming style is a very simple one in theory: "write for you, the reader, not the computer."
#-We thus use an English-like language such as Python as much as possible. We thus avoid showing the 
#cleverness of the coder by combining 7 actions in a single line when multiple lines would make this
#more readable and understandable. 
#-All the 'spaghetti code' of version 2 has been replaced (by virtue of necessity -- we are simulating a
#search-and-rescue robot rather than the detection of numerical digits) or refactored to meet current style.
#-Every piece of code is unit tested or equivalently tested. Before testing we consider what side effects
#a function could have, and we try to test reasonably for these.
#-We avoid short variable names but try to use names which allow you to follow what the variable represents. 
#(Hard to remember what a variable means after seeing a hundred other variables.)
#-We only use classes if really necessary to ensure a data structure is not abused by other parts of the
#program. Otherwise we don't. Again, with apologies to the OO community, the class name is another piece of 
#data for your brain to remember as you read through the code.
#-Unfortunately, there is too much code to keep as a single 'Main' module and we do break up the code into
#imported modules, so there is a class-like requirement (albeit without the class properties) to
#remember the module name to remember, but we have tried to make this as gentle as possible for the 
#human brain. (For development we import the rather explicit but long module 
#names as a shortened abbreviation -- if we start accumulating too many modules, ie,
#at the lower Ebbinghaus number of the human mind, we will replace the abbreviations with the full module name.)
#-We keep functions as small as possible and will break them up if they cover too much
#new material. We try to follow Martin's "Agile Software Development"/"Clean Coder" principle of functions
#doing only one thing. (Although there would be too many functions in the code if we stuck to "one", but the 
#principle is nonetheless respected.)
#
#
#Biological Inspiration of Cognitive Architecture and Cognitive Functioning
#--------------------------------------------------------------------------
#With pride the MBLS implementation of the Meaningful-Based Cognitive Architecture is inspired by
#biological neurological cognitive architectures and biological cognitive functioning. It is NOT the
#goal of the MBLS to implement a simulation of a biological nervous system at a spiking-neuron level.
#Actually it is NOT the intention of the MBLS to simulate a biological nervous system at a higher 
#level either. Rather, we are inspired by biology, and use the valuable design nature has provided, 
#to create the best possible artificial cognitive system. In doing so, however, there may be useful 
#reflections that allow us to better understand the mammalian nervous system, albeit at the 
#mesoscopic level and above. Again, we are inspired by biology, and our simulations may help increase 
#the understanding the latter, but we design and program to create the best possible artificial 
#cognitive functioning == best possible AGI (artificial general intelligence) == 
#best possible HLAI (human level artificial intelligence)
#
#
#Safety
#------
#Safety seems irrelevant at this early point of design and implementation of the MBLS, but such is the
#argument in the AI and AGI communities that for systems which grow to become superintelligence 
#systems it will be argued at their start that it is too early to spend time on safety issues (ie, safety 
#in preventing the system from becoming some unproven superintelligent system that would exponentially
#improve itself and then be a danger to humankind). However, we note one important difference of the 
#MBLS versus other AGI potential systems -- the MBLS not only has an intuitive physics 
#and intuitive psychology but also has among its intuitive systems an intuitive human culture system. 
#Just as it knows at a very basic level that objects are permanent, for example, 
#it knows at a very basic level its purpose is to benefit the humans it interacts with.
#(There are many arguments in the AGI community why this or that safeguard is not adequate, and such 
#arguments could also be applied to the intuitive human culture of the MBLS, but we argue in return this is 
#a very strong safeguard for one, and and for two, at this point in the development of the MBLS we don't 
#have the resources to spend more effort on this issue.)
#
#With regard to the potential for superintelligence, an honest answer would be "yes" -- if the number of 
#working memories in the MBLS is increased and the quasi-instruction set that manipulates vectors in and to 
#and from the working memories is made more sophisticated, and the algorithmic section is ramped up, 
#then yes, a superintelligence of sorts should emerge. But, this is not the goal of the MBLS and 
#no work is planned in this area.
#
#
#Import MBLS Code Modules
#------------------------
#(MBLS program is much more readable by putting dependent functions into external modules which are imported 
#here. As well, program loads faster by doing so.)
#(Make sure these files are in the same directory where your Python program is running or else is in a path 
#which Python can follow to find these files.)
import mbls3_low_level_functions as mbll
import mbls_some_version2_low_level_functions as mbv2
#
#
#Import Python3 Standard Library Modules
#--------------------------------------
#(No need to install anything -- Python will automatically import.)
import random
import sys  #Warning: DEPENDENCIES win64
import os.path #Warning: DEPENDENCIES win64
import platform
import time
from distutils.core import setup, Extension
#
#
#Import Non-Standard Library Modules
#----------------------------------
#(Many of these such as, eg, numpy are widely used and are easy to find, often included with many Python
#distributions, eg, Anaconda; all others are easily installed via PyPi.org Python Package Index -- simply copy
#and run at the command line the 'pip' info from PyPi and the module will be installed on your computer.)
#(If not in PyPi then package and installation information will be available on MBLS GitHub page.)
import numpy as np
#
#


####################

#INTRODUCTION: Why Create this Program?
#
#Introduction
#------------
'''At the time of this writing, despite the human-like performance of artificial neural networks (ANNs) 
in sensory processing and reinforcement learning (Goodfellow, Bengio and Courville, 2016; Mnih, 
Kavukcuoglu, Silver, et al., 2015), such neural networks, trained with a very small quantity of examples, 
cannot causally make sense of their environment or information at the level a four-year old child can 
(Gopnik, Glymour, Sobel et al., 2004; Waismeyer, Meltzoff, and Gopnik, 2015).  
Recent successful work by Graves, Wayne, Reynolds and colleagues (2016) helps to narrow the neural-symbolic 
gap. Their model involves an ANN which can read and write to an external memory, i.e., a hybrid system. 
However, like the human brain, the meaningful-based learning system (MBLS), introduced below, can perform 
the sensory processing associated with ANNs and the efficient symbolic logic associated with human 
cognition, without the use of an external memory, i.e., it is not a physically hybrid system. 

Abstract from 2018 Annual International Conference on Biologically Inspired Cognitive Architectures
Meaningful-Based Cognitive Architecture by Howard Schneider:

"An overview is given of the cognitive architecture of the biologically inspired meaningful-based learning 
system (MBLS). The basic element of the MBLS is a reconfigurable Hopfield-like network (HLN) which can rapidly 
connect to other HLNs depending on the level of abstraction which yields a practical maximal “meaningfulness,” 
defined as the reciprocal of the Shannon entropy of the HLNs. Without any external memory the MBLS synergistically 
processes external data (and internal data – “thoughts”) with sensory processing abilities found in neural networks 
and some of the symbolic logical abilities found in human cognition. In practical applications the MBLS offers 
near-simultaneous pattern recognition and comprehension. In modeling the development of psychotic disorders in humans, 
the MBLS predicts that in many patients the etiology stems from the fragility of the working memory and the 
integration of additional reasoning mechanisms during adolescence."
''' 
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
#Large Data Variables used in the Program
#----------------------------------------
Input_Vector_History = ['start']
#
#Overview
#--------
#Scroll down to "MAIN PROGRAM CODE" section to see what program does at aa
#higher level, and then calls lower level functions.
#
#TL;DR
#-----
'''This code is a simulation of a learning system that tries to combine neural network-like learning
(eg, the way a deep learning network recognizes a photograph) with symbolic-like learning 
(eg, if X=2 and Y=3 then X + Y should be 5). Scroll down to 'Main Program' section to see what the 
code is doing.
'''


####################

#SLEEP/WAKE AND AUTONOMIC FUNCTIONS 

#The sleep/wake and autonomic functions are inspired by the analagous biological functions, but their purpose
#is not to mimic nature but provide a useful level of very high overall control of the MBLS with regard to the 
#sleep/wake functions, and to provide "stimulus->action"=="reflex" == "reptilian-like neurological functioning" 
#ie, no cortical-like functioning but more of stimulus-action functioning although the strong caveat is made
#here that reptiles and birds and have cortical-like portions of their pallium and the stimulus->action effect 
#is actually much more involved and processed than say stimulus->action in a worm. Thus, really the autonomic
#functions should be thought of as providing invertebrate-like stimulus->action processing, or if the case of
#mammals is considered, basic reflexes and basic autonomic processing.
#function but stimulat
#
#This section will be divided in future as number of functions grow into separate sleep/wake section, separate
#reflex autonomic function section (useful for very fast decisions) and more processed autonomic function section.
#
#
def sleep(phase):
	'''
	Enter sleep phase 1 - 3 -- normal sleep phases to accomplish various maintenance and energy conserving routines.
	Sleep phase 4 causes hibernation of the MBLS, ie, it saves data and program exits.
	Sleep phase 5 is considered REM -- again a phase to accomplish various maintenance routines.
	Inspired by biology but goal is for MBLS to create a great AGI, not mimic the biological brain down to spiking neurons.
	'''
	#process hibernation sleep phase request	
	if phase == 4:
		print('MBLS has been put in a deep sleep phase 4 which we currently consider a hibernation rather than maintenance or energy-conserving state.')
		if 'y' in input('Would you like to leave the MBLS asleep and exit? (y/n): '):
			print('\n---->Hibernation is currently interpreted as a system exit code -- program will stop execution.')
			if 'y' in input('Would you like to save data? (Reset operation will use this saved data)(y/n): '):
				save_data()
			print('System exit will now end program.')
			return RESET_CODE_CREATE_NEW_MBSL
		else:
			phase = 3
			print('No hibernation will occur. Sleep phase 4 converted to sleep phase {}.'.format(phase))

	#process other sleep phase requests
	if phase not in (1, 2, 3, 5): 
		print('Possible coding error: sleep phase parameter {} entered is not a sleep inducing value -- no wake to sleep transition occurs.'.format(phase))
		return -1	
	else:
		return set_sleep_phase(phase)
		
