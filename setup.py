from distutils.core import setup

setup(name='kanji_stroke_scraper',
      version='0.5.0',
      #description='Kao Tessur Deck Package',
      author='Chris Loew',
      author_email='cloew123@gmail.com',
      #url='http://www.python.org/sigs/distutils-sig/',
      packages=['kanji_stroke_scraper'],
      install_requires=['argparse', 'backoff', 'pyperclip', 'requests-html', 'cached-property'],
      scripts=['scripts/scrapekanjidiagram']
     )
