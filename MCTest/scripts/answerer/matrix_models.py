import nltk
import numpy as np

from model import Model

st = nltk.stem.lancaster.LancasterStemmer()

index_to_answer_map = ['A', 'B', 'C', 'D']

class WordPairContextWindowFrequency(Model):

  def __init__(self, **kwargs):
    Model.__init__(self, **kwargs)
    if 'stop_words' in kwargs:
      self.stop_words = kwargs['stop_words']
    else:
      self._stop_words_from_file()

  def answer(self, story_question):
    cleaned_story = self._cleaned_text_array(story_question.story.story)
    
    # Ex: [('one', (word_pair_list, word_pair_list, word_pair_list, word_pair_list))]
    tagged_qa_tuples = [(question.one_or_multiple, self._extract_word_pairs(question)) 
                        for question in story_question.questions_list]
    
    answers = []
    for one_or_mult, qa_tuple in tagged_qa_tuples:
      frequencies = tuple([self._qa_frequency(one_or_mult, qa_word_pairs, cleaned_story)
                          for qa_word_pairs in qa_tuple])
      answers.append(frequencies.index(max(frequencies)))
    return [index_to_answer_map[index] for index in answers]

  def train(self, data_set):
    sent_counts = []
    for story_question in data_set.story_question_list:
      story_text = story_question.story.story
      for sentence in nltk.sent_tokenize(story_text):
        is_alpha = lambda x: x.isalpha()
        sent_counts.append(len(filter(is_alpha, nltk.wordpunct_tokenize(sentence))))

    self.avg_sent_len = int(np.mean(sent_counts))

  def _stop_words_from_file(self):
    try:
      stop_words_file = open('stop_words.txt', 'r')
    except:
      print 'Could not open stop_words.txt, stop words not removed'
      return
    self.stop_words = [line.strip() for line in stop_words_file if line != '\n']

  def _word_pair_exists(self, word_pair, cleaned_story, window_size):
    for i in range(0, len(cleaned_story) + 1 - window_size):
      window = cleaned_story[i:i + window_size]
      if word_pair[0] in window and word_pair[1] in window:
        return True
    return False

  def _qa_frequency(self, one_or_mult, qa_word_pairs, cleaned_story):
    # Edge case of questions with all stop words.
    if len(qa_word_pairs) == 0:
      return 0.0

    window_size = self.avg_sent_len if one_or_mult == "one" else self.avg_sent_len * 3
    exists_list = [self._word_pair_exists(word_pair, cleaned_story, window_size) 
                   for word_pair in qa_word_pairs]
    return float(exists_list.count(True)) / float(len(exists_list))

  def _extract_word_pairs(self, question_class):
    return tuple([self._word_pairs(question_class.question, answer_class.answer)
                  for answer_class in question_class.answers])

  def _word_pairs(self, text1, text2):
    word_pairs = []
    for word1 in self._cleaned_text_array(text1):
      for word2 in self._cleaned_text_array(text2):
        if (word1, word2) not in word_pairs:
          word_pairs.append((word1, word2))
    return word_pairs
        
  def _cleaned_text_array(self, text):
    # Possible we get better results WITHOUT stemming...?
    partial_tokenized = [st.stem(word) for word in nltk.wordpunct_tokenize(text.lower())]
    valid_word = lambda x: x not in self.stop_words and x.isalpha()
    return filter(valid_word, partial_tokenized)
