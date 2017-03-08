from bs4 import BeautifulSoup

class LinkParser(object):

    def parse_links(self, html):
        soup = BeautifulSoup(html, 'html5lib')

        links = []

        for link in soup.find_all('a', href=True):
            if link.has_attr('href'):
                # Strip href
                if link['href'] != '#' and link['href'] != '':
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
                    # It's external but not local either! I might not be needed!
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

        parsed_links = {
            'internal': internal_links,
            'external': external_links,
            'querystring': query_params
        }

        return parsed_links