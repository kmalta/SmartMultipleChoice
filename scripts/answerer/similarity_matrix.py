from answerer import AnswerStrategy
from scipy.spatial.distance import cosine
import numpy as np

def tokenize(text):
  return " ".join(gensim.utils.tokenize(text, lower=True))

class SimilarityMatrixStrategy(AnswerStrategy):
  def __init__(self, data_set_obj, model):
    AnswerStrategy.__init__(sef, data_set_obj, model)
    pass
  
  def answer(self, question_class):
    pass

  def __similarity_matrices(self, question_class):
    pass

  def __similarity_matrix(self, question, q_keywords, answers, a_keywords):
    pass
  
  def __tokenize(self, text):
    return " ".join(gensim.utils.tokenize(text, lower=True))

def matrixify(q_vecs, a_vecs):
  array_matrix = []
  for q_vec in q_vecs:
    row = []
    for a_vec in a_vecs:
      row.append(cosine(q_vec, a_vec))
    array_matrix.append(row)
  return np.matrix(array_matrix)

def ExtractMatrices(glove_model, question_class):
  # Generate array of keyword vectors
  q_vecs = []
  for key in question_class.keywords.keys():
    q_vecs.append(glove_model.infer_vector(key))

  answers = [question_class.answer_a, question_class.answer_b,
             question_class.answer_c, question_class.answer_d]

  result_matrices = []
  # Generate answer keyword vectors
  for answer in answers:
    a_vecs = []
    for keyword in answer.keywords.keys():
      a_vecs.append(glove_model.infer_vector(keyword))
    result_matrices.append(matrixify(q_vecs, avecs))

  return result_matrices

def TrainModel(data_set_obj, glove_model):
  for question_class in data_set_obj.questions_list:
    q_vec = glove_model.infer_vector(tokenize(question_class.question))
    answers = [question_class.answer_a, question_class.answer_b,
               question_class.answer_c, question_class.answer_d]
    answer_vecs = [glove_model.infer_vector(tokenize(answer.text)) for answer in answers]
