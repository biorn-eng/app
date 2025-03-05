import sqlite3

def criar_banco():
    conn = sqlite3.connect("sistema.db")
    cursor = conn.cursor()
    
    # Tabela de Itens
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS itens (
            numeracao TEXT PRIMARY KEY,
            instalacao TEXT,
            descricao TEXT,
            justificativa TEXT,
            categoria TEXT,
            data_aquisicao TEXT,
            localizacao TEXT,
            vida_util TEXT,
            observacoes TEXT
        )
    ''')

    # Tabela de Projetos (com os novos campos de definição do projeto e código da obra)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projetos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_projeto TEXT UNIQUE NOT NULL,
            definicao_projeto TEXT,
            codigo_obra TEXT,
            numeracao TEXT,
            instalacao TEXT,
            descricao TEXT,
            justificativa TEXT,
            categoria TEXT,
            data_aquisicao TEXT,
            localizacao TEXT,
            vida_util TEXT,
            observacoes TEXT
        )
    ''')

    # Relacionamento entre Projetos e Itens
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projeto_itens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            projeto_id INTEGER NOT NULL,
            numeracao_item TEXT NOT NULL,
            FOREIGN KEY (projeto_id) REFERENCES projetos(id) ON DELETE CASCADE,
            FOREIGN KEY (numeracao_item) REFERENCES itens(numeracao) ON DELETE CASCADE
        )
    ''')

    # Tabela de Contratos (com as novas colunas)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contratos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo_contrato TEXT UNIQUE NOT NULL,
            descricao_contrato TEXT,
            tipo TEXT CHECK(tipo IN ('Fornecimento', 'Serviço')) NOT NULL
        )
    ''')

    # Relacionamento entre Contratos e Projetos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contrato_projetos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contrato_id INTEGER NOT NULL,
            projeto_id INTEGER NOT NULL,
            FOREIGN KEY (contrato_id) REFERENCES contratos(id) ON DELETE CASCADE,
            FOREIGN KEY (projeto_id) REFERENCES projetos(id) ON DELETE CASCADE
        )
    ''')

    # Relacionamento entre Contratos e Itens
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contrato_itens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contrato_id INTEGER NOT NULL,
            numeracao_item TEXT NOT NULL,
            FOREIGN KEY (contrato_id) REFERENCES contratos(id) ON DELETE CASCADE,
            FOREIGN KEY (numeracao_item) REFERENCES itens(numeracao) ON DELETE CASCADE
        )
    ''')

    conn.commit()
    conn.close()
    print("Banco de dados atualizado com sucesso!")

# Executa a criação do banco
criar_banco()
