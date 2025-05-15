import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

# URL zum Spielplan deiner Mannschaft (Reiter „Spiele“!)
links = [
    {
        "mannschaftsname": "3. Mannschaft",
        "arrayname": "dritteMannschaft",
        "link": "https://www.fupa.net/team/sg-scharmedethuele-m3-2024-25/matches"
    },
    {
        "mannschaftsname": "2. Mannschaft",
        "arrayname": "zweiteMannschaft",
        "link": "https://www.fupa.net/team/sg-scharmedethuele-m2-2024-25/matches"
    }
]


def lade_spiele_von_fupa(url):        
    #mannschaft =
    class Object(object):
        pass
    spiele = Object()
    for mannschaft in url:
        print(mannschaft.mannschaftsname)
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        #setattr(spiele, mannschaft.mannschaf)

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Fehler beim Laden der Seite: {response.status_code}")
            return []

        soup = BeautifulSoup(response.text, "html.parser")


        # Jeder Spiel-Container
        for match in soup.select("div.sc-1cfloyl-0"):
            #print(match)
            try:
                # Datum + Uhrzeit
                date_str = match.select_one("span.sc-lhxcmh-0").get_text(strip=True)
                time_str = match.select_one("span.sc-4yququ-1").get_text(strip=True)
                # Format z.B.: "So., 26.05.2024 15:00"
                date_clean = date_str.replace("So., ", "").replace("Sa., ", "").replace("Fr., ", "").replace("Do., ", "").replace("Mi., ", "").replace("Di., ", "").replace("Mo., ", "")
                dateTime = date_clean #+ " " + time_str
                datum = datetime.strptime(dateTime, "%d.%m.%Y")
                print(dateTime)

                # Gegner
                teams = []
                counter = 0
                for teamsRaw in match.select("div.sc-1cfloyl-7"):
                    counter += 1
                    team = teamsRaw.select("span")
                    team_name = team[0].get_text(strip=True)
                    if len(team) > 2:
                        team_name += " " + team[2].get_text(strip=True)
                    teams.append(team_name)
                    if team_name != "SG Scharmede/Thüle III":
                        gegner = team_name
                        if(counter == 1): 
                            ort = "Auswärtsspiel"
                        else:
                            ort = "Heimspiel"
                print(teams)
                # Ort (falls vorhanden)
                #ort_div = match.select_one("div.MatchRow_location__wJkQD")
                #ort = ort_div.get_text(strip=True) if ort_div else "Ort unbekannt"

                spiele.append({
                    "datum": datum.isoformat(),
                    "zeit": time_str,
                    "gegner": gegner,
                    "ort": ort
                })

            except Exception as e:
                print("Fehler beim Parsen eines Spiels:", e)
                continue

    return spiele

# 🟩 Aufruf
spiele = lade_spiele_von_fupa(links)

# ✅ Ausgabe als JSON-Datei
with open("spiele.json", "w", encoding="utf-8") as f:
    json.dump(spiele, f, ensure_ascii=False, indent=2)

print(f"{len(spiele)} Spiele gefunden und in spiele.json gespeichert.")

 # type: ignore