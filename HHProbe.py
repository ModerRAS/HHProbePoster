import logging
import struct
from logging import info, exception
import time

import lmdb
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter

import config

me = lmdb.open("/var/HHPP/me")
us = lmdb.open("/var/HHPP/us")
asia = lmdb.open("/var/HHPP/asia")
eur = lmdb.open("/var/HHPP/eur")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def fetch(url="https://e-hentai.org/hentaiathome.php"):
    r = requests.Session()
    r.mount('http://', HTTPAdapter(max_retries=30))
    r.mount('https://', HTTPAdapter(max_retries=30))
    html = r.get(url, headers=config.header, cookies=config.cookie).text
    return html


def parser(html: str):
    this_time = time.time()
    dom = BeautifulSoup(html, 'lxml')
    hct = dom.select_one(".hct")
    td = hct.find_all("td")
    my_quality = int(td[11].text)
    # info(this_time)
    # info(my_quality)
    us_table = dom.find("table")
    tr = us_table.find_all("tr")
    new_td = tr[1].find_all("td")
    asia_td = tr[2].find_all("td")
    eur_td = tr[3].find_all("td")
    us_quality = int(new_td[7].text)
    asia_quality = int(asia_td[7].text)
    eur_quality = int(eur_td[7].text)
    # info(us_quality)
    me_db = me.begin(write=True)
    us_db = us.begin(write=True)
    asia_db = asia.begin(write=True)
    eur_db = eur.begin(write=True)
    now = bytearray(struct.pack("d", this_time))
    my_quality_bytes = bytearray(struct.pack("i", my_quality))
    us_quality_bytes = bytearray(struct.pack("i", us_quality))
    asia_quality_bytes = bytearray(struct.pack("i", asia_quality))
    eur_quality_bytes = bytearray(struct.pack("i", eur_quality))
    me_db.put(now, my_quality_bytes)
    us_db.put(now, us_quality_bytes)
    asia_db.put(now, asia_quality_bytes)
    eur_db.put(now, eur_quality_bytes)
    me_db.commit()
    us_db.commit()
    asia_db.commit()
    eur_db.commit()
    info((this_time, my_quality, us_quality, asia_quality, eur_quality))

def Loop():
	while True:
        try:
            parser(fetch())
        except Exception as e:
            exception(e)

        time.sleep(300)
            

if __name__ == '__main__':
    # print(struct.unpack("d", bytearray(struct.pack("d", 1.2)))[0])
    # print(struct.unpack("i", bytearray(struct.pack("i", 10)))[0])
    while True:
        try:
            parser(fetch())
            time.sleep(300)
        except Exception as e:
            exception(e)
            time.sleep(300)
