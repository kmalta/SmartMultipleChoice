import sys
import answerer
from evaluate import EvaluateStrategy
import gensim
import dill as pickle

#GLOBALS

strategy_classes = [
# 'NaiveStrategy',
# #'Doc2VecStrategy',
# 'KeywordEqualWeightStrategy',
# 'KeywordConfidenceStrategy',
# 'TopicWeightedKeywordSumStrategy',
# 'TopicWeightedNaiveSumStrategy',
'RelevancySortingStrategy',
]

qbc_classes = [
'QueryByCommitteeWeighted',
'QueryByCommitteeKOTH'
]

DATA_SET_PICKLE_FILE = '../sharedObjects/data_set_with_question_stats_11_1_15.p'


def main(argv):
  data_set_obj, model = main_loading(argv)
  if data_set_obj == 0:
    return
  run_strategies(data_set_obj, model)
  # run_qbc_strategies(data_set_obj, model)


def run_strategies(data_set_obj, model):
  for strategy in strategy_classes:
    print "Running Strategy for class:", strategy
    strat_class = getattr(answerer, strategy)
    obj = strat_class(data_set_obj, model)
    eval_obj = EvaluateStrategy(obj)
    eval_obj.run_evaluation()
    eval_obj.print_stats()

def run_qbc_strategies(data_set_obj, model):
  for strategy in qbc_classes:
    print "Running Query by Committee for class:", strategy
    qbc_class = getattr(answerer, strategy)
    obj = qbc_class(strategy_classes, data_set_obj, model)
    eval_obj = EvaluateStrategy(obj)
    eval_obj.run_evaluation()
    eval_obj.print_stats()

def main_loading(argv):
  f = open(DATA_SET_PICKLE_FILE, 'r')
  data_set_obj = pickle.load(f)
  f.close()

  w2v_dims = argv[0]
  if w2v_dims in ['50', '100', '200', '300']:
    print "Loading w2v model..."
    model = gensim.models.Word2Vec.load_word2vec_format("../data/glove.6B." + w2v_dims + "d.txt")
  else:
    print "Incorrect number of dimensions specified for word2vec model."
    return [0,0]
  return data_set_obj, model

if __name__ == '__main__':
  main(sys.argv[1:])
