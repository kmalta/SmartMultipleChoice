import sys
sys.path.append('../')
sys.path.append('./')
from answerer import *

class EvaluateStrategy(object):

  def __init__(self, strategy):
    self.strategy = strategy
    self.data_set_len = len(self.strategy.data_set_obj.questions_list)

  def run_evaluation(self, data_set_obj = None):

    if data_set_obj == None:
      data_set_obj = self.strategy.data_set_obj
    for question in data_set_obj.questions_list:
      question.prediction = self.strategy.answer(question)

    self.run_stats()

  def run_stats(self):
    correct = 0
    incorrect = 0

    correct_sum_keyword_confidence = 0
    incorrect_sum_keyword_confidence = 0

    correct_sum_unrecognized_words = 0
    incorrect_sum_unrecognized_words = 0

    total_correct_fill_in_the_blank = 0
    total_incorrect_fill_in_the_blank = 0

    correct_sum_word_count = 0
    incorrect_sum_word_count = 0

    total_correct_contains_nums = 0
    total_incorrect_contains_nums = 0

    total_question_types_correct = 0
    total_statement_types_correct = 0
    total_answer_finisher_types_correct = 0

    total_question_types_incorrect = 0
    total_statement_types_incorrect = 0
    total_answer_finisher_types_incorrect = 0

    for question in self.strategy.data_set_obj.questions_list:
        if question.prediction == question.correct_answer:
          correct += 1
          correct_sum_keyword_confidence += question.ave_keyword_confidence
          correct_sum_unrecognized_words += question.ratio_unrecognized_words
          correct_sum_word_count += question.word_count

          if question.fill_in_the_blank == True:
            total_correct_fill_in_the_blank += 1
          
          if question.contains_numbers == True:
            total_correct_contains_nums += 1

          if question.type == 'question':
            total_question_types_correct += 1
          elif question.type == 'statement':
            total_statement_types_correct += 1
          elif question.type == 'answer_finisher':
            total_answer_finisher_types_correct += 1

        else:
          incorrect += 1
          incorrect_sum_keyword_confidence += question.ave_keyword_confidence
          incorrect_sum_unrecognized_words += question.ratio_unrecognized_words
          incorrect_sum_word_count += question.word_count

          if question.fill_in_the_blank == True:
            total_incorrect_fill_in_the_blank += 1
          
          if question.contains_numbers == True:
            total_incorrect_contains_nums += 1

          if question.type == 'question':
            total_question_types_incorrect += 1
          elif question.type == 'statement':
            total_statement_types_incorrect += 1
          elif question.type == 'answer_finisher':
            total_answer_finisher_types_incorrect += 1

    self.correct = correct
    self.incorrect = incorrect

    self.question_types = total_question_types_correct + total_question_types_incorrect
    self.statement_types = total_statement_types_correct + total_statement_types_incorrect
    self.answer_finisher_types = total_answer_finisher_types_correct + total_answer_finisher_types_incorrect

    self.total_accuracy = float(correct)/self.data_set_len
    self.ave_keyword_confidence = [float(correct_sum_keyword_confidence)/self.correct, float(incorrect_sum_keyword_confidence)/self.incorrect]
    self.ave_ratio_unrecognized_words = [float(correct_sum_unrecognized_words)/self.correct, float(incorrect_sum_unrecognized_words)/self.incorrect]
    self.ave_word_count = [float(correct_sum_word_count)/self.correct, float(incorrect_sum_word_count)/self.incorrect]
    self.ave_contains_numbers = [float(total_correct_contains_nums)/self.correct, float(total_incorrect_contains_nums)/self.incorrect]
    self.ave_fill_in_the_blank = [float(total_correct_fill_in_the_blank)/self.correct, float(total_incorrect_fill_in_the_blank)/self.incorrect]
    self.question_type_accuracy = float(total_question_types_correct)/self.question_types
    self.statement_type_accuracy = float(total_statement_types_correct)/self.statement_types
    self.answer_finisher_type_accuracy = float(total_answer_finisher_types_correct)/self.answer_finisher_types

  def print_stats(self):
    print "##########################################################################################################"
    print "############################################ STRATEGY RESULTS ############################################"
    print "##########################################################################################################"
    print "\n\n"
    print "Class:", str(type(self.strategy).__name__)
    print "\n"
    print "total/number correct/number incorrect:", str(self.data_set_len), str(self.correct), str(self.incorrect)
    print "number of each type (question, statement, answer_finisher):", str(self.question_types), str(self.statement_types), str(self.answer_finisher_types)
    print "\n"
    print "accuracy:", str(self.total_accuracy)
    print "question type accuracy:", str(self.question_type_accuracy)
    print "statement type accuracy:", str(self.statement_type_accuracy)
    print "answer finisher type accuracy:", str(self.answer_finisher_type_accuracy)
    print "\n"
    print "ave keyword confidence (correct, incorrect):", str(self.ave_keyword_confidence[0]), str(self.ave_keyword_confidence[1])
    print "ave unrecognized words (correct, incorrect):", str(self.ave_ratio_unrecognized_words[0]), str(self.ave_ratio_unrecognized_words[1])
    print "ave word count (correct, incorrect):", str(self.ave_word_count[0]), str(self.ave_word_count[1])
    print "ave contains numbers (correct, incorrect):", str(self.ave_contains_numbers[0]), str(self.ave_contains_numbers[1])
    print "ave fill in the blank (correct, incorrect):", str(self.ave_fill_in_the_blank[0]), str(self.ave_fill_in_the_blank[1])
    print "\n\n\n"



