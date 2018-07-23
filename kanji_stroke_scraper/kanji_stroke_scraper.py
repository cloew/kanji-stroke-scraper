from .kanji_svg import KanjiSvg

from requests_html import HTMLSession
from lxml import etree

import backoff
import pyperclip
import sys

BASE_URL = "https://jisho.org/search/{}%20%23kanji"
MAX_TRIES = 4
SVG_SELECTOR = ".stroke_order_diagram--outer_container svg"


class ContentNotFound(Exception):
    """ Represents an error when the content is not found at all """

class ContentNotReady(Exception):
    """ Represents an early load of a page before the content is ready """

@backoff.on_exception(backoff.expo, ContentNotReady, max_tries=MAX_TRIES)
def load_element(pageHtml):
    """ Extract the SVG from the contents """
    pageHtml.render()
    svg = pageHtml.find(SVG_SELECTOR, first=True)
    if not svg:
        raise ContentNotFound()
    if 'display: none' in svg.attrs['style']:
        raise ContentNotReady()
    return svg

def extract_svg(pageHtml):
    """ Extract the SVG from the contents """
    svg = load_element(pageHtml)
    lxmlElement = svg.lxml[0] # the lxml element actually has html as the root element rather than the svg, so grab the first child

    return KanjiSvg(lxmlElement)
    
    return etree.tostring(lxmlElement, method="html", pretty_print=True).decode()

def main(args):
    """ Scrape for the SVG Stroke Order Diagram for a given Kanji """
    kanji = args[0]

    url = BASE_URL.format(kanji)
    session = HTMLSession()
    page = session.get(url)

    try:
        svg = extract_svg(page.html)
    except ContentNotFound:
        print('No SVG found for {}'.format(kanji))
    except ContentNotReady:
        print('SVG not found in page')
    else:
        pyperclip.copy(str(svg))
        print('SVG saved to Clipboard')

if __name__ == '__main__':
    main(sys.argv[1:])
