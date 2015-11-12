# Parse wikipedia XML dump using a MODIFIED version of WikiExtractor

import codecs
import sys
import StringIO

from bs4 import BeautifulSoup
import WikiExtractor

WikiExtractor.expand_templates = False

def parse_text_tag(out, id, title, text_tag):
    WikiExtractor.Extractor(id, title, text_tag).extract(out)

def process_wiki_page(page, out_file):
    soup = BeautifulSoup(page, 'lxml-xml')
    page = soup.find('page')

    id = page.id.text
    title = page.title.text
    text_tag = page.find('text')
    if text_tag.text.startswith('#REDIRECT'):
        return

    parse_text_tag(out_file, id, title, text_tag)

def main():
    with codecs.open(sys.argv[1], encoding='utf-8', mode='r') as in_file, open('wikiextractor_output.txt', 'w') as out_file:
        page = u''
        in_text = False
        for line in in_file:
            processed = line.lstrip()
            if processed.startswith('<page'):
                page += line
                in_text = True
            elif processed.startswith('</page'):
                page += line
                in_text = False
                process_wiki_page(page, out_file)
                page = u''
            elif in_text:
                page += line
                    
if __name__ == '__main__':
    main()
