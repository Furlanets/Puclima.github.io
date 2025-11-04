from flask import Flask, jsonify, render_template
from pymongo import MongoClient
from bson.json_util import dumps
from datetime import datetime

app = Flask(__name__)

# 🔗 Conexão com o MongoDB Atlas
client = MongoClient("mongodb+srv://<usuario>:<senha>@<cluster>.mongodb.net/?retryWrites=true&w=majority")
db = client["seu_banco"]
colecao = db["sua_colecao"]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/temperaturas")
def get_temperaturas():
    try:
        # Busca os registros mais recentes
        temp_interna = colecao.find_one(
            {"bn": "F803320100033CAE"}, sort=[("_id", -1)]
        )
        temp_externa = colecao.find_one(
            {"bn": "F803320100033877"}, sort=[("_id", -1)]
        )

        dados = {
            "interna": temp_interna.get("e", [{}])[0].get("v", None),
            "externa": temp_externa.get("e", [{}])[0].get("v", None),
            "timestamp": datetime.now().isoformat()
        }

        return jsonify(dados)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
