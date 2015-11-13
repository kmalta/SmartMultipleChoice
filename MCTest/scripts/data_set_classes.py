import sys
sys.path.append('../')
sys.path.append('./')
import dill as pickle



class AnswerClass(object):

    def __init__(self, text, letter):
        self.answer = text
        self.letter = letter

    def print_dump(self):
        print self.letter, '  ', self.answer


class QuestionClass(object):

    def __init__(self, question_array):
        self.parse_raw_questions(question_array)
        self.correct_answer = "*not input yet*"

    def parse_raw_questions(self, q_array):

        self.num_sents_answer_location = q_array[0].split(':')[0]
        self.question = q_array[0].split(':')[1][1:]
        answers = []
        i = 0
        letters = ['A', 'B', 'C', 'D']
        for token in q_array[1:]:
            answers.append(AnswerClass(token, letters[i]))
            i += 1
        self.answers = answers

    def print_dump(self):
        print "Number of sentences to find answer: ", self.num_sents_answer_location
        print "Question: ", self.question
        print "\nCorrect Answer: ", self.correct_answer, "\n"
        for answer in self.answers:
            answer.print_dump()
        print "\n"


class StoryClass(object):

    def __init__(self, story_stats, story_text):
        self.unpack_story_stats(story_stats)
        self.process_text(story_text)
        self.create_sentences()

    def unpack_story_stats(self, stats):
        stat_array = stats.split(';')

        self.author = int(stat_array[0].split(':')[1][1:])
        self.time = int(stat_array[1].split(':')[1][1:])
        self.quality_score = int(stat_array[2].split(':')[1][1:])
        self.creativity_word_list = stat_array[3].split(':')[1][1:].split(',')

    def process_text(self, story_text):
        story_text = story_text.replace('\\newline', '\n')
        story_text = story_text.replace('\\tab', '')
        self.story = story_text

    def create_sentences(self):
        self.story_sentences = self.story.replace('.', '\n').replace('!', '\n').replace('?', '\n').split('\n')

    def print_dump(self):
        print "Author: ", str(self.author)
        print "Work time (s): ", str(self.time)
        print "Quality Score: ", str(self.quality_score)
        print "Creativity Words: ", ", ".join(self.creativity_word_list)
        print "\n"
        print "Story: ", self.story
        print "\n"
        print "Sentences: ", '\n'.join(self.story_sentences)
        print "\n"
        print "Number of Sentences: ", str(len(self.story_sentences))
        print "\n"

class StoryAndQuestion(object):

    def __init__(self, _id, story_stats, story, questions):
        self._id = _id
        self.story = StoryClass(story_stats, story)
        self.parse_questions(questions)

    def parse_questions(self, text):
        q = text.split('\t')
        questions_list = []
        for num in range(0, 4):
            questions_list.append(QuestionClass(q[num*5:(num+1)*5]))
        self.questions_list = questions_list

    def print_dump(self):
        print "Question and Story ID: ", self._id
        self.story.print_dump()
        print "\n\n"
        for question in self.questions_list:
            question.print_dump()
            print "\n"
        print "\n"





class DataSet(object):

    def __init__(self, data_path, set_name):
        self.set_name = set_name
        self.data_path = data_path
        self.read_data()

    def read_data(self):
        story_question_list = []

        with open(self.data_path, 'r') as f:
            lines = f.readlines()

            length = len(lines)
            idx = 0
            for line in lines:
                if idx % 10 == 0:
                    print "Processing:", idx, "out of", length
                q = line.split('\t')
                questions = '\t'.join(q[3:])
                story_question_list.append(StoryAndQuestion(q[0], q[1], q[2], questions))
                idx += 1

        f.close()
        self.story_question_list = story_question_list

    def print_dump(self):
        for saq in self.story_question_list:
            print "################################################"
            print "\n"
            saq.print_dump()
            print "\n\n\n"

def add_answers_to_data_set(obj, path_to_answers):
    with open(path_to_answers, 'r') as f:
        lines = f.readlines()

        length = len(lines)
        idx = 0
        for line in lines:
            answers = line.split()
            if idx % 10 == 0:
                print "Processing:", idx, "out of", length
            idx2 = 0
            for answer in answers:
                obj.story_question_list[idx].questions_list[idx2].correct_answer = answer
                idx2 += 1
            idx += 1

def save_object(obj, name):
    f = open('../sharedObjects/' + name, 'w')
    pickle.dump(obj, f)
    f.close()

