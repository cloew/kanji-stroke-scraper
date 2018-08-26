
class KanjiCell:
    """ Represents a Kanji Cell """

    def __init__(self, elements):
        """ Initialize the cell with its elements """
        self.lines = elements[:2]
        self.corePaths = elements[-3:-1]
        self.circle = elements[-1]

        numExtraPaths = len(elements)-5
        print(numExtraPaths)
        self.extraPaths = elements[2:-3]

        self.index = numExtraPaths

    def build(self, index):
        """ Build the KanjiCell for the given index in a new SVG """
        print(index)
        print(self.extraPaths)
        print(self.extraPaths[self.index-index:] == self.extraPaths)
        return self.lines + self.extraPaths[self.index-index:] + self.corePaths + [self.circle]
