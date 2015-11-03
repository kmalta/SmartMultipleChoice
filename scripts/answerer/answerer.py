import gensim
from scipy.spatial.distance import cosine
import numpy as np
import random

class AnswerStrategy(object):

  def __init__(self, data_set_obj, model):
    self.data_set_obj = data_set_obj
    self.model = model


  def answer(self, question_class):
    pass

  def run(self):
    # TODO: Data here is a Pandas dataframe. Need to change this to a list of MultipleChoiceQuestion class
    predictions = []
    for question in self.data_set_obj.questions_list:
      predictions += [ self.answer(question) == question.correct_answer ]
    accuracy = np.mean(predictions)
    return accuracy



class BaselineStrategy(AnswerStrategy):

  def __init__(self, data_set_obj, model, letter):
    AnswerStrategy.__init__(self, data_set_obj, model)
    self.auto_answer = letter

  def answer(self, question_class):
    return self.auto_answer

class BaselineRandomStrategy(AnswerStrategy):

  def __init__(self, data_set_obj, model):
    AnswerStrategy.__init__(self, data_set_obj, model)

  def answer(self, question_class):
    return ['A', 'B', 'C', 'D'][random.randrange(0,3,1)]


class NaiveStrategy(AnswerStrategy):

  def __init__(self, data_set_obj, model):
    AnswerStrategy.__init__(self, data_set_obj, model)
    # Stop list is the top 14 most frequent words from training_set.tsv
    self.stop_list = set('the of a to in is and which that are an on from'.split())

  def answer(self, question_class):
    q_vec = self.__tokenize_and_add(question_class.question)
    options = [question_class.answer_a, question_class.answer_b, question_class.answer_c, question_class.answer_d]
    cos = np.array([cosine(q_vec, self.__tokenize_and_add(x.text)) for x in options])
    return ['A', 'B', 'C', 'D'][cos.argmin()]

  def __tokenize_and_add(self, text):
    text_vec_sum = np.zeros(self.model.vector_size)
    for s in gensim.utils.tokenize(text):
      try:
        if s not in self.stop_list:
          vec = self.model[s.lower()]
          text_vec_sum += vec
      except:
        pass
    return text_vec_sum


class Doc2VecStrategy(AnswerStrategy):

  def __init__(self, data_set_obj, model):
    AnswerStrategy.__init__(self, data_set_obj, model)

  def answer(self, question_class):
    q_vec = self.model.infer_vector(self._tokenize(question_class.question))
    options = [question_class.answer_a, question_class.answer_b, question_class.answer_c, question_class.answer_d]
    cos = np.array([cosine(q_vec, self.model.infer_vector(self._tokenize(x.text))) for x in options])
    return ['A', 'B', 'C', 'D'][cos.argmin()]

  def _tokenize(self, text):
    return " ".join(gensim.utils.tokenize(text, lower=True))


class KeywordEqualWeightStrategy(AnswerStrategy):

  def __init__(self, data_set_obj, model):
    AnswerStrategy.__init__(self, data_set_obj, model)

  def answer(self, question_class):
    q_vec = self.__keyword_sum(question_class.question, question_class.keywords)
    options = [question_class.answer_a, question_class.answer_b, question_class.answer_c, question_class.answer_d]
    cos = np.array([cosine(q_vec, self.__keyword_sum(x.text, x.keywords)) for x in options])
    predicted_answer = ['A', 'B', 'C', 'D'][cos.argmin()]

    return predicted_answer

  def __keyword_sum(self, text, keyword_dict):
    short_text_summary = np.zeros(self.model.vector_size)
    keywords = keyword_dict.keys()
    for key in keywords:
      try:
        if keyword_dict[key] > 0.05:
          vec = self.model[key.lower()]
          short_text_summary += vec
      except:
        pass
    return short_text_summary


class KeywordConfidenceStrategy(AnswerStrategy):

  def __init__(self, data_set_obj, model):
    AnswerStrategy.__init__(self, data_set_obj, model)

  def answer(self, question_class):
    q_vec = self.__keyword_linear_combination(question_class.question, question_class.keywords)
    options = [question_class.answer_a, question_class.answer_b, question_class.answer_c, question_class.answer_d]
    cos = np.array([cosine(q_vec, self.__keyword_linear_combination(x.text, x.keywords)) for x in options])
    return ['A', 'B', 'C', 'D'][cos.argmin()]

  def __keyword_linear_combination(self, text, keyword_dict):
    short_text_summary = np.zeros(self.model.vector_size)
    keywords = keyword_dict.keys()
    for key in keywords:
      try:
        if keyword_dict[key] > 0.05:
          vec = self.model[key.lower()]
          short_text_summary += 100*keyword_dict[key]*vec
      except:
        pass
    return short_text_summary

class TopicWeightedKeywordSumStrategy(AnswerStrategy):

  def __init__(self, data_set_obj, model):
    AnswerStrategy.__init__(self, data_set_obj, model)

  def answer(self, question_class):
    q_vec = self.__topic_keyword_linear_combination(question_class.question, question_class.keywords, question_class.text_tags)
    options = [question_class.answer_a, question_class.answer_b, question_class.answer_c, question_class.answer_d]
    cos = np.array([cosine(q_vec, self.__topic_keyword_linear_combination(x.text, x.keywords, x.text_tags)) for x in options])
    return ['A', 'B', 'C', 'D'][cos.argmin()]

  def __topic_keyword_linear_combination(self, text, keyword_dict, text_tags):
    short_text_summary = np.zeros(self.model.vector_size)
    keywords = keyword_dict.keys()
    for key in keywords:
      try:
        if keyword_dict[key] > 0.05:
          vec = self.model[key.lower()]
          short_text_summary += vec
      except:
        pass

    tags = map(lambda x: (x, text_tags[x]), text_tags.keys())
    tags_sort = sorted(tags, reverse=True, key=lambda x: x[1])

    for tag_tup in tags_sort:
      try:
        vec = self.model[tag_tup[0].lower()]
        short_text_summary += 100*tag_tup[1]*vec
      except:
        pass

    return short_text_summary

class TopicWeightedNaiveSumStrategy(AnswerStrategy):

  def __init__(self, data_set_obj, model):
    AnswerStrategy.__init__(self, data_set_obj, model)
    # Stop list is the top 14 most frequent words from training_set.tsv
    self.stop_list = set('the of a to in is and which that are an on from'.split())

  def answer(self, question_class):
    q_vec = self.__topic_linear_combination(question_class.question, question_class.text_tags)
    options = [question_class.answer_a, question_class.answer_b, question_class.answer_c, question_class.answer_d]
    cos = np.array([cosine(q_vec, self.__topic_linear_combination(x.text, x.text_tags)) for x in options])
    return ['A', 'B', 'C', 'D'][cos.argmin()]

  def __topic_linear_combination(self, text, text_tags):
    text_vec_sum = np.zeros(self.model.vector_size)
    for s in gensim.utils.tokenize(text):
      try:
        if s not in self.stop_list:
          vec = self.model[s.lower()]
          text_vec_sum += vec
      except:
        pass

    tags = map(lambda x: (x, text_tags[x]), text_tags.keys())
    tags_sort = sorted(tags, reverse=True, key=lambda x: x[1])

    for tag_tup in tags_sort:
      try:
        vec = self.model[tag_tup[0].lower()]
        text_vec_sum += 100*tag_tup[1]*vec
      except:
        pass

    return text_vec_sum


if __name__ == '__main__':
  pass

