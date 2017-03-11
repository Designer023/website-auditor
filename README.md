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

--url -u set the url to check. This defaults to 

python main.py -u https://google.com

--depth -d set how many links deep to go. Default is:

python main.py -u https://google.com -d 2

--analyze -a sets whether or not to analyze page load speed with yslow. Default:

python main.py -u https://google.com -a no

## View Results

python webapp.py
