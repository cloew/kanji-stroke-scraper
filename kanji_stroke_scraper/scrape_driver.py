from .kanji_stroke_scraper import KanjiStrokeScraper, ContentNotFound, ContentNotReady
import argparse
import pyperclip

def run(args):
    """ Scrape the Kanji """
    parser = argparse.ArgumentParser(description="Scrape the SVG diagram for a Kanji from jisho.org")
    parser.add_argument('kanji')
    parser.add_argument('--start', '-s', default=1)
    parser.add_argument('--end', '-e', type=int)

    parsedArgs = parser.parse_args(args)

    kanji = parsedArgs.kanji
    start = int(parsedArgs.start) - 1
    end = parsedArgs.end

    scraper = KanjiStrokeScraper()

    try:
        svg = scraper.scrape(kanji, start=start, end=end)
    except ContentNotFound:
        print('No SVG found for {}'.format(kanji))
    except ContentNotReady:
        print('SVG not found in page')
    else:
        pyperclip.copy(str(svg))
        print('SVG saved to Clipboard')
