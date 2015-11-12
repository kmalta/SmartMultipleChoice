import sys
sys.path.append('../')
sys.path.append('./')
import dill as pickle
from parse_mctest_tsv import AnswerClass, QuestionClass, StoryClass, StoryAndQuestion, DataSet
from gensim.models import Word2Vec
import numpy as np
import dill as pickle
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

punctuation = ['"', '.', ',', '!', '?', ';', ':']

def create_corpus_from_data_set_obj(path_list, name):
    corpus = []
    for path in path_list:
        f = open('../sharedObjects/' + path, 'r')
        data_set_obj = pickle.load(f)
        f.close()

        idx = 0
        length = len(data_set_obj.story_question_list)
        for saq in data_set_obj.story_question_list:
            if idx % 10 == 0:
                print "Processing:", idx, "out of", length

            corpus = corpus + saq.story.story_sentences
            for question in saq.questions_list:
                corpus.append(question.question)
            idx += 1

    f = open('../sharedObjects/' + name, 'w')
    write_corpus = '\n'.join(corpus)
    for punc in punctuation:
        write_corpus = write_corpus.replace(punc, '')
    f.write(write_corpus)
    f.close()


def train_w2v_model(corpus_name, model_name):
    f = open('../sharedObjects/' + corpus_name, 'r')
    corpus = f.readlines()
    f.close()
    model = Word2Vec(corpus, workers = 4,
                size = 300, min_count = 2,
                window = 30, sample = 1e-5)

    model.init_sims(replace=True)
    save_model(model, model_name)


def save_model(model, name):
    model.save('../sharedObjects/' + name)


#TRAINS MODELS

create_corpus_from_data_set_obj(['dataSet_mc500_train.p', 'dataSet_mc500_dev.p', 'dataSet_mc500_test.p'], 'mc500_corpus.txt')
train_w2v_model('mc500_corpus.txt', 'w2v_mc500')
