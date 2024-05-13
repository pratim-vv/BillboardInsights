import requests
from bs4 import BeautifulSoup
from typing import List
import json

BASE_URL = 'https://www.last.fm/'


def get_tags(genre_url: str) -> str:
    response = requests.get(genre_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    hidden_div = soup.find('div', class_='hidden')
    if hidden_div:
        data_tealium_data = hidden_div.get('data-tealium-data')
        if data_tealium_data:
            return json.loads(data_tealium_data)['tag']
    return 'Tag Error'
    

def get_information(information: str) -> List[str]:
    search_string = information.strip().replace(' ', '+')
    response = requests.get(BASE_URL + 'search?q=' + search_string)
    soup = BeautifulSoup(response.text, 'html.parser')
    tracks = soup.find('td', class_='chartlist-name')
    if tracks == None:
        return ['Invalid Information', 'Invalid Information', 'Invalid Information']
    first_track = tracks.find('a')
    href_tag = first_track['href']
    tags = get_tags(genre_url=BASE_URL[:-1] + href_tag + '/+tags')
    length = soup.find('td', class_='chartlist-duration').get_text(strip=True)
    return [length, tags, href_tag[7:]]
    

if __name__ == '__main__':

    information = 'Haterade'
    print(get_information(information=information))
    

    