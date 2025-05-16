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

def lade_spiele_von_fupa(teamArray):        
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
            if "row-headline" in elem.get("class", []) or "row-competition" in elem.get("class", []):
                print("überflüssig")
            else:
                match = elem
                #print(match)
                try:
                    """ # Datum + Uhrzeit
                    date_str = match.select_one("span.sc-lhxcmh-0").get_text(strip=True)
                    time_str = match.select_one("span.sc-4yququ-1").get_text(strip=True)
                    # Format z.B.: "So., 26.05.2024 15:00"
                    date_clean = date_str
                    for tag in ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]:
                        date_clean = date_clean.replace(f"{tag}., ", "")
                    if date_clean == "Heute":
                        date_clean = datetime.today().strftime("%d.%m.%Y")
                    dateTime = date_clean + " " + time_str
                    print(dateTime)
                    datum = datetime.strptime(dateTime, "%d.%m.%Y %H:%M") """

                    # Gegner
                    teams = []
                    counter = 0
                    for teamsRaw in match.select("td.column-club"):
                        counter += 1
                        team = teamsRaw.select_one("div.club-name")
                        team_name = clean_text(team.get_text(strip=True))
                        if len(team) > 2:
                            team_name += " " + team[2].get_text(strip=True)
                        teams.append(team_name)
                        if team_name != mannschaft["teamname"]:
                            gegner = team_name
                            if(counter == 1): 
                                ort = "Auswärtsspiel"
                            else:
                                ort = "Heimspiel"
                    print(teams)
                    # Ort (falls vorhanden)
                    #ort_div = match.select_one("div.MatchRow_location__wJkQD")
                    #ort = ort_div.get_text(strip=True) if ort_div else "Ort unbekannt"

                    spieleMannschaft.append({
                        #"datum": datum.isoformat(),
                        #"zeit": time_str,
                        "gegner": gegner,
                        "ort": ort
                    })

                except Exception as e:
                    print("Fehler beim Parsen eines Spiels:", e)
                    continue

            spiele[mannschaft["arrayname"]] = spieleMannschaft

    return spiele

# 🟩 Aufruf
spiele = lade_spiele_von_fupa(links)

# ✅ Ausgabe als JSON-Datei
with open("spiele.json", "w", encoding="utf-8") as f:
    json.dump(spiele, f, ensure_ascii=False, indent=2)

print(f"{len(spiele)} Spiele gefunden und in spiele.json gespeichert.")

 # type: ignore