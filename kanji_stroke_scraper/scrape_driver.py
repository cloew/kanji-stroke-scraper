from .kanji_stroke_scraper import KanjiStrokeScraper, ContentNotFound, ContentNotReady
import pyperclip

def run(args):
    """ Scrape the Kanji """
    kanji = args[0]

    scraper = KanjiStrokeScraper()

    try:
        svg = scraper.scrape(kanji)
    except ContentNotFound:
        print('No SVG found for {}'.format(kanji))
    except ContentNotReady:
        print('SVG not found in page')
    else:
        pyperclip.copy(str(svg))
        print('SVG saved to Clipboard')
