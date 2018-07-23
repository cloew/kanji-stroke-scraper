from .kanji_svg import KanjiSvg

from cached_property import cached_property
from requests_html import HTMLSession

import backoff

BASE_URL = "https://jisho.org/search/{}%20%23kanji"
MAX_TRIES = 4
SVG_SELECTOR = ".stroke_order_diagram--outer_container svg"


class ContentNotFound(Exception):
    """ Represents an error when the content is not found at all """

class ContentNotReady(Exception):
    """ Represents an early load of a page before the content is ready """

class KanjiStrokeScraper:
    """ Helper class to scrape the Kanji Strokes from Jsiho.org """

    def scrape(self, kanji):
        """ Scrape the given Kanji """
        url = BASE_URL.format(kanji)
        page = self.html_session.get(url)

        try:
            svg = self.extract_svg(page.html)
        except ContentNotFound:
            print('No SVG found for {}'.format(kanji))
        except ContentNotReady:
            print('SVG not found in page')
        return svg

    @cached_property
    def html_session(self):
        """ Return the Html Session for this Scraper """
        return HTMLSession()

    def extract_svg(self, pageHtml):
        """ Extract the SVG from the contents """
        svg = self.load_element(pageHtml)
        lxmlElement = svg.lxml[0] # the lxml element actually has html as the root element rather than the svg, so grab the first child

        return KanjiSvg(lxmlElement)

    @backoff.on_exception(backoff.expo, ContentNotReady, max_tries=MAX_TRIES)
    def load_element(self, pageHtml):
        """ Extract the SVG from the contents """
        pageHtml.render()
        svg = pageHtml.find(SVG_SELECTOR, first=True)
        if not svg:
            raise ContentNotFound()
        if 'display: none' in svg.attrs['style']:
            raise ContentNotReady()
        return svg
