__author__ = 'angad'

import sys
from gensim.models import Doc2Vec
from gensim.models.doc2vec import TaggedLineDocument
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def main(argv):
    filename = argv[0]
    size = 100
    window = 10
    min_count = 5
    workers = 4
    documents = TaggedLineDocument(filename)
    model = Doc2Vec(documents, size, window, min_count, workers)
    model.save("doc2vec.model")


if __name__ == '__main__':
    main(sys.argv[1:])