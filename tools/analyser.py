import time
import json

from models.page import PageItem
from models.backlog import BacklogItem
from models.sessions import SessionItem
from models.visited_log import VisitedItem

from .html_importer import HTMLImporter
from .links import LinkParser
from .meta import MetaParser
from .validation import Validator
from .yslow import generate_yslow

class Analyser(object):
    validator_options = {}

    def __init__(self, validator_options):
        self.validator_options = validator_options

    def update_session_stats(self, status_code):
        session = SessionItem()
        html_page = PageItem()
        backlog_item = BacklogItem()

        complete_count = html_page.count_session(self.session_uuid)
        backlog_count = backlog_item.count_session(self.session_uuid)

        session.update_stats(
            self.starting_url,
            self.session_uuid,
            backlog_count,
            complete_count,
            status_code
        )

    def analyse_pages(self, url, depth, performance, validate_w3c):

        backlog_item = BacklogItem()
        backlog_count = backlog_item.count_session(self.session_uuid)

        # Update session with new link
        session = SessionItem()
        session.update_queue(self.starting_url,
                             self.session_uuid, backlog_count)

        session_data =  session.get_session_data(self.session_uuid)
        session_max_depth = session_data['max_depth']

        parsed_html = HTMLImporter(url)
        parsed_html.import_html()

        if not parsed_html.error:

            page_data = {}

            page_data['starting_url'] = self.starting_url
            page_data['session_uuid'] = self.session_uuid
            page_data['url'] = url

            page_data['header'] = parsed_html.response_header

            html_validator = Validator(self.validator_options)

            # Always use the default HTML validator
            page_data['html_errors'] = html_validator.validate_html(
                parsed_html.html_data)

            # Custom Validators
            # W3C - HTML
            if validate_w3c is True:
                page_data['w3c'] = html_validator.validate_w3c(
                    parsed_html.html_data)

            meta_parser = MetaParser()
            page_data['page_meta'] = meta_parser.parse_meta(
                parsed_html.html_data)
            page_data['title'] = meta_parser.parse_title(parsed_html.html_data)

            link_parser = LinkParser()
            page_data['page_links'] = link_parser.parse_links(
                parsed_html.html_data,
                url
            )

            if performance is True:
                print "Analysing page with YSlow. " \
                      "This will take a few seconds..."
                page_data['yslow_results'] = generate_yslow(url)
                print "Page analysis complete"

            # Save data to DB
            html_page = PageItem()
            html_page.upsert(page_data)

            complete_count = html_page.count_session(self.session_uuid)
            session.update_pages(self.starting_url, self.session_uuid,
                                 complete_count)

            # Loop on the next set of links 1 deeper
            depth += 1

            # If this new depth doesn't exceed the max the process new links
            if depth <= session_max_depth:
                for link in page_data['page_links']['internal']:
                    # clean base url and append it to the links
                    url_to_test = "%s%s" % (self.starting_url
                                            .rstrip('/'), link)

                    # Check if the item has already been scanned this session
                    # in the visted_log
                    visited_this_session = self.visited_manager\
                        .visited_this_session(url_to_test, self.session_uuid)

                    # If its not in the visited list then add it to the queue!
                    if visited_this_session is False:
                        backlog_item = BacklogItem()
                        backlog_item.upsert(
                            url_to_test,
                            self.starting_url,
                            self.session_uuid,
                            depth,
                            self.analyse_performance
                        )

    def start(self, resume_session):

        session = SessionItem()
        # Update session details to incomplete since we are started!
        session.update_status_code(self.starting_url, self.session_uuid, 1)

        backlog_item = BacklogItem()

        # If we're not resuming we better add something to start with!
        if not resume_session:
            # Add the initial item to the backlog for processing
            # We use upsert, but in theory a normal add should be fine!
            backlog_item.upsert(self.url, self.starting_url,
                                self.session_uuid, 0, self.analyse_performance)

        # Process backlog while there are items for this session
        while backlog_item.count_session(self.session_uuid) > 0:

            session_data = session.get_session_data(self.session_uuid)
            session_max_depth = session_data['max_depth']

            # Get first of backlog item for this session
            next_page = backlog_item.first_session(self.session_uuid)
            if next_page.depth > session_max_depth:
                break

            # Slow things down a bit (throttle) - Nicer on the servers
            print "Preparing scan..."
            time.sleep(3)

            print ("Scanning: %s") % next_page.url
            self.analyse_pages(next_page.url,
                               next_page.depth, next_page.performance, False)

            backlog_item.pop_first_session(self.session_uuid)
            self.visited_manager.upsert(next_page.url, self.session_uuid)
            print ("Removed: %s from the backlog "
                   "and added it to the visted list") % next_page.url

            self.update_session_stats(1)

            progress = session.session_progress(self.starting_url,
                                                self.session_uuid)
            total_pages = progress['queue_count'] + progress['page_count']
            print ("%i%% complete. %i/%i pages crawled") % (
                progress['percent'], progress['page_count'], total_pages)


        self.update_session_stats(2)

        print "Analysis complete"



    def process_page(self, backlog_item, session_item):
        print ("Analysing %s for %s") % (backlog_item.url, session_item.session_uuid)

        session_manager = SessionItem()
        backlog_manager = BacklogItem()
        visited_manager = VisitedItem()
        page_manager = PageItem()

        parsed_html = HTMLImporter(backlog_item.url)
        parsed_html.import_html()

        if not parsed_html.error:

            page_data = {}

            # Grab data from the context of the processing session
            page_data['starting_url'] = session_item.starting_url
            page_data['session_uuid'] = session_item.session_uuid
            page_data['url'] = backlog_item.url

            # Response headers
            page_data['header'] = parsed_html.response_header


            # Always use the default HTML validator
            html_validator = Validator(self.validator_options)
            page_data['html_errors'] = html_validator.validate_html(
                parsed_html.html_data)

            # Custom Validators
            # W3C - HTML
            if backlog_item.validate_w3c is True:
                page_data['w3c'] = html_validator.validate_w3c(parsed_html.html_data)
            else:
                page_data['w3c'] = None

            # Page meta tags
            meta_parser = MetaParser()
            page_data['page_meta'] = meta_parser.parse_meta(parsed_html.html_data)
            page_data['title'] = meta_parser.parse_title(parsed_html.html_data)

            # Links
            link_parser = LinkParser()
            page_data['page_links'] = link_parser.parse_links(parsed_html.html_data,backlog_item.url)

            if backlog_item.performance is True:
                print "Analysing page with YSlow. This will take a few seconds..."
                page_data['yslow_results'] = generate_yslow(backlog_item.url)
                print "Page analysis complete"
            else:
                page_data['yslow_results'] = None

            # Save Analysed page to DB
            page_manager.upsert(page_data)

            # Update session stats
            complete_count = page_manager.count_session(session_item.session_uuid)
            session_manager.update_pages(session_item.starting_url, session_item.session_uuid,
                                 complete_count)

            # Loop on the next set of links 1 deeper
            new_depth = backlog_item.depth + 1

            # If this new depth doesn't exceed the max the process new links
            if new_depth <= session_item.max_depth:
                for link in page_data['page_links']['internal']:
                    # clean base url and append it to the links
                    url_to_test = "%s%s" % (session_item.starting_url.rstrip('/'), link)

                    # Check if the item has already been scanned this session in the visted_log
                    visited_this_session = visited_manager.visited_this_session(url_to_test, session_item.session_uuid)

                    # If its not in the visited list then add it to the queue!
                    if visited_this_session is False:

                        backlog_manager.upsert(
                            url_to_test,
                            session_item.starting_url,
                            session_item.session_uuid,
                            new_depth,
                            backlog_item.performance
                        )

        else:
            print "There was a problem importing the HTML. Try again later :'("


    def process_backlog(self, current_session_uuid = None):
        session_manager = SessionItem()
        backlog_manager = BacklogItem()
        visited_manager = VisitedItem()
        page_manager = PageItem()

        while backlog_manager.count(current_session_uuid) > 0:
            print "Preparing scan..."
            time.sleep(3)

            next_backlog_item = backlog_manager.first(current_session_uuid)
            backlog_item_session_uuid = next_backlog_item.session_uuid
            backlog_item_url = next_backlog_item.url

            session_item = session_manager.get_session_object(backlog_item_session_uuid)

            #print ("Scanning: %s for session: %s") % (backlog_item_url, backlog_item_session_uuid)

            self.process_page(next_backlog_item, session_item)

            backlog_manager.pop_first(current_session_uuid)
            visited_manager.upsert(backlog_item_url, backlog_item_session_uuid)
            print ("Removed: %s from the backlog and added it to the visted list") % backlog_item_url

            # Update this session and output progress
            complete_count = page_manager.count_session(backlog_item_session_uuid)
            backlog_count = backlog_manager.count_session(backlog_item_session_uuid)

            if backlog_count == 0:
                # Set session to complete if there are no more in the queue!
                status_code = 2 # Complete - no backlog
            else:
                status_code = 1 # In progress still!

            session_manager.update_stats(
                session_item.starting_url,
                session_item.session_uuid,
                backlog_count,
                complete_count,
                1 # 1 processing, 2 complete
            )

            progress = session_manager.session_progress(session_item.starting_url, session_item.session_uuid)
            print ("%i%% complete. %s pages crawled") % ( progress['percent'], progress['fraction'])
