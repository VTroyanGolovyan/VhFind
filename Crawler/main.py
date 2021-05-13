from config import ConfigStorage

from data_base_adaptor import DataBaseAdaptor
from scrapper import Scrapper
from parser import Parser
import time

base_urls = ["https://ru.wikipedia.org/wiki/%D0%92%D0%B8%D0%BA%D0%B8%D0%BF%D0%B5%D0%B4%D0%B8%D1%8F:%D0%90%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D0%BD%D1%8B%D0%B9_%D1%83%D0%BA%D0%B0%D0%B7%D0%B0%D1%82%D0%B5%D0%BB%D1%8C"]

crawler_config = ConfigStorage('/var/www/html/VHFind/Crawler/crawler.ini')
db_adaptor = DataBaseAdaptor(crawler_config.get_config_section('postgresql'))


while True:
    sc = Scrapper(base_urls)
    try:
        sc.extract_urls()
    except Exception as ignore:
        print(ignore)
    urls = sc.get_urls()
    for url in urls:
        try:
            parser = Parser(url)
            parser.parse_all_data()
            db_adaptor.save_content(parser.get_page())
            time.sleep(0.25)
        except Exception as ignore:
            print(ignore)

    base_urls = urls

