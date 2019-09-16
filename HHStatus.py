import logging
import struct
from logging import info, exception
import time

import lmdb
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter

import config

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def fetch(url="https://e-hentai.org/hentaiathome.php"):
    r = requests.Session()
    r.mount('http://', HTTPAdapter(max_retries=30))
    r.mount('https://', HTTPAdapter(max_retries=30))
    html = r.get(url, headers=config.header, cookies=config.cookie).text
    return html


def parser(html: str):
    dom = BeautifulSoup(html, 'lxml')
    hct = dom.select_one(".hct")
    td = hct.find_all("td")
    max_speed = td[9].text
    trust = td[10].text
    my_quality = td[11].text
    hitrate = td[12].text
    hathrate = td[13].text
    return max_speed, trust, my_quality, hitrate, hathrate


if __name__ == '__main__':
    # print(struct.unpack("d", bytearray(struct.pack("d", 1.2)))[0])
    # print(struct.unpack("i", bytearray(struct.pack("i", 10)))[0])
    while True:
        try:
            parser(fetch())
        except Exception as e:
            exception(e)
        time.sleep(60)