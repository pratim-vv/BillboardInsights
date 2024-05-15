"""
billboard_scraper.py

This module provides techniques for retrieving and storing information from the billboard charts.

Includes functions for:
- Gathering all the tracks of a given chart week
- Appending the master-list csv with updated charting track details
"""
from date_tools import generate_dates
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from typing import List
import csv

def get_hot100(week: str) -> List[str]:
    """
    Retrieves Hot 100 chart data for a given week.

    Parameters:
        week (str): The charting week in the format "YYYY-MM-DD".

    Returns:
        (List[List[str]]): A list of lists containing Hot 100 chart data for each song.
            Each inner list contains the following elements:
                - Charting Week (str): The week of the chart data.
                - Chart Position (str): The position of the song on the chart.
                - Song Title (str): The title of the song.
                - Artist (str): The artist of the song.
                - Previous Position (str): The previous position of the song on the chart.
                - Peak Position (str): The peak position of the song on the chart.
                - Weeks on Chart (str): The number of weeks the song has been on the chart.
    
    Raises:
        ValueError: If the HTML structure of a Track is not recognized.
    """
    url = 'https://www.billboard.com/charts/hot-100/' + week + '/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    hot_100 = soup.find_all(class_='o-chart-results-list-row-container')
    chart_data = []
    for song in hot_100:
        title = song.find('h3').get_text(strip=True)
        information = song.find_all(class_='c-label')
        if len(information) == 8:
            song_info = [
                week,                                # charting week
                information[0].get_text(strip=True), # chart position
                title,                               # song title
                information[1].get_text(strip=True), # artist
                information[2].get_text(strip=True), # previous position
                information[3].get_text(strip=True), # peak position
                information[4].get_text(strip=True)  # weeks on chart
                ]
        elif len(information) == 10:                 # New Entries & Re-entries
            song_info = [
                week,                                # charting week
                information[0].get_text(strip=True), # chart position
                title,                               # song title
                information[3].get_text(strip=True), # artist
                information[4].get_text(strip=True), # previous position
                information[5].get_text(strip=True), # peak position
                information[6].get_text(strip=True)  # weeks on chart
                ]
        else:
            raise ValueError("Unnaccounted Track Formatting")
        chart_data.append(song_info)
    
    return chart_data

def append_csv(dates: List[str], file_name='billboard_hot100.csv'):
    """
    Appends Billboard Hot100 chart data for multiple dates to a CSV file.

    Parameters:
        dates (List[str]): A list of charting weeks in the format "YYYY-MM-DD".
        file_name (str): The name of the CSV file to which the data will be appended. 
            Default is 'billboard_hot100.csv'.
    """
    with open(file_name, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        for date in dates:
            hot100_data = get_hot100(date)
            writer.writerows(hot100_data)

if __name__ == '__main__':
   dates = ['2018-01-03'] + generate_dates(weekdays=[5], start_date=datetime(2018, 1, 3))
   append_csv(dates=dates)
   

