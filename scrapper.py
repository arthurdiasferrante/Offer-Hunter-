import requests
from bs4 import BeautifulSoup



def search_offers():
    url = "https://realpython.github.io/fake-jobs"
    print(f"Acessando o site: {url} ...")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    offer_box = soup.find_all("div", class_= "card")
    requires = ["Dev", "Programmer", "Cybersecurity", "System"]

    offer_list = []

    print("--- RASTREIO INICIADO ---")
    for box in offer_box:
        title_element = box.find("h2", class_="title is-5")
        buttons = box.find_all("a")
        link_element = buttons[1]

        title = title_element.text.strip()
        link = link_element["href"]

        for require in requires:
            if require in title:
                formatted_offer = f"<b>{title}</b>\n <a href='{link}'>Acessar vaga</a>\n"
                offer_list.append(formatted_offer)
                break

    if len(offer_list) == 0:
        return "Nenhuma vaga encontrada"

    final_text = "<b>Vagas encontradas: </b>\n\n" + "\n".join(offer_list)
    return final_text


