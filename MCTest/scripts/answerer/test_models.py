import gensim
import dill
import model
from matrix_models import *

word_model = gensim.models.Word2Vec.load_word2vec_format('../../../data/glove.6B.50d.txt')
data_set = dill.load(open('../../sharedObjects/dataSet_mc500_train.p', 'r'))

# reload(model)
#m = model.Word2VecSentencePair(word_model)
m = WordPairContextWindowFrequency()
m.train(data_set)
m.evaluate(data_set, ['Accuracy', 
                      'OneOrMultipleAccuracy',
                      'QualityScoreAccuracy'])
print repr(m.statistics)