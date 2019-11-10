import utils 
import random
from edit_dist_utils import get_all_edit_dist_one


def get_labels(start, word, end, typos_to_label):
    if not start.endswith(' ') and len(start) > 0:
        start = start + ' '
    if not end.startswith(' ') and len(end) > 0:
        end = ' ' + end

    w2i, c2i = utils.load_w2idx()
    model = utils.load_model(len(w2i), len(c2i), 2)
    lines = ['{}{}{}'.format(start, typo, end) for typo in typos_to_label]
    preds = []

    for line in lines:
        word_indices, char_indices = utils.get_word_and_char_indices(line, w2i, c2i)
        pred = utils.predict(model, word_indices, char_indices)
        preds.append(int(pred))

    typo2pred = {}
    for typo, pred in zip(typos_to_label, preds):
        typo2pred[typo] = pred
    return typo2pred

def get_random_typos(word, n = 10):
    all_typos = get_all_edit_dist_one(word)
    samples = random.sample(all_typos, n)
    return samples 

if __name__ == '__main__':
    start = 'this movie was '
    end = ''
    word = ['horrible']

    typos = get_random_typos('horrible', 100)
    typo2pred = get_labels(start, 'DEFAULT', end, typos)
    print(typo2pred)



