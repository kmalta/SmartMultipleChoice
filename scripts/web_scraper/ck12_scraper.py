__author__ = 'angad'

import requests
from bs4 import BeautifulSoup


class Subject(object):
    def __init__(self, url):
        self.url = url
        self.concepts = []
        print "Fetching concepts for " + self.url + " ..."
        self.fetch_concepts()
        print "Done!"

    def fetch_concepts(self):
        r = requests.get(self.url)
        soup = BeautifulSoup(r.text, 'html.parser')
        for x in soup.find_all('li', {'class': 'concepts'}):
            concept_url = x.a.get('href')
            self.concepts += [Concept(concept_url)]
            # break


class Concept(object):
    def __init__(self, url):
        self.url = url
        self.lessons = []
        print "Fetching lessons " + self.url + " ..."
        self.fetch_lessons()
        print "Done!"

    def fetch_lessons(self):
        base_url = 'http://www.ck12.org/api/flx/get/featured/modalities/lesson,lecture,asmtpractice,enrichment,simulationint,simulation,PLIX/'
        lesson_url_base = 'http://www.ck12.org/api/flx/get/perma/modality'
        url = base_url + self.url.split('/')[2]
        r = requests.get(url)
        for x in r.json()['response']['Artifacts']:
            if x['type']['name']=='lesson':
                lesson_id = x['encodedID']
                lesson_perma = x['perma']
                lesson_url = lesson_url_base + lesson_perma + '/' + lesson_id[:-4] + '?format=html'
                self.lessons += [Lesson(lesson_url, x)]
                # break


class Lesson(object):
    def __init__(self, url, json):
        self.url = url
        self.json = json
        self.content = []
        print "Fetching content " + self.url + " ..."
        self.fetch_content()
        print "Done!"

    def fetch_content(self):
        r = requests.get(self.url)
        soup = BeautifulSoup(r.text, 'html.parser')
        self.content = soup
