from datetime import date
from abc import ABC, abstractmethod

class Conta:
    def __init__(self, cliente, numero, agencia):
        self.__saldo = 0.0
        self.__numero = numero
        self.__agencia = agencia
        self.__cliente = cliente
        self.__historico = Historico()

    @property
    def saldo(self):
        return self.__saldo

    @classmethod
    def nova_conta(cls, cliente, numero, agencia):
        return cls(cliente, numero, agencia)

    def sacar(self, valor):
        saldo = self.__saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\nOperação falhou! Você não tem saldo suficiente.")

        elif valor > 0:
            self.__saldo -= valor
            self.__historico.adicionar_transacao(Saque(valor))
            print("\nSaque realizado com sucesso!")
            return True

        else:
            print("\nOperação falhou! O valor informado é inválido.")

        return False

    def depositar(self, valor):
        if valor > 0:
            self.__saldo += valor
            self.__historico.adicionar_transacao(Deposito(valor))
            print("\nDepósito realizado com sucesso!")
        else:
            print("\nOperação falhou! O valor informado é inválido.")
            return False

        return True

    @property
    def historico(self):
        return self.__historico

    @property
    def numero(self):
        return self.__numero

    @property
    def agencia(self):
        return self.__agencia

    @property
    def cliente(self):
        return self.__cliente

class ContaCorrente(Conta):
    def __init__(self, cliente, numero, agencia, limite, limite_saques):
        super().__init__(cliente, numero, agencia)
        self.__limite = limite
        self.__limite_saques = limite_saques

    @property
    def limite(self):
        return self.__limite

    @property
    def limite_saques(self):
        return self.__limite_saques

class Cliente:
    def __init__(self, endereco):
        self.__endereco = endereco
        self.__contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.__contas.append(conta)

    @property
    def endereco(self):
        return self.__endereco

    @property
    def contas(self):
        return self.__contas

class PessoaFisica(Cliente):
    def __init__(self, endereco, cpf, nome, data_nascimento):
        super().__init__(endereco)
        self.__cpf = cpf
        self.__nome = nome
        self.__data_nascimento = data_nascimento

    @property
    def cpf(self):
        return self.__cpf

    @property
    def nome(self):
        return self.__nome

    @property
    def data_nascimento(self):
        return self.__data_nascimento

class Historico:
    def __init__(self):
        self.__transacoes = []

    def adicionar_transacao(self, transacao):
        self.__transacoes.append(transacao)

    @property
    def transacoes(self):
        return self.__transacoes

class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self.__valor = valor

    def registrar(self, conta):
        conta.depositar(self.__valor)

    @property
    def valor(self):
        return self.__valor

class Saque(Transacao):
    def __init__(self, valor):
        self.__valor = valor

    def registrar(self, conta):
        conta.sacar(self.__valor)

    @property
    def valor(self):
        return self.__valor

# testes
cliente = PessoaFisica("Rua das Flores, 123", "123.456.789-10", "Marcela da Silva", date(1985, 4, 23))
conta = ContaCorrente(cliente, 12345, "001", 1000.0, 3)
cliente.adicionar_conta(conta)
cliente.realizar_transacao(conta, Deposito(500.0))
cliente.realizar_transacao(conta, Saque(100.0))

print(f"Saldo atual: R${conta.saldo}")
print("Histórico de transações:")
for transacao in conta.historico.transacoes:
    print(f"- {transacao.__class__.__name__} de R${transacao.valor}")
