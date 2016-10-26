import random
import copy
from Neuron import Neuron


class InputSignal:
    def output(self):
        return self.x

    def __init__(self, x):
        self.x = x


class Brain:

    def __init__(self, input_number, layers, neuron_per_layer, output_number):
        self.inputs = [InputSignal(0) for x in range(input_number)]
        self.layers = []
        prev_layer = self.inputs
        self.fit = 0
        for i in range(layers):
            new_layer = [Neuron(prev_layer)
                         for j in range(neuron_per_layer)]
            self.layers.append(new_layer)
            prev_layer = new_layer
        self.outputs = [Neuron(prev_layer)
                        for i in range(output_number)]

    def output(self, inputs):
        self.set_inputs(inputs)
        return [x.output() for x in self.outputs]

    def set_inputs(self, inputs):
        i = 0
        for x in self.inputs:
            x.x = inputs[i]
            i += 1

    def mutate(self, other, mutation):
        for i in range(len(self.layers)):
            for j in range(len(self.layers[i])):
                self.layers[i][j].mutate(other.layers[i][j], mutation)

    def duplicate(self):
        return copy.deepcopy(self)

    def __str__(self):
        i = 1
        res = ""
        for layer in self.layers:
            res += "Layer {}:\n".format(i)
            for neuron in layer:
                res += str(neuron)
        res += "Output:\n"
        for neuron in self.outputs:
            res += str(neuron)
        return res



def check(x, y):
    if x+y > 0.5:
        return 1.0
    else:
        return -1.0

if __name__ == '__main__':
    population_pool_size = 18
    generation_number = 400
    mutation = 0.05
    fittnes_test_number = 35

    breed_ratio = 0.5
    loss_ratio = 0.3
    new_ration = 0.0

    brain_setup = {
        'input_number': 2,
        'output_number': 1,
        'layers': 1,
        'neuron_per_layer': 1
    }

    steps = []
    fitnes = []
    population = []
    for i in range(population_pool_size):
        population.append(Brain(**brain_setup))

    prev_fit = 0.01
    for i in range(generation_number):
        #print("======== New Generation ========")
        for instance in population:
            instance.fit = 0
            for j in range(fittnes_test_number):
                x = random.random()
                y = random.random()
                good_answer = check(x, y)
                answer = instance.output([x, y])[0]
                #print(answer, " == ", good_answer, end="")
                if answer == good_answer:
                    instance.fit += 1
                    #print("+")
                else:
                    pass
                    #print("-")
        #print("")
        # for instance in population:
        #     print(instance.fit)
        population.sort(key=lambda x: x.fit)
        #print("----- Fitness of instances -----")
        aggr = 0
        for instance in population:
            aggr += instance.fit

        avg_fit = (float(aggr)/len(population))/fittnes_test_number
        fitnes.append(avg_fit)
        #print("average fitness: %.2f, evolved: %.2f" % (avg_fit, avg_fit-prev_fit))
        steps.append(avg_fit-prev_fit)
        prev_fit = avg_fit

        # Breeding
        limit = len(population)-int(len(population)*breed_ratio)
        replace_limit = int(len(population)*loss_ratio)
        new_limit = int(len(population) * new_ration)
        better = population[limit:]
        for i in range(replace_limit):
            population[i] = random.choice(better).duplicate()
        for i in range(replace_limit, limit):
            better_one = random.choice(better)
            population[i].mutate(better_one, mutation)
        for i in range(new_limit):
            j = random.choice(range(limit))
            population[j] = Brain(**brain_setup)

    pos_step_number = sum([1 if x>0 else 0 for x in steps])
    neg_step_number = sum([1 if x<0 else 0 for x in steps])
    avg_step = sum(steps)/len(steps)
    avg_fit = sum(fitnes)/len(fitnes)
    print("negative steps: ", neg_step_number)
    print("positive steps: ", pos_step_number)
    print(pos_step_number-neg_step_number, " more positive steps")
    print("Average steps: ", avg_step)

    print("----------------")
    print("Start fitness: %.2f"% fitnes[0])
    print("Average fitness: %.2f"% avg_fit)
    print("End fitness: %.2f\n"% fitnes[-1])
    print("Total gain: %.2f"% (fitnes[-1]-fitnes[0]))

    best_brain = population[-1]
    final_test = 1000
    good = 0
    for i in range(final_test):
        x = random.random()
        y = random.random()
        good_answer = check(x, y)
        answer = best_brain.output([x, y])[0]
        good += 1 if answer == good_answer else 0

    result = float(good)/final_test
    print("Best trained Brain's test result: ", result)
    print(best_brain)



