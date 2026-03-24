import requests
from bs4 import BeautifulSoup


def try_access():
    url = "https://programathor.com.br/jobs/page/1454"

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
        title_element = box.find("h3")

        if title_element:
            title_classes = title_element.get("class", [])

            if "color-gray" in title_classes:
                print(f"Vagas expiraram na página (encontrei a color-gray), parando a varredura")
                break

        link_element =  box.find("a")
        icon_element = box.find("i", class_="fas fa-map-marker-alt")

        location_text = ""
        if icon_element:
            location_text = icon_element.parent.text.strip()

        if title_element and link_element:
            title = title_element.text.strip()
            link = "https://programathor.com.br" + link_element["href"]

            valid_location = False
            wished_location = ["são paulo", "guarulhos", "remoto"]

            for loc in wished_location:
                if loc in location_text.lower():
                    valid_location = True
                    break

            if valid_location:
                offer_lists.append({"title": title, "link": link, "location": location_text})


    if len(offer_lists) == 0:
        print("Sem vagas aqui")
        return
    print(f"Vagas encontradas ao todo: {len(offer_lists)}")

    for vaga in offer_lists:
        print(f"Vaga: {vaga['title']} | Local: {vaga['location']}\n Link: {vaga['link']}")


try_access()
