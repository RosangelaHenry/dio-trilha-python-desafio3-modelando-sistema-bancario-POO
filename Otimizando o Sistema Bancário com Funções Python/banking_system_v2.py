import json  # Importe a biblioteca json se ainda não estiver importada
from funcoes import *  # Importe suas funções específicas do sistema bancário

# Função para carregar usuários do sistema
def carregar_usuarios():
    try:
        with open('usuarios.json', 'r') as file:
            users = json.load(file)
    except FileNotFoundError:
        users = {}  # Caso o arquivo não exista, inicializa com um dicionário vazio
    
    return users

# Função para verificar login
def verificar_login(cpf, senha):
    users = carregar_usuarios()  # Supondo que carregar_usuarios() retorna um dicionário com os usuários
    if cpf in users and users[cpf]["senha"] == senha:
        return True
    else:
        return False

# Função principal do sistema bancário
def main():
    while True:
        initial_menu()

        opcao = input("=> ")
        limpar_tela()

        if opcao == "1":
            login()

        elif opcao == "2":
            criar_user()

        elif opcao == "3":
            print("Volte sempre!!\n")
            break

        else:
            print("Digite uma opção válida: ")

# Executa main() se este script for executado diretamente
if __name__ == "__main__":
    main()
