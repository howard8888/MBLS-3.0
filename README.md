# MBLS-3.0
Version 3.0  Meaningful Based Learning System (MBLS)

The 'Meaningful Based Learning System' (MBLS) is an implementation of the Meaningful Based Cognitive Architecture.

version 1 - Winter 2017 - Initial transfer from whiteboards to Python simulation. No ANN libraries. Handcoded in Python 2.7.
Shannon diversity used to assess meaningfulness values.

version 2 - Spring 2018 - Switched to Python 3.6. Handcoded. No ANN libraries. Reciprocal of Shannon entropy now used to assess meaningfulness. MBLS modules simulated by Python methods rather than simulating the collection of connected simulated HLNs. Causal memory now extensively used.

version 3 - Summer 2018 -work pending - Code refactored into a more professional appearance to allow future team working, eg, open source, on the code. Robert C. Martin's Clean Code software architecture and style being followed. HLNs being ramped up to 50,000 from a few dozen in previous versions.


Papers describing the Meaningful-Based Cognitive Archtiecture and the MBLS:

Schneider, H., Non-Hybrid Meaningful-Based Learning System Using a Configurable Network of Neural Networks. Proceedings of the 2018 International Conference on Artificial Intelligence pp 96-102; Aug 2018.

Schneider, H., Meaningful-Based Cognitive Architecture. Proceedings of the 2018 Annual International Conference on Biologically Inpsired Architectures (BICA 2018) held on August 22, 2018 as part of the Joint Multi-Conference on Human-Level Artificial Intelligence (HLA-18).

https://www.respekt.cz/spolecnost/muze-pocitac-trpet-psychozou

Schneider, H., Meaningful-Based Cognitive Architecture. Procedia Computer Science, 9th Annual International Conference on Biologically Inspired Cognitive Architectures, BICA 2018,edited by Samsonovich, A.V.,  in press.


Excerpts of paper:

2018 Annual International Conference on Biologically Inspired Cognitive Architectures
Meaningful-Based Cognitive Architecture
Howard Schneider
Sheppard Clinic North, Toronto, ON, Canada
howard.schneider@gmail.com 


Abstract
An overview is given of the cognitive architecture of the biologically inspired meaningful-based learning system (MBLS). The basic element of the MBLS is a reconfigurable Hopfield-like network (HLN) which can rapidly connect to other HLNs depending on the level of abstraction which yields a practical maximal “meaningfulness,” defined as the reciprocal of the Shannon entropy of the HLNs. Without any external memory the MBLS synergistically processes external data (and internal data – “thoughts”) with sensory processing abilities found in neural networks and some of the symbolic logical abilities found in human cognition. In practical applications the MBLS offers near-simultaneous pattern recognition and comprehension. In modeling the development of psychotic disorders in humans, the MBLS predicts that in many patients the etiology stems from the fragility of the working memory and the integration of additional reasoning mechanisms during adolescence. 

Keywords: cognitive architecture, neural networks, cortical minicolumns

1 Introduction
    
    At the time of this writing, despite the human-like performance of artificial neural networks (ANNs) in pattern recognition and reinforcement learning [1,2], such neural networks, trained with a very small quantity of examples, cannot causally make sense of their environment or information at the level a four-year old child can [3,4].
    Recent models by Graves and colleagues help to narrow the neural-symbolic gap with an ANN which can read and write to an external memory, i.e., a hybrid system [5]. However, like the human brain, the meaningful-based learning system (MBLS), described below, can perform the sensory processing associated with ANNs and the efficient symbolic logic associated with human cognition, without the use of an external memory, i.e., it is not a physically hybrid system.
    The basic functional unit of the MBLS is not an artificial neuron but a Hopfield-like network (HLN). The HLN contains a Hopfield neural network along with associated circuitry modifying convergence properties and allowing reconfiguration with other HLNs [6,7]. The HLN can learn and recognize patterns. While Hopfield networks are typically thought of as requiring stationary inputs they can be extended for sequential learning [8]. The weights of the connections between different HLNs can be adjusted gradually with learning as in a conventional ANN, can be adjusted more abruptly to form a more discrete logical relation between two HLNs, and as well can rapidly be reconfigured to on and off values to allow fast and extreme reconfiguration of the HLNs with each other. In rapid reconfigurations, there is an attempt by the HLNs to maximize meaningfulness, where this is defined as the reciprocal of the Shannon entropy, as described below.
