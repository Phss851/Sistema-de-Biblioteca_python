import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Configurar path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.livro_service import LivroService
from backend.categoria_service import CategoriaService
from backend.historico_service import HistoricoService
from models.livro import Livro

class BibliotecaApp:
    def __init__(self, root):
        self.root = root
        self.livro_service = LivroService()
        self.categoria_service = CategoriaService()
        self.historico_service = HistoricoService()
        self.setup_ui()
        self.carregar_dados_iniciais()
    
    def setup_ui(self):
        """Configura a interface gráfica"""
        self.root.title("📚 Sistema de Biblioteca")
        self.root.geometry("900x650")
        
        # Criar abas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Abas
        self.aba_livros = ttk.Frame(self.notebook)
        self.aba_busca = ttk.Frame(self.notebook)
        self.aba_relatorios = ttk.Frame(self.notebook)
        
        self.notebook.add(self.aba_livros, text='📖 Gerenciar Livros')
        self.notebook.add(self.aba_busca, text='🔍 Buscar Livros')
        self.notebook.add(self.aba_relatorios, text='📊 Relatórios')
        
        # Configurar cada aba
        self.setup_aba_livros()
        self.setup_aba_busca()
        self.setup_aba_relatorios()
    
    def setup_aba_livros(self):
        """Aba principal de livros"""
        # Frame de entrada
        frame_entrada = ttk.LabelFrame(self.aba_livros, text="Dados do Livro", padding="15")
        frame_entrada.pack(fill="x", padx=20, pady=10)
        
        # Título
        ttk.Label(frame_entrada, text="Título:*").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entry_titulo = ttk.Entry(frame_entrada, width=40)
        self.entry_titulo.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)
        
        # Autor
        ttk.Label(frame_entrada, text="Autor:*").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.entry_autor = ttk.Entry(frame_entrada, width=40)
        self.entry_autor.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)
        
        # Ano
        ttk.Label(frame_entrada, text="Ano:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.entry_ano = ttk.Entry(frame_entrada, width=40)
        self.entry_ano.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)
        
        # Categoria
        ttk.Label(frame_entrada, text="Categoria:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.combo_categoria = ttk.Combobox(frame_entrada, width=37, state="readonly")
        self.combo_categoria.grid(row=3, column=1, padx=10, pady=5, sticky=tk.W)
        
        # Botões
        frame_botoes = ttk.Frame(frame_entrada)
        frame_botoes.grid(row=4, column=0, columnspan=2, pady=15)
        
        ttk.Button(frame_botoes, text="➕ Adicionar", command=self.adicionar_livro).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botoes, text="✏️ Editar", command=self.editar_livro).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botoes, text="🗑️ Excluir", command=self.excluir_livro).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botoes, text="🔄 Atualizar", command=self.carregar_livros).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botoes, text="🧹 Limpar", command=self.limpar_campos).pack(side=tk.LEFT, padx=5)
        
        # Lista de livros
        frame_lista = ttk.LabelFrame(self.aba_livros, text="Lista de Livros", padding="15")
        frame_lista.pack(fill="both", expand=True, padx=20, pady=10)
        
        colunas = ('ID', 'Título', 'Autor', 'Ano', 'Categoria', 'Data Cadastro')
        self.tree_livros = ttk.Treeview(frame_lista, columns=colunas, show='headings', height=15)
        
        for col in colunas:
            self.tree_livros.heading(col, text=col)
        
        self.tree_livros.column('ID', width=50)
        self.tree_livros.column('Título', width=200)
        self.tree_livros.column('Autor', width=150)
        self.tree_livros.column('Ano', width=80)
        self.tree_livros.column('Categoria', width=120)
        self.tree_livros.column('Data Cadastro', width=120)
        
        scrollbar = ttk.Scrollbar(frame_lista, orient=tk.VERTICAL, command=self.tree_livros.yview)
        self.tree_livros.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_livros.pack(side=tk.LEFT, fill="both", expand=True)
        
        self.tree_livros.bind('<<TreeviewSelect>>', self.selecionar_livro)
    
    def setup_aba_busca(self):
        """Aba de busca"""
        # Frame de busca
        frame_busca = ttk.LabelFrame(self.aba_busca, text="Buscar Livros", padding="15")
        frame_busca.pack(fill="x", padx=20, pady=10)
        
        ttk.Label(frame_busca, text="Buscar por título ou autor:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entry_busca = ttk.Entry(frame_busca, width=40)
        self.entry_busca.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)
        self.entry_busca.bind('<KeyRelease>', self.buscar_livros)
        
        frame_botoes_busca = ttk.Frame(frame_busca)
        frame_botoes_busca.grid(row=1, column=0, columnspan=2, pady=10)
        
        ttk.Button(frame_botoes_busca, text="🔍 Buscar", command=self.buscar_livros).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botoes_busca, text="🧹 Limpar", command=self.limpar_busca).pack(side=tk.LEFT, padx=5)
        
        # Resultados
        frame_resultados = ttk.LabelFrame(self.aba_busca, text="Resultados", padding="15")
        frame_resultados.pack(fill="both", expand=True, padx=20, pady=10)
        
        colunas_busca = ('ID', 'Título', 'Autor', 'Ano', 'Categoria', 'Data Cadastro')
        self.tree_busca = ttk.Treeview(frame_resultados, columns=colunas_busca, show='headings', height=15)
        
        for col in colunas_busca:
            self.tree_busca.heading(col, text=col)
        
        self.tree_busca.column('ID', width=50)
        self.tree_busca.column('Título', width=200)
        self.tree_busca.column('Autor', width=150)
        self.tree_busca.column('Ano', width=80)
        self.tree_busca.column('Categoria', width=120)
        self.tree_busca.column('Data Cadastro', width=120)
        
        scrollbar_busca = ttk.Scrollbar(frame_resultados, orient=tk.VERTICAL, command=self.tree_busca.yview)
        self.tree_busca.configure(yscroll=scrollbar_busca.set)
        scrollbar_busca.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_busca.pack(side=tk.LEFT, fill="both", expand=True)
    
    def setup_aba_relatorios(self):
        """Aba de relatórios"""
        # Controles
        frame_controles = ttk.LabelFrame(self.aba_relatorios, text="Relatórios", padding="15")
        frame_controles.pack(fill="x", padx=20, pady=10)
        
        ttk.Button(frame_controles, text="📊 Histórico Completo", 
                  command=self.mostrar_historico).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_controles, text="📈 Estatísticas", 
                  command=self.mostrar_estatisticas).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_controles, text="📋 Livros por Categoria", 
                  command=self.mostrar_livros_por_categoria).pack(side=tk.LEFT, padx=5)
        
        # Área de relatórios
        frame_relatorios = ttk.LabelFrame(self.aba_relatorios, text="Dados", padding="15")
        frame_relatorios.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Text widget para relatórios
        self.text_relatorios = tk.Text(frame_relatorios, wrap=tk.WORD, width=80, height=20)
        scrollbar_text = ttk.Scrollbar(frame_relatorios, orient=tk.VERTICAL, command=self.text_relatorios.yview)
        self.text_relatorios.configure(yscrollcommand=scrollbar_text.set)
        
        scrollbar_text.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_relatorios.pack(side=tk.LEFT, fill="both", expand=True)
    
    def carregar_dados_iniciais(self):
        """Carrega dados iniciais"""
        self.carregar_categorias()
        self.carregar_livros()
    
    def carregar_categorias(self):
        """Carrega categorias nos comboboxes"""
        categorias = self.categoria_service.listar_categorias()
        nomes_categorias = [cat.nome for cat in categorias]
        self.combo_categoria['values'] = [''] + nomes_categorias
        self.categorias_dict = {cat.nome: cat.id for cat in categorias}
    
    def carregar_livros(self):
        """Carrega todos os livros"""
        for item in self.tree_livros.get_children():
            self.tree_livros.delete(item)
        
        livros = self.livro_service.listar_livros()
        for livro in livros:
            ano = livro.ano_publicacao if livro.ano_publicacao else "-"
            categoria = livro.categoria_nome if livro.categoria_nome else "Sem categoria"
            data = livro.data_cadastro if livro.data_cadastro else "-"
            
            self.tree_livros.insert('', tk.END, values=(
                livro.id, livro.titulo, livro.autor, ano, categoria, data
            ))
    
    def adicionar_livro(self):
        """Adiciona novo livro"""
        titulo = self.entry_titulo.get().strip()
        autor = self.entry_autor.get().strip()
        ano = self.entry_ano.get().strip()
        categoria_nome = self.combo_categoria.get()
        
        if not titulo or not autor:
            messagebox.showerror("Erro", "Título e autor são obrigatórios!")
            return
        
        try:
            ano_int = int(ano) if ano else None
        except ValueError:
            messagebox.showerror("Erro", "Ano deve ser um número!")
            return
        
        categoria_id = self.categorias_dict.get(categoria_nome)
        
        livro = Livro(titulo=titulo, autor=autor, ano_publicacao=ano_int, categoria_id=categoria_id)
        
        try:
            livro_id = self.livro_service.adicionar_livro(livro)
            self.historico_service.registrar_acao(livro_id, "CADASTRO", f"Livro '{titulo}' cadastrado")
            self.limpar_campos()
            self.carregar_livros()
            messagebox.showinfo("Sucesso", "Livro adicionado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao adicionar livro: {str(e)}")
    
    def selecionar_livro(self, event):
        """Quando um livro é selecionado"""
        selection = self.tree_livros.selection()
        if selection:
            item = selection[0]
            values = self.tree_livros.item(item, 'values')
            self.livro_selecionado_id = int(values[0])
    
    def editar_livro(self):
        """Edita livro selecionado"""
        if not hasattr(self, 'livro_selecionado_id'):
            messagebox.showerror("Erro", "Selecione um livro para editar!")
            return
        
        livro = self.livro_service.buscar_livro(self.livro_selecionado_id)
        if livro:
            self.limpar_campos()
            self.entry_titulo.insert(0, livro.titulo)
            self.entry_autor.insert(0, livro.autor)
            if livro.ano_publicacao:
                self.entry_ano.insert(0, str(livro.ano_publicacao))
            
            # Encontrar nome da categoria
            categoria_nome = ""
            for nome, id in self.categorias_dict.items():
                if id == livro.categoria_id:
                    categoria_nome = nome
                    break
            self.combo_categoria.set(categoria_nome)
            
            messagebox.showinfo("Editar", f"Editando: {livro.titulo}\nAltere os campos e clique em 'Adicionar' para salvar.")
    
    def excluir_livro(self):
        """Exclui livro selecionado"""
        if not hasattr(self, 'livro_selecionado_id'):
            messagebox.showerror("Erro", "Selecione um livro para excluir!")
            return
        
        livro = self.livro_service.buscar_livro(self.livro_selecionado_id)
        if livro and messagebox.askyesno("Confirmar", f"Excluir '{livro.titulo}'?"):
            try:
                self.historico_service.registrar_acao(self.livro_selecionado_id, "EXCLUSÃO", f"Livro '{livro.titulo}' excluído")
                self.livro_service.excluir_livro(self.livro_selecionado_id)
                self.limpar_campos()
                self.carregar_livros()
                messagebox.showinfo("Sucesso", "Livro excluído com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir livro: {str(e)}")
    
    def buscar_livros(self, event=None):
        """Busca livros por termo"""
        termo = self.entry_busca.get().strip()
        
        for item in self.tree_busca.get_children():
            self.tree_busca.delete(item)
        
        livros = self.livro_service.buscar_livros(termo)
        
        for livro in livros:
            ano = livro.ano_publicacao if livro.ano_publicacao else "-"
            categoria = livro.categoria_nome if livro.categoria_nome else "Sem categoria"
            data = livro.data_cadastro if livro.data_cadastro else "-"
            
            self.tree_busca.insert('', tk.END, values=(
                livro.id, livro.titulo, livro.autor, ano, categoria, data
            ))
    
    def mostrar_historico(self):
        """Mostra histórico completo"""
        historico = self.historico_service.obter_historico_completo()
        
        self.text_relatorios.delete(1.0, tk.END)
        self.text_relatorios.insert(tk.END, "📋 HISTÓRICO COMPLETO DE AÇÕES\n")
        self.text_relatorios.insert(tk.END, "="*50 + "\n\n")
        
        for item in historico:
            self.text_relatorios.insert(tk.END, f"📅 {item.data_acao}\n")
            self.text_relatorios.insert(tk.END, f"📖 Livro: {item.titulo}\n")
            self.text_relatorios.insert(tk.END, f"🔧 Ação: {item.acao}\n")
            if item.detalhes:
                self.text_relatorios.insert(tk.END, f"📝 Detalhes: {item.detalhes}\n")
            self.text_relatorios.insert(tk.END, "-"*30 + "\n")
    
    def mostrar_estatisticas(self):
        """Mostra estatísticas"""
        stats = self.historico_service.obter_estatisticas()
        livros = self.livro_service.listar_livros()
        
        self.text_relatorios.delete(1.0, tk.END)
        self.text_relatorios.insert(tk.END, "📊 ESTATÍSTICAS DA BIBLIOTECA\n")
        self.text_relatorios.insert(tk.END, "="*50 + "\n\n")
        
        self.text_relatorios.insert(tk.END, f"📚 Total de Livros: {stats['total_livros']}\n\n")
        
        self.text_relatorios.insert(tk.END, "📂 Livros por Categoria:\n")
        for cat in stats['livros_por_categoria']:
            self.text_relatorios.insert(tk.END, f"  • {cat['nome']}: {cat['quantidade']} livros\n")
    
    def mostrar_livros_por_categoria(self):
        """Mostra relatório de livros por categoria"""
        livros = self.livro_service.listar_livros()
        categorias = {}
        
        for livro in livros:
            cat_nome = livro.categoria_nome if livro.categoria_nome else "Sem categoria"
            if cat_nome not in categorias:
                categorias[cat_nome] = []
            categorias[cat_nome].append(livro)
        
        self.text_relatorios.delete(1.0, tk.END)
        self.text_relatorios.insert(tk.END, "📂 LIVROS POR CATEGORIA\n")
        self.text_relatorios.insert(tk.END, "="*50 + "\n\n")
        
        for categoria, livros_cat in categorias.items():
            self.text_relatorios.insert(tk.END, f"🏷️ {categoria} ({len(livros_cat)} livros):\n")
            for livro in livros_cat:
                self.text_relatorios.insert(tk.END, f"  • {livro.titulo} - {livro.autor}\n")
            self.text_relatorios.insert(tk.END, "\n")
    
    def limpar_campos(self):
        """Limpa campos de entrada"""
        self.entry_titulo.delete(0, tk.END)
        self.entry_autor.delete(0, tk.END)
        self.entry_ano.delete(0, tk.END)
        self.combo_categoria.set('')
        if hasattr(self, 'livro_selecionado_id'):
            del self.livro_selecionado_id
    
    def limpar_busca(self):
        """Limpa busca"""
        self.entry_busca.delete(0, tk.END)
        for item in self.tree_busca.get_children():
            self.tree_busca.delete(item)

if __name__ == "__main__":
    root = tk.Tk()
    app = BibliotecaApp(root)
    root.mainloop()