import time

from models.page import PageItem
from models.backlog import BacklogItem
from models.visited_log import VisitedItem

from .html_importer import HTMLImporter
from .links import LinkParser
from .meta import MetaParser
from .validation import Validator
from .yslow import generate_yslow


class Analyser(object):

    url = ''
    starting_url = ''
    session_uuid = ''
    max_depth = 0
    validator_options = {}
    analyse_performance = False
    visited_manager = VisitedItem()

    def __init__(self, url, starting_url, session_uuid, max_depth, validator_options, analyse_performance):
        self.url = url
        self.starting_url = starting_url
        self.session_uuid = session_uuid
        self.max_depth = max_depth
        self.validator_options = validator_options
        self.analyse_performance = analyse_performance


    def update_yslow(self):
        yslow_results = generate_yslow(self.url)

        html_page = PageItem()
        html_page.update_yslow(self.url, yslow_results)


    def analyse_pages(self, url, depth):

        parsed_html = HTMLImporter(url)
        parsed_html.import_html()

        if not parsed_html.error:

            page_data = {}

            page_data['starting_url'] = self.starting_url
            page_data['session_uuid'] = self.session_uuid
            page_data['url'] = url

            page_data['header'] = parsed_html.response_header

            html_validator = Validator(self.validator_options)
            page_data['html_errors'] = html_validator.validate_html(
                parsed_html.html_data)

            meta_parser = MetaParser()
            page_data['page_meta'] = meta_parser.parse_meta(
                parsed_html.html_data)
            page_data['title'] = meta_parser.parse_title(parsed_html.html_data)

            link_parser = LinkParser()
            page_data['page_links'] = link_parser.parse_links(
                parsed_html.html_data)

            if self.analyse_performance is True:
                print "Analysing page with YSlow. This will take a few seconds"
                page_data['yslow_results'] = generate_yslow(url)
                print "YSlow done!"

            # Save data to DB
            html_page = PageItem()
            html_page.upsert(page_data)

            # Loop on the next set of links 1 deeper
            depth += 1

            # If this new depth doesn't exceed the max then loop through the urls for this page!
            if depth <= self.max_depth:
                for link in page_data['page_links']['internal']:
                    # clean base url and append it to the links
                    url_to_test = "%s%s" % (self.starting_url.rstrip('/'), link)

                    # Check if the item has already been scanned this session in
                    # in the visted_log
                    visited_this_session = self.visited_manager.visited_this_session(url_to_test, self.session_uuid)

                    # If its not in the visited list then add it to the queue!
                    if visited_this_session is False:
                        backlog_item = BacklogItem()
                        backlog_item.upsert(
                            url_to_test,
                            self.starting_url,
                            self.session_uuid,
                            depth
                        )

    def start(self):
        # Add the initial item to the backlog so there is something to process
        backlog_item = BacklogItem()
        # We use upsert, but in theory a normal add should be fine!
        backlog_item.upsert(self.url, self.starting_url, self.session_uuid, 0)

        # Process backlog while there are items for this session
        while backlog_item.count_session(self.session_uuid) > 0:
            # Get first of backlog item for this session
            next_page = backlog_item.first_session(self.session_uuid)
            if next_page.depth > self.max_depth:
                break

            print "Scanning: " + next_page.url
            self.analyse_pages(next_page.url, next_page.depth)

            backlog_item.pop_first_session(self.session_uuid)
            print "Removed: " + next_page.url

            self.visited_manager.add(next_page.url, self.session_uuid)
            print "Added to visited list"

            print "Sleeping for a moment..."
            # Slow things down a bit - Nicer on the server
            time.sleep(5)
