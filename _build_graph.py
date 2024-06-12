import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Qt5Agg')  # Choose backend here


def draw_graph(numbers_list):
    plt.plot(np.arange(len(numbers_list)), numbers_list)
    plt.title(f'Currently at {numbers_list[-1]}')
    plt.show()


def read_numbers_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return [int(line.strip()) for line in file.readlines()]


if __name__ == '__main__':
    directory = sys.argv[1]
    numbers = read_numbers_from_file(f'{directory}/resources/graph.txt')
    draw_graph(numbers)
