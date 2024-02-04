from bs4 import BeautifulSoup
import json
import requests
from dotenv import load_dotenv
import os
from openai import OpenAI

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}


def search(query):
    url = f'https://www.google.com/search?q={query} issues in sustainability&ie=utf-8&oe=utf-8&num=10'
    html = requests.get(url, headers=headers)

    soup = BeautifulSoup(html.text, 'html.parser')

    allData = soup.find_all("div", {"class": "g"})

    g = 0
    Data = []
    l = {}
    for i in range(0, len(allData)):
        link = allData[i].find('a').get('href')

        if link is not None:
            if link.find('https') != -1 and link.find('http') == 0 and link.find('aclk') == -1:
                g += 1
                l["link"] = link
                try:
                    l["title"] = allData[i].find('h3', {"class": "DKV0Md"}).text
                except:
                    l["title"] = None

                try:
                    l["description"] = allData[i].find("div", {'data-sncf': ['1', '2', '3']}).text
                except:
                    l["description"] = None

                l["position"] = g

                Data.append(l)

                l = {}

            else:
                continue

        else:
            continue

    return Data
