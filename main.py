import requests
import selectorlib  # used to only extract particular information
from sendemail import send_email

URL = 'http://programmer100.pythonanywhere.com/tours/'  # The URL we are extracting Data from
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/39.0.2171.95 Safari/537.36'}


def scraper(url):
    """Scrape the page source from the URL"""
    response = requests.get(url, headers=HEADERS)
    text = response.text
    return text


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file('extract.yaml')
    value = extractor.extract(source)['tours']
    return value





def store(extracted):
    with open('data.txt', 'a') as file:
        file.write(extracted + '\n')


def read():
    with open('data.txt', 'r') as file:
        return file.read()


if __name__ == '__main__':
    scraped = scraper(URL)
    extracted = extract(scraped)
    print(extracted)
    content = read()
    if extracted != 'No upcoming tours':
        if extracted not in content:
            store(extracted)
            send_email(message='Hey! New Event was Found')
