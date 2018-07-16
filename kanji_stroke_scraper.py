from requests_html import HTMLSession
from lxml import etree

import pyperclip
import sys

TEST_URL = "https://jisho.org/search/%E5%AE%B6%20%23kanji"
SVG_SELECTOR = ".stroke_order_diagram--outer_container svg"

def extract_svg(pageHtml):
    """ Extract the SVG from the contents """ 
    session = HTMLSession()
    r = session.get(TEST_URL)
    r.html.render()
    svg = pageHtml.find(SVG_SELECTOR, first=True)
    lxmlElement = svg.lxml[0] # the lxml element actually has html as the root element rather than the svg, so grab the first child
    return etree.tostring(lxmlElement, pretty_print=True).decode()

def main(args):
    """ Scrape for the SVG Stroke Order Diagram for a given Kanji """
    session = HTMLSession()
    page = session.get(TEST_URL)
    page.html.render()

    svg = extract_svg(page.html)
    pyperclip.copy(svg)
    print('SVG saved to Clipboard')

if __name__ == '__main__':
    main(sys.argv[1:])
