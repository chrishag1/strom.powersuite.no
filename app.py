from flask import Flask, render_template
import sqlite3
from etterspor_data import hent_data, ny_hent_data


app = Flask(__name__)

@app.route('/')
def index():  # put application's code here
    strømavtaler, standard_avtaler = hent_data()

    return render_template("index.html", stromavtaler=strømavtaler, standard_avtale=standard_avtaler)


@app.route("/embeded")
def embeded():
    strømavtaler, standard_avtaler = hent_data()

    return render_template("embeded.html", stromavtaler=strømavtaler, standard_avtale=standard_avtaler)


@app.route("/embeded-mini")
def power():
    strømavtaler, standard_avtaler = hent_data()

    return render_template("power.html", stromavtaler=strømavtaler, standard_avtale=standard_avtaler)


@app.route("/test")
def test():
    #strømavtaler, standard_avtaler = ny_hent_data()
    strømavtaler = ny_hent_data()
    print(strømavtaler)
    return render_template("test/side_med_komponenter.html",
                           leverandører=strømavtaler.get("leverandører"),
                           strømavtaler=strømavtaler.get("strømavtaler"),
                           standard_leverandør=strømavtaler.get("standard_leverandør"),
                           standard_strømavtale=strømavtaler.get("standard_avtale")
    )


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
