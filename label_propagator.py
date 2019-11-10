import construct_graph
import numpy as np 

class LabelPropagator():
	def __init__(self, word):
		nodes, edges = construct_graph.construct_graph(word)
		print("Number of nodes: {}, number of edges{}/{}".format(len(nodes), len(edges), len(nodes) * (len(nodes) - 1)/2))
		self.idx2neighbors, self.idx2node, self.node2idx = construct_graph.construct_neighbor_map(nodes, edges)
		self.nodes = nodes
		self.edges = edges 

	def add_labels(self, label_map):
		self.hard_labels = {}
		for key in label_map:
			self.hard_labels[self.node2idx[key]] = label_map[key]


	def propagate_labels(self, n_iters = 100):
		num_nodes = len(self.nodes)
		current_labels = np.ones(num_nodes) / 2
		for idx in self.hard_labels:
			current_labels[idx] = self.hard_labels[idx]

		for i in range(num_nodes):
			if i not in self.hard_labels:
				neighbor_mean = current_labels[self.idx2neighbors[i]].mean()
				current_labels[i] = neighbor_mean

		self.labels = current_labels 
		node_dict = {}
		for i in range(len(self.labels)):
			node = self.idx2node[i]
			node_dict[node] = self.labels[i]
		return node_dict

