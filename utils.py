import os
import biLstm_char_only
from nltk.corpus import stopwords as SW
from collections import defaultdict
import string
import pickle
import numpy as np 


MODEL_DIR = '/Users/erikjones/Documents/Stanford 2019:20/Autumn CS224W/Project/Adversarial-Misspellings/model_dumps'


def load_model():
	model = biLstm_char_only.BiLSTM()
	model_path = os.path.join(MODEL_DIR, 'bilstm-char-only')
	trainer = model.build_model(nwords, nchars, ntags)
	model.load(model_path)
	return model 

def predict(word_indices, char_indices):
    scores = model.calc_scores(word_indices, char_indices)
    pred = np.argmax(scores.npvalue())
    return pred

def get_word_and_char_indices(line, w2i, c2i):
    words = [x for x in line.split(" ")]
    word_idxs = [w2i[x] for x in line.split(" ")]
    char_idxs = []
    for word in words: char_idxs.append([c2i[i] for i in word])
    return word_idxs, char_idxs

def load_w2idx(w2idx_dir = 'vocab_dumps'):
	with open(os.path.join(w2idx_dir, 'w2i.pkl')) as f:
            w2i = pickle.load(f)
	with open(os.path.join(w2idx_dir, 'c2i.pkl')) as f:
            c2i = pickle.load(f)
        return w2i, c2i
		

if __name__ == '__main__':
	#model = load_model()
	#print(model)
	load_w2idx()
