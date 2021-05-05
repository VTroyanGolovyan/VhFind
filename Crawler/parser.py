import requests
from bs4 import BeautifulSoup
from langdetect import detect
from fonetika.soundex import RussianSoundex, EnglishSoundex


def letters_detect(text: str) -> str:
    """detect letters language in text"""
    if set(text).issubset(set('qwertyuiopasdfghjklzxcvbnm')):
        return 'en'
    if set(text).issubset(set('йцукенгшщзхъфывапролджэячсмитьбюё')):
        return 'ru'
    return 'undefined'


class Token:
    """Token class"""
    def __init__(self, token: str):
        self.text = token
        self.metaphone = ""
        self.lang = letters_detect(token)
        if self.lang == 'ru':
            soundex = RussianSoundex(delete_first_letter=True)
            self.metaphone = soundex.transform(token)
        if self.lang == 'en':
            soundex = EnglishSoundex(delete_first_letter=True)
            self.metaphone = soundex.transform(token)

    def __hash__(self) -> int:
        return self.text.__hash__()

    def __str__(self):
        return 'Token: ' + self.text


class Page:
    """Class for page data storage"""

    def __init__(self, url: str, title: str, tokenized_content: list):
        self.url = url
        self.title = title
        self.tokenized_content = tokenized_content
        self.id = 0
        self.lang = detect(' '.join(
            [token.text for token in self.tokenized_content])
        )

    def get_counted_tokens(self) -> dict:
        """Dict with tokens as keys and frequency as values"""
        result = dict()
        for token in self.tokenized_content:
            if token in result:
                result[token] += 1
            else:
                result[token] = 1
        return result

    def set_id(self, id: int):
        self.id = id


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

    def _tokenize_content(self, bs_parser: BeautifulSoup):
        """Get tokens list from page text content"""
        body = bs_parser.find('body')
        text = str(body.text)
        text = text.lower()
        extra = set("""1234567890-=@#$%^&*()_+,/<>;:'"[{}]!.?"'""")
        for letter in extra:
            text = text.replace(letter, "")

        self.tokenized_content = [Token(token) for token in text.split()]

    def _parse_title(self, bs_parser):
        """Page title"""
        title = bs_parser.find('title')
        self.title = str(title.text)
