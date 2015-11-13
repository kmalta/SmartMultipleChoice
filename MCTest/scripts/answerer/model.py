import gensim
from scipy.spatial.distance import cosine, euclidean
from itertools import permutations
import traceback
import numpy as np
import random

class Model(object):

  def __init__(self, **kwargs):
    pass

  def answer(self, story_and_question):
    pass

  def evaluate(self, data_set, evaluations = None):
    if evaluations:
      pass
    else:
      # run all
      pass

  def train(self, data_set):
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
