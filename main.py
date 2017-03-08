import argparse
import json

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

url = args.url
parsed_html = HTMLImporter(url)
parsed_html.import_html()

# Create an object with the details we want to save
page_data = {}
page_data['url'] = url

page_data['header'] = parsed_html.response_header

html_validator = Validator(validator_options)
page_data['html_errors'] = html_validator.validate_html(parsed_html.html_data)

meta_parser = MetaParser()
page_data['page_meta'] = meta_parser.parse_meta(parsed_html.html_data)
page_data['title'] = meta_parser.parse_title(parsed_html.html_data)

link_parser = LinkParser()
page_data['page_links'] = link_parser.parse_links(parsed_html.html_data)

#Save data to DB
html_page = PageItem()
html_page.add(page_data)

#Let the user know!
print ("Scanning done!")