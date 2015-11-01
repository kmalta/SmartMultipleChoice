import sys
from answerer import BaselineStrategy, BaselineRandomStrategy, NaiveStrategy, KeywordEqualWeightStrategy
from answerer import KeywordConfidenceStrategy, TopicWeightedKeywordSumStrategy, TopicWeightedNaiveSumStrategy
from evaluate import EvaluateStrategy
import gensim
import dill as pickle

DATA_SET_PICKLE_FILE = '../sharedObjects/data_set_with_question_stats_11_1_15.p'

def main(argv):
  f = open(DATA_SET_PICKLE_FILE, 'r')
  data_set_obj = pickle.load(f)
  f.close()

  w2v_dims = argv[0]
  if w2v_dims in ['50', '100', '200', '300']:
    model = gensim.models.Word2Vec.load_word2vec_format("../data/glove.6B." + w2v_dims + "d.txt")
  else:
    print "Incorrect number of dimensions specified for word2vec model."
    return

  # baselineA = BaselineStrategy(data_set_obj, model, 'A')
  # baselineB = BaselineStrategy(data_set_obj, model, 'B')
  # baselineC = BaselineStrategy(data_set_obj, model, 'C')
  # baselineD = BaselineStrategy(data_set_obj, model, 'D')
  # baselineRand = BaselineRandomStrategy(data_set_obj, model)
  # naive = NaiveStrategy(data_set_obj, model)
  # keywordsEqual = KeywordEqualWeightStrategy(data_set_obj, model)
  # keywordsConfidence = KeywordConfidenceStrategy(data_set_obj, model)
  topicKeywordSum = TopicWeightedKeywordSumStrategy(data_set_obj, model)
  # topicNaiveSum = TopicWeightedNaiveSumStrategy(data_set_obj, model)

  evaluateKeywordsConfidence = EvaluateStrategy(topicKeywordSum)
  evaluateKeywordsConfidence.run_evaluation()

  # print "Baseline A Strategy:", str(baselineA.run())
  # print "Baseline B Strategy:", str(baselineB.run())
  # print "Baseline C Strategy:", str(baselineC.run())
  # print "Baseline D Strategy:", str(baselineD.run())
  # print "Baseline Random Strategy:", str(baselineRand.run())
  # print "Naive Strategy:", str(naive.run())
  # print "Keyword Equal Strategy:", str(keywordsEqual.run())
  # print "Keyword Confidence Strategy:", str(keywordsConfidence.run())
  # print "Topic Weight Keyword Strategy:", str(topicKeywordSum.run())
  # print "Topic Weight Naive Strategy:", str(topicNaiveSum.run())


if __name__ == '__main__':
  main(sys.argv[1:])
