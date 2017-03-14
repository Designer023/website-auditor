import requests
import time
from tidylib import tidy_document


VALIDATOR_URL = 'https://validator.w3.org/nu/?out=json'


class Validator(object):
    options = {}

    def __init__(self, options):
        self.options = options

    def validate_html(self, html):
        document, errors = tidy_document(html, options=self.options)

        html_errors = errors.splitlines()

        return html_errors

    def validate_w3c(self, html):

        print "Validating with W3C"

        time.sleep(3)

        headers = {'Content-Type': 'text/html'}

        response = requests.post(VALIDATOR_URL,
                                 files=dict(out='json', content=html),
                                 headers=headers)

        print response.content

        return response.content