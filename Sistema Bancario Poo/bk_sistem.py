from abc import ABC, abstractmethod
from datetime import datetime

# Lista de usuários
usuarios = []
contas = []

# Classe que representa o usuário
class Usuario:
    def __init__(self, endereco, email, senha):
        self.contas = []
        self.endereco = endereco
        self.email = email
        self.senha = senha

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

    @classmethod
    def criar_usuario(cls, endereco, email, senha, **kwargs):
        if "nome" in kwargs and "aniversario" in kwargs and "cpf" in kwargs:
            return PessoaFisica(endereco, email, senha, **kwargs)
        elif "nome" in kwargs and "cnpj" in kwargs:
            return PessoaJuridica(endereco, email, senha, **kwargs)
        else:
            raise ValueError("Informações de usuário inválidas")

    @staticmethod
    def autenticar(email, senha):
        for usuario in usuarios:
            if usuario.email == email and usuario.senha == senha:
                return usuario
        return None


# Subclasse de usuário que representa um usuário individual/pessoal
class PessoaFisica(Usuario):
    def __init__(self, endereco, email, senha, nome, aniversario, cpf):
        super().__init__(endereco, email, senha)
        self.nome = nome
        self.aniversario = aniversario
        self.cpf = cpf

    def __str__(self):
        return f"Pessoa Física: {self.endereco}, {self.email}, {self.senha}, {self.nome}, {self.aniversario}, {self.cpf}"


# Subclasse de Usuário que representa um usuário corporativo
class PessoaJuridica(Usuario):
    def __init__(self, endereco, email, senha, nome, cnpj):
        super().__init__(endereco, email, senha)
        self.nome = nome
        self.cnpj = cnpj

    def __str__(self):
        return f"Pessoa Jurídica: {self.endereco}, {self.email}, {self.senha}, {self.nome}, {self.cnpj}"


# Classe que representa uma conta simples
class Conta:
    def __init__(self, id_conta, usuario):
        self._saldo = 0
        self._agencia = "0001"
        self._historico = Historico()
        self._id_conta = id_conta
        self._usuario = usuario

    @classmethod
    def nova_conta(cls, usuario, id_conta, tipo_conta):
        if tipo_conta == "1":
            return ContaCorrente(id_conta, usuario, tipo_conta)
        else:
            print("Tipo inválido, selecione um tipo válido")
            return None
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def id_conta(self):
        return self._id_conta
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def usuario(self):
        return self._usuario
    
    @property
    def historico(self):
        return self._historico
    
    def saque(self, valor):
        saldo = self._saldo
        valor_excedido = valor > saldo

        if valor_excedido:
            print("\n Falha na operação, você não tem saldo suficiente.")
            return False

        elif valor > 0:
            self._saldo -= valor
            print("\n Saque realizado com sucesso!")
            return True
        
        else:
            print("Falha! Valor inválido.")
            return False
        
    def deposito(self, valor):
        if valor > 0:
            self._saldo += valor
            print("Depósito realizado com sucesso!")
            return True

        else:
            print("Falha na operação! Valor inválido")
            return False


# Subclasse de Conta que representa o tipo de conta atual
class ContaCorrente(Conta):
    def __init__(self, id_conta, usuario, tipo_conta, limite_valor=500, limite_saque=3):
        super().__init__(id_conta, usuario)
        self._limite_valor = limite_valor
        self._limite_saque = limite_saque
        self._tipo = tipo_conta

    def saque(self, valor):
        quantidade_saque = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])

        limite_excedido = valor > self._limite_valor
        limite_saque_excedido = quantidade_saque >= self._limite_saque

        if limite_excedido:
            print("Falha! o valor do Saque excede o limite permitido para sua conta.")
            return False

        elif limite_saque_excedido:
            print("Falha! Número máximo de saques excedido.")
            return False

        else:
            return super().saque(valor)
        
    def __str__(self):
        return f"""
        Agência:\t{self.agencia}
        C/C:\t\t{self.id_conta}
        Titular:\t{self.usuario.nome}
        """


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
        
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            }
        )


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.saque(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.deposito(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
