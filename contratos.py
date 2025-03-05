import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

def criar_aba_contratos(notebook):
    aba_contratos = ttk.Frame(notebook)
    notebook.add(aba_contratos, text="Planos de Contratação")

    frame_top = tk.Frame(aba_contratos)
    frame_top.pack(fill="x", pady=10, padx=10)

    btn_novo_plano = tk.Button(frame_top, text="Criar Novo Plano", command=lambda: abrir_janela_novo_plano(tree))
    btn_novo_plano.pack()

    frame_tabela = tk.Frame(aba_contratos)
    frame_tabela.pack(fill="both", expand=True, padx=10, pady=10)

    # lista de colunas para incluir o tipo de contrato
    colunas = ("ID", "Nome", "Código", "Descrição", "Tipo de Contrato")
    tree = ttk.Treeview(frame_tabela, columns=colunas, show="headings")

    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, width=150)

    tree.pack(fill="both", expand=True)

    btn_excluir = tk.Button(aba_contratos, text="Excluir Plano Selecionado", command=lambda: excluir_plano(tree))
    btn_excluir.pack(pady=10)

    atualizar_tabela(tree)

def abrir_janela_novo_plano(tree):
    janela_novo = tk.Toplevel()
    janela_novo.title("Novo Plano de Contratação")
    janela_novo.geometry("1200x600")

    tk.Label(janela_novo, text="Nome do Contrato:").pack()
    entry_nome = tk.Entry(janela_novo)
    entry_nome.pack()

    tk.Label(janela_novo, text="Código do Contrato:").pack()
    entry_codigo = tk.Entry(janela_novo)
    entry_codigo.pack()

    tk.Label(janela_novo, text="Descrição do Contrato:").pack()
    entry_descricao = tk.Text(janela_novo, height=5, width=50)
    entry_descricao.pack()

    tk.Label(janela_novo, text="Tipo de Contrato:").pack()
    tipo_contrato = ttk.Combobox(janela_novo, values=["Fornecimento", "Serviço"])
    tipo_contrato.set("Fornecimento")  # Definir o valor padrão como "Fornecimento"
    tipo_contrato.pack()

    frame_tabela = ttk.Frame(janela_novo)
    frame_tabela.pack(pady=10, fill=tk.BOTH, expand=True)

    # mostrar todas as colunas de projetos
    colunas = ("Selecionado", "ID", "Nome do Projeto", "Definição do Projeto", "Código da Obra", "Item", "Instalação", 
               "Descrição do Item", "Justificativa", "Categoria", "Data Aquisição", "Localização", "Vida Útil", "Observações")
    tree_itens = ttk.Treeview(frame_tabela, columns=colunas, show="headings")

    for col in colunas:
        tree_itens.heading(col, text=col)
        tree_itens.column(col, width=120)

    tree_itens.pack(fill=tk.BOTH, expand=True)

    # Atualizando a consulta para buscar todas as colunas necessárias
    conn = sqlite3.connect("sistema.db")
    cursor = conn.cursor()
    cursor.execute(""" 
        SELECT p.id, p.nome_projeto, p.definicao_projeto, p.codigo_obra, i.numeracao, i.instalacao, i.descricao, 
               i.justificativa, i.categoria, i.data_aquisicao, i.localizacao, i.vida_util, i.observacoes 
        FROM projetos p 
        JOIN projeto_itens pi ON p.id = pi.projeto_id 
        JOIN itens i ON pi.numeracao_item = i.numeracao
    """)
    itens = cursor.fetchall()
    conn.close()

    selecionados = {}
    for item in itens:
        item_id = item[0]
        selecionados[item_id] = tk.BooleanVar()
        tree_itens.insert("", "end", values=("☐",) + item, tags=(str(item_id),))

    def toggle_selecao(event):
        selected_item = tree_itens.focus()
        if selected_item:
            item_values = tree_itens.item(selected_item, "values")
            item_id = int(item_values[1])
            if selecionados[item_id].get():
                selecionados[item_id].set(False)
                tree_itens.item(selected_item, values=("☐",) + item_values[1:])
            else:
                selecionados[item_id].set(True)
                tree_itens.item(selected_item, values=("☑",) + item_values[1:])

    tree_itens.bind("<ButtonRelease-1>", toggle_selecao)

    def salvar_plano():
        nome = entry_nome.get()
        codigo = entry_codigo.get()
        descricao = entry_descricao.get("1.0", tk.END).strip()  # A descrição vem do campo de texto
        tipo = tipo_contrato.get()  # O tipo vem do combobox
        itens_selecionados = [key for key, var in selecionados.items() if var.get()]

        if not nome or not codigo or not descricao:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
            return

        try:
            # Verificar se o código do contrato já existe
            conn = sqlite3.connect("sistema.db")
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(1) FROM contratos WHERE codigo_contrato = ?", (codigo,))
            if cursor.fetchone()[0] > 0:
                messagebox.showerror("Erro", "Código de contrato já existe!")
                conn.close()
                return

            # Inserir dados na tabela contratos
            cursor.execute(
                "INSERT INTO contratos (codigo_contrato, descricao_contrato, tipo) VALUES (?, ?, ?)", 
                (codigo, descricao, tipo)  # Agora o tipo vai para a coluna "tipo" e a descrição vai para "descricao_contrato"
            )
            contrato_id = cursor.lastrowid

            # Inserir os itens selecionados no contrato
            for item_id in itens_selecionados:
                cursor.execute("INSERT INTO contrato_itens (contrato_id, numeracao_item) VALUES (?, ?)", 
                               (contrato_id, item_id))

            # Associar os projetos selecionados ao contrato
            for item_id in itens_selecionados:
                cursor.execute(""" 
                    INSERT INTO contrato_projetos (contrato_id, projeto_id) 
                    VALUES (?, ?)
                """, (contrato_id, item_id))

            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", "Plano de contratação salvo com sucesso!")
            janela_novo.destroy()
            atualizar_tabela(tree)

        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Erro de integridade no banco de dados!")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro inesperado: {e}")

    btn_salvar = tk.Button(janela_novo, text="Salvar Plano", command=salvar_plano)
    btn_salvar.pack()

def atualizar_tabela(tree):
    for item in tree.get_children():
        tree.delete(item)

    conn = sqlite3.connect("sistema.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, codigo_contrato, descricao_contrato, tipo FROM contratos")
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)
    conn.close()

def excluir_plano(tree):
    item_selecionado = tree.selection()
    if not item_selecionado:
        messagebox.showerror("Erro", "Selecione um plano para excluir!")
        return
    
    plano_id = tree.item(item_selecionado)["values"][0]
    
    conn = sqlite3.connect("sistema.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contratos WHERE id = ?", (plano_id,))
    conn.commit()
    conn.close()
    
    messagebox.showinfo("Sucesso", "Plano excluído!")
    atualizar_tabela(tree)
