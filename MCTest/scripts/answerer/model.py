import gensim
from scipy.spatial.distance import cosine
import numpy as np

import evaluation

class Model(object):

  def __init__(self, **kwargs):
    self.trained = False
    self.stop_words = self._stop_words_from_file()

    pass

  def _answer(self, story_question):
    """Must return answers for the four questions in one story, output format: ['A', 'A', 'A', 'A']"""
    pass

  def predict(self, data_set):
    """Will call self._answer on all stories in data_set and return a list of answer lists.
    output format: [['A', 'A', 'A', 'A'], ..., ['A', 'A', 'A', 'A']]"""
    if not self.trained:
      print "Model not trained"
      return
    all_answers = []
    for story_question in data_set.story_question_list:
      all_answers += [self._answer(story_question)]
      # break
    return all_answers

  def _process_data_set(self, data_set):
    pass

  def evaluate(self, data_set, evaluations = None):
    """Sets self.statistics for all evalutions. Evaluations must be a list of evaluation names"""
    if not self.trained:
      print "Model not trained"
      return
    if evaluations == None:
      pass
    else:
      self._process_data_set(data_set)
      predictions = self.predict(data_set)
      keys = evaluation.model_eval_dict.keys() if evaluations == 'all' else evaluations
      evals = [evaluation.model_eval_dict[key](data_set, predictions) for key in keys]
      for _eval in evals:
        _eval.evaluate()
      self.statistics = [(keys[evals.index(_eval)], _eval.statistic) for _eval in evals]

  def train(self, data_set):
    self.trained = True
    pass

  def _stop_words_from_file(self):
    """Reads the stop_words file and returns a list of stop_words"""
    try:
      stop_words_file = open('./stop_words.txt', 'r')
    except:
      print 'Could not open stop_words.txt, stop words not removed'
      return
    return [line.strip() for line in stop_words_file if line != '\n']


class WordVectorModel(Model):

  def __init__(self, word_model, **kwargs):
    Model.__init__(self, **kwargs)
    self.word_model = word_model

  def _tokenize(self, text, lower=True):
    """Returns text which is tokenized, stripped, and lowered (optional)."""
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

class Word2VecSentencePair(WordVectorModel):

  def __init__(self, word2vec_model, **kwargs):
    WordVectorModel.__init__(self, word2vec_model, **kwargs)
    self.trained = True

  def _answer(self, story_question):
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
    return answers
