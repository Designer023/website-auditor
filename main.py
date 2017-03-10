import argparse
import json
import uuid

import datetime

from tools.analyser import Analyser

with open('tidy-options.json') as data_file:
    validator_options = json.load(data_file)

parser = argparse.ArgumentParser(description='Scan a url for code validation')
parser.add_argument('-u', '--url', default='http://localhost:8000', type=str)
parser.add_argument('-d', '--depth', default=2, type=int)
parser.add_argument('-s', '--session', default=None, type=str)
parser.add_argument('-a', '--analyse', default=False, type=bool)
args = parser.parse_args()

print ("Scanning url %s and links %i deep...") % (args.url, args.depth)

# Resume session checking
if args.session is None:
    # Generate a uniquie timestamp based on device /
    session_uuid = uuid.uuid1()
else :
    session_uuid = args.session

print ("Session UUID: %s") % session_uuid


starting_url = args.url
max_depth = args.depth

# THE URL CAN CHANGE FROM THIS POINT.
url = starting_url

# Start the scanning and analysing
analyser = Analyser(url, starting_url, session_uuid, max_depth, validator_options)

# Optional YSlow
if args.analyse is True:
    analyser.analyse_performance = True

# Start the analysis
analyser.start()

#Let the user know!
print ("Scanning done!")