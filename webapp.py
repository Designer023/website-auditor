#!flask/bin/python
from settings.settings import *
from flask import Flask, jsonify, render_template, send_from_directory, request, Response

from models.page import PageItem

# Setup Flask App
app = Flask(__name__, static_url_path = "/static", static_folder = "static")


# Setup the routes for Flask

# API

@app.route('/api/v1.0/auditor/results', methods=['GET'])
def get_status():

    pages = PageItem()
    pages_list = pages.getPages()

    return jsonify(pages_list)



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