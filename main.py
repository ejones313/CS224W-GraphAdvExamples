import labeler
from label_propagator import LabelPropagator
from edit_dist_utils import get_all_edit_dist_one
import math
import numpy as np
from matplotlib import pyplot as plt

def compute_accuracy(predicted_labels, true_labels):
    total = 0
    num_correct = 0
    for typo in true_labels:
        total += 1
        assert typo in predicted_labels
        if math.fabs(predicted_labels[typo] - true_labels[typo]) < 0.5:
            num_correct += 1
    return num_correct, total

class Plotter():
    def __init__(self):
        plt.figure()
        plt.xlabel('Percentage of labeled vertices')
        plt.ylabel('Accuracy')
        plt.title('Adversarial Example Prediction based on Number of Labeled Vertices')
        self.legend = []

    def plot_line(self, X, Y, label):
        plt.plot(X, Y)
        self.legend.append(label)

    def save(self, filename):
        plt.legend(self.legend)
        plt.savefig(filename)

def plot_results(X, Y):
    plt.figure()
    plt.xlabel('Percentage of labeled vertices')
    plt.ylabel('Accuracy')
    plt.title('Adversarial Example Prediction based on Number of Labeled Vertices')
    plt.plot(np.array(X), np.array(Y))
    plt.savefig('fine_results.png')


def main():
    start = 'this movie was '
    word = 'fine'
    end = ''
    perturbation_types = [(1000, 'insertions'), (100, 'deletions'), (10, 'substitutions'), (1111, 'all')]
    #TODO, make plot containing all different types of typos 
    plotter = Plotter()
    n_graph_elements = len(get_all_edit_dist_one(word))
    for filetype, name in perturbation_types:
        X = []
        Y = []
        for n_label in range(10, n_graph_elements + 1, 10):
            X.append(n_label /(n_graph_elements + 1))
            typos = labeler.get_random_typos(word, n_label)
            typo2pred = labeler.get_labels(start, 'DEFAULT', end, typos)
            all_typos = labeler.get_random_typos(word, n_graph_elements)
            all_typos2pred = labeler.get_labels(start, 'DEFAULT', end, all_typos)
            lp = LabelPropagator(word, filetype = filetype) #Only use the filetype when we make edges
            lp.add_labels(typo2pred)
            new_labels = lp.propagate_labels()
            num_correct, total = compute_accuracy(new_labels, all_typos2pred)
            #print(new_labels)
            #print(all_typos2pred)
            print("{}/{} = {} correct".format(num_correct, total, num_correct / total))
            Y.append(num_correct / total)
        plotter.plot_line(X, Y, name)
    plotter.save('graphs/{}.png'.format(word))
    #print(X)
    #print(Y)
    #plot_results(X, Y)


if __name__ == '__main__':
    main()