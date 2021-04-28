# Scraping-AJAX-Website-and-storing-data-locally
================================================
Just a little personal project of mine. The point is to collect housing market data and analyze it long term, identify pricing trends in the neighborhood and determine what is a good deal based on historical data. The site being scraped uses some form of AJAX/Dynamically loaded Javascript, so scraping the HTML data becomes a little more involved than just being able to step through the site's urls. This is because dynamic javascript is able to render the contents of your web session without changing the url you are on. To get around this, this script will use a chrome driver and the python selenium module.

A few things to note when scraping:

- scrape with a proxy vpn just in case.
- have a list of user agents to rotate through.
- Be courteous with the timing of your requests. This code makes about 1 server request every few seconds. 
- Create a cache of the data so that you do not re-scrape data you already have, unless the data has changed.
- If you can scrape in random intervals throughout the day this probably makes it easier on the server.
- Try to scrape during low user traffic times, i.e: overnight
- Check the robots.txt page of the site and do not make requests to the pages that the site is restricting. Check this on "WEBSITE_NAME.COM/ROBOTS.TXT"

Disclaimer: This project is purely for entertainment and the data gathered has not and will not be used in any commercial capacity. Please respect any copyrighted data from any website that you may scrape. 

Webpage address will be censored to protect the site.


Resources:
Download the SQLite application:
https://www.sqlite.org/download.html

Download the Chrome Driver exe:
https://chromedriver.chromium.org/downloads

Interfacing Python with SQLite using the SQLite3 module:
https://docs.python.org/3/library/sqlite3.html

Get started with Selenium:
https://selenium-python.readthedocs.io/getting-started.html





