import requests
import time
import datetime
import sqlite3

def hent_stromavtaler():
    url = "https://strom-api.forbrukerradet.no/products/grid/524"
    params = {
        "yearlyKwhConsumption": "16000"
    }
    response = requests.get(url, params=params)
    stromavtaler = sorted(response.json(), key=lambda x: x["name"])
    return stromavtaler

def tom_database():
    database = sqlite3.connect("strom.db")
    peker = database.cursor()
    peker.execute("DROP TABLE avtaler")
    peker.execute("""CREATE TABLE avtaler (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
            navn TEXT NOT NULL,
            selskap TEXT NOT NULL,
            paaslag DECIMAL NOT NULL,
            maanedspris DECIMAL NOT NULL,
            kwpris DECIMAL NOT NULL
        );
    """)

    database.commit()
    database.close()


def legg_inn_stromavtaler():
    stromavtaler = hent_stromavtaler()

    database = sqlite3.connect("strom.db")

    peker = database.cursor()

    for avtale in stromavtaler:
        if avtale["expiredAt"] is None:
            navn = avtale["name"]
            selskap = avtale["organization"]["name"]
            paaslag = avtale["currentPrice"]["addonPrice"]
            maanedspris = avtale["fee"]["finalMonthlyFee"]
            kwpris = round(avtale["currentPrice"]["finalKwPrice"], 2)

            peker.execute("INSERT INTO avtaler (navn, selskap, paaslag, maanedspris, kwpris) VALUES (?, ?, ?, ?, ?)",
                          (navn, selskap, paaslag, maanedspris, kwpris))

    database.commit()
    database.close()


def oppdater_priser():
    tom_database()
    legg_inn_stromavtaler()

if __name__ == "__main__":

    while True:
        oppdater_priser()
        naa = datetime.datetime.now()
        sov = (datetime.datetime(naa.year, naa.month, naa.day, 7, 00, 00) - naa).seconds
        print(f"sover i {sov} sekunder")
        time.sleep(sov)

