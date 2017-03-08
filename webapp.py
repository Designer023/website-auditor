#!flask/bin/python
from settings.settings import *
from flask import Flask, jsonify, render_template, send_from_directory, request, Response

from models.page import PageItem

# Setup Flask App
app = Flask(__name__, static_url_path = "/static", static_folder = "static")


# Setup the routes for Flask
@app.route('/')
def root():
    return render_template('index.html')


@app.route('/auditor/api/v1.0/results', methods=['GET'])
def get_status():

    pages = PageItem()
    pages_list = pages.getPages()

    return jsonify(pages_list)


if __name__ == '__main__':
    app.run(debug=True)