"""
Edit distance utils...
"""
from collections import defaultdict
import numpy as np
import random
import string
from itertools import permutations

def process_filetype(filetype):
    insert = (filetype // 1000) % 2 == 1
    delete = (filetype // 100) % 2 == 1
    substitute = (filetype // 10) % 2 == 1
    swap = filetype % 2 == 1
    return insert, delete, substitute, swap

def get_all_edit_dist_one(word, filetype = 1111, sub_restrict = None, modify_end = False):
    """
    Allowable edit_dist_one perturbations:
        1. Insert any lowercase characer at any position other than the start
        2. Delete any character other than the first one
        3. Substitute any lowercase character for any other lowercase letter other than the start
        4. Swap adjacent characters
    We also include the original word. Filetype determines which of the allowable perturbations to use.
    """
    insert, delete, substitute, swap = process_filetype(filetype)
    #last_mod_pos is last thing you could insert before
    last_mod_pos = len(word) if modify_end else len(word) - 1
    ed1 = set()
    for pos in range(1, last_mod_pos + 1): #can add letters at the end
        if delete and pos < last_mod_pos:
            deletion = word[:pos] + word[pos + 1:]
            ed1.add(deletion)
        if swap and pos < last_mod_pos - 1:
            #swapping thing at pos with thing at pos + 1
            swaped = word[:pos] + word[pos + 1] + word[pos] + word[pos + 2:]
            ed1.add(swaped)
        for letter in string.ascii_lowercase:
            if insert:
                #Insert right after pos - 1
                insertion = word[:pos] + letter + word[pos:]
                ed1.add(insertion)
            can_substitute = sub_restrict is None or letter in sub_restrict[word[pos]]
            if substitute and pos < last_mod_pos and can_substitute:
                substitution = word[:pos] + letter + word[pos + 1:]
                ed1.add(substitution)
    #Include original word
    ed1.add(word)
    return ed1

def preprocess_ed1_neighbors(vocab, modify_end = False, sub_restrict = None, filetype = 1111):
    vocab = set([word.lower() for word in vocab])
    typo2words = defaultdict(set)
    for word in vocab:
        ed1_typos = get_all_edit_dist_one(word, filetype = filetype, sub_restrict = sub_restrict, modify_end = modify_end)
        for typo in ed1_typos:
            typo2words[typo].add(word)

    word2neighbors = defaultdict(set)
    for typo in typo2words:
        for word in typo2words[typo]:
            word2neighbors[word] = word2neighbors[word].union(typo2words[typo])
    return word2neighbors

def ed1_neighbors_mat(vocab, modify_end = False, sub_restrict = None, filetype = 1111):
    vocab = [word.lower() for word in vocab]
    word2idx = dict([(word, i) for i, word in enumerate(vocab)])
    word2neighbors = preprocess_ed1_neighbors(vocab, modify_end = modify_end, sub_restrict = sub_restrict, filetype = filetype)
    edges = set()
    for word in word2neighbors:
        for neighbor in word2neighbors[word]:
            edge = [word, neighbor]
            edge.sort()
            edge = tuple(edge)
            edges.add(edge)
    edge_mat = np.zeros((len(vocab), len(vocab)), dtype = int)
    for edge in edges:
        vtx1, vtx2 = edge
        idx1, idx2 = word2idx[vtx1], word2idx[vtx2]
        edge_mat[idx1][idx2] = 1
        edge_mat[idx2][idx1] = 1
    return edge_mat


def edit_distance(str1, str2):
    #from geeks2geeks
    m, n = len(str1), len(str2)
    dp = [[0 for x in range(n+1)] for x in range(m+1)]
    for i in range(m+1):
        for j in range(n+1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif str1[i-1] == str2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i][j-1],
                                   dp[i-1][j],
                                   dp[i-1][j-1])
    return dp[m][n]

def is_edit_distance_one_linear(s1, s2):
    #from geeks2geeks
    if s1 == s2:
        return True
    m = len(s1)
    n = len(s2)
    if abs(m - n) > 1:
        return False
    count = 0
    i = 0
    j = 0
    while i < m and j < n:
        # If current characters dont match
        if s1[i] != s2[j]:
            if count == 1:
                return False
            if m > n:
                i+=1
            elif m < n:
                j+=1
            else:
                i+=1
                j+=1
            count+=1
            if count > 1:
                return False
        else:
            i+=1
            j+=1
    if i < m or j < n:
        count+=1
    return count == 1

if __name__ == '__main__':
    #vocab = ['plain', 'pin', 'panda']
    #w2n = preprocess_ed1_neighbors(vocab)
    #print(w2n)
    #e = ed1_neighbors_mat(vocab)
    #print(e)
    while True:
        word = input("Enter a word: ")
        print("Total number of words: {}".format(len(get_all_edit_dist_one(word))))


    """
    a = get_all_edit_dist_one('bots', modify_end = False, filetype = 1111)
    print(a)
    print(len(a))
    print('bos' in a)
    """
