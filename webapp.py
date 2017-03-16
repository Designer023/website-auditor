#!flask/bin/python
import json
import threading
import uuid

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

# Setup the routes for Flask

# Sockets
#
# @socketio.on('message')
# def handle_message(message):
#     emit('results_updated', 'huzzah ' + str(message))
#

# API

def start(url, session_uuid):
    session = SessionItem()
    session.create(url, session_uuid)

    analyser = Analyser(url,
                        url,
                        session_uuid,
                        0,
                        validator_options,
                        False)
    resume_session = False

    analyser.start(resume_session)
    # Socket IO and threads... :( unhappy face! TBC
    # socketio.send('results_updated', True)
    # socketio.emit('message')



# Session list - list of all sessions
@app.route('/api/v1.0/auditor/sessions', methods=['GET', 'POST'])
def get_sessions():
    if request.method == 'POST':
        form_data = request.form
        url = form_data['url']

        # Generate a uniquie timestamp based on device and time /
        session_uuid = uuid.uuid1()


        t = threading.Thread(target=start, args=(url, session_uuid))
        t.daemon = True
        t.start()


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

# CATCH ALL FOR FRONTEND - Handled by reaact router unless caught above!

@app.route('/')
def root():
    return render_template('index.html')


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template('index.html')


if __name__ == '__main__':
    socketio.run(app, debug=True)
