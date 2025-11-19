from backend.database import Database
from models.livro import Categoria

class CategoriaService:
    def __init__(self):
        self.db = Database()
    
    def listar_categorias(self):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM categorias ORDER BY nome')
            categorias = []
            for row in cursor.fetchall():
                categorias.append(Categoria(row['id'], row['nome']))
            return categorias
    
    def buscar_categoria_por_id(self, categoria_id):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM categorias WHERE id = ?', (categoria_id,))
            row = cursor.fetchone()
            return Categoria(row['id'], row['nome']) if row else None