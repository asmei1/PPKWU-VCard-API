from flask import Flask, jsonify, request
from bs4 import BeautifulSoup
import requests
import vobject

app = Flask(__name__)

SERVER_URL = "https://localhost/"
BASE_URL = "https://panoramafirm.pl/szukaj?k="


def prepare_worker_property(property):
    p = property
    if not p:
        p = None
    else:
        p = p.text.strip()
        if p == "brak":
            p = None

    return p

def generate_worker_properties(link):
    if not link:
        return {}, 400

    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    company_name = soup.find("h1").text
    details = soup.find("div", class_="contact-data")

    email = prepare_worker_property(details.find("a", class_="addax-cs_ip_mod_send_email"))
    phone = prepare_worker_property(details.find("a", class_="addax-cs_ip_phonenumber_click"))
    website = prepare_worker_property(details.find("a", {"target": "_blank"}))

    return company_name, email, phone, website

def generate_worker_vcard(link):
    company_name, email, phone, website = generate_worker_properties(link)
    v = vobject.vCard()
    v.add("n")
    v.add("fn")
    v.fn.value = company_name
    if email:
        v.add("email")
        v.email.value = email
        v.email.type_param = 'INTERNET'

    if website:
        v.add("website")
        v.website.value = website
        v.website.type_param = 'INTERNET'

    if phone:
        v.add("tel")
        v.tel.value = phone
        v.tel.type_param = 'VOICE'

    return v.serialize()

@app.route('/get_worker_vcard', methods=["GET"])
def get_worker_vcard():
    page = request.args.get('page')

    vCard = generate_worker_vcard(page)
    return {"vcard", jsonify(vCard)}




if __name__ == '__main__':
    app.run()
