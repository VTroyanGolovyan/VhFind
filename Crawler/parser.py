import re

import requests
from bs4 import BeautifulSoup


class Page:
    def __init__(self, url: str, title: str, tokenized_content: list):
        self.url = url
        self.title = title
        self.tokenized_content = tokenized_content


class Parser:
    def __init__(self, url: str):
        self.url = url
        self.raw_data = ''
        self.tokenized_content = []
        self.title = ''

    def get_page(self) -> Page:
        return Page(
            self.url,
            self.title,
            self.tokenized_content
        )

    def parse_all_data(self):
        self._extract_raw_data()
        parser = BeautifulSoup(self.raw_data, 'lxml')
        self._tokenize_content(parser)

    def _extract_raw_data(self):
        response = requests.get(self.url)
        self.raw_data = response.text

    def _tokenize_content(self, bs_parser):
        body = bs_parser.find('body')
        text = str(body.text)
        text = text.lower()
        extra = set("""1234567890-=@#$%^&*()_+,/<>;:'"[{}]!.?"'""")
        for letter in extra:
            text = text.replace(letter, "")

        self.tokenized_content = text.split()

    def _get_title(self, bs_parser):
        title = bs_parser.find('title')
        self.title = str(title.text)
