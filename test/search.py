from bs4 import BeautifulSoup
import json
import requests

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

def search(query):
    url = f'https://www.google.com/search?q={query}&ie=utf-8&oe=utf-8&num=10'
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

# Get user input for the search query
user_query = input("What do you want to search for? ")
query_result = search(user_query)

# If one of the result is a wikipedia article, summarize the content of the article and put it as its description
for result in query_result:
    if 'wikipedia' in result['link']:
        wikipedia_url = result['link']
        wikipedia_html = requests.get(wikipedia_url, headers=headers)
        wikipedia_soup = BeautifulSoup(wikipedia_html.text, 'html.parser')
        try:
            wikipedia_summary = wikipedia_soup.find('p').text
            result['description'] = wikipedia_summary
        except:
            pass


# Create a json file and write the data to it
with open('data.json', 'w') as file:
    json.dump(query_result, file)
