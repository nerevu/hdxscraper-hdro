## UN OCHA FTS API Collector

Collector for the [UN Human Development Report Office API](http://hdr.undp.org/en).

## Setup

*local*

(You are using a [virtualenv](http://www.virtualenv.org/en/latest/index.html), right?)

    sudo pip install -r requirements.txt
    manage setup
    manage init

*ScraperWiki Box*

    make setup
    manage -m Scraper init

## Usage

*local*

    manage run

*ScraperWiki Box*

    manage -m Scraper run

The results will be stored in a SQLite database `scraperwiki.sqlite`.
