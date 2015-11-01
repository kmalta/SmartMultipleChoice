import dill as pickle
from multiple_choice_indico import *

DATA_SET_PICKLE_FILE = '../sharedObjects/smarter_tha_8th_grader_training_set_data_classes.p'

f = open(DATA_SET_PICKLE_FILE, 'r')
data_set_obj = pickle.load(f)
f.close()

for question in data_set_obj.questions_list:
	print question.question




# unlogged_question = QuestionIndico('100853', 'A mutation that occurs in an organism that reproduces sexually will most likely affect the traits of the offspring if the mutation', 
# 			   'B', 'is located in the cells of the nervous system.', 'alters DNA in a gamete of the parent.', 'alters the behavior of the organisms.',
# 			   'is located near the locus of a chromosome.')

# data_set_obj.questions_list.append(unlogged_question)
# data_set_obj.questions_list = sorted(data_set_obj.questions_list, key=lambda x: x._id)

# _ids = map(lambda x: x._id, data_set_obj.questions_list)

# for _id in _ids:
#   _id = int(_id)
#   index = _id - 100000
#   data_set_obj.questions_list[index - 1]._id = _id
#   print data_set_obj.questions_list[index - 1]._id


# save_object(data_set_obj, 'smarter_tha_8th_grader_training_set_data_classes_10_29_15.p')

