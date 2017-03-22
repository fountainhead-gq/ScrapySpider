# -*- coding: utf-8 -*-

import sys
from multiprocessing import Pool
import requests
import os
from bs4 import BeautifulSoup

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36'
}

def crawl_url_name(_id):
    url = "http://www.ximalaya.com/tracks/{0}.json".format(_id)
    body = requests.get(url, headers=header).json()
    name = body['title'] + ".mp3"
    url = body['play_path_64']

    return url, name

def download_file(url, name):
    r = requests.get(url, stream=True, headers=header)
    if name not in '122. How much do parents matter?.mp3':
        with open(name, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

    return name + "downloaded."

def download(_id):
    url, name = crawl_url_name(_id)
    return download_file(url, name)

def get_ids(web_url):
    r = requests.get(web_url, headers=header)
    soup = BeautifulSoup(r.text, "html.parser")
    newlist = soup.find("div", { "class" : "personal_body" })
    allids = newlist.get("sound_ids")
    idlist = allids.split(",")
    return idlist

def main(web_url):
    print("crawling web with:", web_url)
    ids = get_ids(web_url)
    print("Fetching ids: ", ids)

    with Pool(5) as p:
        p.map(download, ids)

if __name__ == '__main__':
    try:
        main(sys.argv[1])
        print("Finished")
    except IndexError:
        print("python xmly.py http://www.ximalaya.com/album/4486765")
