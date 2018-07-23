from kanji_stroke_scraper import main as scrape

import sys


def main(args):
    """ Scrape for the SVG Stroke Order Diagram for a given Kanji """
    scrape(args)

if __name__ == '__main__':
    main(sys.argv[1:])
