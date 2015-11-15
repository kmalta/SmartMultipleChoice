from model import Model
from data_set_class import *


class EnsembleMethod(Model):

  def __init__(self, models_for_ensemble, **kwargs):
    Model.__init__(self, kwargs)
    self.ensemble = models_for_ensemble
    self.trained = 0

  def evaluate(self):
    if self.trained == 0:
      "Models in ensemble not trained"
      return

  def kappa_diversity(self):
    pass



class EnsembleMax(EnsembleMethod):

  def __init__(self, models_for_ensemble, **kwargs):
    EnsembleMethod.__init__(self, models_for_ensemble, kwargs)
    self.ensemble = models_for_ensemble

  def _answer(self, story_and_question):
    buckets = self._list_of_buckets()
    question_attribute_list = self._get_attributes(story_and_quesiton)
    answers = []
    for i in range(0,4):
      for j in range(0, len(question_attribute_list)):




  def _get_attributes(self, story_and_quesiton):
    attribute_list = []
    for question in story_and_question.questions_list:
      attribute_list.append([self._get_quality(story_and_question(story)), 
                             self._get_one_or_multiple(question)])
    return attribute_list

  def buckets(self):
    return [['one', 'multiple'], [80, 85, 90, 95, 100]]

  def _get_quality(self, story):
    return story.quality_score

  def _get_one_or_multiple(self, question):
    return question.one_or_multiple

  def predict(self, data_set):
    if self.trained == 0:
      self.train(data_set)
    return [self.__answer(saq) for saq in data_set.story_and_question_list]

  def train(self, data_set):
    for model in self.ensemble:
      model.train(data_set)
    self.trained = 1
    self._partition_data_set(data_set)
    self._create_answer_dict()


  def _partition_data_set(self, data_set):
    
    predictions = self.predict(data_set)
    keys = evaluation.model_eval_dict.keys() if evaluations == 'all' else evaluations
    evals = [evaluation.model_eval_dict[key](data_set, predictions) for key in keys]
    for _eval in evals:
      _eval.evaluate()
    self.statistics = [(keys[evals.index(_eval)], _eval.statistic) for _eval in evals]