"""
date_tools.py

This module provides utility functions for working with dates in regards to the Billboard Hot 100 charts.

Includes functions for:
- Generating dates within a specified timeframe and weekdays.
- Retrieving the week of a Billboard chart in which the chart data is tallied from a provided URL.
- Extracting the day of the week from a "Week of" string provided by Billboard.
- Detecting days when the tallying weekday changes for tracking top songs of the week on the Billboard Hot 100 chart.
"""


import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from typing import List, Tuple

def generate_dates(weekdays=[0], start_date=datetime(1958, 8, 4), end_date=datetime.now()) -> List[str]:
    """
    Gets all dates between given times that correspond with given weekdays

    Parameters:
        weekdays (List[int]): Weekdays that user wishes to find (Mon. = 0, Tues. = 1, etc.)
        start_date (datetime): Starting date
        end_date (datetime): Ending date

    Returns:
        dates (List[str]): List of all dates that fit within given timeframe and weekday parameter, formatted as "Year-Month-Day"
    """
    dates = []
    current_date = start_date
    while current_date <= end_date:
        if current_date.weekday() in weekdays: 
            dates.append(current_date.strftime('%Y-%m-%d'))
        current_date += timedelta(days=1)
    return dates

def week_of(url: str) -> str:
    """
    Gets chart week timefram given Billboard url

    Parameters:
        url (str): Url of Billboard 100 weekly chart

    Returns:
        week_of (str): Gets string detailing the chart week,  formatted as "Week of Month Day, Year"
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    week_of = soup.find('p', class_='a-font-primary-medium-xs').get_text(strip=True)
    return week_of

def get_day_of_week(date_string: str) -> str:
    """
    Given week of string provided by billboard, returns day of the week

    Parameters:
        date_string (str): Week string provided by billboard, formatted as "Week of Month Day, Year"
    
    Returns:
        day_of_week (str): Returns weekday of provided st5ring
    """
    date_part = date_string.split(" ")[-3:]
    reconstructed_date_string = " ".join(date_part)
    date_object = datetime.strptime(reconstructed_date_string, "%B %d, %Y")
    day_of_week = date_object.strftime("%A")
    return day_of_week

def detect_day_switch() -> List[Tuple]:
    """
    All days in which the tallying weekday changes for tracking top songs of the week for the BillBoard Hot 100

    Returns:
        switches (List[(str, str, str)]): A tuple indicating when the tallying weekday changed, formatted as (date, week of, weekday)
    """
    baseline = 'https://www.billboard.com/charts/hot-100/'
    current_day = None
    switches = []
    for date in generate_dates():
        url = baseline + date + '/'
        week = week_of(url)
        weekday = get_day_of_week(week)
        if current_day != weekday:
            information = (date, week, weekday) 
            switches.append(information)
            print(information)
            current_day = weekday
    return switches

if __name__ == '__main__':
    print(detect_day_switch())

    """
    Output:
    ('1958-08-04', 'Week of August 4, 1958', 'Monday')
    ('1962-01-01', 'Week of January 6, 1962', 'Saturday')
    ('1976-06-28', 'Week of July 4, 1976', 'Sunday')
    ('1976-07-05', 'Week of July 10, 1976', 'Saturday')
    ('2018-01-01', 'Week of January 3, 2018', 'Wednesday')
    ('2018-01-08', 'Week of January 13, 2018', 'Saturday')
    """

