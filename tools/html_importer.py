import httplib
import urllib2


class HTMLImporter(object):
    url = ''
    response_header = []
    html_data = []
    error = False

    def __init__(self, url):
        self.url = url

    def import_html(self):
        request = self.url
        try:
            response = urllib2.urlopen(request)
            self.response_header = response.info()
            self.html_data = response.read()
            response.close()
        except urllib2.HTTPError, e:
            print ('HTTPError = ' + str(e.code))
            self.error = True
        except urllib2.URLError, e:
            print ('URLError = ' + str(e.reason))
            self.error = True
        except httplib.HTTPException, e:
            print ('HTTPException')
            self.error = True


