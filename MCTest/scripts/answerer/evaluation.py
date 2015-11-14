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


class BucketAccuracy(EvaluationBase):

  def __init__(self, data_set, predictions, func_handle, buckets_list):
    EvaluationBase.__init__(self, data_set, predictions)
    self.bucketed_results, self.bucket_totals = func_handle(data_set)
    self.buckets_list = buckets_list


  def evaluate(self):
    num_correct = [0 for i in range(0,len(self.buckets_list))]
    for i in range(0, len(self.data_set.story_question_list)):
      for j in range(0,4):
        if self.predictions[i][j] == self.correct_answers[i][j]:
          num_correct[self.buckets_list.index(self.bucketed_results[i][j])] += 1
    self.statistic = [float(num_correct[i])/(self.bucket_totals[i]) for i in range(0, len(self.buckets_list))]

  def plot(self):
    pass




def accuracy(data_set):
  pass
  #return 2 things

def oneOrMultipleAccuracy(data_set):
  pass
  #return 2 things

def qualityScoreAccuracy(data_set):
  pass
  #return 2 things




