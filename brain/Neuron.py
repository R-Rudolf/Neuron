import random


class Neuron:

    def __init__(self, inputs_in, non_linear_function=None):
        self.weights = [random.random()*2-1
                        for x in range(len(inputs_in)+1)]
        self.inputs = inputs_in

        def signum(f):
            return -1.0 if f < 0 else 1.0

        if non_linear_function is not None:
            self.s = non_linear_function
        else:
            self.s = signum

    def output(self):
        # if len(inputs) != len(self.weights):
        #     return None

        agg = 0
        i = 0

        # Weight input signals
        for signal_in in self.inputs:
            if type(signal_in) is float:
                agg += signal_in * self.weights[i]
            else:
                agg += signal_in.output()*self.weights[i]
            i += 1

        # Add drift
        agg -= self.weights[-1]

        # Flow through given non linear function
        return self.s(agg)

    def mutate(self, other, mutation=0):
        #newNeuron = Neuron(self.inputs, self.s)
        i = 0
        for i in range(len(self.weights)):
            self.weights[i] = (self.weights[i] + other.weights[i])/2 + \
                              (random.random()*2-1)*mutation
        #return newNeuron

    def __str__(self):
        i=0
        res = "Neuron:\n"
        for w in self.weights[:-1]:
            i+=1
            res += "\tw%d: %.3f\n"%(i, w)
        res += "\tbias: %.3f\n" % self.weights[-1]
        return res


if __name__ == '__main__':
    signals = [0.0, 0.0]
    a = Neuron(signals)
    b = Neuron(signals)
    c = Neuron(signals)

    d = Neuron([a, b, c])
    print(d.output())
    a.mutate(b)
