from requests_html import HTMLSession
from lxml import etree

import backoff
import pyperclip
import sys

TEST_URL = "https://jisho.org/search/%E5%AE%B6%20%23kanji"
MAX_TRIES = 4
SVG_SELECTOR = ".stroke_order_diagram--outer_container svg"

class ContentNotReady(Exception):
    """ Represents an early load of a page before the content is ready """

@backoff.on_exception(backoff.expo, ContentNotReady, max_tries=MAX_TRIES)
def load_element(pageHtml):
    """ Extract the SVG from the contents """
    pageHtml.render()
    svg = pageHtml.find(SVG_SELECTOR, first=True)
    if 'display: none' in svg.attrs['style']:
        print('Loaded element before it was ready')
        raise ContentNotReady()
    return svg

def extract_svg(pageHtml):
    """ Extract the SVG from the contents """
    svg = load_element(pageHtml)
    lxmlElement = svg.lxml[0] # the lxml element actually has html as the root element rather than the svg, so grab the first child
    return etree.tostring(lxmlElement, pretty_print=True).decode()

def main(args):
    """ Scrape for the SVG Stroke Order Diagram for a given Kanji """
    session = HTMLSession()
    page = session.get(TEST_URL)
    # page.html.render()

    try:
        svg = extract_svg(page.html)
    except ContentNotReady:
        print('SVG not found in page')
    else:
        pyperclip.copy(svg)
        print('SVG saved to Clipboard')

if __name__ == '__main__':
    main(sys.argv[1:])
