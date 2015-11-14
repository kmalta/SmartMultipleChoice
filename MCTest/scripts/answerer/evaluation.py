import matplotlib

class EvaluationBase(object):

  def __init__(self, data_set, predictions):
    self.data_set = data_set
    self.predictions = predictions
    self._get_correct_answers()

  def evaluate(self):
    pass

  def plot(self):
    pass

  def _get_correct_answers(self):
    correct_answers = []
    for story_and_question in self.data_set.story_question_list:
      correct_answers.append([question.correct_answer for question in story_and_question.questions_list])

    self.correct_answers = correct_answers


class BucketAccuracy(EvaluationBase):

  def __init__(self, data_set, predictions):
    EvaluationBase.__init__(self, data_set, predictions)

  def evaluate(self):
    num_correct = [0 for i in range(0,len(self.buckets))]
    for i in range(0, len(self.data_set.story_question_list)):
      for j in range(0,4):
        if self.predictions[i][j] == self.correct_answers[i][j]:
          num_correct[self.buckets.index(self.bucketed_results[i][j])] += 1
    self.statistic = [float(num_correct[i])/(self.bucket_totals[i]) for i in range(0, len(self.buckets))]

  def _make_bucket_totals(self, buckets, bucketed_results):
    self.bucket_totals = [len(filter(lambda x: x == z, [y for inner in bucketed_results for y in inner])) for z in buckets]


  def plot(self):
    pass


class Accuracy(BucketAccuracy):

  def __init__(self, data_set, predictions):
    BucketAccuracy.__init__(self, data_set, predictions)
    self._setup(data_set, predictions)

  def _setup(self, data_set, predictions):
    buckets = [0,1]
    print repr(predictions), repr(self.correct_answers)
    bucketed_results = []
    for i in range(0, len(data_set.story_question_list)):
        story_results = []
        for j in range(0,4):
          if predictions[i][j] == self.correct_answers[i][j]:
            story_results.append(1)
          else:
            story_results.append(0)
        bucketed_results.append(story_results)
    self.bucketed_results = bucketed_results
    self.buckets = buckets
    self._make_bucket_totals(buckets, bucketed_results)



class OneOrMultipleAccuracy(BucketAccuracy):

  def __init__(self, data_set, predictions):
    BucketAccuracy.__init__(self, data_set, predictions)
    self._setup(data_set, predictions)

  def _setup(self, data_set, predictions):
    buckets = ['one', 'multiple']
    bucketed_results = []
    for i in range(0, len(data_set.story_question_list)):
      story_results = []
      for j in range(0,4):
        story_results.append(data_set.story_question_list[i].questions_list[j].one_or_multiple)
      bucketed_results.append(story_results)
    self.bucketed_results = bucketed_results
    self.buckets = buckets
    self._make_bucket_totals(buckets, bucketed_results)

class QualityScoreAccuracy(BucketAccuracy):

  def __init__(self, data_set, predictions):
    BucketAccuracy.__init__(self, data_set, predictions)
    self._setup(data_set, predictions)

  def _setup(self, data_set, predictions):
    buckets = [80, 85, 90, 95, 100]
    bucketed_results = []
    for i in range(0, len(data_set.story_question_list)):
      story_results = []
      for j in range(0,4):
        story_results.append(data_set.story_question_list[i].story.quality_score)
      bucketed_results.append(story_results)
    self.bucketed_results = bucketed_results
    self.buckets = buckets
    self._make_bucket_totals(buckets, bucketed_results)

# class EnsembleEvaluationBase(EvaluationBase):
#
#   def __init__(self, data_set, models):
#     EvaluationBase.__init__(self, data_set, predictions)
#     self.models = models
#
#   def evaluate(self):
#

# Define after the classes
model_eval_dict = {'Accuracy': Accuracy,
                   'OneOrMultipleAccuracy': OneOrMultipleAccuracy,
                   'QualityScoreAccuracy': QualityScoreAccuracy}
