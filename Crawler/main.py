from data_base_adaptor import DataBaseAdaptor
from scrapper import Scrapper
from parser import Parser
import time

base_urls = ["https://vhdev.software", "https://github.com", "https://mipt.ru"]

num = 0
db_adaptor = DataBaseAdaptor()

while True:
    sc = Scrapper(base_urls)
    try:
        sc.extract_urls()
    except Exception:
        pass
    urls = sc.get_urls()
    for url in urls:
        try:
            parser = Parser(url)
            parser.parse_all_data()
            db_adaptor.save_content(num, parser.get_page())
            num += 1
            time.sleep(0.25)
        except Exception as ignore:
            pass

    base_urls = urls[0:100]

