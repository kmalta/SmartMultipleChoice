__author__ = 'angad'

import scripts.web_scraper.ck12_scraper as ck
import dill as pickle

subject_urls = ['http://www.ck12.org/earth-science/',
                'http://www.ck12.org/life-science/',
                'http://www.ck12.org/physical-science/',
                'http://www.ck12.org/biology/',
                'http://www.ck12.org/chemistry/',
                'http://www.ck12.org/physics/']
subjects = []
for s in subject_urls:
    subjects += [ck.Subject(s)]
    # break

f = open('../../sharedObjects/ck12_content.p', 'wb')
pickle.dump(subjects, f)
f.close()