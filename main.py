from kanji_stroke_scraper import run

import sys


def main(args):
    """ Scrape for the SVG Stroke Order Diagram for a given Kanji """
    run(args)

if __name__ == '__main__':
    main(sys.argv[1:])
