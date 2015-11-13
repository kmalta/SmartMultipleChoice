import matplotlib

class EvaluationBase(object):

  def __init__(self, data_set, predictions):
    self.data_set = data_set
    self.predictions = predictions
    __get_correct_answers()

  def evaluate(self):
    pass

  def plot(self):
    pass

  def __get_correct_answers(self):
    correct_answers = []
    for story_and_question in self.data_set.story_question_list:
      correct_answers.append([question.correct_answer for question in story_and_question.questions_list])

    self.correct_answers = correct_answers

class Accuracy(EvaluationBase):

  def __init__(self, data_set, predictions):
    EvaluationBase.__init__(self, data_set, predictions)

  def evaluate(self):
    num_correct = 0
    for i in range(0, len(self.data_set.story_question_list)):
      for j in range(0,4):
        if self.predictions[i][j] == self.correct_answers[i][j]:
          num_correct += 1
    self.statistic = float(num_correct)/(len(self.data_set.story_question_list) * 4)

  def plot(self):
    pass


class OneVsMultipleAccuracy(EvaluationBase):

  def __init__(self, data_set, predictions):
    EvaluationBase.__init__(self, data_set, predictions)
    __setup()

  def evaluate(self):

    pass

  def __setup(self):
    one_or_multiple = []
    for story_and_question in self.data_set.story_question_list:
      one_or_multiple.append([question.one_or_multiple for question in story_and_question.questions_list])

    self.one_or_multiple = one_or_multiple

