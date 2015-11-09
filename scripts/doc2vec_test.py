__author__ = 'angad'

from answerer import Doc2VecStrategy
import gensim
import dill as pickle

DATA_SET_PICKLE_FILE = 'sharedObjects/data_set_with_question_stats_11_1_15.p'

f = open(DATA_SET_PICKLE_FILE, 'r')
data_set_obj = pickle.load(f)
f.close()

doc = Doc2VecStrategy(data_set_obj, model=gensim.models.Doc2Vec.load("doc2vec.model"))
print doc.run()
