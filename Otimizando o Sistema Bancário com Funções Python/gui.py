import tkinter as tk
from tkinter import messagebox
from banking_system_v2 import verificar_login, usuarios, login, criar_conta, acessar_conta  # Ajuste para importar as funções necessárias

# Função chamada quando o botão de login é clicado
def login_button_click():
    cpf = cpf_entry.get()
    senha = senha_entry.get()

    if verificar_login(cpf, senha):
        messagebox.showinfo("Login", f"Bem-vindo, {usuarios[cpf]['nome']}!")
        login(cpf)  # Chama a função de login passando o CPF do usuário
    else:
        messagebox.showerror("Login", "CPF ou senha inválidos. Tente novamente.")

# Criar a janela principal
janela = tk.Tk()
janela.title("Sistema Bancário")
janela.geometry("600x200")  # Ajuste o tamanho conforme necessário

# Criar os widgets da GUI
cpf_label = tk.Label(janela, text="CPF:")
cpf_entry = tk.Entry(janela)

senha_label = tk.Label(janela, text="Senha:")
senha_entry = tk.Entry(janela, show="*")

login_button = tk.Button(janela, text="Login", command=login_button_click)

# Posicionar os widgets na janela usando grid para um layout mais organizado
cpf_label.grid(row=0, column=0, padx=10, pady=10)
cpf_entry.grid(row=0, column=1, padx=10, pady=10)
senha_label.grid(row=1, column=0, padx=10, pady=10)
senha_entry.grid(row=1, column=1, padx=10, pady=10)
login_button.grid(row=2, column=1, padx=10, pady=10)

# Iniciar o loop de eventos da GUI
janela.mainloop()
