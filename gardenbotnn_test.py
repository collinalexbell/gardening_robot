from gardenbotnn import Garden_Bot_NN
from gardenbotnn import Garden_Bot_Edge
import json

def test_default_nn_creation():
    bot = Garden_Bot_NN()

    #Specific neurons must exist
    #Has neuron inputs on left, right, and front for sensing gardens.
    assert 'garden_left' in bot.neurons
    assert 'garden_right' in bot.neurons
    #Has neuron inputs on left, right, and front for sensing customers
    assert 'customer_left' in bot.neurons
    assert 'customer_right' in bot.neurons
    #Has neuron inputs for sensing how much food the bot has
    assert 'food_level' in bot.neurons
    #Has output neuron on tail that fires to move forward
    assert 'tail_motor' in bot.neurons
    #Has left and right output neuron to turn
    assert 'left_turn' in bot.neurons
    assert 'right_turn' in bot.neurons
    #Clock input for neural updates
    assert 'clock' in bot.neurons

    assert 'hidden1' in bot.neurons
    assert 'hidden2' in bot.neurons

    #All neurons must have a type and value of 0
    for index, item in bot.neurons.items():
        assert 'type' in item
        assert item['value'] == 0


    #Net has 6 input neurons with each with 3 randomized edges
    assert len(bot.inputs) == 6
    for o in bot.outputs + bot.hidden:
#       6 input & 2 hidden
        if o in bot.outputs:
            assert len(o['in_edges']) == 8
        else:
            assert len(o['in_edges']) == 6
        for e in o['in_edges']:
            assert type(e) == Garden_Bot_Edge
            assert e.weight > -1 and e.weight < 1
            assert e.speed > -1 and e.speed < 1



    #Each output neuron has a randomized threshold and exitation decay rate
    for neuron in bot.outputs + bot.hidden:
        assert neuron['decay'] > 0 and neuron['decay'] < 1
        assert neuron['threshold'] > 0 and neuron['threshold'] < 1

#NEED TO FIX DNA ENCODING TO SHOW HIDDEN next to outputs
def test_nn_encode_dna():
    #DNA will be an array of numbers
    #[[n1.threshhold, n1.decay, [[in1.weight, in1.speed]]]]
    bot = Garden_Bot_NN()
    dna = bot.encode_dna()
    #print(dna)

#   Iterate through the entire DNA
#   Outputs first, then hidden, then inputs
    for index, neuron in enumerate(bot.outputs + bot.hidden):
        assert type(dna[index]) == list
        assert dna[index][0] == neuron['threshold']
        assert dna[index][1] == neuron['decay']
        assert type(dna[index][2]) == list
        for ind, n_input in enumerate(dna[index][2]):
            #n_inputs = [in1.weight, in1.speed]
            assert type(n_input) == list
            assert n_input[0] == neuron['in_edges'][ind].weight
            assert n_input[1] == neuron['in_edges'][ind].speed
        last_ind = index
    #print(last_ind)
    for index, neuron in enumerate(bot.inputs):
        assert dna[index + last_ind + 1][0] == neuron['threshold']
        assert dna[index + last_ind + 1][1] == neuron['decay']

def test_edge_equality():
    edge1 = Garden_Bot_Edge([],.5,.6)
    edge2 = Garden_Bot_Edge([],.4,.7)
    edge1_copy = Garden_Bot_Edge([], .5, .6)

    #Test if it detects different from neurons
    edge1_copy_wo_fr = Garden_Bot_Edge([5],.5,.6)
    assert edge1 != edge1_copy_wo_fr

    assert edge1 == edge1_copy
    assert edge1 != edge2

def test_nn_decode_dna():
    bot = Garden_Bot_NN()
    dna = bot.encode_dna()

    decoded_bot = Garden_Bot_NN(dna)
    decoded_bot_dna = decoded_bot.encode_dna()

    #Defined as the neuron dictionary equals each other. Must define equality for edges as well
    assert dna == decoded_bot_dna

def test_calculate_stimulus():
    dna = json.loads(open('zero_dna.json').read())
    bot = Garden_Bot_NN(dna)

    #Select target output, compute stimulus and make sure it matches correct stimulus

    #Test the 0 case
    target_output = bot.outputs[0]
    print(target_output)
    bot.compute_stimulus(target_output)

    assert target_output['stimulus'] == 0

    #Test 1 input case
    #print(bot.outputs[0]['in_edges'][0].weight)
    bot.outputs[0]['in_edges'][0].weight = .4
    bot.outputs[0]['in_edges'][0].fr['output'] = 1
    bot.compute_stimulus(target_output)

    #Test 2 input case
    target_output['stimulus'] = 0
    bot.outputs[0]['in_edges'][1].weight = .4
    bot.outputs[0]['in_edges'][1].fr['output'] = 1
    bot.compute_stimulus(target_output)

    assert target_output['stimulus'] == .8

    #Test 1 input case with 2 time integration
    target_output['stimulus'] = 0
    bot.outputs[0]['in_edges'][1].fr['output'] = 0
    bot.compute_stimulus(target_output)
    bot.compute_stimulus(target_output)

    assert target_output['stimulus'] == .8

def test_run_net():
    dna = json.loads(open('zero_dna.json').read())
    bot = Garden_Bot_NN(dna)

    target_output = bot.outputs[0]

    target_output['stimulus'] = 0
    target_output['threshold'] = 1
    bot.outputs[0]['in_edges'][0].weight = .4
    bot.outputs[0]['in_edges'][0].fr['output'] = 1
    bot.outputs[0]['in_edges'][1].weight = .4
    bot.outputs[0]['in_edges'][1].fr['output'] = 1
    bot.run_net()

    #Test that the two inputs output has disipated
    assert bot.outputs[0]['in_edges'][0].fr['output'] == 0
    assert bot.outputs[0]['in_edges'][1].fr['output'] == 0


    #Test that the stimulus decays from .8 to .7
    target_output['decay'] = .1
    bot.run_net()
    assert target_output['stimulus'] == .7


    #Test that output of target_output is 1
    bot.outputs[0]['in_edges'][0].fr['output'] = 1
    bot.run_net()
    assert target_output['output'] == 1

    #Assert that the neurons stimulus is 0 after neuron firing
    assert target_output['stimulus'] == 0








