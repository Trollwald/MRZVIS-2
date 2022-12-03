import random
import math
import os


symbols_dictionary = {'-': -1, '*': 1}
max_side = 512
side_of_image = 5


def load_images_from_files():
    list_of_images = []
    for filename in os.listdir("images"):
        path = os.path.join("images", filename)
        if filename.endswith(".txt"):
            with open(path) as f:
                images = f.read(max_side)
                images = str.replace(images, "\n", "")
                images = str.replace(images, "\r", "")
                list_of_numbers = []
                for img in images:
                    list_of_numbers.append(symbols_dictionary[img])
                list_of_images.append(list_of_numbers)
    return list_of_images


def symbol_of_number(number):
    symbols_dict = {-1: '-', 1: '*'}
    return symbols_dict[number]


def print_image(image, size):
    i = 0
    for img in image:
        print(f"{symbol_of_number(img)}", end='')
        i += 1
        if i % size == 0:
            print()


class Net:
    def __init__(self, side):
        self.next_steps = False
        self.W = []
        self.Y = []
        self.images = []
        self.neurons = 0
        self.side = side
        self.max_iterations = 500
        self.current = 0

    def working_with_neurons(self, side):
        self.neurons = int(math.pow(side, 2))
        for i in range(0, self.neurons):
            self.W.append([0 for _ in range(0, self.neurons)])

    def train_neural_net(self, list_of_images):
        self.images.append(list_of_images)
        X = list_of_images
        for i in range(0, self.neurons):
            for j in range(0, self.neurons):
                if i != j:
                    self.W[i][j] = self.W[i][j] + X[i] * X[j]
                else:
                    self.W[i][j] = 0

    def recover_image(self, image_in_numbers, side):
        self.Y = image_in_numbers
        iteration = 0
        print('Changed neurons:: ')
        while self.images.count(self.Y) == 0:
            self.recovering_steps(side)
            iteration = iteration + 1
            if self.current >= self.max_iterations:
                print(self.current)
                return False, self.Y, iteration
        return True, self.Y, iteration

    def recovering_steps(self, side):
        activate_func = lambda x: round((math.exp(2 * x) - 1) / (math.exp(2 * x) + 1), 6)  # tan as function
        net_range = random.randrange(0, self.neurons, 1)
        net = 0
        for i in range(0, self.neurons):
            net = net + self.Y[i] * self.W[i][net_range]
        signnet = activate_func(net)
        if signnet == self.Y[net_range]:
            self.current += 1
        else:
            print(f'Neuron {net_range}: was {self.Y[net_range]}  became  {signnet}')
            self.Y[net_range] = signnet
            if self.next_steps:
                print_image(self.Y, side)
                print('\n')
            self.current = 0


if __name__ == '__main__':
    list_of_images = load_images_from_files()
    with open("corrupted.txt") as f:
        contents = f.read(max_side)
        contents = str.replace(contents, "\n", "")
        contents = str.replace(contents, "\r", "")
        image_in_numbers = []
        for sign in contents:
            image_in_numbers.append(symbols_dictionary[sign])

    net = Net(side_of_image)
    print("Images to learn:")
    for i in list_of_images:
        print_image(i, side_of_image)
        print()
    net.working_with_neurons(side_of_image)

    for each_list in list_of_images:
        net.train_neural_net(each_list)
    print()
    
    print("Corrupted image to fix: ")
    print_image(image_in_numbers, side_of_image)
    print()
    (recognize, wrong_num, iters) = net.recover_image(image_in_numbers, side_of_image)
    print()

    if recognize:
        print(f"Iterations to restore image: {iters}")
    else:
        print(f"Error! The last iteration: {iters} ")
    print_image(wrong_num, side_of_image)

