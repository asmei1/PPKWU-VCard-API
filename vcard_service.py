from flask import Flask
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

SERVER_URL = "https://localhost/"
BASE_URL = "https://panoramafirm.pl/szukaj?k="


@app.route('/get_list_workers_vcards/<name>', methods=["GET"])
def get_list_with_workers_vcards(name):
    if not name:
        return {}, 400

    page = requests.get(BASE_URL + name)
    soup = BeautifulSoup(page.content, "html.parser")
    links_to_companies = [a['href'] for a in soup.find_all("a", class_="company-name")]

    workers_vcards = []

    for link in links_to_companies:
        workers_vcards.append(generate_worker_vcard(link))

    print(workers_vcards)

    return {"Hello": "World"}

def prepare_worker_property(property):
    p = property
    if not p:
        p = None
    else:
        p = p.text.strip()
        if p == "brak":
            p = None

    return p

def generate_worker_vcard(link):
    if not link:
        return {}, 400

    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    company_name = soup.find("h1").text
    details = soup.find("div", class_="contact-data")

    email = prepare_worker_property(details.find("a", class_="addax-cs_ip_mod_send_email"))
    phone = prepare_worker_property(details.find("a", class_="addax-cs_ip_phonenumber_click"))
    website = prepare_worker_property(details.find("a", {"target": "_blank"}))

    return company_name



if __name__ == '__main__':
    app.run()
