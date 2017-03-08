import argparse

import urllib2
from tidylib import tidy_document
from bs4 import BeautifulSoup
import json


from models.page import PageItem

from tools.links import LinkParser
link_parser = LinkParser()

from tools.meta import MetaParser

meta_parser = MetaParser()

html_page = PageItem()


parser = argparse.ArgumentParser(description='Scan a url for code validation')
parser.add_argument('-u', '--url', default='http://localhost:8000', type=str)
parser.add_argument('-d', '--depth', default=0, type=int)
args = parser.parse_args()

print ("Scanning url %s and links %i deep...") % (args.url, args.depth)

page_data = {}

url = args.url
page_data['url'] = url

response = urllib2.urlopen(url)

header = response.info()
page_data['header'] = header

html = response.read()
response.close()

data = {}
with open('tidy-options.json') as data_file:
    data = json.load(data_file)


document, errors = tidy_document(html,
    options=data)
# print document
#print errors

page_data['html_errors'] = errors.splitlines()


soup = BeautifulSoup(html, 'html5lib')

page_data['title'] = soup.title.string


page_data['page_meta'] = meta_parser.parse_meta(html)
page_data['page_links'] = link_parser.parse_links(html)



html_page.add(page_data)
print ("Scanning done!")