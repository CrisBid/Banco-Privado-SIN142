from fastapi import HTTPException, status
from validate_docbr import CPF
from psycopg2.extras import RealDictCursor
from app.models.UserModel import CadastroData, LoginData, ValorData, ChavePixData, TransferenciaData

def cadastrar_usuario(data: CadastroData, db):
    cpf_v = CPF()
    if not cpf_v.validate(data.cpf):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid CPF")
    
    with db.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(
            """
            INSERT INTO usuarios (nome, cpf, data_nascimento, email, senha, tel)
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;
            """,
            (data.nome, data.cpf, data.data_nascimento, data.email, data.senha, data.tel)
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

# Continue adicionando os demais serviços conforme necessário


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