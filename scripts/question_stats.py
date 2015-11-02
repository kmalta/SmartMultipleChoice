import dill as pickle
from multiple_choice_indico import *
import gensim

DATA_SET_PICKLE_FILE = '../sharedObjects/smarter_tha_8th_grader_training_set_data_classes_10_29_15.p'


def create_question_stats():
    f = open(DATA_SET_PICKLE_FILE, 'r')
    data_set_obj = pickle.load(f)
    f.close()

    model = gensim.models.Word2Vec.load_word2vec_format("../data/glove.6B.50d.txt")

    i = 0
    for question in data_set_obj.questions_list:
        i += 1
        if i % 100 == 0:
            print "Processed Question:", str(i), "out of", str(len(data_set_obj.questions_list))
        compute_keyword_average(question)
        ratio_unrecognized_words(question, model)
        fill_in_the_blank(question)
        word_count(question)
        part_of_speech_tagging(question)
        densest_clusters(question)
        contains_numbers(question)
        question_or_statement(question)

    save_object(data_set_obj, 'data_set_with_question_stats_11_1_15.p')


def compute_keyword_average(question_class):
    key_dict = question_class.keywords
    vals = key_dict.values()
    question_class.ave_keyword_confidence = float(sum(vals))/len(vals)

def ratio_unrecognized_words(question_class, model):
    unrecognized = 0
    question_text_array = question_class.question.split()
    for word in question_text_array:
        try:
            model[word]
        except:
            unrecognized += 1
    question_class.ratio_unrecognized_words = float(unrecognized)/len(question_text_array)

def fill_in_the_blank(question_class):
    if '_' in question_class.question:
        question_class.fill_in_the_blank = True
    else:
        question_class.fill_in_the_blank = False

def word_count(question_class):
    question_class.word_count = len(question_class.question.split())

def part_of_speech_tagging(question_class):
    #Fuck this for now, this gunna be hard
    1

def densest_clusters(question_class):
    #this shit will be hard too
    1

def contains_numbers(question_class):
    for word in question_class.question.split():
        if word.isdigit():
            question_class.contains_numbers = True
            return
    question_class.contains_numbers = False
    return

def question_or_statement(question_class):
    if question_class.question[-1] == '?':
        question_class.type = 'question'
    elif question_class.question[-1] == '.':
        question_class.type = 'statement'
    else:
        question_class.type = 'answer_finisher'



# RUNS THE SCRIPT
#create_question_stats()