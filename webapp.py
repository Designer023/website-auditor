#!flask/bin/python
import json

from settings.settings import *
from flask import Flask, jsonify, render_template, send_from_directory, request, Response

from models.page import PageItem

# Setup Flask App
from tools.analyser import Analyser

with open('tidy-options.json') as data_file:
    validator_options = json.load(data_file)

app = Flask(__name__, static_url_path = "/static", static_folder = "static")


# Setup the routes for Flask

# API

@app.route('/api/v1.0/auditor/results', methods=['GET'])
def get_sessions():

    pages = PageItem()
    pages_list = pages.getPages()

    return jsonify(pages_list)

@app.route('/api/v1.0/auditor/detail/<path:page_id>', methods=['GET'])
def get_detail_for_page(page_id):

    pages = PageItem()

    page_data = pages.get_page_data(page_id)

    data = {}
    data['data'] = page_data

    return jsonify(data)

@app.route('/api/v1.0/auditor/yslow/<path:page_id>', methods=['GET'])
def update_yslow_for_page(page_id):

    pages = PageItem()
    page_data = pages.get_page_data(page_id)

    analyser = Analyser(page_data['url'],
                        page_data['starting_url'],
                        0,
                        0,
                        validator_options)

    analyser.generate_yslow()


    # Get the generated updated data

    page_data = pages.get_page_data(page_id)

    data = {}
    data['data'] = page_data

    return jsonify(data)


# CATCH ALL FOR FRONTEND

@app.route('/')
def root():
    return render_template('index.html')


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)