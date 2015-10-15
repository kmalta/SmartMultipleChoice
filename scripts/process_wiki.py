import logging
import os.path
import sys

from gensim.corpora import WikiCorpus

# TAKES ABOUT 5 HOURS TO RUN
# FILE DOWNLOADED FROM THIS LINK: 
#       https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2
# YOU DO NOT NEED TO DO THIS, MODELS ONLY NEED TO BE TRAINED ONCE, AND I'VE ALREADY 
# TAKEN CARE OF THIS

logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
logging.root.setLevel(level=logging.INFO)
logger.info("running %s" % ' '.join(sys.argv))

space = " "
i = 0

output = open('../models/wiki.en.text', 'w')
wiki = WikiCorpus('../../enwiki-20100622-pages-articles.xml.bz2',  lemmatize=False)

# print wiki
# for text in wiki.get_texts():
#     output.write(space.join(text) + "\n")
#     i = i + 1
#     if (i % 10000 == 0):
#         logger.info("Saved " + str(i) + " articles")

# output.close()
# logger.info("Finished Saved " + str(i) + " articles")