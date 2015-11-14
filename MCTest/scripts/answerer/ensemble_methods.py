from model import Model
from data_set_class import *


class EnsembleMethod(Model):

  def __init__(self, models_for_ensemble, **kwargs):
    Model.__init__(self, kwargs)
    self.ensemble = models_for_ensemble

  def kappa_diversity(self):
    pass



class EnsembleMax(EnsembleMethod):

  def __init__(self, models_for_ensemble, **kwargs):
    EnsembleMethod.__init__(self, models_for_ensemble, kwargs)
    self.ensemble = models_for_ensemble

  def __answer(self, story_and_question):

  def predict(self, data_set):
    if self.trained == 0:
      self.train(data_set)
    return [self.__answer(saq) for saq in data_set.story_and_question_list]


  def train(self, data_set):
    for model in self.ensemble:
      if model.trained == 0:
        model.train(data_set)

    self.trained = 1