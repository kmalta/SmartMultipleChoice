import sys
sys.path.append('../../alchemyapi_python')
sys.path.append('../')
from alchemyapi import AlchemyAPI


class shortTextAlchemy(object):

    def __init__(self, text):
        self.alchemyapi = AlchemyAPI()
        self.text = text

    def entity_extraction(self, text):


    def keyword_extraction(self, text):


class questionAlchemy(shortTextAlchemy):

    def __init__(self, text):

class answerAlchemy(shortTextAlchemy):

    def __init__(self, text):