from parser import Page
import json


class DataBaseAdaptor:
    def __init__(self):
        self.save_path = '/home/vh/VHFind/Crawler/save/'

    def save_content(self, number: int, page: Page):
        """Save page content to data index"""
        with open(self.save_path + str(number) + '.txt', 'w') as file:
            file.write(json.dumps(page.tokenized_content))
