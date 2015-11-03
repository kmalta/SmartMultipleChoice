import sys
from answerer import BaselineStrategy, BaselineRandomStrategy, NaiveStrategy, KeywordEqualWeightStrategy
from answerer import KeywordConfidenceStrategy, TopicWeightedKeywordSumStrategy, TopicWeightedNaiveSumStrategy
from evaluate import EvaluateStrategy
from qbc import QueryByCommitteeWeighted, QueryByCommitteeKOTH
import gensim
import dill as pickle

strategy_classes = ['BaselineRandomStrategy', 'NaiveStrategy', 
                    'KeywordEqualWeightStrategy', 'KeywordConfidenceStrategy', 
                    'TopicWeightedKeywordSumStrategy', 'TopicWeightedNaiveSumStrategy']

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

  print "Creating qbc classes..."
  kingOfTheHill = QueryByCommitteeKOTH(strategy_classes, data_set_obj, model)
  ave = QueryByCommitteeWeighted(strategy_classes, data_set_obj, model)

  print "Training qbc objects..."
  kingOfTheHill.train(data_set_obj)
  ave.train(data_set_obj)

  print "Creating and running evaluation metrics of qbc classes..."
  evaluateKingOfTheHill = EvaluateStrategy(kingOfTheHill)
  evaluateKingOfTheHill.run_evaluation(data_set_obj)
  evaluateKingOfTheHill.print_stats()

  evaluateAve = EvaluateStrategy(ave)
  evaluateAve.run_evaluation(data_set_obj)
  evaluateAve.print_stats()




  # baselineA = BaselineStrategy(data_set_obj, model, 'A')
  # baselineB = BaselineStrategy(data_set_obj, model, 'B')
  # baselineC = BaselineStrategy(data_set_obj, model, 'C')
  # baselineD = BaselineStrategy(data_set_obj, model, 'D')
  # baselineRand = BaselineRandomStrategy(data_set_obj, model)
  # naive = NaiveStrategy(data_set_obj, model)
  # keywordsEqual = KeywordEqualWeightStrategy(data_set_obj, model)
  # keywordsConfidence = KeywordConfidenceStrategy(data_set_obj, model)
  # topicKeywordSum = TopicWeightedKeywordSumStrategy(data_set_obj, model)
  # topicNaiveSum = TopicWeightedNaiveSumStrategy(data_set_obj, model)

  # The below code creates evalutation classes to run the strategies
  # and print the appropriate stats

  # evaluateNaive = EvaluateStrategy(naive)
  # evaluateNaive.run_evaluation()
  # evaluateNaive.print_stats()

  # evaluateKeywordsEqual = EvaluateStrategy(keywordsEqual)
  # evaluateKeywordsEqual.run_evaluation()
  # evaluateKeywordsEqual.print_stats()

  # evaluateKeywordsConfidence = EvaluateStrategy(keywordsConfidence)
  # evaluateKeywordsConfidence.run_evaluation()
  # evaluateKeywordsConfidence.print_stats()

  # evaluateTopicKeywordSum = EvaluateStrategy(topicKeywordSum)
  # evaluateTopicKeywordSum.run_evaluation()
  # evaluateTopicKeywordSum.print_stats()

  # evaluateTopicNaiveSum = EvaluateStrategy(topicNaiveSum)
  # evaluateTopicNaiveSum.run_evaluation()
  # evaluateTopicNaiveSum.print_stats()


if __name__ == '__main__':
  main(sys.argv[1:])
