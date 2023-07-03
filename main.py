import requests
import selectorlib  # used to only extract particular information
from sendemail import send_email
import time
import sqlite3

"INSERT INTO events VALUES ('Tigers','Tiger City','1989.05.20')"

URL = 'http://programmer100.pythonanywhere.com/tours/'  # The URL we are extracting Data from
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/39.0.2171.95 Safari/537.36'}

connection = sqlite3.connect('data.db')  # Connecting to the DB
cursor = connection.cursor()  # cursor object serves as the object that can execute the queries


def scraper(url):
    """Scrape the page source from the URL"""
    response = requests.get(url, headers=HEADERS)
    text = response.text
    return text


def extract(source):
    """Extracting the Content We want"""
    extractor = selectorlib.Extractor.from_yaml_file('extract.yaml')
    value = extractor.extract(source)['tours']
    return value


def store(extracted):
    row = extracted.split(',')
    row = [item.strip() for item in row]

    cursor = connection.cursor()
    cursor.execute("INSERT INTO events VALUES (?,?,?)", row)
    connection.commit()


def read(extracted):
    row = extracted.split(',')
    row = [item.strip() for item in row]
    band, city, date = row

    cursor.execute("SELECT * FROM events WHERE band = ? AND city = ? AND date = ?,", (band, city, date))
    rows = cursor.fetchall()
    print(rows)
    return rows


if __name__ == '__main__':
    while True:
        scraped = scraper(URL)
        extracted = extract(scraped)
        print(extracted)

        if extracted != 'No upcoming tours':
            row = read(extracted)
            if not row:
                store(extracted)
                send_email(message='Hey! New Event was Found')
        time.sleep(1000)
