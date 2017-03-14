from tidylib import tidy_document


class Validator(object):
    options = {}

    def __init__(self, options):
        self.options = options

    def validate_html(self, html):
        document, errors = tidy_document(html, options=self.options)

        html_errors = errors.splitlines()

        return html_errors
