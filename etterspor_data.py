import sqlite3


def hent_data():
    database = sqlite3.connect("strom.db")
    peker = database.cursor()

    stromavtaler = peker.execute("SELECT * FROM avtaler").fetchall()
    database.close()

    standard_avtale = ()

    for avtale in stromavtaler:
        if avtale[1].lower() == "eletra spot":
            standard_avtale = avtale

    return stromavtaler, standard_avtale