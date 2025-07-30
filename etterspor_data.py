from database import Database


def hent_data():
    database = Database("strom.db")

    stromavtaler = database.execute("SELECT * FROM avtaler", fetchall=True)

    standard_avtale = ()

    for avtale in stromavtaler:
        if avtale["navn"].lower() == "eletra spot 0":
            standard_avtale = avtale

    return stromavtaler, standard_avtale