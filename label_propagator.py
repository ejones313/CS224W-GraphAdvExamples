import construct_graph
import numpy as np 

class LabelPropagator():
	def __init__(self, word):
		nodes, edges = construct_graph.construct_graph(word)
		self.idx2neighbors = construct_graph.construct_neighbor_map(nodes, edges)
		self.nodes = nodes
		self.edges = edges 

	def add_labels(self, label_map):
		self.hard_labels = label_map 

	def propagate_labels(self, n_iters = 100):
		num_nodes = len(self.nodes)
		current_labels = np.ones(num_nodes) / 2
		for idx in label_map:
			current_labels[idx] = self.hard_labels[idx]

		for i in range(num_nodes):
			if i not in self.hard_labels:
				neighbor_mean = current_labels[self.idx2neighbors[i]].mean()
				current_labels[i] = neighbor_mean

		self.labels = current_labels 
		return current_labels

