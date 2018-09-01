# MBLS-3.0
Version 3.0  Meaningful Based Learning System (MBLS)

The 'Meaningful Based Learning System' (MBLS) is an implementation of the Meaningful Based Cognitive Architecture.

**version 1** - Winter 2017 - Initial transfer from whiteboards to Python simulation. No ANN libraries. Handcoded in Python 2.7.
Shannon diversity used to assess meaningfulness values.

**version 2** - Spring 2018 - Switched to Python 3.6. Handcoded. No ANN libraries. Reciprocal of Shannon entropy now used to assess meaningfulness. MBLS modules simulated by Python methods rather than simulating the collection of connected simulated HLNs. Causal memory now extensively used. Full development prematurely terminated for transition to Version 3 to allow collaboration and to more scientifically address concepts that the Meaningful-Based Cognitive Architecture proposes.

**version 3** - Summer 2018 -work pending - Code refactored into a more professional appearance to allow future team collaboration with the code. Robert C. Martin's Clean Code software architecture and style being followed. HLNs are being ramped up to 50,000 from a few dozen in previous versions, with the goal of obtaining quantitative experimental data to better validate key concepts behind the Meaningful-Based Cognitive Architecture.

See below for key concepts that I wish to demonstrate in MBLS-3. 

**Papers** describing the Meaningful-Based Cognitive Archtiecture and the MBLS:

Schneider, H., Non-Hybrid Meaningful-Based Learning System Using a Configurable Network of Neural Networks. Proceedings of the 2018 International Conference on Artificial Intelligence pp 96-102; Aug 2018.

Schneider, H., Meaningful-Based Cognitive Architecture. Proceedings of the 2018 Annual International Conference on Biologically Inpsired Architectures (BICA 2018) held on August 22, 2018 as part of the Joint Multi-Conference on Human-Level Artificial Intelligence (HLA-18).

https://www.respekt.cz/spolecnost/muze-pocitac-trpet-psychozou

Schneider, H., Meaningful-Based Cognitive Architecture. Procedia Computer Science, 9th Annual International Conference on Biologically Inspired Cognitive Architectures, BICA 2018,edited by Samsonovich, A.V.,  in press.

**PowerPoint slides** (in PDF format) of my presentation at the BICA section of the HLAI-18 in Prague, Czech Republic can be downloaded from this GitHub page, and give an idea of the key concepts behind the Meaningful-Based Cognitive Architecture and the MBLS implementation. The papers cannot be reproduced for download here but an abstract is given below. (However, they can readily be obtained via a Google search and downloaded from the publishers.)

**Excerpts of paper**:

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
    ....
    ....
    
 **Key concepts to demonstrate in MBLS-3 **
 
 -
    
   
  
