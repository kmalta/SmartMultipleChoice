import gensim
from scipy.spatial.distance import cosine, euclidean
from itertools import permutations
import traceback
import numpy as np
import random
from evalutations import *

class Model(object):

  def __init__(self, **kwargs):
    self.trained = 0
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



      else:


  def train(self, data_set):
    self.trained = 1
    pass

"""
NaiveModel example to demonstrate key word arguments (kwarg) usage
class NaiveModel(Model):

  def __init__(self, **kwargs):
    Model.__init__(self, kwargs)
    self.word2vec = kwargs['word2vec']

  def answer(self, story_and_question):
    pass

"""
