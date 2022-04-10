import urllib.request
from slugify import slugify
import os
import re
import html

import requests


class scraper:
    def __init__(self):
        self.master_url = input("Enter URL: ")
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

        '''format urls'''
        self.urls = [url + '.mov' for url in self.urls]
        self.urls = [html.unescape(url) for url in self.urls]
        self.urls = [url.replace(" ", "%20") for url in self.urls]

        '''scrape video names'''
        self.vid_names = re.findall(
            r"(?<=.mov\">).*(?=<\/a>)",
            self.master_data.text,
        )

        '''format names'''
        # self.vid_names = [name.replace(" ", "-") for name in self.vid_names]
        # self.vid_names = [name.replace(".", "_") for name in self.vid_names]
        # self.vid_names = [name.replace(":", "-") for name in self.vid_names]
        # self.vid_names = [name.replace("<sub>", "-")
        #                   for name in self.vid_names]
        # self.vid_names = [name.replace("</sub>", "")
        #                   for name in self.vid_names]
        self.vid_names = [slugify(name) for name in self.vid_names]
        self.vid_names = [name + '.mov' for name in self.vid_names]

        print("Total number of URLs available: ", len(self.urls))

    def download_urls(self):
        for name, link in zip(self.vid_names, self.urls):
            if not(os.path.exists('files/'+name)):
                print("Downloading file: ", name)
                urllib.request.urlretrieve(link, 'files/'+name)


if __name__ == '__main__':
    obj = scraper()
    obj.scrape_urls()
    obj.download_urls()

    print('Finished download!')
