from fastapi import FastAPI, HTTPException, Depends, status
from validate_docbr import CPF
from psycopg2.extras import RealDictCursor
from app.models.UserModel import CadastroData, LoginData, ValorData, ChavePixData, TransferenciaData
from hashlib import sha256
import psycopg2

def cadastrar_usuario(data: CadastroData, db):
    cpf_v = CPF()
    if not cpf_v.validate(data.cpf):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid CPF")
    
    with db.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(
            """
            INSERT INTO usuarios (nome, cpf, data_nascimento, login, senha, tel)
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;
            """,
            (data.nome, data.cpf, data.data_nascimento, data.login, data.senha, data.tel)
        )
        user_id = cursor.fetchone()["id"]
        db.commit()
    
    return {"message": "User registered successfully", "user_id": user_id}

def login_usuario(data: LoginData, db):
    with db.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(
            "SELECT id, senha FROM usuarios WHERE login = %s;",
            (data.login,)
        )
        user = cursor.fetchone()
        if user and user['senha'] == data.senha:
            return {"message": "Login successful", "user_id": user['id']}
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid login credentials")

# Função para hashear a senha
def hash_password(password):
    return sha256(password.encode()).hexdigest()

# Função para obter um usuário pelo login
def get_user_by_login(db, login):
    with db.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("SELECT * FROM usuarios WHERE login = %s;", (login,))
        return cursor.fetchone()

# Função para criar um usuário
def create_user(db, nome, cpf, data_nascimento, login, senha, tel):
    senha_hashed = hash_password(senha)
    with db.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(
            """
            INSERT INTO usuarios (nome, cpf, data_nascimento, login, senha, tel)
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;
            """,
            (nome, cpf, data_nascimento, login, senha_hashed, tel)
        )
        user_id = cursor.fetchone()["id"]
        db.commit()
    return {"message": "User created successfully", "user_id": user_id}

# Função para realizar o login de um usuário
def login_user(db, login, senha):
    user = get_user_by_login(db, login)
    if user and user["senha"] == hash_password(senha):
        return {"message": "Login successful", "user": user}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid login credentials")

# Função para atualizar o saldo
def update_saldo(db, user_id, valor):
    with db.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(
            """
            UPDATE usuarios
            SET saldo = saldo + %s
            WHERE id = %s;
            """,
            (valor, user_id)
        )
        db.commit()
    return {"message": "Saldo updated successfully"}

# Função para obter o saldo do usuário
def get_saldo(db, user_id):
    with db.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("SELECT saldo FROM usuarios WHERE id = %s;", (user_id,))
        saldo = cursor.fetchone()["saldo"]
    return {"saldo": saldo}

# Função para definir uma chave PIX para o usuário
def set_chave_pix(db, user_id, chave_pix):
    with db.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(
            """
            UPDATE usuarios
            SET chave_pix = %s
            WHERE id = %s;
            """,
            (chave_pix, user_id)
        )
        db.commit()
    return {"message": "Chave PIX updated successfully"}

# Função para obter um usuário pelo ID
def get_user_by_id(db, user_id):
    with db.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("SELECT * FROM usuarios WHERE id = %s;", (user_id,))
        return cursor.fetchone()

""""

from hashlib import sha256

# Funções auxiliares do banco
def hash_password(password):
    return sha256(password.encode()).hexdigest()

def get_user_by_login(conn, login):
    cur = conn.cursor()
    cur.execute("SELECT * FROM usuarios WHERE login=?", (login,))
    return cur.fetchone()

def create_user(conn, nome, cpf, data_nascimento, login, senha, tel):
    senha_hashed = hash_password(senha)
    sql = ''' INSERT INTO usuarios(nome, cpf, data_nascimento, login, senha, tel)
              VALUES(?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (nome, cpf, data_nascimento, login, senha_hashed, tel))
    conn.commit()
    return cur.lastrowid

def login_user(conn, login, senha):
    user = get_user_by_login(conn, login)
    if user and user[5] == hash_password(senha):
        return user
    return None

def update_saldo(conn, user_id, valor):
    sql = ''' UPDATE usuarios
              SET saldo = saldo + ?
              WHERE id = ? '''
    cur = conn.cursor()
    cur.execute(sql, (valor, user_id))
    conn.commit()

def get_saldo(conn, user_id):
    cur = conn.cursor()
    cur.execute("SELECT saldo FROM usuarios WHERE id=?", (user_id,))
    return cur.fetchone()[0]

def set_chave_pix(conn, user_id, chave_pix):
    sql = ''' UPDATE usuarios
              SET chave_pix = ?
              WHERE id = ? '''
    cur = conn.cursor()
    cur.execute(sql, (chave_pix, user_id))
    conn.commit()

def get_user_by_id(conn, user_id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM usuarios WHERE id=?", (user_id,))
    return cur.fetchone()


"""