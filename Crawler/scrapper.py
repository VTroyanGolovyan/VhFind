import time

from bs4 import BeautifulSoup
import requests
from link_worker import LinkWorker


class Scrapper:
    def __init__(self, base_urls: list):
        self.base_urls = base_urls
        self.urls = set()

    def extract_urls(self):
        """Extract all urls by base urls"""
        for url in self.base_urls:
            try:
                new_urls = Scrapper._get_page_urls(url)
                self.urls = set.union(self.urls, new_urls)
                time.sleep(0.25)
            except ConnectionError:
                pass

    def get_urls(self) -> list:
        """Return scrapped urls list"""
        return list(self.urls)

    @staticmethod
    def _get_page_urls(url: str) -> set:
        """Parse urls from page"""
        result = set()
        response = requests.get(url)
        parser = BeautifulSoup(response.text, 'lxml')
        lw = LinkWorker(url, '')
        for a_element in parser.find_all('a'):
            link_string = str(a_element.get('href'))
            if link_string.find('https://') == -1 and link_string.find(':') != -1:
                continue
            if link_string.find('https://') != -1:
                result.add(link_string)
            else:
                lw.update_link(link_string)
                result.add(lw.get_absolute_link())
        return result
