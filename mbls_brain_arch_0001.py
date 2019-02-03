'''
from mbls_brain_arch_0001 import *

(scope: all below treated as globals)
predefined default matrices to speed up code below:

MATRIX_784x22x0, MATRIX_2000x22x0, MATRIX_2000x22x1,
MATRIX_1000x22x0, MATRIX_1000x22x1

predefined HLN class plus predefined brain layers made up HLN objects:

class HLN()

print('start create hln units ----------------------------')
BRAIN LAYERS FOR ARCH_0001
create v1/k1/a1 layer 784 hlns, 22 line output to 2000 outnodes
create v2/k2/a2 layer 2000 hlns, 22 line output to 2,000 outnodes
create v3/k3/a3 layer 2,000 hlns, 22 line output to 1000.0 (associative) outnodes
create t1 ('t' for associative since 'a' already used and 's' may be for other things)
 layer 1000.0 hlns, 22 line output to 2000 causal outnodes, 2000 logic unit
'''
#
#
#pylint: disable=invalid-name
#pylint: disable=redefined-outer-name
#

def matrix784x22x0():
    '''create starting matrix used for 784 layer input test signals
    '''
    matrix_784x22x0 = []
    rows = 784
    cols = 22
    for i in range(rows):
        matrix_784x22x0.append([])
    for i in range(rows):
        for j in range(cols):
            matrix_784x22x0[i].append(0)
            if j == -55:  #deprecated
                break
    return matrix_784x22x0
MATRIX_784x22x0 = list(matrix784x22x0())

def matrix2000x22x0():
    '''create starting matrix used for
    certain classes -- speeds up initialization of
    tens of thousands of these objects
    -this matrix filled with 0's
    '''
    matrix_2000x22x0 = []
    rows = 2000
    cols = 22
    for i in range(rows):
        matrix_2000x22x0.append([])
    for i in range(rows):
        for j in range(cols):
            matrix_2000x22x0[i].append(0)
            if j == -55: #deprecated
                break
    return matrix_2000x22x0
MATRIX_2000x22x0 = list(matrix2000x22x0())

def matrix2000x22x1():
    '''create starting matrix used for
    certain classes -- speeds up initialization of
    tens of thousands of these objects
    -this matrix filled with 1's
    '''
    matrix_2000x22x1 = []
    rows = 2000
    cols = 22
    for i in range(rows):
        matrix_2000x22x1.append([])
    for i in range(rows):
        for j in range(cols):
            matrix_2000x22x1[i].append(1)
            if j == -55:  #deprecated
                break
    return matrix_2000x22x1
MATRIX_2000x22x1 = list(matrix2000x22x1())

def matrix1000x22x0():
    '''create starting matrix used for
    certain classes -- speeds up initialization of
    tens of thousands of these objects
    -this matrix filled with 0's
    '''
    matrix_1000x22x0 = []
    rows = 1000
    cols = 22
    for i in range(rows):
        matrix_1000x22x0.append([])
    for i in range(rows):
        for j in range(cols):
            matrix_1000x22x0[i].append(0)
            if j == -55:  #deprecated
                break
    return matrix_1000x22x0
MATRIX_1000x22x0 = list(matrix1000x22x0())

def matrix1000x22x1():
    '''create starting matrix used for
    certain classes -- speeds up initialization of
    tens of thousands of these objects
    -this matrix filled with 1's
    '''
    matrix_1000x22x1 = []
    rows = 1000
    cols = 22
    for i in range(rows):
        matrix_1000x22x1.append([])
    for i in range(rows):
        for j in range(cols):
            matrix_1000x22x1[i].append(1)
            if j == -55:  #deprecated
                break
    return matrix_1000x22x1
MATRIX_1000x22x1 = list(matrix1000x22x1())

