import sys
import urllib.request

TEST_URL = "https://jisho.org/search/%E5%AE%B6%20%23kanji"

def main(args):
    """ Scrape for the SVG Stroke Order Diagram for a given Kanji """
    with urllib.request.urlopen(TEST_URL) as f:
        contents = f.read().decode()
    print(contents)
    print(len(contents.split('\n')))

if __name__ == '__main__':
    main(sys.argv[1:])
