from backend.database import Database
from models.livro import Livro

class LivroService:
    def __init__(self):
        self.db = Database()
    
    def adicionar_livro(self, livro):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO livros (titulo, autor, ano_publicacao, categoria_id)
                VALUES (?, ?, ?, ?)
            ''', (livro.titulo, livro.autor, livro.ano_publicacao, livro.categoria_id))
            conn.commit()
            return cursor.lastrowid
    
    def listar_livros(self):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Buscar dados básicos
            cursor.execute('SELECT id, titulo, autor, ano_publicacao, categoria_id, data_cadastro FROM livros ORDER BY titulo')
            livros_basicos = cursor.fetchall()
            
            livros_completos = []
            for livro_basico in livros_basicos:
                # Buscar categoria
                categoria_nome = None
                if livro_basico[4]:  # categoria_id
                    cursor.execute('SELECT nome FROM categorias WHERE id = ?', (livro_basico[4],))
                    cat_result = cursor.fetchone()
                    if cat_result:
                        categoria_nome = cat_result[0]
                
                livro = Livro(
                    id=livro_basico[0],
                    titulo=livro_basico[1],
                    autor=livro_basico[2],
                    ano_publicacao=livro_basico[3],
                    categoria_id=livro_basico[4],
                    categoria_nome=categoria_nome,
                    data_cadastro=livro_basico[5]
                )
                livros_completos.append(livro)
            
            return livros_completos
    
    def buscar_livro(self, livro_id):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, titulo, autor, ano_publicacao, categoria_id, data_cadastro FROM livros WHERE id = ?', (livro_id,))
            row = cursor.fetchone()
            
            if not row:
                return None
            
            # Buscar categoria
            categoria_nome = None
            if row[4]:  # categoria_id
                cursor.execute('SELECT nome FROM categorias WHERE id = ?', (row[4],))
                cat_result = cursor.fetchone()
                if cat_result:
                    categoria_nome = cat_result[0]
            
            return Livro(
                id=row[0],
                titulo=row[1],
                autor=row[2],
                ano_publicacao=row[3],
                categoria_id=row[4],
                categoria_nome=categoria_nome,
                data_cadastro=row[5]
            )
    
    def buscar_livros(self, termo=""):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            search_term = f'%{termo}%'
            
            cursor.execute('''
                SELECT id, titulo, autor, ano_publicacao, categoria_id, data_cadastro 
                FROM livros 
                WHERE titulo LIKE ? OR autor LIKE ? 
                ORDER BY titulo
            ''', (search_term, search_term))
            
            livros_encontrados = cursor.fetchall()
            livros = []
            
            for row in livros_encontrados:
                # Buscar categoria
                categoria_nome = None
                if row[4]:  # categoria_id
                    cursor.execute('SELECT nome FROM categorias WHERE id = ?', (row[4],))
                    cat_result = cursor.fetchone()
                    if cat_result:
                        categoria_nome = cat_result[0]
                
                livro = Livro(
                    id=row[0],
                    titulo=row[1],
                    autor=row[2],
                    ano_publicacao=row[3],
                    categoria_id=row[4],
                    categoria_nome=categoria_nome,
                    data_cadastro=row[5]
                )
                livros.append(livro)
            
            return livros
    
    def atualizar_livro(self, livro):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE livros 
                SET titulo=?, autor=?, ano_publicacao=?, categoria_id=?
                WHERE id=?
            ''', (livro.titulo, livro.autor, livro.ano_publicacao, livro.categoria_id, livro.id))
            conn.commit()
    
    def excluir_livro(self, livro_id):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM livros WHERE id = ?', (livro_id,))
            conn.commit()