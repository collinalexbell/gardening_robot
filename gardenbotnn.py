from random import random
import random as rnd

class Garden_Bot_Edge:
    def __init__(self, fr, weight, speed):
        self.fr = fr
        self.weight = weight
        self.speed = speed

    def __eq__(self, other_self):
        if self.fr == other_self.fr and self.weight == other_self.weight and self.speed == other_self.speed:
            return True
        else:
            return False


class Garden_Bot_NN:
    def __init__(self, dna = []):

        #Each neuron has a name
        self.neurons = {}

        #Has neuron inputs on left, right, and front for sensing gardens.
        garden_sensors = ['garden_left', 'garden_right']
        for sensor in garden_sensors:
            self.neurons[sensor] = {}
            self.neurons[sensor]['type'] = 'input'

        #Has neuron inputs on left, right, and front for sensing customers
        customer_sensors = ['customer_left', 'customer_right']
        for sensor in customer_sensors:
            self.neurons[sensor] = {}
            self.neurons[sensor]['type'] = 'input'

        #Has neuron inputs for sensing how much food the bot has
        self.neurons['food_level'] = {}
        self.neurons['food_level']['type'] = 'input'

        #Clock input for neural updates
        self.neurons['clock'] = {}
        self.neurons['clock']['type'] = 'input'

        #Has output neuron on tail that fires to move forward
        self.neurons['tail_motor'] = {}
        self.neurons['tail_motor']['type'] = 'output'

        #Has left and right output neuron to turn
        turn_motors = ['left_turn', 'right_turn']
        for motor in turn_motors:
            self.neurons[motor] = {}
            self.neurons[motor]['type'] = 'output'

#       Has hidden nuerons
        hidden_neurons = ['hidden1', 'hidden2']
        for neuron in hidden_neurons:
            self.neurons[neuron] = {}
            self.neurons[neuron]['type'] = 'hidden'


        #Create list of inputs and outputs
        self.inputs = []
        self.outputs = []
        self.hidden = []

        for index, neuron in self.neurons.items():
            neuron['value'] = 0
            if neuron['type'] is 'input':
                self.inputs.append(neuron)
            if neuron['type'] is 'output':
                self.outputs.append(neuron)
            if neuron['type'] is 'hidden':
                self.hidden.append(neuron)

        #Fully connect the inputs to the outputs
        #print(dna)
        for index, o in enumerate(self.outputs + self.hidden + self.inputs):
            if(dna):
                try:
                    o['decay'] = dna[index][1]
                    o['threshold'] = dna[index][0]
                except:
                    print('index is {}'.format(index))
                    print('dna @ index is {}'.format(dna[index]))
            else:
                o['decay'] = random()
                o['threshold'] = random()
            o['stimulus'] = 0
            o['output'] = 0
            o['in_edges'] = []
            if(o['type'] == 'output'):
                for i_index, i in enumerate(self.hidden + self.inputs):
                    if(dna):
                        o['in_edges'].append(Garden_Bot_Edge(i,dna[index][2][i_index][0], dna[index][2][i_index][1]))
                    else:
                        o['in_edges'].append(Garden_Bot_Edge(i,(random()-.5)*2,(random()-.5)*2 ))
            if(o['type'] == 'hidden'):
                for i_index, i in enumerate(self.inputs):
                    if(dna):
                        o['in_edges'].append(Garden_Bot_Edge(i,dna[index][2][i_index][0], dna[index][2][i_index][1]))
                    else:
                        o['in_edges'].append(Garden_Bot_Edge(i,(random()-.5)*2,(random()-.5)*2 ))

    def encode_dna(self):
        #[[n1.threshhold, n1.decay, [[in1.weight, in1.speed]]]]
        dna = []
        #print(self.outputs)
        #print(self.outputs + self.inputs)
        for index, neuron in enumerate(self.outputs + self.hidden + self.inputs):
            #Each neuron gets its own list of dna attributes
            dna_neuron = []
            dna_neuron.append(neuron['threshold'])
            dna_neuron.append(neuron['decay'])
            dna_neuron_inputs = []
            for input_index, neuron_input in enumerate(neuron['in_edges']):
                weight = neuron_input.weight
                speed = neuron_input.speed
                dna_neuron_inputs.append([weight, speed])
            dna_neuron.append(dna_neuron_inputs)
            dna.append(dna_neuron)
        return dna

    def run_net(self):
        #Check that all inputs have an output
        for i, inp in enumerate(self.inputs):
            if 'output' not in inp:
                raise KeyError('input {} does not have an output value'.format(i))
        for index, neuron in enumerate(self.outputs + self.hidden + self.inputs):
            #Decay the stimulus
            if neuron['stimulus'] > 0:
                #print(neuron)
                neuron['stimulus'] = round(neuron['stimulus'] - neuron['decay'], 5)
                if neuron['stimulus'] < 0:
                    neuron['stimulus'] = 0
            self.compute_stimulus(neuron)
            neuron['output'] = 0
            if neuron['stimulus'] >= neuron['threshold'] and neuron['threshold'] > 0:
                neuron['output'] = 1
                neuron['stimulus'] = 0

    def compute_stimulus(self, o):
        d_stimulus = 0
        #print('type of o is {}'.format(type(o)))
        #print('\n\n\n')
        #print(o['in_edges'])
        for edge in o['in_edges']:
            d_stimulus += edge.fr['output'] * edge.weight
        o['stimulus'] += d_stimulus


def mutate_dna(dna):
    percent_of_mutations = .02
    alpha = .002
    for neuron in dna:
        if random() < percent_of_mutations:
            print('mutation')
            neuron[0] += neuron[0] * rnd.uniform(-1*alpha, alpha)
            neuron[0] = abs(neuron[0])
        if random() < percent_of_mutations:
            print('mutation')
            neuron[1] += neuron[0] * rnd.uniform(-1*alpha, alpha)
            neuron[1] = abs(neuron[1])
        for in_node in neuron[2]:
            if random() < percent_of_mutations:
                print('mutation')
                in_node[0] += in_node[0] * rnd.uniform(-1*alpha, alpha)
            if random() < percent_of_mutations:
                print('mutation')
                in_node[1] += in_node[1] * rnd.uniform(-1*alpha, alpha)
                in_node[1] = abs(in_node[1])



    #print(dna)
    return dna

if __name__ == '__main__':
    nnet = Garden_Bot_NN()
    dna = nnet.encode_dna()
    print(dna)
    print('\n\n')
    print(mutate_dna(nnet.encode_dna()))










