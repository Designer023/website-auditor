import urllib2


class HTMLImporter(object):
    url = ''
    response_header = []
    html_data = []

    def __init__(self, url):
        self.url = url

    def import_html(self):
        response = urllib2.urlopen(self.url)

        self.response_header = response.info()
        self.html_data = response.read()
        response.close()
