class Livro:
    def __init__(self, id=None, titulo="", autor="", ano_publicacao=None, categoria_id=None, categoria_nome="", data_cadastro=""):
        self.id = id
        self.titulo = titulo
        self.autor = autor
        self.ano_publicacao = ano_publicacao
        self.categoria_id = categoria_id
        self.categoria_nome = categoria_nome
        self.data_cadastro = data_cadastro

class Historico:
    def __init__(self, id=None, livro_id=None, acao="", detalhes="", data_acao="", titulo=""):
        self.id = id
        self.livro_id = livro_id
        self.acao = acao
        self.detalhes = detalhes
        self.data_acao = data_acao
        self.titulo = titulo

class Categoria:
    def __init__(self, id=None, nome=""):
        self.id = id
        self.nome = nome