# Parse wikipedia XML dump using a MODIFIED version of WikiExtractor

import sys
import StringIO

from bs4 import BeautifulSoup
import WikiExtractor

WikiExtractor.expand_templates = False

def parse_text_tag(out, id, title, text_tag):
    WikiExtractor.Extractor(id, title, text_tag).extract(out)

def main():
    with open(sys.argv[1], 'r') as in_file, open('wikiextractor_output.txt', 'w') as out_file:
        soup = BeautifulSoup(in_file, 'lxml-xml')
        pages = soup.find_all('page')

        for page in pages:
            id = page.id.text
            title = page.title.text
            text_tag = page.find('text')
            if text_tag.text.startswith('#REDIRECT'):
                continue

            parse_text_tag(out_file, id, title, text_tag)

if __name__ == '__main__':
    main()
