from flask import Flask
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

BASE_URL = "https://panoramafirm.pl/szukaj?k="

@app.route('/get_list_of_workers/<name>', methods=["GET"])
def string_api(name):
    if not name:
        return {}, 400

    page = requests.get(BASE_URL + name)
    soup = BeautifulSoup(page.content, "html.parser")
    links_to_companies = soup.find_all("a")

    return {"Hello": "World"}


if __name__ == '__main__':
    app.run()
