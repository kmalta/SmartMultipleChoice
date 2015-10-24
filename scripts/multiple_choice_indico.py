import sys
sys.path.append('../')
sys.path.append('./')
from secrets import *
from indicoio import config, named_entities, keywords, text_tags
import dill as pickle

config.api_key = INDICO_API_KEY

class ShortTextIndico(object):

    def __init__(self, text):
        self.text = text
        self.entity_extraction(text)
        self.keywords_extraction(text)
        self.text_tags_extraction(text)

    def entity_extraction(self, text):
        self.named_entities = named_entities(text)

    def keywords_extraction(self, text):
        self.keywords = keywords(text)

    def text_tags_extraction(self, text):
        self.text_tags = text_tags(text)


class AnswerIndico(ShortTextIndico):

    def __init__(self, text, letter):
        ShortTextIndico.__init__(self, text)
        self.letter = letter


class QuestionIndico(ShortTextIndico):

    def __init__(self, _id, question, correct_answer, answer_a_text, answer_b_text, answer_c_text, answer_d_text):
        ShortTextIndico.__init__(self, question)
        self._id = _id
        self.question = question
        self.correct_answer = correct_answer
        self.answer_a = AnswerIndico(answer_a_text, 'A')
        self.answer_b = AnswerIndico(answer_b_text, 'B')
        self.answer_c = AnswerIndico(answer_c_text, 'C')
        self.answer_d = AnswerIndico(answer_d_text, 'D')

class DataSet(object):

    def __init__(self, data_path):
        self.data_path = data_path
        self.read_data()

    def read_data(self):
        questions_list = []

        with open(self.data_path, 'r') as f:
            lines = f.readlines()

            length = len(lines)
            idx = 0
            for line in lines[1:]:
                idx += 1
                if idx % 10 == 0:
                    print "Processing:", idx, "out of", length
                q = line.split('\t')
                try:
                    questions_list.append(QuestionIndico(q[0], q[1], q[2], q[3], q[4], q[5], q[6]))
                except:
                    print "ERROR reading question:", repr(q)

        f.close()
        self.questions_list = questions_list


def save_object(obj, name):
    f = open('../sharedObjects/' + name, 'w')
    pickle.dump(obj, f)
    f.close()


#TEST FOR READING DATA

data = DataSet('../../data_set/training_set.tsv')
save_object(data, 'smarter_tha_8th_grader_training_set_data_classes.p')

for question in data.questions_list:
    print "#################################################"
    print "#################################################"
    print "\n"
    print "Question ID:", question._id
    print "\n"
    print "Quesion:", question.question
    print "\n"
    print "Answer A:", question.answer_a
    print "Answer B:", question.answer_b
    print "Answer C:", question.answer_c
    print "Answer D:", question.answer_d
    print "\n"
    print "Correct Answer:", question.correct_answer
    print "\n\n"

