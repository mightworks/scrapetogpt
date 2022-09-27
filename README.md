# Scrape to GPT

Scrape to GPT is designed to quickly collect user reviews for a chosen website, and then synthesize those reviews into a concise summary. This makes it easy to get an "at-a-glance" view for what users are saying about a website--beyond just the numerical rating.

## Installation

- After you clone the repository and setup your environment, run **pip install -r requirements.txt** to install dependencies

- If you want to use the GPT-3 summary feature, you'll need an OpenAI key. This can be found in the "View API Keys" section of your OpenAI account.

- Your key is read in through an environment variable, so you'll need to run **export OPENAI_API_KEY="your-key-here.."** before you run the crawler

## Usage

Scrape to GPT is designed to be used entirely from the command line using the Scrapy CLI. Ensure you're in the root directory of the project, then run:

    scrapy crawl scrapeit -a domain=[domain-to-scrape] pages=[pages-to-scrape] -a summarize=[True/False] -o [output-file].json

This will scrape Trustpilot for reviews about your chosen website, and save the raw data a json file. If summarize=True, a sample of the reviews will be compiled and sent to GPT-3 for sythensis.

Example:

    ~/scrapetogpt$ scrapy crawl scrapeit -a domain=ebay.com -a summarize=True -a pages=1 -o ebay.json

    Starting scraping..

    Scraping finished.

    Compiling summary..

    "eBay is a popular online marketplace where users can buy and sell items. Users generally find the service to be useful. However, some users have had negative experiences with the site. Complaints include receiving empty envelopes from sellers, being charged excessive fees, and poor customer service. Overall sentiment appears to be mixed."