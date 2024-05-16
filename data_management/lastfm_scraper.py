"""
lastfm_scraper.py

This module provides functions for collecting song information from Last.fm

Includes functions for:
- Gathering the song tags of a given url corresponding to a track.
- Gathering song metadata information given a search 
- Creating a csv file easily access songs without repeated searches
- Collecting song information and storing within a csv file
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

    Parameters:
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

def generate_track_csv() -> None:
    """
    Generates a CSV file containing track information.
    """

    def create_tuple_set_from_csv(csv_file='billboard_hot100.csv'):
        tuple_set = set()
        with open(csv_file, 'r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if len(row) >= 3:  # Ensure there are at least 3 columns
                    tuple_set.add((row[2], row[3]))  # Tuple containing elements from 2nd and 3rd columns
        return tuple_set
    
    def collect_tracks():
        for pairing in create_tuple_set_from_csv():
            with open('output.csv', 'w', newline='') as output_file:
                csv_writer = csv.writer(output_file)
                csv_writer.writerows(pairing)
    
    collect_tracks()


def collection_song_information(file_name='song_information.csv', start_idx=0, end_idx=31266) -> None:
    """
    Collects information about songs and writes it to a CSV file.

    This function reads song information from a file named 'tracks.csv' and writes
    it to a CSV file specified by 'file_name'. It collects information for songs 
    within the range of indices specified by 'start_idx' and 'end_idx' (inclusive).

    Parameters:
        file_name (str): The name of the CSV file to write the information to. 
        start_idx (int): The start index of songs to collect information for. 
        end_idx (int): The end index of songs to collect information for. 
    """
    def get_tracks(start=0, end=31266, file_name='tracks.csv'):
        tracks = []
        with open(file_name, 'r') as file:
            csv_reader = csv.reader(file)
            for index, row in enumerate(csv_reader):
                if start <= index <= end:
                    tracks.append(tuple(row))  # Join the row elements into a single string
        return tracks

    tracks = get_tracks(start=start_idx, end=end_idx)
    with open(file_name, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        for title, artist in tracks:
            information = get_information(title + ' ' + artist)
            writer.writerow([title, artist] + information)
            print(f'{title}, {artist}')
    

if __name__ == '__main__':
    collection_song_information(start_idx=3001, end_idx=10000)
    

    