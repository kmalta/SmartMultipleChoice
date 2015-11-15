import gensim
import dill
from model import *
from ensemble_methods import *
from matrix_models import *

word_model = gensim.models.Word2Vec.load_word2vec_format('../../../data/glove.6B.300d.txt')
data_set_train = dill.load(open('../../sharedObjects/dataSet_mc500_train.p', 'r'))
data_set_dev = dill.load(open('../../sharedObjects/dataSet_mc500_dev.p', 'r'))

# reload(model)
print "\n\n\n\n\n"
m1 = Word2VecSentencePair(word_model)
m2 = WordPairContextWindowFrequency()
m1.train(data_set_train)
m2.train(data_set_train)
m1.evaluate(data_set_dev, 'all')
print repr(m1.statistics)
print "\n\n\n\n\n"
m2.evaluate(data_set_dev, 'all')
print repr(m2.statistics)
print "\n\n\n\n\n"
m = EnsembleMax(m1, m2)
m.train(data_set_train)
m.evaluate(data_set_dev, 'all')
print repr(m.statistics)
print repr(m.diversity_matrix)