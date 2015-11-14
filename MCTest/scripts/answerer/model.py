import gensim
from scipy.spatial.distance import cosine
import numpy as np

from evaluation import *

class Model(object):

  def __init__(self, **kwargs):
    self.trained = 0
    self.stop_words = self._stop_words_from_file()
    pass

  def answer(self, data_set):
    pass

  def predict(self, data_set):
    self.train(data_set)
    pass

  def evaluate(self, data_set, evaluations = None):
    if not self.trained:
      print "Model not trained"
      return
    if evaluations == None:
      pass
    else:
      predictions = self.predict(data_set)
      keys = eval_dict.keys() if evaluations == 'all' else evaluations
      evals = [eval_dict[key](data_set, predictions) for key in keys]
      for _eval in evals:
        _eval.evaluate
      self.statistics = [(key, _eval.statistic) for _eval in evals]

  def train(self, data_set):
    self.trained = 1
    pass

  def _stop_words_from_file(self):
    """Reads the stop_words file and returns a list of stop_words"""
    try:
      stop_words_file = open('MCTest/scripts/answerer/stop_words.txt', 'r')
    except:
      print 'Could not open stop_words.txt, stop words not removed'
      return
    return [line.strip() for line in stop_words_file if line != '\n']

  def _tokenize(self, text, lower=True):
    """Returns text which is tokenized, stipped, and lowered (optional)."""
    r = []
    for s in gensim.utils.tokenize(text, lower=lower):
      if s not in self.stop_words:
        r += [s]
    return ' '.join(r)

  def _vectorize_and_add(self, text):
    """ Converts text to vectors using self.word_model and adds all the vectors"""
    words = text.split()
    sum = np.zeros(self.word_model.vector_size)
    for w in words:
      try:
        v = self.word_model[w]
        sum += v
      except:
        pass
    return sum

"""
NaiveModel example to demonstrate key word arguments (kwarg) usage
class NaiveModel(Model):

  def __init__(self, **kwargs):
    Model.__init__(self, kwargs)
    self.word2vec = kwargs['word2vec']

  def answer(self, story_and_question):
    pass

"""


class Word2VecSentencePair(Model):

  def __init__(self, word2vec_model):
    Model.__init__(self)
    self.word_model = word2vec_model

  def answer(self, data_set):
    """Returns a list of answers to all stories"""
    all_answers = []
    for story_question in data_set.story_question_list:
      story_sentence_vectors = [self._vectorize_and_add(self._tokenize(x)) for x in story_question.story.story_sentences]
      answers = []
      for question in story_question.questions_list:
        answer_min_cosines = []
        for answer in question.answers:
          question_answer = self._tokenize(question.question + ' ' + answer.answer)
          question_answer_vector = self._vectorize_and_add(question_answer)
          answer_cosines = []
          for story_sentence_vector in story_sentence_vectors:
            answer_cosines += [cosine(story_sentence_vector, question_answer_vector)]
          answer_min_cosines += [min(answer_cosines)]
        answers += [['A', 'B', 'C', 'D'][np.array(answer_min_cosines).argmin()]]
      all_answers += [answers]
      # break
    return all_answers