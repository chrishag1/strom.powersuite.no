from flask import Flask, render_template
import sqlite3
from etterspor_data import hent_data


app = Flask(__name__)

@app.route('/')
def hello_world():  # put application's code here
    strømavtaler, standard_avtaler = hent_data()

    return render_template('index.html', stromavtaler=strømavtaler, standard_avtale=standard_avtaler)


if __name__ == '__main__':
    app.run()
