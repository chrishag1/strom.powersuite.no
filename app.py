from flask import Flask, render_template
import sqlite3
from etterspor_data import hent_data


app = Flask(__name__)

@app.route('/')
def index():  # put application's code here
    strømavtaler, standard_avtaler = hent_data()

    return render_template('index.html', stromavtaler=strømavtaler, standard_avtale=standard_avtaler)


@app.route("/embeded")
def embeded():
    strømavtaler, standard_avtaler = hent_data()

    return render_template('embeded.html', stromavtaler=strømavtaler, standard_avtale=standard_avtaler)


@app.route("/test")
def test():
    strømavtaler, standard_avtaler = hent_data()

    return render_template('test.html', stromavtaler=strømavtaler, standard_avtale=standard_avtaler)


if __name__ == '__main__':
    app.run(host="192.168.1.81", port=5000, debug=True)
