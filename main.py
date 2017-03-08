import argparse
import json
import uuid

from models.page import PageItem

from tools.html_importer import HTMLImporter
from tools.links import LinkParser
from tools.meta import MetaParser
from tools.validation import Validator

with open('tidy-options.json') as data_file:
    validator_options = json.load(data_file)

parser = argparse.ArgumentParser(description='Scan a url for code validation')
parser.add_argument('-u', '--url', default='http://localhost:8000', type=str)
parser.add_argument('-d', '--depth', default=0, type=int)
args = parser.parse_args()

print ("Scanning url %s and links %i deep...") % (args.url, args.depth)

session_uuid = uuid.uuid3(uuid.NAMESPACE_DNS, 'python.org')

print ("Session UUID: %s") % session_uuid

starting_url = args.url
max_depth = args.depth

# THE URL CAN CHANGE FROM THIS POINT.
url = starting_url


def analyse_pages(url):

    parsed_html = HTMLImporter(url)
    parsed_html.import_html()

    page_data = {}

    page_data['starting_url'] = starting_url
    page_data['url'] = url

    page_data['header'] = parsed_html.response_header

    html_validator = Validator(validator_options)
    page_data['html_errors'] = html_validator.validate_html(
        parsed_html.html_data)

    meta_parser = MetaParser()
    page_data['page_meta'] = meta_parser.parse_meta(parsed_html.html_data)
    page_data['title'] = meta_parser.parse_title(parsed_html.html_data)

    link_parser = LinkParser()
    page_data['page_links'] = link_parser.parse_links(parsed_html.html_data)

    for link in page_data['page_links']['internal']:
        print link

    # Save data to DB
    html_page = PageItem()
    html_page.upsert(page_data)


analyse_pages(url)


#
# def recursiveUrl(url,depth):
#
#     if depth == 2:
#         return url
#     else:
#         page=urllib2.urlopen(url)
#         soup = BeautifulSoup(page.read(), "html5lib")
#         newlink = soup.find('a') # find just the first one
#         if len(newlink) == 0:
#             return url
#         else:
#             return url, recursiveUrl(newlink,depth+1)
#
#
# def getLinks(url):
#     page=urllib2.urlopen(url)
#     soup = BeautifulSoup(page.read(), "html5lib")
#     links = soup.find_all('a', {'class':'site-footer__about-link'})
#     for link in links:
#         links.append(recursiveUrl(link,0))
#     return links
#
# links = getLinks(url)
# print links

#Let the user know!
print ("Scanning done!")