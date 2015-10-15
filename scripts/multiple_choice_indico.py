import sys
sys.path.append('../')
sys.path.append('./')
import secrets.py
import word2vec_model_setup
from indicoio import config, named_entities, keywords, text_tags


config.api_key = INDICO_API_KEY

class ShortTextIndico(object):

    def __init__(self, text):
        self.text = text
        self.entity_extraction(text)
        self.keywords_extraction(text)
        self.text_tags(text)

    def entity_extraction(self, text):
        self.named_entities = named_entities(text)

    def keywords_extraction(self, text):
        self.keywords = keywords(text)

    def text_tags_extraction(self, text):
        self.text_tags = text_tags(text)


class AnswerIndico(ShortTextIndico):

    def __init__(self, text, letter):
        super().__init__(text)
        self.letter = letter


class QuestionIndico(ShortTextIndico):

    def __init__(self, _id, question, correct_answer, answer_a_text, answer_b_text, answer_c_text, answer_d_text):
        super().__init__(question)
        self.question = question
        self.question_id = _id
        self.correct_answer = correct_answer
        self.answer_a = AnswerIndico(answer_a_text)
        self.answer_b = AnswerIndico(answer_b_text)
        self.answer_c = AnswerIndico(answer_c_text)
        self.answer_d = AnswerIndico(answer_d_text)

class DataSet(object):

    def __init__(self, data_path):
        self.data_path = data_path
        self.model = Word2Vec.load('../models/word2vec_model')
        self.read_data()

    def read_data(self):
        questions_list = []

        with open(data_path, 'r') as f:
            lines = f.readlines()

            for line in lines[1:]:
                q = line.split('\t')
                try: 
                    questions_list.append(QuestionIndico(q[0], q[1], q[2], q[3], q[4], q[5], q[6]))
                except:
                    print "ERROR: ", repr(q)

        self.questions_list = questions_list




