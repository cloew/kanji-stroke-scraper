from .kanji_stroke_scraper import KanjiStrokeScraper, ContentNotFound, ContentNotReady
from .kanji_svg import KanjiSvg
import argparse
import pyperclip

from lxml import etree as ET


def scrape(parsedArgs):
    kanji = parsedArgs.kanji
    start = int(parsedArgs.start) - 1
    end = parsedArgs.end

    scraper = KanjiStrokeScraper()

    try:
        svg = scraper.scrape_svg(kanji, start=start, end=end)
    except ContentNotFound:
        print('No SVG found for {}'.format(kanji))
    except ContentNotReady:
        print('SVG not found in page')
    else:
        pyperclip.copy(str(svg))
        print('SVG saved to Clipboard')
        
def convert_svg(parsedArgs):
    with open(parsedArgs.kanji, encoding='utf-8') as file:
        svg = file.read()
        start = int(parsedArgs.start) - 1
        end = parsedArgs.end
        
        lxmlElement = ET.fromstring(svg)
        svg = KanjiSvg(lxmlElement, start=start, end=end)
        pyperclip.copy(str(svg))
        print('SVG saved to Clipboard')
        
def parse_kanji_info(parsedArgs):
    kanji = parsedArgs.kanji

    scraper = KanjiStrokeScraper()

    kanji_info = scraper.scrape_kanji_info(kanji)
    pyperclip.copy(kanji_info)
    print('Kanji Info saved to Clipboard')

def run(args):
    """ Scrape the Kanji """
    parser = argparse.ArgumentParser(description="Scrape the SVG diagram for a Kanji from jisho.org")
    parser.add_argument('kanji')
    parser.add_argument('--start', '-s', default=1)
    parser.add_argument('--end', '-e', type=int)
    parser.add_argument('-svg', action='store_true')
    parser.add_argument('--kanjiinfo', '-ki', action='store_true')

    parsedArgs = parser.parse_args(args)
    
    if parsedArgs.svg:
        convert_svg(parsedArgs)
    elif parsedArgs.kanjiinfo:
        parse_kanji_info(parsedArgs)
    else:
        scrape(parsedArgs)
