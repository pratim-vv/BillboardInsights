import requests
from bs4 import BeautifulSoup
from typing import List

BASE_URL = 'https://www.last.fm/'



def get_genre(information: str) -> List[str]:
    search_string = information.strip().replace(' ', '+')
    response = requests.get(BASE_URL + 'search?q=' + search_string)
    soup = BeautifulSoup(response.text, 'html.parser')
    tracks = soup.find('td', class_='chartlist-name')
    if tracks == None:
        return ['Invalid Information']
    first_track = tracks.find_all('a')
    return [first_track]
    

if __name__ == '__main__':

    information = 'Haterade'
    print(get_genre(information=information))
    