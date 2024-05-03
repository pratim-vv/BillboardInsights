
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def generate_dates(days=[0], start_date=datetime(1958, 8, 4), end_date=datetime.now()):
    dates = []
    current_date = start_date
    while current_date <= end_date:
        if current_date.weekday() in days: 
            dates.append(current_date.strftime('%Y-%m-%d'))
        current_date += timedelta(days=1)
    return dates

def week_of(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.find('p', class_='a-font-primary-medium-xs').get_text(strip=True)

def get_day_of_week(date_string: str) -> str:
    date_part = date_string.split(" ")[-3:]
    reconstructed_date_string = " ".join(date_part)
    date_object = datetime.strptime(reconstructed_date_string, "%B %d, %Y")
    day_of_week = date_object.strftime("%A")

    return day_of_week

def detect_day_switch():
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