import requests
from bs4 import BeautifulSoup


def try_access():
    global title, link
    url = "https://programathor.com.br/jobs"

    headers = {
        "User-agent": "Mozilla/5.0 (Windows NT10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0 Safari/537.36"
    }

    print(f"Testando acesso ao site: {url} ...")

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    offer_box = soup.find_all("div", class_="cell-list")
    requires = ["Estágio", "Internship", "Júnior", "Estagiário"]

    offer_lists = []

    print("--- RASTREANDO ---")
    for box in offer_box:
        title_element = box.find("h3", class_="text-24 line-height-30")
        link_element =  box.find("a")

        if title_element and link_element:
            title = title_element.text.strip()
            link = "https://programathor.com.br" + link_element["href"]

        offer_lists.append({"title": title, "link": link})


    if len(offer_lists) == 0:
        print("Sem vagas aqui")
        return
    print(f"Vagas encontradas ao todo: {len(offer_lists)}")

    for vaga in offer_lists:
        print(f"Vaga: {vaga['title']} | Link: {vaga['link']}")

try_access()
