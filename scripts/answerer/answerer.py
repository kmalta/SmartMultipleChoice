import csv
import gensim
from scipy.spatial.distance import cosine
import numpy as np

class MultipleChoiceQuestion(object):
  
  def __init__(self, init_values):
    self.id = init_values['id']
    self.correctAnswer = init_values['correctAnswer']
    self.question = init_values['question']
    self.answerA = init_values['answerA']
    self.answerB = init_values['answerB']
    self.answerC = init_values['answerC']
    self.answerD = init_values['answerD']

class AnswerStrategy(object):

  def __init__(self):
    pass

  def answer(self, mc):
    pass

class NaiveStrategy(AnswerStrategy):

  def __init__(self):
    print "Initializing strategy..."
    self.model = gensim.models.Word2Vec.load_word2vec_format("data/glove.6B.50d.txt")
    # Stop list is the top 14 most frequent words from training_set.tsv
    self.stop_list = set('the of a to in is and which that are an on from'.split())
    print "Done!"

  def answer(self, mc):
    q_sum = self.__tokenize_and_add(mc.question)
    options = [mc.answerA, mc.answerB, mc.answerC, mc.answerD]
    cos = np.array([cosine(q_sum, self.__tokenize_and_add(x)) for x in options])
    return ['A', 'B', 'C', 'D'][cos.argmax()]

  def __tokenize_and_add(self, sentence):
    sentence_sum = np.zeros(self.model.vector_size)
    for s in gensim.utils.tokenize(sentence):
      try:
        if s not in self.stop_list:
          v = self.model[s.lower()]
          sentence_sum += v
      except:
        pass
    return sentence_sum

  def test(self, data):
    # TODO: Data here is a Pandas dataframe. Need to change this to a list of MultipleChoiceQuestion class
    print "Testing data..."
    predictions = []
    for row in xrange(data.shape[0]):
      mc = MultipleChoiceQuestion(data.loc[row, :])
      predictions += [a.answer(mc) == data.loc[row, 'correctAnswer']]
    accuracy = np.mean(predictions)
    print "Done!"
    return accuracy


class Answerer(object):
  
  def __init__(self, strategy):
    self._strategy = strategy

  def answer(self, mc):
    return self._strategy.answer(mc)

  def test(self, data):
    return self._strategy.test(data)

if __name__ == '__main__':
  pass
  
