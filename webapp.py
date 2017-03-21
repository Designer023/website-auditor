#!flask/bin/python
import json
import threading
import uuid

import time
from random import randint

from models.backlog import BacklogItem
from models.sessions import SessionItem
# from settings.settings import *
from flask import Flask, jsonify, render_template, request, Response
from flask_socketio import SocketIO
from flask_socketio import send, emit


from models.page import PageItem

# Setup Flask App
from models.visited_log import VisitedItem
from tools.analyser import Analyser

with open('tidy-options.json') as data_file:
    validator_options = json.load(data_file)

app = Flask(__name__, static_url_path="/static", static_folder="static")
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

backlog_thread = None

# Setup the routes for Flask

# Threaded processes (to handle queue backlog)

# def backlog_watcher():
#
#     print "Backlog processing starting!"
#
#     analyser = Analyser(validator_options)
#     analyser.process_backlog()
#
#
#     print "Queue done, take 5!.."
#     time.sleep(5)
#     backlog_watcher()


def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")

def create_new_session(url, session_uuid, depth, performance):
    print "I will add a new session and item too the backlog to be processed"

    session_manager = SessionItem()
    session_manager.create(url, session_uuid, depth)
    # Add the starting link to the session so there is a backlog to process

    p = str2bool(performance)
    print type(p)
    print p

    backlog_manager = BacklogItem()
    # Note stating depth = 0
    backlog_manager.add(url, url, session_uuid, 0, p)



# API

# Session list - list of all sessions
@app.route('/api/v1.0/auditor/sessions', methods=['GET', 'POST'])
def get_sessions():
    if request.method == 'POST':

        form_data = request.form

        url = form_data['url']
        depth = int(form_data['depth'])
        performance = form_data['performance']

        # Generate a uniquie timestamp based on device and time /
        session_uuid = uuid.uuid1()

        create_new_session(url, session_uuid, depth, performance)

        return jsonify(True)
    else:
        sessions = SessionItem()
        session_list = {}
        session_list['sessions'] = sessions.get_sessions()

        return jsonify(session_list)

# Session list - list of all sessions
@app.route('/api/v1.0/auditor/sessions/<path:session_uuid>', methods=['GET', 'DELETE'])
def get_session_with_uuid(session_uuid):
    if request.method == 'DELETE':
        # DELETE ALL TYPES BELONGING TO SESSION

        # Find queue
        backlogged = BacklogItem()
        backlogged.delete(session_uuid)

        # Find pages
        pages = PageItem()
        pages.delete(session_uuid)

        # Find session
        sessions = SessionItem()
        sessions.delete(session_uuid)

        # Find visited
        visited = VisitedItem()
        visited.delete(session_uuid)

        return jsonify(True)

    else:
        sessions = SessionItem()
        session_list = {}
        session_list['sessions'] = sessions.get_sessions(session_uuid)

        return jsonify(session_list)

# Session list - list of all sessions
@app.route('/api/v1.0/auditor/results/<path:session_uuid>', methods=['GET'])
def get_all_results(session_uuid):

    pages = PageItem()
    pages_list = pages.getPages(session_uuid)

    return jsonify(pages_list)

@app.route('/api/v1.0/auditor/detail/<path:page_id>', methods=['GET'])
def get_detail_for_page(page_id):

    pages = PageItem()

    page_data = pages.get_page_data(page_id)

    data = {}
    data['data'] = page_data

    return jsonify(data)

# CATCH ALL FOR FRONTEND - Handled by react router unless caught above!

@app.route('/')
def root():
    return render_template('index.html')


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template('index.html')


if __name__ == '__main__':
    # global backlog_thread
    # backlog_thread = threading.Thread(target=backlog_watcher())
    # backlog_thread.daemon = True
    # backlog_thread.start()
    # if backlog_thread is None:
    #     backlog_thread = socketio.start_background_task(target=backlog_watcher)

    socketio.run(app, debug=True, use_reloader=True)
