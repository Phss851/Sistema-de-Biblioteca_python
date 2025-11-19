from backend.database import Database
from models.livro import Historico
from datetime import datetime

class HistoricoService:
    def __init__(self):
        self.db = Database()
    
    def registrar_acao(self, livro_id, acao, detalhes=""):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO historico (livro_id, acao, detalhes, data_acao)
                VALUES (?, ?, ?, ?)
            ''', (livro_id, acao, detalhes, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            conn.commit()
    
    def obter_historico_completo(self):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT h.*, l.titulo 
                FROM historico h
                JOIN livros l ON h.livro_id = l.id
                ORDER BY h.data_acao DESC
            ''')
            historico = []
            for row in cursor.fetchall():
                historico.append(Historico(
                    row['id'], row['livro_id'], row['acao'],
                    row['detalhes'], row['data_acao'], row['titulo']
                ))
            return historico
    
    def obter_estatisticas(self):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Total de livros
            cursor.execute('SELECT COUNT(*) as total FROM livros')
            total_livros = cursor.fetchone()['total']
            
            # Livros por categoria
            cursor.execute('''
                SELECT c.nome, COUNT(l.id) as quantidade 
                FROM categorias c 
                LEFT JOIN livros l ON c.id = l.categoria_id 
                GROUP BY c.id, c.nome
            ''')
            livros_por_categoria = cursor.fetchall()
            
            return {
                'total_livros': total_livros,
                'livros_por_categoria': livros_por_categoria
            }