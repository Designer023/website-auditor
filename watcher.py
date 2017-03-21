import json
import time

from tools.analyser import Analyser

with open('tidy-options.json') as data_file:
    validator_options = json.load(data_file)


def backlog_watcher(pause_time=5):

    print "Backlog processing starting!"

    analyser = Analyser(validator_options)
    analyser.process_backlog()

    print "Queue done, take %i!.." % pause_time
    time.sleep(pause_time)
    backlog_watcher(pause_time)

if __name__ == '__main__':
    backlog_watcher(10)