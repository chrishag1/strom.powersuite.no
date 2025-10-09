import base64
import io

from flask import Flask, render_template, redirect, request, jsonify
from flask_cors import CORS
from local_request.etterspor_data import hent_data, ny_hent_data
from local_request.ai_request import hent_avtale_fra_bilde, hent_avtale_fra_pdf
from datetime import datetime
from logg_foring import loggForing

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

CORS(app)

@app.route("/ai_fetch", methods=["POST"])
def ai_fetch():
    logg_fil = loggForing(f"logging/fil_{datetime.now()}.txt")
    try:

        if request.method != "POST":
            return jsonify({"RequestError": "Invalid request"}), 404

        if "file" not in request.files:
            return jsonify({"FileError": "No file found"}), 400

        fil = request.files["file"]
        fil.filename = fil.filename.lower()

        if ".png" in fil.filename or ".jpg" in fil.filename or ".jpeg" in fil.filename:
            print("bilde")
            json_info = hent_avtale_fra_bilde(fil)
            print("kom og tork")

        elif ".pdf" in fil.filename:
            print("pdf")
            json_info = hent_avtale_fra_pdf(fil)
        else:
            print("nope")
            return jsonify({"FileError": "File not supported"}), 400


        logg_fil.logg_priser(json_info)
        print("ferdig")
        return jsonify(json_info), 200

    except Exception as e:
        logg_fil.logg_feilmelding(e)
        print(e)
        return str(e), 500

@app.route("/")
def index():
    strømavtaler = ny_hent_data()

    return render_template("index.html",
                           leverandører=strømavtaler.get("leverandører"),
                           strømavtaler=strømavtaler.get("strømavtaler"),
                           standard_leverandør=strømavtaler.get("standard_leverandør"),
                           standard_strømavtale=strømavtaler.get("standard_avtale")
                           )

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
