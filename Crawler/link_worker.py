from urllib.parse import urljoin


class LinkWorker:
    def __init__(self, page, relative_link):
        self.page = page
        self.relative_link = relative_link

    def get_absolute_link(self):
        """Transform and return absolute link from relative"""
        result = urljoin(self.page, self.relative_link)
        return result

    def update_link(self, url):
        """Change relative link"""
        self.relative_link = url
