from .kanji_stroke_scraper import KanjiStrokeScraper, ContentNotFound, ContentNotReady
import argparse
import pyperclip

def run(args):
    """ Scrape the Kanji """
    parser = argparse.ArgumentParser(description="Scrape the SVG diagram for a Kanji from jisho.org")
    parser.add_argument('kanji')

    parsedArgs = parser.parse_args(args)
    print(args)
    print(parsedArgs)

    scraper = KanjiStrokeScraper()

    try:
        svg = scraper.scrape(parsedArgs.kanji)
    except ContentNotFound:
        print('No SVG found for {}'.format(parsedArgs.kanji))
    except ContentNotReady:
        print('SVG not found in page')
    else:
        pyperclip.copy(str(svg))
        print('SVG saved to Clipboard')
