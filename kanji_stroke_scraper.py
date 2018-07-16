from requests_html import HTMLSession
from lxml import etree

import backoff
import pyperclip
import sys

BASE_URL = "https://jisho.org/search/{}%20%23kanji"
MAX_TRIES = 4
SVG_SELECTOR = ".stroke_order_diagram--outer_container svg"

REAPLCEMENTS = {
    'class="stroke_order_diagram--bounding_box"': 'style="fill: none; stroke: #ddd; stroke-width: 2; stroke-linecap: square;"',
    'class="stroke_order_diagram--guide_line"': 'style="fill: none; stroke: #ddd; stroke-width: 2; stroke-linecap: square; stroke-linejoin: square; stroke-dasharray: 5, 5;"',
    'class="stroke_order_diagram--current_path"': 'style="fill: none; stroke: #000; stroke-width: 3; stroke-linecap: round; stroke-linejoin: round;"',
    'class="stroke_order_diagram--path_start"': 'style="fill: rgba(255,0,0,0.7); stroke: none;"',
    'class="stroke_order_diagram--existing_path"': 'style="fill: none; stroke: #aaa; stroke-width: 3; stroke-linecap: round; stroke-linejoin: round;"'
}

class ContentNotReady(Exception):
    """ Represents an early load of a page before the content is ready """

@backoff.on_exception(backoff.expo, ContentNotReady, max_tries=MAX_TRIES)
def load_element(pageHtml):
    """ Extract the SVG from the contents """
    pageHtml.render()
    svg = pageHtml.find(SVG_SELECTOR, first=True)
    if 'display: none' in svg.attrs['style']:
        raise ContentNotReady()
    return svg

def extract_svg(pageHtml):
    """ Extract the SVG from the contents """
    svg = load_element(pageHtml)
    lxmlElement = svg.lxml[0] # the lxml element actually has html as the root element rather than the svg, so grab the first child
    return etree.tostring(lxmlElement, pretty_print=True).decode()

def clean_svg(svg):
    """ Clean the SVG so the classes are replaced with inline styles """
    for classAttr, styleAttr in REAPLCEMENTS.items():
        svg = svg.replace(classAttr, styleAttr)
    return svg

def main(args):
    """ Scrape for the SVG Stroke Order Diagram for a given Kanji """
    kanji = args[0]

    url = BASE_URL.format(kanji)
    session = HTMLSession()
    page = session.get(url)

    try:
        svg = extract_svg(page.html)
    except ContentNotReady:
        print('SVG not found in page')
    else:
        svg = clean_svg(svg)
        pyperclip.copy(svg)
        print('SVG saved to Clipboard')

if __name__ == '__main__':
    main(sys.argv[1:])
