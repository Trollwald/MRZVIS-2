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

