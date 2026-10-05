import os
from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
import mysql.connector
import jwt
import datetime

# Configurações para a chave secreta do JWT
SECRET_KEY = os.environ["JWT_SECRET_KEY"]
if not SECRET_KEY.strip():
    raise RuntimeError("JWT_SECRET_KEY must be set")

# Inicializando o Blueprint
auth = Blueprint('auth', __name__)

# Conexão com MySQL
def get_db_connection():
    connection = mysql.connector.connect(
        host=os.environ.get("MYSQL_HOST", "localhost"),
        user=os.environ.get("MYSQL_USER", "root"),
        password=os.environ["MYSQL_PASSWORD"],
        database=os.environ.get("MYSQL_DATABASE", "petland")
    )
    return connection

# Função para gerar o token JWT
def gerar_token(cpf, tipo_usuario):
    token = jwt.encode({
        'cpf': cpf,
        'tipo_usuario': tipo_usuario,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }, SECRET_KEY, algorithm="HS256")
    return token

# Função para verificar o token JWT
def verificar_token(token):
    try:
        dados = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return dados
    except:
        return None

# Rota de login para clientes e colaboradores
@auth.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()

    cpf = data.get('cpf')
    senha = data.get('senha')

    if not cpf or not senha:
        return jsonify({"message": "CPF e senha são obrigatórios"}), 400

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Verificar se é um cliente ou colaborador
    cursor.execute("SELECT * FROM cliente WHERE cpf_cliente = %s", (cpf,))
    cliente = cursor.fetchone()

    if cliente:
        # Verifica a senha
        if check_password_hash(cliente['senha_cliente'], senha):
            token = gerar_token(cliente['cpf_cliente'], 'cliente')
            return jsonify({
                "message": "Login efetuado com sucesso",
                "token": token
            }), 200
        else:
            return jsonify({"message": "Senha incorreta"}), 401

    # Se não for cliente, verificar se é colaborador
    cursor.execute("SELECT * FROM colaboradores WHERE cpf_colaborador = %s", (cpf,))
    colaborador = cursor.fetchone()

    if colaborador:
        if colaborador['senha_backOffice'] == senha:
            token = gerar_token(colaborador['cpf_colaborador'], 'colaborador')
            return jsonify({
                "message": "Login efetuado com sucesso",
                "token": token
            }), 200
        else:
            return jsonify({"message": "Senha incorreta"}), 401

    # Caso não encontre o CPF em nenhum dos dois
    return jsonify({"message": "CPF não encontrado"}), 404


# Função para proteger rotas usando o JWT
def token_required(f):
    def decorator(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({"message": "Token de autenticação é necessário"}), 403

        try:
            dados = verificar_token(token)
            if not dados:
                return jsonify({"message": "Token inválido"}), 403
        except:
            return jsonify({"message": "Token inválido"}), 403

        return f(dados, *args, **kwargs)
    decorator.__name__ = f.__name__
    return decorator

# Exemplo de rota protegida
@auth.route('/api/protegido', methods=['GET'])
@token_required
def rota_protegida(dados):
    return jsonify({
        "message": "Você acessou uma rota protegida!",
        "cpf": dados['cpf'],
        "tipo_usuario": dados['tipo_usuario']
    }), 200

