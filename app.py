from selenium import webdriver
from flask import Flask, render_template, request, jsonify
import subprocess
from flask_cors import CORS

LOJA_SCRIPT_MAP = {
    "Assaí": "centaurus/back-end/models/date_paths/assai.py",
    "Atacadão": "centaurus/back-end/models/date_paths/atacadão.py",
    "Cometa Supermercados": "centaurus/back-end/models/date_paths/cometa.py",
    "Frangolândia Supermercados": "centaurus/back-end/models/date_paths/frangolandia.py",
    "Novo Atacarejo": "centaurus/back-end/models/date_paths/novoatacarejo.py",
    "GBarbosa (Grupo Cencosud)": "centaurus/back-end/models/date_paths/gbarbosa.py"
}

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://solutionscentaurus.netlify.app/"}})

@app.route('/executar_script', methods=['POST'])
def executar_script():
    data = request.get_json()
    loja = data.get('loja')

    script_path = LOJA_SCRIPT_MAP.get(loja)

    if not script_path:
        return jsonify({"message": f"Loja '{loja}' não mapeada para nenhum script."}), 400

    try:
        result = subprocess.run(
            ["python", script_path, loja],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return jsonify({"message": f"Erro ao executar o script: {result.stderr}"}), 500

        return jsonify({"message": f"Script '{loja}' executado com sucesso para o loja '{loja}'."})
    except Exception as e:
        return jsonify({"message": f"Erro inesperado: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
