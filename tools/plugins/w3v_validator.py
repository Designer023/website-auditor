import requests

VALIDATOR_URL = 'https://validator.w3.org/nu/?out=json'

class W3CValidator(object):

    def validateHTML(self, html):

        headers = {'Content-Type': 'text/html'}

        response = requests.post(VALIDATOR_URL,
                             files=dict(out='json', content=html),
                             headers=headers
                             )

        return response.content
