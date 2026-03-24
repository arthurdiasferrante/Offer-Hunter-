import random
import time

import requests
from bs4 import BeautifulSoup


def set_page_range(initial_page, last_page):
    if initial_page > last_page:
        return "O número da página final não pode ser maior que o da página inicial"

    if last_page - initial_page > 40:
        return "O valor máximo permitido de páginas por vez é 40"
    else:
        return search_offers_programathor(initial_page, last_page)



def search_offers_programathor(initial_page, last_page):

    headers = {
        "User-agent": "Mozilla/5.0 (Windows NT10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0 Safari/537.36"
    }


    requires = ["Estágio", "Internship", "Júnior", "Estagiário"]
    offer_lists = []

    print("--- RASTREANDO ---")
    while initial_page <= last_page:
        url = f"https://programathor.com.br/jobs/page/{initial_page}"
        print(f"Lendo: {url}")
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
        except requests.exceptions.Timeout:
            return "⏱️ Timeout ao acessar Programathor. Tente novamente em instantes."
        except requests.exceptions.HTTPError as e:
            return f"⚠️ Erro HTTP ao buscar vagas: {e.response.status_code}"
        except requests.exceptions.RequestException:
            return "⚠️ Não foi possível acessar Programathor agora. Tente novamente mais tarde."

        soup = BeautifulSoup(response.text, "html.parser")

        offer_box = soup.find_all("div", class_="cell-list")
        if not offer_box:
            return "⚠️ A estrutura da página mudou. Tente novamente mais tarde."

        for box in offer_box:
            title_element = box.find("h3")

            if title_element:
                title_classes = title_element.get("class", [])

                if "color-gray" in title_classes:
                    initial_page = last_page + 100
                    print(f"Vagas expiraram na página (encontrei a color-gray), parando a varredura")
                    break

            link_element =  box.find("a")
            icon_element = box.find("i", class_="fas fa-map-marker-alt")

            location_text = ""
            if icon_element:
                location_text = icon_element.parent.text.strip()

            if title_element and link_element:
                title = title_element.text.strip()
                href = link_element.get("href") if link_element else None
                if not href:
                    continue
                link = "https://programathor.com.br" + link_element["href"]

                valid_location = False
                wished_location = ["são paulo", "guarulhos", "remoto"]

                for loc in wished_location:
                    if loc in location_text.lower():
                        valid_location = True
                        break

                if valid_location:
                    offer_lists.append({"title": title, "link": link, "location": location_text})

        initial_page += 1
        time.sleep(random.randint(1, 6))


    if len(offer_lists) == 0:
        return "❌ Nenhuma vaga encontrada com esses filtros no momento"

    final_text = f"🎯 Vagas encontradas ao todo: {len(offer_lists)}\n\n"

    offers_text = []
    for offer in offer_lists:
        offer_str = f"📌 Vaga: {offer['title']}\n📍 Local: {offer['location']}\n🔗 Acesse: {offer['link']}"
        offers_text.append(offer_str)

    msg_spliter = []
    current_text = final_text

    for offer_str in offers_text:
        if len(current_text) + len(offer_str) > 4000:
            msg_spliter.append(current_text)
            current_text = offer_str
        else:
            current_text += "\n\n" + offer_str

    if current_text:
        msg_spliter.append(current_text)

    return msg_spliter
