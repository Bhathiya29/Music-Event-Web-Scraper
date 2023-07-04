import requests
import selectorlib  # used to only extract particular information
import sendemail
import time
import sqlite3

"INSERT INTO events VALUES ('Tigers','Tiger City','1989.05.20')"

URL = 'http://programmer100.pythonanywhere.com/tours/'  # The URL we are extracting Data from
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/39.0.2171.95 Safari/537.36'}


class Event:

    def scraper(self, url):
        """Scrape the page source from the URL"""
        response = requests.get(url, headers=HEADERS)
        text = response.text
        return text

    def extract(self, source):
        """Extracting the Content We want"""
        extractor = selectorlib.Extractor.from_yaml_file('extract.yaml')
        value = extractor.extract(source)['tours']
        return value


class Database:

    def __init__(self):
        self.connection = sqlite3.connect('data.db')  # Connecting to the DB
        # self.cursor = connection.cursor()  # cursor object serves as the object that can execute the queries

    def store(self, extracted):
        row = extracted.split(',')
        row = [item.strip() for item in row]

        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO events VALUES (?,?,?)", row)
        self.connection.commit()

    def read(self, extracted):
        row = extracted.split(',')
        row = [item.strip() for item in row]
        band, city, date = row

        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM events WHERE band = ? AND city = ? AND date = ?,", (band, city, date))
        rows = cursor.fetchall()
        print(rows)
        return rows


if __name__ == '__main__':
    while True:
        event = Event()
        scraped = event.scraper(URL)
        extracted = event.extract(scraped)
        print(extracted)

        if extracted != 'No upcoming tours':
            database = Database()
            row = database.read(extracted)
            if not row:
                database.store(extracted)
                email = sendemail.Email()
                email.send_email(message='Hey! New Event was Found')
        time.sleep(1000)
