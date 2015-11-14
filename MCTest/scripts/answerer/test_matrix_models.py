from matrix_models import *
from evaluation import OneOrMultipleAccuracy
import dill as pickle

data_set = pickle.load(open("../../sharedObjects/dataSet_mc500_dev.p", "r"))
model = WordPairContextWindowFrequency()
model.train(data_set)

predictions = [model.answer(story_question)
               for story_question in data_set.story_question_list]

print predictions

print model.avg_sent_len

story_question = data_set.story_question_list[0]

print model._cleaned_text_array(story_question.story.story)

print model._extract_word_pairs(story_question.questions_list[2])

"""
accuracy = OneOrMultipleAccuracy(data_set, predictions)
accuracy.evaluate()
print accuracy.statistic
"""
