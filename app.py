from flask import Flask, render_template, redirect, request, jsonify
from flask_cors import CORS
from local_request.etterspor_data import hent_data, ny_hent_data
from local_request.ai_request import hent_avtale_fra_bilde, hent_avtale_fra_pdf


app = Flask(__name__)
CORS(app)

@app.route("/ai_fetch", methods=["POST"])
def ai_fetch():
    if request.method != "POST":
        return jsonify({"RequestError": "Invalid request"}), 404

    if "file" not in request.files:
        return jsonify({"FileError": "No file found"}), 400

    fil = request.files["file"]

    print(fil)

    if ".png" in fil.filename or ".jpg" in fil.filename or ".jpeg" in fil.filename:
        print("bilde")
        json_info = hent_avtale_fra_bilde(fil.read())
        print("kom og tørk")
        return jsonify(json_info), 200

    elif ".pdf" in fil.filename:
        print("pdf")
        json_info = hent_avtale_fra_pdf(fil.read())
        print("kom og tørk")
        return jsonify(json_info), 200

    else:
        print("nope")
        return jsonify({"FileError": "File not supported"}), 400



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
    strømavtaler = ny_hent_data()
    return render_template("test/side_med_komponenter.html",
                           leverandører=strømavtaler.get("leverandører"),
                           strømavtaler=strømavtaler.get("strømavtaler"),
                           standard_leverandør=strømavtaler.get("standard_leverandør"),
                           standard_strømavtale=strømavtaler.get("standard_avtale")
                           )

@app.route("/")
def ny_index():
    strømavtaler = ny_hent_data()
    return render_template("index.html",
                           leverandører=strømavtaler.get("leverandører"),
                           strømavtaler=strømavtaler.get("strømavtaler"),
                           standard_leverandør=strømavtaler.get("standard_leverandør"),
                           standard_strømavtale=strømavtaler.get("standard_avtale")
    )


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
