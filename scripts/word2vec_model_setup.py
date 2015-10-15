from gensim.models import Word2Vec
from gensim.corpora import WikiCorpus
from gensim.models.word2vec import LineSentence
import numpy as np
import cPickle
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def load_corpus():
    with open('../../data_set/wiki_en') as f:
        corpus = f.read()
        return corpus


def train_model():
    corpus = load_corpus()
    model = word2vec.Word2Vec(corpus, workers=4,
                size=500, min_count = 5,
                window = 50, sample = 1e-5)

    model.init_sims(replace=True)
    save_model(model)

def save_model(model):
    model.save('../models/word2vec_wiki_model')

#RUNS THE MODEL TRAINING
#WARNING: THIS SHIT WILL TAKE FOREVER
train_model()
