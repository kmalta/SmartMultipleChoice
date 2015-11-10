from ebooklib import epub
from os import walk
from bs4 import BeautifulSoup
from gensim.utils import tokenize


BOOKS_DIR = 'data/books/'


files = [d+f for (d, _, files) in walk(BOOKS_DIR) for f in files]
print "Found %d files" % (len(files))

paragraphs = []
for f in files:
    print "Parsing", f
    book = epub.read_epub(f)
    content = [BeautifulSoup(x.content, 'html.parser') for x in book.get_items_of_type(9)]
    for c in content:
        paragraph_parse_tags = ['p', 'ol', 'ul']
        for tag in paragraph_parse_tags:
            for element in c.find_all(tag):
                text = element.get_text(' ', strip=True).encode('ascii', "ignore")
                # TODO: remove hyperlinks
                text = " ".join(tokenize(text, lowercase=True))
                if text != '':
                    paragraphs += [text]
    print "Done!"

OUTPUT_FILE = 'ck_12_paragraphs_all.txt'
with open(OUTPUT_FILE, 'w') as f:
    print "Writing all paragraphs to",
    f.writelines(paragraphs)