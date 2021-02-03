import lxml
from lxml import html
import requests
from celery import Celery
from pymongo import MongoClient

app = Celery('mvptasks', broker='redis://localhost')


@app.task
def parse_monster(link):
    response = requests.get(link, stream=True)
    root = lxml.html.fromstring(response.content)
    atributos = []
    propriedades = []

    title_elem = root.xpath("//div[@class='widget-content']/legend[@class='entry-title']")
    title = title_elem[0].text.strip()
    atributos = get_attri(atributos, root)

    propriedades = get_propi(propriedades, root)

    print(f"Monstro: {title}")
    print(f"Atributos: {atributos}")
    print(f"Props: {propriedades}")
    info = {"name": title, "atributes": atributos, "property": propriedades}
    saver(info)


def saver(info):
    client = MongoClient('localhost',
                         username='root',
                         password='example')
    db = client['mvp']
    db.mvp.insert_one(info)
    print("salvo")


def get_propi(propriedades, root):
    p = 1
    while p < 10:
        attr_elem = root.xpath(
            f"//table[@class='table table-bordered table-striped table-condensed table-full'][2]/thead/tr/th[{p}]/span")
        value_elem = root.xpath(
            f"//table[@class='table table-bordered table-striped table-condensed table-full'][2]/tbody/tr/td[{p}]")
        value = value_elem[0].text.strip()
        attr = attr_elem[0].text.strip()
        propriedades.append({attr: value})
        p += 1
    return propriedades


def get_attri(atributos, root):
    i = 1
    y = 1
    while i < 11:
        value_elem = root.xpath(
            f"//div[@class='widget-content']/table[@class='table table-bordered table-striped table-condensed table-full'][1]/tbody/tr[1]/td[{i}]")
        attr_elem = root.xpath(
            f"//div[@class='widget-content']/table[@class='table table-bordered table-striped table-condensed table-full'][1]/thead/tr/th[{i}]")
        if value_elem[0].text.strip() == "":
            value_elem = root.xpath(
                f"//div[@class='widget-content']/table[@class='table table-bordered table-striped table-condensed table-full'][1]/tbody/tr[1]/td[{i}]/span")

        value = value_elem[0].text.strip()
        attr = attr_elem[0].text.strip()
        atributos.append({attr: value})
        i += 1

    while y < 12:
        value_elem = root.xpath(
            f"//div[@class='widget-content']/table[@class='table table-bordered table-striped table-condensed table-full'][1]/tbody/tr[3]/td[{y}]")
        attr_elem = root.xpath(
            f"//div[@class='widget-content']/table[@class='table table-bordered table-striped table-condensed table-full'][1]/tbody/tr[2]/th[{y}]")
        if value_elem[0].text.strip() == "":
            value_elem = root.xpath(
                f"//div[@class='widget-content']/table[@class='table table-bordered table-striped table-condensed table-full'][1]/tbody/tr[3]/td[{y}]/span")

        value = value_elem[0].text.strip()
        attr = attr_elem[0].text.strip()
        atributos.append({attr: value})
        y += 1

    return atributos