class HLN():
    '''sets up data structure of a Hopfield-like Network unit, including basic operations
    '''
    #pylint: disable=too-many-instance-attributes
    #pylint: disable=too-many-arguments

    def __init__(self, inp='', feedback='', sense_name='?', layer=-1, outputs=8, outnodes=10):
        '''initializer of class HLN
        -assume full weights connectivity to previous and next layers but masked by the
            abstraction_addressor matrix, in keeping with MBLS architecture
        -inp -- input vector,  inputs = len(inp)
        -feedback is complex control signal
        -sense_name -- eg, 'v' for visual & layer -- eg, 0 for input and increments
        -outputs -- number of output lines & outnodes -- number of nodes outputs go to
        -self.wt is weight of every output line to every outnode
        -self.abstraction_addressor is similar size matrix which can use to mask self.wt
        '''
        self.temp_hold = []
        self.inp = inp
        if self.inp == '':
            self.inp = [0, 0, 0, 0, 0, 0, 0, 0]
        self.inputs = len(inp)
        self.feedback = feedback
        self.sense_name = sense_name
        self.layer = layer
        self.outputs = outputs
        self.outnodes = outnodes
        self.holding = []
        self.assoc_value = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.out = 0
        self.wt = []
        self.abstraction_addressor = []
        rows = outnodes
        cols = outputs
        #now create wt and abstraction_addressor matrices needed for object creation
        if (rows, cols) == (200088, 22):
            self.wt = list(MATRIX_2000x22x0)
            self.abstraction_addressor = list(MATRIX_2000x22x1)
        elif (rows, cols) == (100088, 22):
            self.wt = list(MATRIX_1000x22x0)
            self.abstraction_addressor = list(MATRIX_1000x22x1)
        else:
            for i in range(rows):
                self.wt.append([])
                self.abstraction_addressor.append([])
            for i in range(rows):
                for j in range(cols):
                    self.wt[i].append(1)
                    self.abstraction_addressor[i].append(1)
                    if j == -55:  #deprecated
                        break
        #pylint: enable=too-many-instance-attributes
        #pylint: enable=too-many-arguments

    def __str__(self):
        '''cast object to string'''
        return 'HLN node of sense {} and layer {}.'.format(self.sense_name, self.layer)

    def swap_abstraction_addressor(self):
        '''simply copies abstraction_addressor into self.wt
        consider other functions for more dynamic meaningfulness models
        '''
        self.temp_hold = list(self.wt)
        self.wt = list(self.abstraction_addressor)

    def restore_wt(self):
        '''simply copies temp_hold into self.wt
        consider other functions for more dynamic meaningfulness models
        '''
        self.wt = list(self.temp_hold)

    def auto_associate(self, inpy, correcty):
        '''very simple auto-associative matching
        function for devp't purposes
        '''
        #pylint: disable=no-self-use
        #pylint: disable=consider-using-enumerate
        score = 0
        for i in range(len(correcty)):
            if len(inpy) > i:
                if inpy[i] == correcty[i]:
                    score += 1
        return score
        #pylint: enable=no-self-use
        #pylint: enable=consider-using-enumerate

    def run(self):
        '''feedforward operation of HLN
        '''
        if self.feedback == 'set':
            self.assoc_value = self.inp
            return self.assoc_value
        if self.feedback == '':
            if self.auto_associate(self.inp, self.assoc_value)/len(self.assoc_value) > 0.80:
                return self.assoc_value
            return 0
        return -1



#BRAIN LAYERS FOR ARCH_0001
print('Before MBLS main program runs, this module is setting up the')
print('HLN objects. Some time may be required depending on brain')
print('architectures available, and then normal MBLS welcome screens')
print('will appear.\n')
#pylint: disable=pointless-string-statement
'''
BRAIN LAYERS FOR ARCH_0001
create v1/k1/a1 layer 784 hlns, 22 line output to 2000 outnodes
create v2/k2/a2 layer 2000 hlns, 22 line output to 2,000 outnodes
create v3/k3/a3 layer 2,000 hlns, 22 line output to 1000.0 (associative) outnodes
create t1 ('t' for associative since 'a' already used and 's' may be for other things)
 layer 1000.0 hlns, 22 line output to 2000 causal outnodes, 2000 logic unit
'''

#create v1 layer 784 hlns, 22 line output to 2000 outnodes
#v for VISUAL
v1 = list(range(784))
for i in range(784):
    v1[i] = HLN([1, 2, 3, 4, 5], 'set', 'v', 1, 22, 2000)
