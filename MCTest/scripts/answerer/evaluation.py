import matplotlib


eval_dict = {'accuracy': [BucketAccuracy, accuracy], 
             'oneOrMultipleAccuracy': [BucketAccuracy, oneOrMultipleAccuracy],
             'qualityScoreAccuracy': [BucketAccuracy, qualityScoreAccuracy]}

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

  def __init__(self, data_set, predictions, func_handle):
    EvaluationBase.__init__(self, data_set, predictions)
    self.bucketed_results, self.buckets_list, self.bucket_totals = func_handle(data_set, predictions, self.correct_answers)


  def evaluate(self):
    num_correct = [0 for i in range(0,len(self.buckets_list))]
    for i in range(0, len(self.data_set.story_question_list)):
      for j in range(0,4):
        if self.predictions[i][j] == self.correct_answers[i][j]:
          num_correct[self.buckets_list.index(self.bucketed_results[i][j])] += 1
    self.statistic = [float(num_correct[i])/(self.bucket_totals[i]) for i in range(0, len(self.buckets_list))]

  def plot(self):
    pass


def accuracy(data_set, predictions, correct_answers):
  buckets = [0,1]
  bucketed_results = []
  for i in range(0, len(data_set.story_question_list)):
      story_results = []
      for j in range(0,4):
        if predictions[i][j] == correct_answers[i][j]:
          story_results.append(1)
        else:
          story_results.append(0)
      bucketed_results.append(story_results)
  return bucketed_results, buckets, 
  [len(filter(lambda x: x == z, [y for inner in bucketed_results for y in inner])) for z in buckets]


def oneOrMultipleAccuracy(data_set, predictions, correct_answers):
  buckets = ['one', 'multiple']
  bucketed_results = []
  for i in range(0, len(data_set.story_question_list)):
    story_results = []
    for j in range(0,4):
      story_results.append(data_set.story_question_list[i].questions_list[j].one_or_multiple)
    bucketed_results.append(story_results)
  return bucketed_results, buckets,
    [len(filter(lambda x: x == z, [y for inner in bucketed_results for y in inner])) for z in buckets]


def qualityScoreAccuracy(data_set, predictions, correct_answers):
  buckets = [80, 85, 90, 95, 100]
  bucketed_results = []
  for i in range(0, len(data_set.story_question_list)):
    story_results = []
    for j in range(0,4):
      story_results.append(data_set.story_question_list[i].story.quality_score)
    bucketed_results.append(story_results)
  return bucketed_results, buckets,
    [len(filter(lambda x: x == z, [y for inner in bucketed_results for y in inner])) for z in buckets]



