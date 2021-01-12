import re

from flask import Flask, jsonify, request, send_file, render_template
from bs4 import BeautifulSoup
import requests
import vobject

app = Flask(__name__)

SERVER_URL = "https://localhost/"
BASE_URL = "https://panoramafirm.pl/"


def prepare_worker_property(property):
    p = property
    if not p:
        p = None
    else:
        p = p.text.strip()
        if p == "brak":
            p = None

    return p


def parse_address(property):
    if not property:
        return None

    tokens = property.split(",")
    if len(tokens) != 2:
        return None

    street = tokens[0]
    postal_code, *city, region = tokens[1].split(" ")
    city = " ".join(city)

    return street.strip(), postal_code.strip(), city.strip(), region.strip()


def generate_worker_properties(link):
    if not link:
        return {}, 400

    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    company_name = soup.find("h1").text
    details = soup.find("div", class_="contact-data")

    email = prepare_worker_property(details.find("a", class_="addax-cs_ip_mod_send_email"))
    phone = prepare_worker_property(details.find("a", class_="addax-cs_ip_phonenumber_click"))
    website = details.find(text=re.compile(r'\b({0})\b'.format("Strona www"), flags=re.IGNORECASE))
    if website:
        website = prepare_worker_property(website.findNext('div'))
    social_media = details.find(text=re.compile(r'\b({0})\b'.format("Media społecznościowe"), flags=re.IGNORECASE))
    if social_media:
        social_media = prepare_worker_property(social_media.findNext('div'))

    address = (soup.select_one('.address > div > div:nth-of-type(2)'))
    if address:
        address = address.text.strip()

    return company_name, email, phone, website, social_media, address


def generate_worker_vcard(link):
    company_name, email, phone, website, social_media, address = generate_worker_properties(link)
    v = vobject.vCard()
    v.add("n")
    v.add("fn")
    v.fn.value = company_name
    if email:
        v.add("email")
        v.email.value = email

    if website:
        v.add("website")
        v.website.value = website

    if phone:
        v.add("tel")
        v.tel.value = phone

    if social_media:
        v.add("url")
        v.url.value = social_media

    if address:
        v.add("adr")
        adr = parse_address(address)
        if adr:
            v.add("adr")
            v.adr.value = vobject.vcard.Address(
                street=adr[0] or '',
                city=adr[2] or '',
                region=adr[3] or '',
                code=adr[2] or '',
                country='',
                box='',
                extended=''
            )
    return v.serialize()


@app.route('/get_worker_vcard', methods=["GET"])
def get_worker_vcard():
    page = request.args.get('page')

    vCard = generate_worker_vcard(page)

    import io
    f = io.BytesIO(str.encode(vCard))
    return send_file(f, mimetype="text/x-vcard")


@app.route('/parse_and_produce_workers', methods=["GET"])
def parse_and_produce_workers():
    companies = []
    name = request.args.get('name', "")
    page_count = int(request.args.get('page_count', "1"))
    limit = int(request.args.get('limit', "20"))

    if not name or page_count < 0 or limit < 1:
        return {}, 400

    for i in range(1, page_count + 1):
        url = BASE_URL + name + "/firmy," + str(i)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        companies += [(a.text.strip(), a['href']) for a in soup.find_all("a", class_="company-name")]

    companies = companies[:limit]

    return render_template('worker_list.html', name=name, companies=companies)


if __name__ == '__main__':
    app.run()
