import re

from bs4 import BeautifulSoup


class LinkParser(object):

    def parse_links(self, html, url):
        soup = BeautifulSoup(html, 'html5lib')

        links = []
        hash = '#'

        # Todo: Regex for urls - the current if/try method is crude!
        # http(s):// that's not this site url
        # ?querystrings
        # external links
        # mailto
        # ../ - try and resolve to current url?!
        # #hash anchors

        for link in soup.find_all('a', href=True):
            if link.has_attr('href'):
                if hash not in link['href']:
                    if link['href'] != '' and link['href'] != '/':
                        links.append(link['href'])

        unique_links = []

        for i in links:
            if i not in unique_links:
                unique_links.append(i)

        query_params = []
        external_links = []
        internal_links = []

        for link in unique_links:

            try:
                # Look for links with an external protocol on
                link.index('http')
                external_links.append(link)
                try:
                    # Catch internal links that have the full domain on them!
                    link.index(url)
                    internal_links.append(link)
                except:
                    # It's external but not local either!
                    pass

            except ValueError:
                # No external protocol so it must be internal!
                try:
                    # Does it have a query string on?
                    link.index('?')
                    query_params.append(link)
                except ValueError:
                    # Just a regular internal link
                    internal_links.append(link)


        # Get CSS Links

        css_links = soup.find_all('link', rel="stylesheet", href=True)
        css_links_all = list()
        for css_link in css_links:
            css_links_all.append(css_link['href'])

        js_links = soup.find_all('script', src=re.compile(".*"))
        js_links_all = list()
        for js_link in js_links:
            js_links_all.append(js_link['src'])


        parsed_links = {
            'internal': internal_links,
            'external': external_links,
            'querystring': query_params,
            'css': css_links_all,
            'javascript': js_links_all
        }

        return parsed_links