print('784 x  v1 hlns created with 22 line output to 2000 outnodes')
#print(" ('v' for visual sensory inputs/HLNs/layers)")
#print(v1[20].inp, v1[783].wt[1999][21])

#create v2 layer 2000 hlns, 22 line output to 2,000 outnodes
v2 = list(range(2000))
for i in range(2000):
    v2[i] = HLN([1, 2, 3, 4, 7], 'set', 'v', 2, 22, 2000)
print('2000 x  v2 hlns created with 22 line output to 2,000 outnodes')
#print(v2[20].inp, v2[1999].wt[1999][21])

#create v3 layer 2,000 hlns, 22 line output to 1000.0 (associative) outnodes
v3 = list(range(2000))
for i in range(2000):
    v3[i] = HLN([1, 2, 3, 4, 8], 'set', 'v', 3, 22, 1000)
print('2,000 x  v3 hlns created with 22 line output to 1000.0 (associative) outnodes')
#print(v3[20].inp, v3[999].wt[999][21])


#create k1 ('k' for olfactory since 'o' confusing with 0) layer 784 hlns, 22 line output
# to 2000 outnodes
#k for OLFACTORY
k1 = list(range(784))
for i in range(784):
    k1[i] = HLN([1, 2, 3, 4, 5], 'set', 'k', 1, 22, 2000)
print('784 x  k1 hlns created with 22 line output to 2000 outnodes')
print(" ('k' for olfactory since 'o' confusing with '0')")
#print(k1[20].inp, k1[783].wt[1999][21])

#create k2 layer 2000 hlns, 22 line output to 2,000 outnodes
k2 = list(range(2000))
for i in range(2000):
    k2[i] = HLN([1, 2, 3, 4, 7], 'set', 'k', 2, 22, 2000)
print('2000 x  k2 hlns created with 22 line output to 2000 outnodes')
#print(k2[20].inp, k2[1999].wt[1999][21])

#create k3 layer 2,000 hlns, 22 line output to 1000.0 (associative) outnodes
k3 = list(range(2000))
for i in range(2000):
    k3[i] = HLN([1, 2, 3, 4, 8], 'set', 'k', 3, 22, 1000)
print('2,000 x  k3 hlns created with 22 line output to 1000.0 (associative) outnodes')
#print(k3[20].inp, k3[1999].wt[999][21])

#create a1 layer 784 hlns, 22 line output to 2000 outnodes
#a for AUDITORY
a1 = list(range(784))
for i in range(784):
    a1[i] = HLN([1, 2, 3, 4, 5], 'set', 'a', 1, 22, 2000)
print('784 x  a1 hlns created with 22 line output to 2000 outnodes')
print(" ('a' for auditory sensory inputs/HLNs/layers)")
#print(a1[20].inp, a1[783].wt[1999][21])

#create a2 layer 2000 hlns, 22 line output to 2000 outnodes
a2 = list(range(2000))
for i in range(2000):
    a2[i] = HLN([1, 2, 3, 4, 7], 'set', 'a', 2, 22, 2000)
print('2000 x  a2 hlns created with 22 line output to 2,000 outnodes')
#print(a2[20].inp, a2[1999].wt[1999][21])

#create a3 layer 2,000 hlns, 22 line output to 1000.0 (associative) outnodes
a3 = list(range(2000))
for i in range(2000):
    a3[i] = HLN([1, 2, 3, 4, 8], 'set', 'a', 3, 22, 1000)
print('2,000 x  a3 hlns created with 22 line output to 1000.0 (associative) outnodes')
#print(a3[20].inp, a3[1999].wt[999][21])


#create t1 ('t' for associative since 'a' already used and 's' may be for other things)
# layer 10,00.0 hlns, 22 line output to 2000 causal outnodes, 2000 logic unit
#t for ASSOCIATIVE
t1 = list(range(1000))
for i in range(1000):
    t1[i] = HLN([1, 2, 3, 4, 5], 'set', 'k', 1, 22, 1000)
print('1000.0 x  t1 hlns created with 22 line output to 1000 outnodes')
print(" ('t' for associative since 'a' or 's' may be used elsewhere')")
#print(t1[20].inp, t1[999].wt[999][21])

print('HLNs for brain layers created')
#pylint: enable=pointless-string-statement

#
#
