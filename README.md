# Site Auditor

[![Build Status](https://travis-ci.org/Designer023/website-auditor.svg?branch=master)](https://travis-ci.org/Designer023/website-auditor)

## About

This tool is currently a WIP. The aim is to create a front end webapp that a developer can use to analyse the web pages they are creating for issues and performance enhancements. 

Currently the app runs from the command line as `python main.py` (see installation notes) and will crawl the url provided to the depth provided and generate a set of reports (csv) in the reports directory.

[bugs/issues](https://github.com/Designer023/website-auditor/issues)

## Why

To audit websites, some of which aren't accessible publicly. The audit is for validation, performance and SEO.

There are a few tools out there that do bits of what I am after, but either they cost money, are very slow and also don't do everything that I needed in one place - so I created [another tool](https://xkcd.com/927/)!

## Installation

brew install tidy-html5

brew install phantomjs

brew install yarn

setup a virtualenvironment (preferable)

pip install -r requirements.txt

yarn

npm install gulp

gulp

## Configuration

cp settings/settings_example.py settings/settings.py

Then edit to provide valid database name, user, and password settings.

## Run

`python main.py -u http://localhost:8000`

## Options

Resume session with depth of 3 links and do performance reviews using YSlow.

`python main.py -u http://localhost:8000 -d 3 -s 33a257d4-0664-11e7-9aa7-24a074f076f8 -p`

-h, --help show the help message and exit

-u URL, --url URL The URL to start the crawl with. 0 depth (see -d) will crawl only the input URL

-d DEPTH, --depth DEPTH Depth of the search when following internal links

-s SESSION, --session SESSION Resume a previous session by adding the session key

-p, --performance Run performance tools (YSlow). Because the test is slow and resource intensive, this is best done after all other metrics are passing for an audit

-nr, --no-report Prevent the generate of CSVs in the report directory. Ideal if you are using the web app

-nc, --no-crawl Prevent a crawl. Ideal for generating reports based on existing crawls

## View Results

### CSV

If the CSVs flag is on then reports will be generated into the `reports/` directory

### Web app

Run `python webapp.py` and visit `http://127.0.0.1:5000`


## Basic Roadmap

See the [issues log for enhancements](https://github.com/Designer023/website-auditor/issues?q=is%3Aopen+is%3Aissue+label%3Aenhancement)