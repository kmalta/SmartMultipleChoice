import sys
sys.path.append('../')
sys.path.append('./')
from secrets import *
import indicoio

import shelve


indicoio.config.api_key = INDICO_API_KEY

class batch_tags(object):
  def __init__(self, tags):
    self.batch_tags = indicoio.sentiment(tags)

  def print_batches(self):
    print repr(self.batch_tags)

def test_batch_tags():
  return batch_tags(['Here is a sentence', 'Here is another sentence', 'This is a paragraph'])

def add_to_shelf(key, value):
  d = shelve.open('shelf_location')
  d[key] = value
  d.close()

def modify_shelf(key, value):
  d = shelve.open('shelf_location')
  d[key].modified = value
  d.close()

#add_to_shelf('sentiments', test_batch_tags())

modify_shelf('sentiments', 'Hi Brandon!')
