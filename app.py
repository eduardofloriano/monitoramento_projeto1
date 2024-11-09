import os
import datetime
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import json
import sqlite3

import logging



app = Flask(__name__)
CORS(app)


handler = logging.FileHandler('logs/flask_app.log')  # Log to a file
app.logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)
app.logger.addHandler(handler)


# Crie uma métrica de exemplo (contador de requisições)
REQUEST_COUNT = Counter('http_requests_total', 'Total de requisições HTTP', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('http_request_latency_seconds', 'Latência das requisições HTTP em segundos', ['method', 'endpoint'])
HTTP_ERRORS = Counter('http_errors_total', 'Total de respostas HTTP com erro', ['method', 'endpoint', 'status_code'])


def log_message(level, message):
    """Loga uma mensagem com o nível especificado."""

    log_methods = {
        'debug': app.logger.debug,
        'info': app.logger.info,
        'warning': app.logger.warning,
        'error': app.logger.error,
        'critical': app.logger.critical
    }
    if level in log_methods:
        log_methods[level](f"{message}")
    else:
        app.logger.error(f"Unrecognized logging level: {level}")


# Middleware para contar requisições
@app.before_request
def before_request():
    REQUEST_COUNT.labels(method=request.method, endpoint=request.path).inc()

# Rota para o Prometheus coletar as métricas
@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

# Endpoint para devolver todos as pessoas cadastradas
@app.route('/')
def home():
    #log_message('info', 'This is an INFO message')
    #log_message('debug', 'This is a DEBUG message')
    #log_message('warning', 'This is a WARNING message')
    #log_message('error', 'This is an ERROR message')
    #log_message('critical', 'This is a CRITICAL message')
    return "API de veiculos"

@app.route('/veiculos', methods=['GET'])
def veiculos():
    try:
        log_message('info', 'Executando endpoint GET de veiculos...')
        sql = '''SELECT renavan, placa, marca, modelo FROM veiculos'''
        log_message('info', 'Query: ' + sql)
        with sqlite3.connect('veiculos.db') as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(sql)
            result = cursor.fetchall()
            log_message('info', 'Query executada com sucesso!')
            return json.dumps([dict(ix) for ix in result]), 200
    except Exception as e:
        log_message('error', 'Erro ao executar o Endpoint Get de veiculos')
        return jsonify(error=str(e)), 500

@app.route('/veiculo/<placa>', methods=['GET', 'DELETE'])
def veiculo_por_placa(cpf):
    try:
        log_message('info', 'Executando endpoint de veiculo/placa...')
        sqlGET = '''SELECT renavan, placa, marca, modelo FROM veiculos WHERE placa=?'''
        sqlDELETE = 'DELETE FROM veiculos WHERE placa = ?'
        with sqlite3.connect('veiculos.db') as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            if request.method == 'GET':
                log_message('info', 'Query: ' + sqlGET)
                cursor.execute(sqlGET, [cpf])
                result = cursor.fetchall()
                if result:
                    log_message('info', 'Query executada com sucesso!')
                    return json.dumps([dict(ix) for ix in result]), 200
                msgErroVeiculoGet = "Veiculo não encontrado"
                log_message('warning', msgErroVeiculoGet)
                return jsonify(error=msgErroVeiculoGet), 404
            elif request.method == 'DELETE':
                log_message('info', 'Query: ' + sqlDELETE)
                cursor.execute(sqlDELETE, (cpf,))
                if cursor.rowcount == 0:
                    msgErroVeiculoDelete = "Veiculo não encontrado"
                    log_message('warning', msgErroVeiculoDelete)
                    return jsonify(error=msgErroVeiculoDelete), 404
                conn.commit()
                log_message('info', "Query executada com sucesso!")
                return jsonify(success="Veiculo deletado com sucesso"), 200
    except Exception as e:
        log_message('error', 'Erro ao executar o Endpoint /pessoa/cpf')
        return jsonify(error=str(e)), 500

@app.route('/veiculo', methods=['POST'])
def insere_atualiza_veiculo():
    log_message('info', 'Executando endpoint de veiculo POST...')
    data = request.get_json(force=True)
    renavan = data.get('renavan')
    placa = data.get('placa')
    marca = data.get('marca')
    modelo = data.get('modelo')
    try:
        with sqlite3.connect('veiculos.db') as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()            
            #log_message('info', 'Buscando a Pessoa na base de dados...')
            cursor.execute('SELECT 1 FROM veiculos WHERE placa=?', (placa,))
            exists = cursor.fetchone()
            if exists:
                log_message('warning', 'Veiculo encontrada com sucesso!')
                log_message('info', 'Executando atualizacao...')
                cursor.execute('UPDATE veiculos SET renavan=?, marca=?, modelo=? WHERE placa=?', (renavan, marca, modelo, placa))
                conn.commit()
                log_message('info', 'Veiculo atualizado com sucesso')
                return jsonify(success="Veiculo atualizado com sucesso"), 200
            log_message('warning', 'Veiculo nao encontrada')
            log_message('info', 'Executando insercao' )
            cursor.execute('INSERT INTO veiculos (renavan, placa, marca, modelo) VALUES (?, ?, ?, ?)', (renavan, placa, marca, modelo))
            conn.commit()
            log_message('info', 'Veiculo inserido com sucesso' )
            return jsonify(success="Veiculo inserido com sucesso"), 201
    except Exception as e:
        log_message('error', 'Erro ao executar o Endpoint /veiculo')
        return jsonify(error=str(e)), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)