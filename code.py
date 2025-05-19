import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import re

def clean_text(text):
    # Entfernt Zero-Width Spaces und andere unsichtbare Unicode-Zeichen
    return re.sub(r'[\u200b\u200e\u200f\u202a-\u202e]', '', text)

# URL zum Spielplan deiner Mannschaft (Reiter „Spiele“!)
links = [
    {
        "teamname": "SG Scharmede/Thüle III",
        "mannschaftsname": "3. Mannschaft",
        "arrayname": "dritteMannschaft",
        "link": "https://www.fussball.de/ajax.team.next.games/-/mode/PAGE/team-id/027EAGRR2O000000VS5489B1VU8ROJMK"
    }
]

#print(links)

def lade_spieleSeiten_von_fussball_de(teamArray):
    spiele = {}
    for mannschaft in teamArray:
        spieleMannschaft = []
        print(mannschaft["mannschaftsname"])
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        link = mannschaft["link"]

        #setattr(spiele, mannschaft.mannschaf)

        response = requests.get(link, headers=headers)
        if response.status_code != 200:
            print(f"Fehler beim Laden der Seite: {response.status_code}")
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        tbody = soup.select_one("tbody")


        # Jeder Spiel-Container
        for elem in tbody.select("tr"):
            #print(elem)
            if "row-headline" in elem.get("class", []):
                None
            elif "row-competition" in elem.get("class", []):
                dateWrapper = elem.select_one("td.column-date").get_text(strip=True).split("|")
                date = dateWrapper[0]
                time = dateWrapper[1]
                # Datum + Uhrzeit
                # Format z.B.: "So., 26.05.2024 15:00"
                date_clean = date
                for tag in ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]:
                    date_clean = date_clean.replace(f"{tag}, ", "")
                if date_clean == "Heute":
                    date_clean = datetime.today().strftime("%d.%m.%Y")
                date_clean = date_clean[:8]
                dateTime = date_clean + " " + time
                datum = datetime.strptime(dateTime, "%d.%m.%y %H:%M")
                print(datum)
            else:
                match = elem
                try:
                    toGame = match.select_one("td.column-detail")
                    linkToGame = toGame.select_one("a").get("href",[])

                    res = requests.get(linkToGame, headers=headers)
                    if res.status_code != 200:
                        print(f"Fehler beim Laden der Seite: {res.status_code}")
                        return []

                    matchSite = BeautifulSoup(res.text, "html.parser")
                    # Gegner
                    for matchTeams in matchSite.select("div.team-name"):
                        matchTeam = clean_text(matchTeams.select_one("a").get_text(strip=True))
                        if matchTeam != mannschaft["teamname"]:
                            gegner = matchTeam
                        print(matchTeam)

                    matchLocation = matchSite.select_one("a.location").get_text(strip=True)
                    #Google Maps Link:
                    #matchLocation = matchSite.select_one("a.location").get("href",[])
                    ort = matchLocation or "Ort unbekannt"
                    print(ort)

                    spieleMannschaft.append({
                        "datum": datum.isoformat(),
                        "zeit": time,
                        "gegner": gegner,
                        "ort": ort
                    })

                except Exception as e:
                    print("Fehler beim Parsen eines Spiels:", e)
                    continue

            spiele[mannschaft["arrayname"]] = spieleMannschaft

    return spiele

# 🟩 Aufruf
spiele = lade_spieleSeiten_von_fussball_de(links)

# ✅ Ausgabe als JSON-Datei
with open("spiele.json", "w", encoding="utf-8") as f:
    json.dump(spiele, f, ensure_ascii=False, indent=2)

print(f"{len(spiele)} Spiele gefunden und in spiele.json gespeichert.")

 # type: ignore