def create_table(conn):
    sql_create_users_table = """ CREATE TABLE IF NOT EXISTS usuarios (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    nome TEXT NOT NULL,
                                    cpf TEXT NOT NULL UNIQUE,
                                    data_nascimento TEXT NOT NULL,
                                    login TEXT NOT NULL UNIQUE,
                                    senha TEXT NOT NULL,
                                    saldo REAL DEFAULT 0.0,
                                    chave_pix TEXT UNIQUE,
                                    tel INTEGER[11]
                                ); """
    conn.execute(sql_create_users_table)