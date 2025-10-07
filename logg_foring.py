import json


class loggForing:
    def __init__(self, fil_sti):
        self.fil_sti = fil_sti

    def logg_ankomst(self, mottat_fil):
        with open(self.fil_sti, "w") as fil:
            fil.write(f"mottok fil: {mottat_fil.filename}, av størrelse {mottat_fil.__sizeof__()}\n")

    def logg_priser(self, json_objekt):
        with open(self.fil_sti, "a") as fil:
            fil.write("Prisene på avtalen: \n")
            json.dump(json_objekt, fil, indent=4)


    def logg_feilmelding(self, feilmelding):
        with open(self.fil_sti, "a") as fil:
            fil.write(f"feilmelding: {feilmelding}\n")
