import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

def criar_aba_consultas(notebook):
    aba_consultas = ttk.Frame(notebook)
    notebook.add(aba_consultas, text="Consultas")

    # Filtros de pesquisa
    frame_filtros = tk.Frame(aba_consultas)
    frame_filtros.pack(fill="x", padx=10, pady=5)

    tk.Label(frame_filtros, text="Filtrar por Instalação:").grid(row=0, column=0)
    entry_instalacao = tk.Entry(frame_filtros)
    entry_instalacao.grid(row=0, column=1)

    tk.Label(frame_filtros, text="Filtrar por Projeto:").grid(row=0, column=2)
    entry_projeto = tk.Entry(frame_filtros)
    entry_projeto.grid(row=0, column=3)

    tk.Label(frame_filtros, text="Filtrar por Contrato:").grid(row=0, column=4)
    entry_contrato = tk.Entry(frame_filtros)
    entry_contrato.grid(row=0, column=5)

    # Botão para buscar os dados
    btn_filtrar = tk.Button(
        frame_filtros, text="Buscar",
        command=lambda: buscar_dados(tree, entry_instalacao.get(), entry_projeto.get(), entry_contrato.get())
    )
    btn_filtrar.grid(row=0, column=6, padx=10)

    # Tabela para exibir os resultados
    frame_tabela = tk.Frame(aba_consultas)
    frame_tabela.pack(fill="both", expand=True, padx=10, pady=10)

    colunas = ("ID", "Instalação", "Descrição", "Projeto", "Código da Obra", "Definição do Projeto", "Contrato", "Tipo de Contrato", "Código do Contrato", "Descrição do Contrato")
    tree = ttk.Treeview(frame_tabela, columns=colunas, show="headings")

    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, width=150)

    tree.pack(fill="both", expand=True)

    # Realiza a busca inicial sem filtros
    buscar_dados(tree)

def buscar_dados(tree, instalacao="", projeto="", contrato=""):
    """Busca dados corretamente relacionados a projetos e contratos"""
    for item in tree.get_children():
        tree.delete(item)

    conn = sqlite3.connect("sistema.db")
    cursor = conn.cursor()

    # Consulta SQL corrigida para garantir que todos os itens sejam exibidos com os dados dos projetos e contratos
    query = """
        SELECT i.numeracao, i.instalacao, i.descricao,
               p.nome_projeto, p.codigo_obra, p.definicao_projeto,
               c.codigo_contrato, c.tipo, c.descricao_contrato
        FROM itens i
        LEFT JOIN projeto_itens pi ON i.numeracao = pi.numeracao_item
        LEFT JOIN projetos p ON pi.projeto_id = p.id
        LEFT JOIN contrato_itens ci ON i.numeracao = ci.numeracao_item
        LEFT JOIN contratos c ON ci.contrato_id = c.id
    """

    # Condições de filtragem
    params = []

    if instalacao:
        query += " WHERE i.instalacao LIKE ?"
        params.append(f"%{instalacao}%")
    
    if projeto:
        if params:
            query += " AND p.nome_projeto LIKE ?"
        else:
            query += " WHERE p.nome_projeto LIKE ?"
        params.append(f"%{projeto}%")

    if contrato:
        if params:
            query += " AND c.codigo_contrato LIKE ?"
        else:
            query += " WHERE c.codigo_contrato LIKE ?"
        params.append(f"%{contrato}%")

    cursor.execute(query, params)
    resultados = cursor.fetchall()

    # Depuração: Exibir os resultados no terminal
    print("Resultados encontrados:", resultados)

    for row in resultados:
        tree.insert("", "end", values=row)

    conn.close()

