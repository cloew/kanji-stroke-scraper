from distutils.core import setup

setup(name='kanji_stroke_scraper',
      version='0.2.00',
      #description='Kao Tessur Deck Package',
      author='Chris Loew',
      author_email='cloew123@gmail.com',
      #url='http://www.python.org/sigs/distutils-sig/',
      packages=['kanji_stroke_scraper'],
      install_requires=['backoff', 'pyperclip', 'requests-html', 'cached-property'],
      scripts=['scripts/scrapekanjidiagram']
     )
