#
#
#MBLS Simulation 
#Meaningful Based Learning System implementation of the Meaningful-Based Cognitive Architecture
#Language: Python 3.6  
#CPU, GPU, OS: Independent unless noted below
#
#Howard Schneider
#howard.schneider@gmail.com
#
#
####################

#TABLE OF CONTENTS
#Software is (or should be) written for humans, not computers. The source code below
#should tell a story to you, dear reader, just as any good book would. The language thus
#chosen is English-like Python (with a smattering of optimized C++ at the readable level).
#We do not program aimlessly to add more features or this or that -- we program to tell
#you a story.
#
#  Table of Contents
#  -----------------
#  0. Preface: Version and Technical Notes
#  1. Introduction: Why Create this Program?
#  2. Lower-Level Assist Functions
#     2a. Main Module Lower-Level Assist Functions
#     2b. Imported Module
#  3. High-Level MBLS Architecture Visible Functions
#     3a. Main Module High-Level MBLS Architecture Visible Functions
#     3b. Imported Module
#  4. Main Program Code
#  5. Embedded Software Management
#
#


####################

#PREFACE: Version and Technical Notes
#
#Version Info
#------------
VERSION_NUMBER = 3.01
VERSION_FILE_NAME = 'mbls301.py'
'''Migration history: 1.0 Pyth27 -> 2.0 Pyth36
	-> 2.0x Basic MBLS -> goal 2.1x MBLS 5000 HLNs -> work prematurely stopped for transition to
	->MBLS 3.0:
	-details of MBLS 3.0 on GitHub page
	-simulation to be tailored with capabilities to handle simple case of MBLS search-and-rescue robot
	-no longer focus on recognizing digits but general sensory inputs
	-ramp up to 50,000 HLNs
	-'''
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
Input_Vector_History=['start']
#
#Overview
#--------
#Scroll down to "MAIN PROGRAM CODE" section to see what program does at aa
#higher level, and then calls lower level functions.
#
#



####################

#LOWER-LEVEL ASSIST FUNCTIONS -- help other functions do their tasks 
#(further below are the MBLS Architecture functions)
#Lower-level assist functions do one or a few lower-level tasks,
#while the higher-level assist functions do more of function calling
#to prevent too much code in the main code section
#
#def welcome function put into module extra_fcns.py
#
def set_debugging_level():	
....
....

