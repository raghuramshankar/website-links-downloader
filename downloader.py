from distutils.util import subst_vars
import os
import re
import html

import requests


class scraper:
    def __init__(self):
        self.master_url = (
            "http://mocha-java.uccs.edu/ECE5720/index.html"
        )
        self.master_data = requests.get(
            self.master_url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            },
            allow_redirects=False,
        )

    def scrape_urls(self):
        self.urls = re.findall(
            r"(?<=a href=\").*(?=\.mov\")",
            self.master_data.text,
        )

        self.urls = [url + '.mov' for url in self.urls]

        self.urls = [html.unescape(url) for url in self.urls]

        print("Total number of URLs available: ", len(self.urls))


if __name__ == '__main__':
    obj = scraper()
    obj.scrape_urls()
