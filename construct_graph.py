from edit_dist_utils import get_all_edit_dist_one
from collections import defaultdict
import numpy as np

def construct_graph(word, filetype = 1111):
	typo2edges = defaultdict(set)
	valid_words = set()
	ed1typos = get_all_edit_dist_one(word, filetype = filetype)
	alltypos = get_all_edit_dist_one(word)
	#Iterating through all typos in our original graph
	for ed1typo in alltypos:
		#valid_words.add(ed1typo)
		#Only adding things that appear in the perturbation of the specific typo
		for ed2typo in get_all_edit_dist_one(ed1typo, filetype = filetype):
			#valid_words.add(ed2typo)
			if ed2typo in alltypos and ed2typo != ed1typo:
				typo2edges[ed1typo].add(ed2typo)
	nodes = alltypos 
	edges = set()
	#Makes graph undirected, can possibly change
	for typo in typo2edges:
		for dst in typo2edges[typo]:
			if typo < dst:
				edges.add((typo, dst))
			else:
				edges.add((dst, typo))
	print("Filetype: {}, num edges: {}".format(filetype, len(edges)))
	return nodes, edges

def construct_neighbor_map(nodes, edges):
	idx2node = {i:node for i, node in enumerate(nodes)}
	node2idx = {node:i for i, node in enumerate(nodes)}

	node2neighbors = defaultdict(set)
	for edge in edges:
		src, dst = edge 
		src_idx, dst_idx = node2idx[src], node2idx[dst]
		node2neighbors[src_idx].add(dst_idx)
		node2neighbors[dst_idx].add(src_idx)

	for idx in node2neighbors:
		idx_set = node2neighbors[idx]
		idx_array = np.array(list(idx_set))
		node2neighbors[idx] = idx_array

	return node2neighbors, idx2node, node2idx



if __name__ == '__main__':
	while True:
		word = input("Enter a valid word: ")
		nodes, edges = construct_graph(word)
		n2n, idx2node, node2idx = construct_neighbor_map(nodes, edges)
		print(n2n)
		print(len(n2n))
