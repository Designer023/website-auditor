import os
import logging
import subprocess
import json


APP_ROOT = os.path.dirname(os.path.realpath(__file__))
YSLOW = os.path.join(APP_ROOT, 'yslow.js')
PHANTOMJS = "/usr/local/Cellar/phantomjs/2.1.1/bin/phantomjs"




def yslow(url):
    try:
        f = subprocess.Popen([PHANTOMJS, YSLOW, "--info grade", url], stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT, shell=False)
        out = f.communicate()[0]
        return json.loads(out)
    except Exception, e:
        logging.fatal("Error parsing message: %s" % e)

def generate_yslow(url):
    d = yslow(url)
    scores = d['g'].keys()

    yslow_scores = {}
    yslow_scores['load_time'] = d['lt']
    yslow_scores['size'] = d['w']
    yslow_scores['score'] = d['o']
    yslow_scores['scores'] = d['o']
    breakdown = {}

    for k in scores:
        breakdown[k] = d['g'][k].get(u'score', None)

    yslow_scores['breakdown'] = breakdown

    return yslow_scores
