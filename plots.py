import math
import random
import matplotlib.pyplot as plt

def plot_functions():
    first_sigmoid = []
    second_sigmoid = []
    third_sigmoid = []

    num_points = 10
    for i in range(0, num_points):
        value =  2.0 / (1 + math.exp(math.log(i+1) - math.log(4)))
        other_value =  1.0 / (1 + math.exp(math.log(i+2)))
        another_value =  1.0 / (1 + math.exp(math.log(i+1)))

        first_sigmoid.append(value)
        second_sigmoid.append(other_value)
        third_sigmoid.append(another_value)

    y = range(num_points)
    plt.plot(y, first_sigmoid, 'ro')
    # plt.plot(y, second_sigmoid, '-')
    # plt.plot(y, third_sigmoid, 'v')
    plt.show()


def simulate_states():

    values = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    log_divisor = []
    no_log_divisor = []
    num_points = 1000
    for _ in range(0, num_points):
        exp_gain = 0
        for value in values:
            sigmoid_val = 1.0 / (1 + math.exp(math.log(value+1)))
            exp_gain = exp_gain + sigmoid_val

        log_divisor_value = float(exp_gain) / math.log(len(values))
        no_log_divisor_value = float(exp_gain) / len(values)

        log_divisor.append(log_divisor_value)
        no_log_divisor.append(no_log_divisor_value)

        index_to_increment = random.randrange(len(values))
        values[index_to_increment] = values[index_to_increment] + 1

    x_axis = range(num_points)
    plt.plot(x_axis, log_divisor, 'r-')
    plt.plot(x_axis, no_log_divisor, 'b-')
    plt.show()

if __name__ == "__main__":
    simulate_states()