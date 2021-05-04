import requests
from bs4 import BeautifulSoup


class Page:
    """Class for page data storage"""
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
        """Get parsed page"""
        return Page(
            self.url,
            self.title,
            self.tokenized_content
        )

    def parse_all_data(self):
        """Parse all data from page"""
        self._extract_raw_data()
        parser = BeautifulSoup(self.raw_data, 'lxml')
        self._parse_title(parser)
        self._tokenize_content(parser)

    def _extract_raw_data(self):
        """Extract raw page data(HTML text)"""
        response = requests.get(self.url)
        self.raw_data = response.text

    def _tokenize_content(self, bs_parser):
        """Get tokens list from page text content"""
        body = bs_parser.find('body')
        text = str(body.text)
        text = text.lower()
        extra = set("""1234567890-=@#$%^&*()_+,/<>;:'"[{}]!.?"'""")
        for letter in extra:
            text = text.replace(letter, "")

        self.tokenized_content = text.split()

    def _parse_title(self, bs_parser):
        """Page title"""
        title = bs_parser.find('title')
        self.title = str(title.text)
