# Site Auditor

## About

This tool is currently a WIP. The aim is to create a front end webapp that a developer can use to analyse the web pages they are creating for issues and performance enhancements. 

Currently the app runs from the command line as `python main.py` (see installation notes) and will crawl the url provided to the depth provided and generate a set of reports in the reports directory.

THERE ARE BUGS with with the depth crawling currently, the backlog/queue and visted log... however these are on my radar to fix ASAP. 

Please feel free to submit PRs and bugs/issues, but as this is currently a WIP I may need to drop features or change direction at a short notice. There will be a roadmap in the near future.

## Why

I needed to audit a huge website that wan't accessible publicly. The audit was for validation, performance and SEO so I decided to create a tool that would generate what I needed so I can focus on activly improving things.

There are a few tools out there that do bits of what I am after, but either they cost money, are very slow and also don't do everything that I needed in one place - so I created [another tool](https://xkcd.com/927/)!

I'm also trying to learn more Python and backend bits!

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

python main.py

## Options

-h, --help show the help message and exit

-u URL, --url URL The URL to start the crawl with. 0 depth (see -d) will crawl only the input URL

-d DEPTH, --depth DEPTH Depth of the search when following internal links

-s SESSION, --session SESSION Resume a previous session by adding the session key

-p, --performance Run performance tools (YSlow). Because the test is slow and resource intensive, this is best done after all other metrics are passing for an audit

-nr, --no-report Prevent the generate of CSVs in the report directory. Ideal if you are using the web app

-nc, --no-crawl Prevent a crawl. Ideal for generating reports based on existing crawls

## View Results

python webapp.py
