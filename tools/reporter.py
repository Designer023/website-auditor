import ast
import os

import csv

import errno

from models.page import PageItem


class Reporter(object):

    def report(self, type):

        if type == 'csv':
            print 'CSV Generating...'

            report_files = ['reports/summary.csv', 'reports/links.csv', 'reports/errors.csv', 'reports/yslow.csv']

            for report_file in report_files:
                # Create report directory and files
                if not os.path.exists(os.path.dirname(report_file)):
                    try:
                        os.makedirs(os.path.dirname(report_file))
                    except OSError as exc:  # Guard against race condition
                        if exc.errno != errno.EEXIST:
                            raise

            summaryFile = open('reports/summary.csv', 'wt')

            wr = csv.writer(summaryFile, quoting=csv.QUOTE_ALL)
            wr.writerow( ('URL', 'Page title', 'Validation Errors') )

            linkFile = open('reports/links.csv', 'wt')
            errorFile = open('reports/errors.csv', 'wt')
            yslowFile = open('reports/yslow.csv', 'wt')

            wr_error = csv.writer(errorFile, quoting=csv.QUOTE_ALL)
            wr_error.writerow(('URL', 'Error'))

            # Yslow - See: http://yslow.org/faq/ for rule names
            wr_yslow = csv.writer(yslowFile, quoting=csv.QUOTE_ALL)
            wr_yslow.writerow((
                'URL',
                'Load time',
                'Page size (kB)',
                'Score',
                'Content Delivery Network (CDN)',
                'Compress components with gzip',
                'Use cookie-free domains',
                'Put CSS at top',
                'Reduce DNS lookups',
                'Remove duplicate JavaScript and CSS',
                'Avoid empty src or href',
                'Configure entity tags (ETags)',
                'Add Expires headers',
                'Avoid CSS expressions',
                'Make JavaScript and CSS external',
                'Make favicon small and cacheable',
                'Do not scale images in HTML',
                'Put JavaScript at bottom',
                'Reduce cookie size',
                'Reduce the number of DOM elements',
                'Minify JavaScript and CSS',
                'Avoid HTTP 404 (Not Found) error',
                'Avoid AlphaImageLoader filter',
                'Make fewer HTTP requests',
                'Avoid URL redirects',
                'Make Ajax cacheable',
                'Use GET for AJAX requests'
            ))

            pages = PageItem()
            pages_list = pages.getPages()

            links_internal = set()
            links_external = set()
            links_query = set()

            for page in pages_list['pages']:
                wr.writerow(( str(page['url']), str(page['title']), str(len(page['html_errors'])) ))

                # Errors
                for error in page['html_errors']:
                    wr_error.writerow(( str(page['url']), str(error)))

                # Add links to links list
                for link in page['page_links']['internal']:
                    links_internal.add(link)

                for link in page['page_links']['external']:
                    links_external.add(link)

                for link in page['page_links']['querystring']:
                    links_query.add(link)

                # YSlow

                yslow_results = page['yslow_results']

                if yslow_results:
                    yslow_breakdown = yslow_results['breakdown']
                    wr_yslow.writerow((
                        page['url'],
                        yslow_results['load_time'],
                        yslow_results['size'] / 1024,
                        yslow_results['score'],

                        yslow_breakdown['ycdn'],
                        yslow_breakdown['ycompress'],
                        yslow_breakdown['ycookiefree'],
                        yslow_breakdown['ycsstop'],
                        yslow_breakdown['ydns'],
                        yslow_breakdown['ydupes'],
                        yslow_breakdown['yemptysrc'],
                        yslow_breakdown['yetags'],
                        yslow_breakdown['yexpires'],
                        yslow_breakdown['yexpressions'],
                        yslow_breakdown['yexternal'],
                        yslow_breakdown['yfavicon'],
                        yslow_breakdown['yimgnoscale'],
                        yslow_breakdown['yjsbottom'],
                        yslow_breakdown['ymincookie'],
                        yslow_breakdown['ymindom'],
                        yslow_breakdown['yminify'],
                        yslow_breakdown['yno404'],
                        yslow_breakdown['ynofilter'],
                        yslow_breakdown['ynumreq'],
                        yslow_breakdown['yredirects'],
                        yslow_breakdown['yxhr'],
                        yslow_breakdown['yxhrmethod'],
                    ))







            linkFile = open('reports/links.csv', 'wt')

            wr_link = csv.writer(linkFile, quoting=csv.QUOTE_ALL)
            wr_link.writerow(('Link', 'Type'))
            for link in links_internal:
                wr_link.writerow(( str(link), 'Internal' ))

            for link in links_query:
                wr_link.writerow(( str(link), 'Query string' ))

            for link in links_external:
                wr_link.writerow(( str(link), 'External' ))

