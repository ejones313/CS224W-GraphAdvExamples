import labeler
from label_propagator import LabelPropagator


def main():
    start = 'this movie was '
    word = 'fine'
    end = ''
    typos = labeler.get_random_typos(word, 100)
    typo2pred = labeler.get_labels(start, 'DEFAULT', end, typos)
    lp = LabelPropagator(word)
    lp.add_labels(typo2pred)
    new_labels = lp.propagate_labels()
    print(new_labels)


if __name__ == '__main__':
    main()