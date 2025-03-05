import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

def carregar_projetos(tree):
    conn = sqlite3.connect("sistema.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome_projeto, definicao_projeto, codigo_obra FROM projetos")
    projetos = cursor.fetchall()
    conn.close()

    tree.delete(*tree.get_children())
    for projeto in projetos:
        tree.insert("", "end", values=projeto)

def criar_projeto(tree):
    janela = tk.Toplevel()
    janela.title("Criar Novo Projeto")
    janela.geometry("900x400")

    tk.Label(janela, text="Nome do Projeto:").pack()
    entry_nome = tk.Entry(janela)
    entry_nome.pack()

    tk.Label(janela, text="Definição do Projeto:").pack()
    entry_definicao = tk.Entry(janela)
    entry_definicao.pack()

    tk.Label(janela, text="Código da Obra:").pack()
    entry_codigo = tk.Entry(janela)
    entry_codigo.pack()

    frame_tabela = ttk.Frame(janela)
    frame_tabela.pack(pady=10, fill=tk.BOTH, expand=True)

    colunas = ("Selecionado", "Numeracao", "Instalacao", "Descricao", "Justificativa", "Categoria", "Data Aquisição", "Localização", "Vida Útil", "Observações")
    tree_itens = ttk.Treeview(frame_tabela, columns=colunas, show="headings")
    
    for col in colunas:
        tree_itens.heading(col, text=col)
        tree_itens.column(col, width=100)
    
    tree_itens.pack(fill=tk.BOTH, expand=True)

    conn = sqlite3.connect("sistema.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM itens")
    itens = cursor.fetchall()
    conn.close()

    selecionados = {}

    for item in itens:
        selecionados[item[0]] = tk.BooleanVar()
        tree_itens.insert("", "end", values=("☐",) + item)
    
    def toggle_selecao(event):
        selected_item = tree_itens.focus()
        if selected_item:
            item_values = tree_itens.item(selected_item, "values")
            numeracao = item_values[1]  # Primeiro valor após a caixa de seleção
            if selecionados[numeracao].get():
                selecionados[numeracao].set(False)
                tree_itens.item(selected_item, values=("☐",) + item_values[1:])
            else:
                selecionados[numeracao].set(True)
                tree_itens.item(selected_item, values=("☑",) + item_values[1:])
    
    tree_itens.bind("<ButtonRelease-1>", toggle_selecao)
    
    def salvar_projeto():
        nome = entry_nome.get()
        definicao = entry_definicao.get()
        codigo = entry_codigo.get()
        itens_selecionados = [key for key, var in selecionados.items() if var.get()]

        if not nome:
            messagebox.showerror("Erro", "O nome do projeto é obrigatório!")
            return

        conn = sqlite3.connect("sistema.db")
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO projetos (nome_projeto, definicao_projeto, codigo_obra) VALUES (?, ?, ?)",
                           (nome, definicao, codigo))
            projeto_id = cursor.lastrowid

            for numeracao in itens_selecionados:
                cursor.execute("INSERT INTO projeto_itens (projeto_id, numeracao_item) VALUES (?, ?)", (projeto_id, numeracao))

            conn.commit()
            messagebox.showinfo("Sucesso", "Projeto criado com itens selecionados!")
            carregar_projetos(tree)
            janela.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Já existe um projeto com esse nome!")
        conn.close()

    btn_salvar = tk.Button(janela, text="Salvar Projeto", command=salvar_projeto)
    btn_salvar.pack()

def criar_aba_projetos(notebook):
    aba_projetos = ttk.Frame(notebook)
    notebook.add(aba_projetos, text="Projetos")

    btn_novo_projeto = ttk.Button(aba_projetos, text="Criar Novo Projeto", command=lambda: criar_projeto(tree))
    btn_novo_projeto.pack()

    colunas = ("ID", "Nome do Projeto", "Definição", "Código da Obra")
    tree = ttk.Treeview(aba_projetos, columns=colunas, show="headings")
    
    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, width=150)
    
    tree.pack(fill=tk.BOTH, expand=True)
    carregar_projetos(tree)
    return aba_projetos
