from config import ConfigStorage

from data_base_adaptor import DataBaseAdaptor
from scrapper import Scrapper
from parser import Parser
import time

base_urls = ["https://vhdev.software", "https://www.m24.ru/news", "https://mipt.ru"]

num = 0

crawler_config = ConfigStorage('/home/vh/VHFind/Crawler/crawler.ini')
db_adaptor = DataBaseAdaptor(crawler_config.get_config_section('postgresql'))


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

