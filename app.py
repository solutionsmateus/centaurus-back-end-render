from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import os
import sys
import uuid
import time 

app = Flask(__name__)
CORS(app, origins="https://solutionscentaurus.netlify.app")

UPLOAD_FOLDER = 'Downloads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/execute_uploaded_script_conditional', methods=['POST'])
def execute_uploaded_script_conditional():
    if 'file' not in request.files:
        return jsonify({"message": "Nenhum arquivo enviado!"}), 400

    uploaded_file = request.files['file']

    if uploaded_file.filename == '':
        return jsonify({"message": "Nenhum arquivo selecionado."}), 400

    if not uploaded_file.filename.lower().endswith('.py'):
        return jsonify({"message": "Apenas arquivos Python (.py) são permitidos."}), 400

    unique_filename = str(uuid.uuid4()) + "_" + uploaded_file.filename
    file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
    
    try:
        uploaded_file.save(file_path)
        print(f"DEBUG: Arquivo '{uploaded_file.filename}' salvo temporariamente como '{file_path}'")
        time.sleep(0.5)

        script_name = uploaded_file.filename.lower()
        execution_message = ""
        script_output = ""
        script_error = ""
        return_code = -1 

        # --- Lógica de Execução Condicional ---
        if script_name == 'assai.py':
            execution_message = "Executando script Assaí..."
        elif script_name == 'atacadao.py':
            execution_message = "Executando script Atacadão..."
        elif script_name == 'cometa.py':
            execution_message = "Executando script Cometa..."
        elif script_name == 'novoatacarejo.py':
            execution_message = "Executando script Novo Atacarejo..."
        elif script_name == 'frangolandia.py':
            execution_message = "Executando script Frangolândia..."
        elif script_name == 'gbarbosa.py':
            execution_message = "Executando script GBarbosa..."
        elif script_name == 'atakarejo.py':
            execution_message = "Executando script Atakarejo..."
        else:
            return jsonify({
                "message": (f"Nome de arquivo '{script_name}' não reconhecido para execução. "
                            f"Nenhum script foi executado. Por favor, envie um dos arquivos conhecidos.")
            }), 400
        
        print(f"DEBUG: {execution_message}")
        result = subprocess.run(
            [sys.executable, file_path],
            capture_output=True,
            text=True,
            check=False 
        )
        
        script_output = result.stdout.strip()
        script_error = result.stderr.strip()
        return_code = result.returncode

        if return_code == 0:
            final_message = f"{execution_message} Concluído com sucesso! Saída:\n{script_output}"
            status_code = 200
        else:
            final_message = (f"{execution_message} Falhou com erro (código {return_code}).\n"
                             f"Saída:\n{script_output}\n"
                             f"Erro:\n{script_error}")
            status_code = 500

        print(f"DEBUG: Finalizando execução. Status: {status_code}, Mensagem: {final_message}")
        return jsonify({"message": final_message}), status_code

    except Exception as e:
        print(f"DEBUG: Ocorreu um erro inesperado: {e}")
        return jsonify({"message": f"Ocorreu um erro inesperado no servidor: {str(e)}"}), 500
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"DEBUG: Arquivo temporário '{unique_filename}' removido.")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
