import argparse
import json
import uuid

import time

from models.page import PageItem
from models.backlog import BacklogItem

from tools.html_importer import HTMLImporter
from tools.links import LinkParser
from tools.meta import MetaParser
from tools.validation import Validator
from tools.yslow import generate_yslow

with open('tidy-options.json') as data_file:
    validator_options = json.load(data_file)

parser = argparse.ArgumentParser(description='Scan a url for code validation')
parser.add_argument('-u', '--url', default='http://localhost:8000', type=str)
parser.add_argument('-d', '--depth', default=2, type=int)
args = parser.parse_args()

print ("Scanning url %s and links %i deep...") % (args.url, args.depth)

session_uuid = uuid.uuid3(uuid.NAMESPACE_DNS, 'python.org')

print ("Session UUID: %s") % session_uuid

starting_url = args.url
max_depth = args.depth

# THE URL CAN CHANGE FROM THIS POINT.
url = starting_url


def analyse_pages(url, depth):

    parsed_html = HTMLImporter(url)
    parsed_html.import_html()

    if not parsed_html.error:

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

        page_data['yslow_results'] = generate_yslow(url)

        # Save data to DB
        html_page = PageItem()
        html_page.upsert(page_data)

        # Loop on the next set of links 1 deeper
        depth += 1
        for link in page_data['page_links']['internal']:
            # clean base url and append it to the links
            url_to_test = "%s%s" % (starting_url.rstrip('/'), link)
            backlog_item = BacklogItem()
            backlog_item.upsert(url_to_test, starting_url, session_uuid, depth)



backlog_item = BacklogItem()
backlog_item.upsert(url, starting_url, session_uuid, 0)


while backlog_item.count() > 0:
    next_page = backlog_item.first()
    if next_page.depth >= max_depth:
        break

    print "Scanning: " + next_page.url
    analyse_pages(next_page.url, next_page.depth)

    backlog_item.popFirst()
    print "Removed: " +  next_page.url

    # Slow things down a bit - Nicer on the server
    time.sleep(5)



#Let the user know!
print ("Scanning done!")