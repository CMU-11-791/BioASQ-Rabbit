from setuptools import setup
setup(
  name = 'deiis',
  packages = ['deiis'], # this must be the same as the name above
  version = '0.0.6',
  description = 'Python classes for CMU 11-791',
  author = 'Keith Suderman',
  author_email = 'suderman@cs.vassar.edu',
  url = 'https://github.com/CMU-11-791/python-deiis', # use the URL to the github repo
  download_url = 'https://github.com/CMU-11-791/python-deiis/archive/0.0.6.tar.gz',
  keywords = ['cmu', 'deiis', 'nlp', 'web services'], # arbitrary keywords
  install_requires = ['requests', 'nltk'],
  classifiers = [],
)