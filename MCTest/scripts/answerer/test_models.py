import gensim
import dill
from model import *
from ensemble_methods import *
from matrix_models import *

word_model = gensim.models.Word2Vec.load_word2vec_format('../../../data/glove.6B.50d.txt')
data_set = dill.load(open('../../sharedObjects/dataSet_mc500_train.p', 'r'))

# reload(model)
m1 = Word2VecSentencePair(word_model)
m2 = WordPairContextWindowFrequency()

m = EnsembleMax(m1, m2)

m.train(data_set)
m.evaluate(data_set, ['Accuracy', 
                      'OneOrMultipleAccuracy',
                      'QualityScoreAccuracy'])
print repr(m.statistics)
print repr(m.diversity_matrix)