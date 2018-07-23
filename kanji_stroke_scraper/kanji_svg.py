from lxml import etree

REPLACEMENTS = {
    'class="stroke_order_diagram--bounding_box"': 'style="fill: none; stroke: #ddd; stroke-width: 2; stroke-linecap: square;"',
    'class="stroke_order_diagram--guide_line"': 'style="fill: none; stroke: #ddd; stroke-width: 2; stroke-linecap: square; stroke-linejoin: square; stroke-dasharray: 5, 5;"',
    'class="stroke_order_diagram--current_path"': 'style="fill: none; stroke: #000; stroke-width: 3; stroke-linecap: round; stroke-linejoin: round;"',
    'class="stroke_order_diagram--path_start"': 'style="fill: rgba(255,0,0,0.7); stroke: none;"',
    'class="stroke_order_diagram--existing_path"': 'style="fill: none; stroke: #aaa; stroke-width: 3; stroke-linecap: round; stroke-linejoin: round;"'
}

class KanjiSvg:
    """ Helper class to mange the Kanji Svg retrieved from Jisho.org """

    def __init__(self, xml):
        """ Initialize with the xml """
        self.xml = xml

    def __str__(self):
        """ Convert the Kanji Svg to a string """
        svg = etree.tostring(self.xml, method="html", pretty_print=True).decode()
        return self.clean_svg(svg)

    def clean_svg(self, svg):
        """ Clean the SVG so the classes are replaced with inline styles """
        for classAttr, styleAttr in REPLACEMENTS.items():
            svg = svg.replace(classAttr, styleAttr)
        return svg
