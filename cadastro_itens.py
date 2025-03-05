import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sqlite3
import pandas as pd
from banco import criar_banco

def carregar_excel():
    file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
    if not file_path:
        return
    try:
        df = pd.read_excel(file_path)
        conn = sqlite3.connect("sistema.db")
        cursor = conn.cursor()
        
        for _, row in df.iterrows():
            try:
                cursor.execute('''INSERT INTO itens (numeracao, instalacao, descricao, justificativa, categoria, data_aquisicao, localizacao, vida_util, observacoes) 
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                                (row['Numeração'], row['Instalação'], row['Descrição da revitalização'], row['Justificativa'], 
                                 row['Categoria/tipo'], row['Data de aquisição'], row['Localização'], row['Vida útil remanescente'], row['Observações']))
            except sqlite3.IntegrityError:
                pass  # Ignorar duplicatas
        
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Dados importados com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao carregar arquivo: {str(e)}")

def criar_aba_cadastro(notebook):
    aba_cadastro = ttk.Frame(notebook)
    notebook.add(aba_cadastro, text="Cadastro de Itens")

    ttk.Label(aba_cadastro, text="Cadastro de Itens").pack()
    btn_carregar = ttk.Button(aba_cadastro, text="Carregar Excel", command=carregar_excel)
    btn_carregar.pack(pady=10)

    return aba_cadastro
