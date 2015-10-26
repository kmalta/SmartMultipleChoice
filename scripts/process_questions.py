from answerer import Answerer, NaiveStrategy, MultipleChoiceQuestion

import csv

QUESTIONS_FILE = '../sharedObjects/training_set.tsv'

def check_answer(mc, answer):
  result = "CORRECT" if mc.correctAnswer == answer else "INCORRECT"
  return result

def answer_questions(question_file):
  with open(question_file, 'r') as questions:
    reader = csv.DictReader(questions, delimiter='\t')
    question_answerer = Answerer(NaiveStrategy())
    for row in reader:
      mc = MultipleChoiceQuestion(row)
      answer = question_answerer.answer(mc)
      print "--------------------"
      print mc.question
      print check_answer(mc, answer[0]), '     ', answer
     
if __name__ == '__main__':
  answer_questions(QUESTIONS_FILE)
