import requests
import selectorlib  # used to only extract particular information

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


if __name__ == '__main__':
    scraped = scraper(URL)
    extracted = extract(scraped)
    print(extracted)

