import requests
from bs4 import BeautifulSoup


def search_offers_programathor():
    url = "https://programathor.com.br/jobs"

    headers = {
        "User-agent": "Mozilla/5.0 (Windows NT10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0 Safari/537.36"
    }

    print(f"Testando acesso ao site: {url} ...")

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


    if len(offer_lists) == 0:
        return "❌ Nenhuma vaga encontrada com esses filtros no momento"

    final_text = f"🎯 Vagas encontradas ao todo: {len(offer_lists)}\n\n"

    offers_text = []
    for offer in offer_lists:
        offer_str = f"📌 Vaga: {offer['title']} | 📍 Local: {offer['location']}\n🔗 Acesse: {offer['link']}"
        offers_text.append(offer_str)

    offers_found = "\n\n".join(offers_text)
    return final_text + offers_found
