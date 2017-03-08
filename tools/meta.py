from bs4 import BeautifulSoup

class MetaParser(object):

    def parse_meta(self, html):
        soup = BeautifulSoup(html, 'html5lib')

        page_meta = []
        for tag in soup.find_all("meta"):
            page_meta.append(str(tag))

        return page_meta

    def parse_title(self, html):
        soup = BeautifulSoup(html, 'html5lib')

        try:
            return soup.title.string
        except AttributeError:
            return ''