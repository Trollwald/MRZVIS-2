import random
import math
from  load_func import *

next_steps = False
W=[]
Y = []
images = []
max_iterations = 400
current = 0
neurons = 0

def working_with_neurons(side):
    global neurons, W
    neurons = int(math.pow(side, 2))
    neurons = neurons
    for i in range(0, neurons):
        W.append([0 for _ in range(0, neurons)])


def train_neural_net(image):
    global neurons, W, images
    images.append(image)
    X = image
    for i in range(0, neurons):
        for j in range(0, neurons):
            if i != j:
                W[i][j] = W[i][j] + X[i] * X[j]
            else:
                W[i][j] = 0


def recover_image(image_in_numbers, side):
    global Y, max_iterations
    Y = image_in_numbers
    iteration = 0
    print('Changed neurons:: ')
    while images.count(Y) == 0:
        recovering_steps(side)
        iteration = iteration + 1
        if current >= max_iterations:
            print(current)
            return False, Y, iteration
    return True, Y, iteration


def recovering_steps(side):
    global current, Y, neurons, next_steps
    activate_func = lambda x: round((math.exp(2 * x) - 1) / (math.exp(2 * x) + 1), 6) #tan as function
    net_range = random.randrange(0, neurons, 1)
    net = 0
    for i in range(0, neurons):
        net = net + Y[i] * W[i][net_range]
    signnet = activate_func(net)
    if signnet == Y[net_range]:
        current += 1
    else:
        print(f'Neuron {net_range}: was {Y[net_range]}  became  {signnet}')
        Y[net_range] = signnet
        if next_steps:
            print_image(Y, side)
            print('\n')
        current = 0


def main():
    images = load_images_from_files()
    with open("corrupted.txt") as f:
        contents = f.read(max_side)
        contents = str.replace(contents, "\n", "")
        contents = str.replace(contents, "\r", "")
        image_in_numbers = []
        for sign in contents:
             image_in_numbers.append(symbols_dictionary[sign])

    print("Images to learn:")
    for i in images:
        print_image(i, side_of_image)
        print()
    working_with_neurons(side_of_image)
    for each_list in images:
        train_neural_net(each_list)
    print()

    print("Corrupted image to fix: ")
    print_image(image_in_numbers, side_of_image)
    print()
    (recognize, wrong_num, iters) = recover_image(image_in_numbers, side_of_image)
    print()

    if recognize:
        print(f"Iterations to restore image: {iters}")
    else:
        print(f"Error! The last iteration: {iters} ")
    print_image(wrong_num, side_of_image)


if __name__ == '__main__':
    main()