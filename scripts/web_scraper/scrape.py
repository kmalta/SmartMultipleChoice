__author__ = 'angad'

import scripts.web_scraper.ck12_scraper as ck

corpus = ck.Corpus()
corpus.dump_paragraphs('ck12_paragraphs.txt')
