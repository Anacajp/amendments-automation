from flask import Flask, jsonify
import os
import subprocess
import threading
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)

@app.route('/health')
def health():
    """Endpoint para verificar se o serviço está funcionando"""
    return jsonify({
        "status": "healthy", 
        "timestamp": datetime.now().isoformat(),
        "service": "Automação de Emendas"
    })

@app.route('/run-automation', methods=['POST'])
def run_automation():
    """Endpoint para executar a automação - EXECUÇÃO DIRETA (sem thread)"""
    try:
        logging.info("Iniciando automação via Cloud Scheduler...")
        
        # Executar DIRETAMENTE (sem thread) para economizar recursos
        # Cloud Run vai "dormir" depois que terminar
        result = subprocess.run(
            ["python", "src/main.py"], 
            check=True, 
            capture_output=True, 
            text=True,
            cwd="/app"
        )
        
        # Exibir logs detalhados do main.py
        if result.stdout:
            logging.info("Output do main.py:")
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    logging.info(f"   {line}")
        
        if result.stderr:
            logging.warning("Stderr do main.py:")
            for line in result.stderr.strip().split('\n'):
                if line.strip():
                    logging.warning(f"   {line}")
        
        logging.info("Automação concluída!")
        
        return jsonify({
            "status": "completed", 
            "message": "Automação executada com sucesso",
            "timestamp": datetime.now().isoformat(),
            "execution_time": "Verifique logs para detalhes"
        }), 200
        
    except subprocess.CalledProcessError as e:
        logging.error(f"Erro na automação: {e}")
        logging.error(f"stderr: {e.stderr}")
        return jsonify({
            "status": "error",
            "error": f"Processo falhou: {str(e)}",
            "stderr": e.stderr,
            "timestamp": datetime.now().isoformat()
        }), 500
        
    except Exception as e:
        logging.error(f"Erro inesperado: {e}")
        return jsonify({
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/')
def root():
    """Endpoint principal com informações do serviço"""
    return jsonify({
        "service": "Automação de Emendas",
        "status": "running",
        "description": "Serviço para automatizar download e atualização de planilhas de emendas",
        "endpoints": {
            "health": "GET /health - Verificar saúde do serviço",
            "run": "POST /run-automation - Executar automação"
        },
        "timestamp": datetime.now().isoformat()
    })

@app.route('/logs')
def get_logs():
    """Endpoint para verificar logs básicos"""
    return jsonify({
        "service": "Automação de Emendas",
        "log_level": "INFO",
        "message": "Para logs detalhados, use Google Cloud Logging",
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    logging.info(f"Iniciando servidor Flask na porta {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
