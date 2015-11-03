import sys
import answerer
from answerer import BaselineStrategy, BaselineRandomStrategy, NaiveStrategy, KeywordEqualWeightStrategy
from answerer import KeywordConfidenceStrategy, TopicWeightedKeywordSumStrategy, TopicWeightedNaiveSumStrategy
from answerer import Doc2VecStrategy
from evaluate import EvaluateStrategy
from qbc import QueryByCommitteeWeighted, QueryByCommitteeKOTH
import gensim
import dill as pickle

#GLOBALS

strategy_classes = [
'NaiveStrategy',
#'Doc2VecStrategy',
'KeywordEqualWeightStrategy',
'KeywordConfidenceStrategy',
'TopicWeightedKeywordSumStrategy',
'TopicWeightedNaiveSumStrategy',
]

qbc_classes = [
'QueryByCommitteeWeighted',
'QueryByCommitteeKOTH'
]

DATA_SET_PICKLE_FILE = '../sharedObjects/data_set_with_question_stats_11_1_15.p'




def main(argv):
  f = open(DATA_SET_PICKLE_FILE, 'r')
  data_set_obj = pickle.load(f)
  f.close()

  w2v_dims = argv[0]
  if w2v_dims in ['50', '100', '200', '300']:
    print "Loading w2v model..."
    model = gensim.models.Word2Vec.load_word2vec_format("../data/glove.6B." + w2v_dims + "d.txt")
  else:
    print "Incorrect number of dimensions specified for word2vec model."
    return

  run_strategies(data_set_obj, model)
  # run_qbc_strategies(data_set_obj, model)


def run_strategies(data_set_obj, model):
  for strategy in strategy_classes:
    strat_class = getattr(answerer, strategy)
    obj = strat_class(data_set_obj, model)
    eval_obj = EvaluateStrategy(obj)
    eval_obj.run_evaluation()
    eval_obj.print_stats()

def run_qbc_strategies(data_set_obj, model):
  for strategy in qbc_classes:
    qbc_class = getattr(answerer, strategy)
    obj = qbc_class(strategy_classes, data_set_obj, model)
    eval_obj = EvaluateStrategy(obj)
    eval_obj.run_evaluation()
    eval_obj.print_stats()

if __name__ == '__main__':
  main(sys.argv[1:])
