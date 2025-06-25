from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import subprocess
import json
import os
from pathlib import Path 

app = Flask(__name__)
CORS(app, origins="https://solutionscentaurus.netlify.app" )

LOJA_SCRIPT_MAP = {
    "Assaí": "models/assai.py",
    # "Atacadão": "models/atacadao.py", # Comente ou remova, pois não teremos esses scripts
    # "Cometa Supermercados": "models/cometa.py",
    # "Frangolândia Supermercados": "models/frangolandia.py",
    # "Novo Atacarejo": "models/novoatacarejo.py",
    # "GBarbosa (Grupo Cencosud)": "models/gbarbosa.py",
    # "Novo Atacarejo": "models/novoatacarejo.py"
}

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
            print(f"Erro do subprocess (stderr): {result.stderr}")
            print(f"Erro do subprocess (stdout): {result.stdout}")
            return jsonify({"message": f"Erro ao executar o script: {result.stderr}"}), 500

        downloaded_files = []
        for line in result.stdout.splitlines():
            if line.startswith("DOWNLOADED_FILES:"):
                try:
                    json_str = line.replace("DOWNLOADED_FILES:", "").strip()
                    downloaded_files = json.loads(json_str)
                    print(f"Caminhos de arquivos capturados: {downloaded_files}")
                except json.JSONDecodeError:
                    print(f"Falha ao decodificar JSON de arquivos baixados: {json_str}")
                break
        
        file_urls = []
        for fpath_full_server_path in downloaded_files:
            base_filename = os.path.basename(fpath_full_server_path)
            file_urls.append(f"/download_file/{base_filename}")

        return jsonify({
            "message": f"Script '{loja}' executado com sucesso.",
            "files": file_urls,
            "downloaded_paths_on_server": downloaded_files 
        })
    except Exception as e:
        print(f"Erro inesperado no app.py: {str(e)}")
        return jsonify({"message": f"Erro inesperado no servidor: {str(e)}"}), 500

@app.route('/download_file/<filename>')
def download_file(filename):
    download_base_dir_on_server = Path("downloads")

    try:
        found_path = None
        for root, _, files in os.walk(download_base_dir_on_server):
            if filename in files:
                found_path = Path(root) / filename 
                break 
        if found_path and found_path.exists():
            print(f"Servindo arquivo: {found_path}")
            return send_file(str(found_path), as_attachment=True, download_name=filename)
        else:
            print(f"Arquivo '{filename}' não encontrado em '{download_base_dir_on_server}' ou subdiretórios.")
            return jsonify({"message": "Arquivo não encontrado."}), 404
    except Exception as e:
        print(f"Erro ao servir arquivo '{filename}': {e}")
        return jsonify({"message": "Erro interno ao tentar baixar arquivo."}), 500

if __name__ == '__main__':
    app.run(debug=True)
