from database import Database


def hent_data():
    database = Database("strom.db")

    stromavtaler = database.execute("SELECT * FROM avtaler", fetchall=True)

    standard_avtale = ()

    for avtale in stromavtaler:
        if avtale["navn"].lower() == "eletra spot 0":
            standard_avtale = avtale

    return stromavtaler, standard_avtale


def fjern_eletra(strømliste: list):
    index_til_fjerning = []
    for index, value in enumerate(strømliste):
        if "sol" in value.get("navn").lower() or "ansatt" in value.get("navn").lower():
            index_til_fjerning.append(index)

    for index in index_til_fjerning[::-1]:
        strømliste.pop(index)

    strømliste.reverse()


def ny_hent_data():
    database = Database("strom.db")

    alle_leverandører = set()

    for leverandør in database.execute("SELECT selskap FROM avtaler", fetchall=True):
        alle_leverandører.add(leverandør.get("selskap"))

    alle_leverandører = sorted(alle_leverandører)

    alle_strømavtaler = {}
    for leverandør in alle_leverandører:
        strømavtaler = database.execute("SELECT * FROM avtaler where selskap = ?", (leverandør, ), fetchall=True)
        if "eletra" in leverandør.lower():
            fjern_eletra(strømavtaler)

        alle_strømavtaler[leverandør] = strømavtaler

    standard_avtale = database.execute("SELECT * FROM avtaler where navn = ?", ("Eletra Spot 0", ), fetchone=True)
    standard_leverandør = [standard_avtale.get("selskap")]

    return {
        "leverandører" : alle_leverandører,
        "strømavtaler" : alle_strømavtaler,
        "standard_leverandør" : standard_leverandør,
        "standard_avtale" : standard_avtale
    }
