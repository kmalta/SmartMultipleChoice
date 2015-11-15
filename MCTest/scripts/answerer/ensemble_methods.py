from model import Model
import itertools
from collections import namedtuple


class EnsembleMethod(Model):

  def __init__(self, *args):
    Model.__init__(self)
    self.ensemble = [i for arg in args for i in arg]

class EnsembleMax(EnsembleMethod):

  def __init__(self, *args):
    EnsembleMethod.__init__(self, args)


  def _get_attributes(self, data_set):
    for saq in data_set.story_question_list:
      for question in saq.questions_list:
        question.attribute_tuple = (self._get_one_or_multiple(question),
                                    self._get_quality(saq.story))

  def buckets(self):
    return [['one', 'multiple'], [80, 85, 90, 95, 100]]

  def _get_quality(self, story):
    return story.quality_score

  def _get_one_or_multiple(self, question):
    return question.one_or_multiple

  def _answer(self, story_and_question):
    answers = []
    for i in range(0,4):
      answers.append(self.ensemble[self.answer_dict[story_and_question.questions_list[i].attribute_tuple]]._answer(story_and_question)[i])
    return answers


  def _create_diversity_matrix(self, predictions):
    self.diversity_matrix = []
    flat_predictions = [[i for question_predictions in model_predictions for i in question_predictions] for model_predictions in predictions]
    for i in range(0, len(self.ensemble)):
      diversity_row = []
      for j in range(0, len(self.ensemble)):
        diversity_row.append(float(len(filter(lambda x: x[0] != x[1], zip(flat_predictions[i], flat_predictions[j]))))/len(flat_predictions[0]))
      self.diversity_matrix.append(diversity_row)


  def _partition_data_set(self, data_set):
    self.partition_tuples = list(itertools.product(*self.buckets()))
    self.partition_counts = dict((el,0) for el in self.partition_tuples)
    for saq in data_set.story_question_list:
      for q in saq.questions_list:
        self.partition_counts[q.attribute_tuple] += 1

  def _create_answer_dict(self, data_set):
    predictions = [model.predict(data_set) for model in self.ensemble]
    self._create_diversity_matrix(predictions)
    self.correct_totals = []
    for i in range(0, len(self.ensemble)):
      correct = dict((el,0) for el in self.partition_tuples)
      for j in range(0, len(data_set.story_question_list)):
        for k in range(0, 4):
          if predictions[i][j][k] == self.correct_answers[j][k]:
            correct[data_set.story_question_list[j].questions_list[k].attribute_tuple] += 1
      self.correct_totals.append(correct)
    self.answer_dict = dict((tup, self._get_index_of_max(tup)) for tup in self.partition_tuples)

  def _get_index_of_max(self, tup):
    index = 0
    _max = 0
    for i in range(0, len(self.ensemble)):
      if self.correct_totals[i][tup] > _max:
        _max = self.correct_totals[i][tup]
        index = i
    return index

  def _get_correct_answers(self, data_set):
    correct_answers = []
    for story_and_question in data_set.story_question_list:
      correct_answers.append([question.correct_answer for question in story_and_question.questions_list])

    self.correct_answers = correct_answers


  def train(self, data_set):
    for model in self.ensemble:
      print model
      model.train(data_set)
    self._get_attributes(data_set)
    self._get_correct_answers(data_set)
    self._partition_data_set(data_set)
    self._create_answer_dict(data_set)
    self.trained = True

