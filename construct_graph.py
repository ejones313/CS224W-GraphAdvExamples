from edit_dist_utils import get_all_edit_dist_one
from collections import defaultdict

def construct_graph(word):
	typo2edges = defaultdict(set)
	valid_words = set()
	ed1typos = get_all_edit_dist_one(word)
	for ed1typo in get_all_edit_dist_one(word):
		#valid_words.add(ed1typo)
		for ed2typo in get_all_edit_dist_one(ed1typo):
			#valid_words.add(ed2typo)
			if ed2typo in ed1typos and ed2typo != ed1typo:
				typo2edges[ed1typo].add(ed2typo)
	nodes = ed1typos 
	edges = set()
	for typo in typo2edges:
		for dst in typo2edges[typo]:
			if typo < dst:
				edges.add((typo, dst))
			else:
				edges.add((dst, typo))
	return nodes, edges



if __name__ == '__main__':
	while True:
		word = input("Enter a valid word: ")
		nodes, edges = construct_graph(word)
		print(len(nodes), len(edges), len(nodes) * (len(nodes) - 1)/2)

