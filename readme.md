# MBLS-3.0
# Version 3.0 Meaningful Based Learning System (MBLS) #

The 'Meaningful Based Learning System' (**MBLS**) is an implementation of the **Meaningful Based Cognitive Architecture**.

## What Project Does ##

The MBLS creates an AGI (artificial general intelligence) via synergistically integrating the sensory processing abilities found in neural networks with many of the symbolic logical abilities found in human cognition. The basic unit of the MBLS is a reconfigurable Hopfield-like Network unit (HLN). HLNs can reconfigure with each other in an attempt to achieve a practical maximal 'meaningfulness' (defined as the reciprocal of the Shannon entropy of the HLNs). A portion of the HLNs are configured for hierarchical sensory processing, others as causal memory (including holding of multiple world views), and others organized as logic/working memory larger units which can process vectors from other parts of the MBLS, in accordance with intuitive physics, intuitive psychology, intuitive scheduling and intuitive world views stored in the preconfigured (instinctual) core goals module. 

See below for key concepts that I wish to demonstrate in MBLS-3.

![image of child from slidedeck](https://github.com/howard8888/MBLS-3.0/blob/master/image_from_slidedeck_2.jpg)



## How to Install & Dev Environment ##
This is a Python-based project. Installation is intended to be very straightforward.

At the time of this writing, the code uses Python 3.6 with modules imported from the Standard Library or PyPI. 

For development no specific IDE or other tools are required.

Installation and dev details are given at the beginning of the source code.


## Licensing ##
All code of the MBLS-3.0 Project is open source, as per the license on this GitHub page. As well, all modules imported into the code are open source, as per similar open source licenses.


## Papers describing the Meaningful-Based Cognitive Architecture and the MBLS: ##

(A prepublication of the Procedia article is on this GitHub page for download.)

Schneider, H., Non-Hybrid Meaningful-Based Learning System Using a Configurable Network of Neural Networks. Proceedings of the 2018 International Conference on Artificial Intelligence pp 96-102; Aug 2018.

Schneider, H., Meaningful-Based Cognitive Architecture. Proceedings of the 2018 Annual International Conference on Biologically Inspired Architectures (BICA 2018) held on August 22, 2018 as part of the Joint Multi-Conference on Human-Level Artificial Intelligence (HLA-18).

[https://www.respekt.cz/spolecnost/muze-pocitac-trpet-psychozou](https://www.respekt.cz/spolecnost/muze-pocitac-trpet-psychozou "<hyperlink to article>")

Schneider, H., Meaningful-Based Cognitive Architecture. Procedia Computer Science, 9th Annual International Conference on Biologically Inspired Cognitive Architectures, BICA 2018,edited by Samsonovich, A.V., in press.

**PowerPoint slides** (in PDF format) of my presentation at the BICA section of the HLAI-18 in Prague, Czech Republic can be downloaded from this GitHub page, and give an idea of the key concepts behind the Meaningful-Based Cognitive Architecture and the MBLS implementation.

**Excerpts of paper**:

2018 Annual International Conference on Biologically Inspired Cognitive Architectures

Meaningful-Based Cognitive Architecture

Howard Schneider

Sheppard Clinic North, Toronto, ON, Canada

[howard.schneider@gmail.com](howard.schneider@gmail.com)
> 
> Abstract
> 
> An overview is given of the cognitive architecture of the biologically inspired meaningful-based learning system (MBLS). The basic element of the MBLS is a reconfigurable Hopfield-like network (HLN) which can rapidly connect to other HLNs depending on the level of abstraction which yields a practical maximal “meaningfulness,” defined as the reciprocal of the Shannon entropy of the HLNs. Without any external memory the MBLS synergistically processes external data (and internal data – “thoughts”) with sensory processing abilities found in neural networks and some of the symbolic logical abilities found in human cognition. In practical applications the MBLS offers near-simultaneous pattern recognition and comprehension. In modeling the development of psychotic disorders in humans, the MBLS predicts that in many patients the etiology stems from the fragility of the working memory and the integration of additional reasoning mechanisms during adolescence.
> 
> Keywords: cognitive architecture, neural networks, cortical minicolumns
> 
> 1 Introduction
> 
> At the time of this writing, despite the human-like performance of artificial neural networks (ANNs) in pattern recognition and reinforcement learning [1,2], such neural networks, trained with a very small quantity of examples, cannot causally make sense of their environment or information at the level a four-year old child can [3,4]. .....
> 
> ....


## Version History ##

**version 1** - Winter 2017 - Initial transfer from whiteboards to Python simulation. No ANN libraries. Hand coded in Python 2.7. Shannon diversity used to assess meaningfulness values. (No GitHub repository ever created -- local files.)

**version 2**- Spring 2018 - Refactored to Python 3.6. Hand coded. No ANN libraries. Reciprocal of Shannon entropy now used to assess meaningfulness. MBLS modules still simulated by Python methods rather than being simulated by some of the collection of connected simulated HLNs. Causal memory now extensively used. Full development prematurely terminated for transition to Version 3 to allow collaboration and to more scientifically address concepts that the Meaningful-Based Cognitive Architecture proposes. (No GitHub repository ever created -- local files.)

**version 3** - Summer 2018 -work pending - Code refactored into a more professional appearance to allow future team collaboration with the code. HLNs are being ramped up to 50,000 from a few dozen in previous versions, with the goal of obtaining quantitative experimental data to better validate key concepts behind the Meaningful-Based Cognitive Architecture. (GitHub repository is MBLS-3.0 )



## Key concepts to demonstrate in MBLS-3: ##

- To better describe the architecture of the MBLS from a conventional classification. (Keep in mind that the MBLS "arbitrary program" actually changes with each sensory input or internal input (ie, "thought") -- it is no longer the same program or machine.) Empirically show the MBLS must act as a Turing machine when the Working Memory is used, but at other times can act as a super-Turing machine, with the caveat that this description may not be valid, ie, do such machines even exist theoretically.


- To show that psychosis (retrieval of incorrect vectors not associated with the reality at hand and cognitive dysfunction) is inevitable if Working Memory without error-correcting circuitry or software is used and becomes stressed.


- To show that an intervention that reduces the likelihood of psychosis in the MBLS will by analogous intervention reduce the likelihood of a young person of developing chronic schizophrenia.
50,000 proposed HLNs for MBLS-3 are not sufficient to implement the presentation example (eg, see slides which can be downloaded from this GitHub page) of the MBLS Search-and-Rescue Robot, but are enough to show a simplified Search-and-Rescue Robot simulation.


- Better implementation of causal memory.


- Better use of causal memory in the Working Memory to allow one-example learning


- Better use of causal memory in the Working Memory to allow one-example extrapolation


- Show separation of Procedural Memory and Declarative Memory as most Cognitive Architectures do, is not necessary


- To show meaningfulness feature extracts more data out of an input sensory vector than not using the feature


- To see if backpropagation of MBLS-2 between the HLNs can be replaced by one-shot reinforcement learning in MBLS-3


- To better define minimal intuitive physics required


- To better define minimal intuitive psychology required


- To better define minimal intuitive planning required


- To better define minimal intuitive meta-learning required


- To better define minimal human culture required to ensure safe operation, direct wiring to emotional center


- To better interweave subsymbolic and symbolic processes in the MBLS


- To better allow meaningfulness to be used adjunctly in the symbolic processes, rather than just as input sensory vector processing


- To better implement reinforcement learning via consciousness/goals/emotional centers


- To better implement the autonomic modules and account for incorporation within the a physical system, such as the MBLS Search-and-Rescue robot


- Effect of the autonomic modules in response to surprise negative stimuli


- More work on the pre-configuration Python algorithms


- More work on the Python learned/stored algorithms to better control library functions


- More realistic Python quasi-back propagation


- Implement the discrete learning features made available in the previous version/ implement semantic nets


- Better use of the dual functions of the feedback vector to the HLNs -- meaningfulness and learning of the pattern at hand


- Better use of the system-wide meaningfulness feedback vector


- Fine tuning of the vector convergence circuitry in the HLN simulation so that the Hopfield nets remain usable in a large network


- Start transition from the Python high functional simulation of the Working Memory to simulation by individual HLNs


- More dynamic algorithms for reconfiguration of the HLNs rather than the very static algorithms used in previous version


- Start implementing the functions of the sequential/error-correcting module and interweave with the rest of the MBLS


- Consider implementing meta-prototyping structures versus intuitive algorithms


- To better define minimal algorithms for world building


- To better define minimal algorithms for logic operations on world models from causal memory


- Given all the other structures, to better define minimal algorithms for common sense-like ability


- To decide which levels of sensory hierarchy to feed directly into Working Memory, and which to not, ie, V1 vs V4 situation


- See if can start implementing some simple language features with 50,000 HLNs


- Lifelong learning -- one item per HLN


- Lifelong learning -- start holding multiple items per HLN


- Intuitive goals


- Sequences of thoughts in MBLS (ie, feed output of working memory back in as input to the MBLS)


- Self-awareness -- define better causal recording of Working Memory for better problem solving


- Self-awareness -- define better causal recording of Working Memory for better transparency


- Self-awareness (consciousness center/emotional/reward module) solving class imbalance problem and resulting overfitting to correct