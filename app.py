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

        subprocess.Popen('start cmd', shell=True)
        
        process = subprocess.Popen('cmd.exe', stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
        command_cd = f"cd {UPLOAD_FOLDER}\n"
        process.stdin.write(command_cd)
        process.stdin.flush()

        # Executa o script Python
        command_exec = f"python.exe {unique_filename}\n"
        process.stdin.write(command_exec)
        process.stdin.flush()
        
        # Fecha o stdin para que o processo possa terminar
        process.stdin.close()

        # Captura a saída e os erros
        stdout, stderr = process.communicate(timeout=60) # Adicionado timeout para evitar bloqueio
        
        print("STDOUT:\n", stdout)
        print("STDERR:\n", stderr)
        
        script_output = stdout.strip()
        script_error = stderr.strip()
        return_code = process.returncode

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
            execution_message = (f"Nome de arquivo '{script_name}' não reconhecido para execução específica. "
                                f"Tentando executar o script via CMD.")

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

    except subprocess.TimeoutExpired:
        process.kill()
        stdout, stderr = process.communicate()
        print("DEBUG: Processo CMD excedeu o tempo limite.")
        return jsonify({"message": "O processo de execução do script excedeu o tempo limite."}), 500
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


