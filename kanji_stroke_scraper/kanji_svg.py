from .kanji_cell import KanjiCell

from cached_property import cached_property
from lxml import etree

REPLACEMENTS = {
    'class="stroke_order_diagram--bounding_box"': 'style="fill: none; stroke: #ddd; stroke-width: 2; stroke-linecap: square;"',
    'class="stroke_order_diagram--guide_line"': 'style="fill: none; stroke: #ddd; stroke-width: 2; stroke-linecap: square; stroke-linejoin: square; stroke-dasharray: 5, 5;"',
    'class="stroke_order_diagram--current_path"': 'style="fill: none; stroke: #000; stroke-width: 3; stroke-linecap: round; stroke-linejoin: round;"',
    'class="stroke_order_diagram--path_start"': 'style="fill: rgba(255,0,0,0.7); stroke: none;"',
    'class="stroke_order_diagram--existing_path"': 'style="fill: none; stroke: #aaa; stroke-width: 3; stroke-linecap: round; stroke-linejoin: round;"'
}

class KanjiSvg:
    """ Represents the Kanji Svg retrieved from Jisho.org """

    def __init__(self, xml, start=0, end=None):
        """ Initialize with the xml """
        self.start = start
        self.end = end


        elements = list(xml)
        cells = []
        elementsInCurrentCell = []
        for element in elements[6:]:
            elementsInCurrentCell.append(element)
            if element.tag == 'circle':
                cells.append(elementsInCurrentCell)
                elementsInCurrentCell = []

        self.cells = [KanjiCell(cell) for cell in cells]

    @cached_property
    def xml(self):
        """ Build the XML for this KanJI SVG """
        cells = self.cells[self.start:self.end]
        startOffset = self.start*100
        fullWidth = len(self.cells)*100
        viewWidth = len(cells)*100

        root = etree.Element("svg", style="height: 100px; width: {}px;".format(viewWidth), viewbox="{} 0 {} 100".format(startOffset, viewWidth))
        
        descriptionElement = etree.Element("desc")
        descriptionElement.text = "Kanji SVG from Jisho.org"
        root.append(descriptionElement)

        root.append(etree.Element("line", style="fill: none; stroke: #ddd; stroke-width: 2; stroke-linecap: square;", x1="1", x2=str(fullWidth-1), y1="1", y2="1"))
        root.append(etree.Element("line", style="fill: none; stroke: #ddd; stroke-width: 2; stroke-linecap: square;", x1=str(startOffset+1), x2=str(startOffset+1), y1="1", y2="99"))
        root.append(etree.Element("line", style="fill: none; stroke: #ddd; stroke-width: 2; stroke-linecap: square;", x1="1", x2=str(fullWidth-1), y1="99", y2="99"))
        root.append(etree.Element("line", style="fill: none; stroke: #ddd; stroke-width: 2; stroke-linecap: square; stroke-linejoin: square; stroke-dasharray: 5, 5;", x1="0", x2=str(fullWidth), y1="50", y2="50"))

        for i, cell in enumerate(cells):
            root.extend(cell.build(i))
        return root

    def __str__(self):
        """ Convert the Kanji Svg to a string """
        svg = etree.tostring(self.xml, method="html", pretty_print=True).decode()
        return self.clean_svg(svg)

    def clean_svg(self, svg):
        """ Clean the SVG so the classes are replaced with inline styles """
        for classAttr, styleAttr in REPLACEMENTS.items():
            svg = svg.replace(classAttr, styleAttr)
        return svg
