"""
lastfm_scraper.py

This module provides functions for collecting song information from Last.fm

Includes functions for:
- Gathering the song tags of a given url corresponding to a track.
- Collecting song metadata information given a search 
- Creating a csv file easily access songs without repeated searches
"""


import requests
from bs4 import BeautifulSoup
from typing import List
import json
import csv

BASE_URL = 'https://www.last.fm/'


def get_tags(tag_url: str) -> str:
    """
    Retrieves song tags associated with a given URL.

    Args:
        tag_url (str): The URL of the genre.

    Returns:
        tags (str): The tags associated with the song URL, or 'Tag Error' if not found.
    """
    tags = 'Tag Error'
    response = requests.get(tag_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    hidden_div = soup.find('div', class_='hidden')
    if hidden_div:
        data_tealium_data = hidden_div.get('data-tealium-data')
        if data_tealium_data:
            tags = json.loads(data_tealium_data)['tag']
    return tags
    

def get_information(information: str) -> List[str]:
    """
    Retrieves song information related to a given search query.

    Parameters:
        information (str): Information for song identification, given in form of "Song Title Artist"

    Returns:
        song_information (List[str]): Song metadata from search query in the format of [Runtime, Tags, LastFm Reference]
    """
    search_string = information.strip().replace(' ', '+')
    response = requests.get(BASE_URL + 'search?q=' + search_string)
    soup = BeautifulSoup(response.text, 'html.parser')
    tracks = soup.find('td', class_='chartlist-name')
    if tracks == None:
        return ['Invalid Information', 'Invalid Information', 'Invalid Information']
    first_track = tracks.find('a')
    href_tag = first_track['href']
    tags = get_tags(tag_url=BASE_URL[:-1] + href_tag + '/+tags')
    length = soup.find('td', class_='chartlist-duration').get_text(strip=True)
    song_information = [length, tags, href_tag[7:]]
    return song_information
    

if __name__ == '__main__':

    information = 'Haterade'
    print(get_information(information=information))
    

    