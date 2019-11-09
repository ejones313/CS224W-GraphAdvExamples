import utils 


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
        print(line)
        word_indices, char_indices = utils.get_word_and_char_indices(line, w2i, c2i)
        print(char_indices)
        pred = utils.predict(model, word_indices, char_indices)
        print(type(pred))
        preds.append(pred)

    typo2pred = {}
    for typo, pred in zip(typos_to_label, preds):
        typo2pred[typo] = pred
    return typo2pred

if __name__ == '__main__':
    start = 'this movie was '
    end = ''
    typos = ['good', 'bad', 'great', 'horrible']
    typo2pred = get_labels(start, 'DEFAULT', end, typos)
    print(typo2pred)



