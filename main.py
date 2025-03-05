import tkinter as tk
from tkinter import ttk
from banco import criar_banco
from cadastro_itens import criar_aba_cadastro
from projetos import criar_aba_projetos
from contratos import criar_aba_contratos
from consultas import criar_aba_consultas

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador de Projetos")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)

        criar_aba_cadastro(self.notebook)
        criar_aba_projetos(self.notebook)
        criar_aba_contratos(self.notebook)
        criar_aba_consultas(self.notebook)
        

if __name__ == "__main__":
    criar_banco()
    root = tk.Tk()
    app = App(root)
    root.mainloop()
