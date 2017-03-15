import time
from tidylib import tidy_document

from tools.plugins.w3v_validator import W3CValidator



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

        validator = W3CValidator()
        validated_result = validator.validateHTML(html)

        print validated_result

        return validated_result