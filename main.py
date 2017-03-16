import argparse
import json
import uuid

from models.sessions import SessionItem
from tools.analyser import Analyser
from tools.reporter import Reporter

if __name__ == "__main__":

    with open('tidy-options.json') as data_file:
        validator_options = json.load(data_file)

    parser = argparse.ArgumentParser(
        description='Audit web pages for code '
                    'validation and performance reports')

    parser.add_argument('-u', '--url',
                        type=str,
                        help='URL to start the crawl with. '
                             '0 will crawl only the input URL')
    parser.add_argument('-d', '--depth',
                        default=0,
                        type=int,
                        help='Depth of the search when following '
                             'internal links')
    parser.add_argument('-s', '--session',
                        default=None,
                        type=str,
                        help='Resume a previous session by adding '
                             'the session key')
    parser.add_argument('-t', '--throttle',
                        default=3,
                        type=int,
                        help='Time (seconds) between each page test. '
                             'Low is harder on servers, high takes longer!')
    parser.add_argument('-p', '--performance',
                        dest='performance',
                        action='store_true',
                        help='Run performance tools (YSlow). Because the '
                             'test is slow and resource intensive, this is '
                             'best done after all other metrics are '
                             'passing for an audit')
    parser.set_defaults(performance=False)
    parser.add_argument('-nr', '--no-report',
                        dest='report',
                        action='store_false',
                        help='Prevent the generate of CSVs in the report '
                             'directory. Ideal if you are using the web app')
    parser.set_defaults(report=True)
    parser.add_argument('-nc', '--no-crawl',
                        dest='crawl',
                        action='store_false',
                        help='Prevent a crawl. Ideal for generating reports '
                             'based on existing crawls')
    parser.set_defaults(crawl=True)

    args = parser.parse_args()

    # If crawling a URL MUST be specified
    if args.crawl is True and not args.url:
        parser.error('No url specified. I need this to do my job! use -u or '
                     '--url and add the url to the page to '
                     'test e.g. -u http://localhost:8000')

    print ("Scanning url %s and links %i deep...") % (args.url, args.depth)

    resume_session = False
    # Resume session checking
    if args.session is None:
        # Generate a uniquie timestamp based on device and time /
        session_uuid = uuid.uuid1()
    else:
        session_uuid = args.session
        resume_session = True

    session = SessionItem()
    session.create(args.url, session_uuid, args.depth)

    print ("Session UUID: %s") % session_uuid

    # Start the scanning and analysing
    analyser = Analyser(args.url,
                        args.url,
                        session_uuid,
                        validator_options,
                        args.performance)

    # Start the analysis
    if args.crawl is True:
        analyser.start(resume_session)

    # Reporting
    if args.report is True:
        reporter = Reporter()
        reporter.report('csv')
        # TODO: Add args for other report types. Need to create the report gen

    # Let the user know!
    print ("Audit complete! Have a nice day :)")
