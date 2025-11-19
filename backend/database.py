import sqlite3
from contextlib import contextmanager

class Database:
    def __init__(self, db_name='biblioteca.db'):
        self.db_name = db_name
        self._create_tables()
    
    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()
    
    def _create_tables(self):
        with self.get_connection() as conn:
            # Tabela de categorias
            conn.execute('''
                CREATE TABLE IF NOT EXISTS categorias (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL UNIQUE
                )
            ''')
            
            # Tabela de livros
            conn.execute('''
                CREATE TABLE IF NOT EXISTS livros (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    autor TEXT NOT NULL,
                    ano_publicacao INTEGER,
                    categoria_id INTEGER,
                    data_cadastro DATE DEFAULT CURRENT_DATE,
                    FOREIGN KEY (categoria_id) REFERENCES categorias (id)
                )
            ''')
            
            # Tabela de histórico
            conn.execute('''
                CREATE TABLE IF NOT EXISTS historico (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    livro_id INTEGER NOT NULL,
                    acao TEXT NOT NULL,
                    detalhes TEXT,
                    data_acao DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (livro_id) REFERENCES livros (id)
                )
            ''')
            
            # Categorias personalizadas
            categorias_padrao = [
                'Ficção', 'Ação', 'Aventura', 'Comédia', 
                'Infantil', 'Romance', 'Fantasia', 'Ciência'
            ]
            
            for categoria in categorias_padrao:
                try:
                    conn.execute('INSERT OR IGNORE INTO categorias (nome) VALUES (?)', (categoria,))
                except:
                    pass
            
            conn.commit()
            print("✅ Banco de dados criado com sucesso!")