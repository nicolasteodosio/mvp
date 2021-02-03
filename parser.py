import lxml
import requests
from lxml import html
from tasks import parse_monster

MVPS_URL = "https://browiki.org/wiki/MVP"

if __name__ == '__main__':
    res = requests.get(MVPS_URL, stream=True)
    root = lxml.html.fromstring(res.content)

    links = root.xpath("//span[@class='plainlinks']/a[@class='external text']/@href")

    for link in links:
        if "monster" in link:
            parse_monster.delay(link)
