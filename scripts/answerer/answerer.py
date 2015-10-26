import csv

class MultipleChoiceQuestion(object):
  
  def __init__(self, init_values):
    self.id = init_values['id']
    self.correctAnswer = init_values['correctAnswer']
    self.question = init_values['question']
    self.answerA = init_values['answerA']
    self.answerB = init_values['answerB']
    self.answerC = init_values['answerC']
    self.answerD = init_values['answerD']

class AnswerStrategy(object):

  def __init__(self):
    pass

  def answer(self, mc):
    pass

class NaiveStrategy(AnswerStrategy):

  def __init__(self):
    pass
  
  def answer(self, mc):
    """TODO: Implement this"""
    return ('A', mc.answerA)

class Answerer(object):
  
  def __init__(self, strategy):
    self._strategy = strategy

  def answer(self, mc):
    return self._strategy.answer(mc)

if __name__ == '__main__':
  pass
  
