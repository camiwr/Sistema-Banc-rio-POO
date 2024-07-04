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
    LIMITE_SAQUES_PADRAO = 3

    def __init__(self, cliente, numero, agencia, limite):
        super().__init__(cliente, numero, agencia)
        self.__limite = limite
        self.__limite_saques = self.LIMITE_SAQUES_PADRAO
        self.__numero_saques = 0

    @property
    def limite(self):
        return self.__limite

    @property
    def limite_saques(self):
        return self.__limite_saques

    @property
    def numero_saques(self):
        return self.__numero_saques

    @numero_saques.setter
    def numero_saques(self, valor):
        self.__numero_saques = valor

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

def menu():
    menu_texto = """\n
    =_=_=_=_=_=_ MENU =_=_=_=_=_=_=

    [1] Cadastrar Usuário
    [2] Cadastrar Conta Corrente
    [3] Depositar
    [4] Sacar
    [5] Extrato
    [6] Listar Contas
    [0] Sair
    => """
    return input(menu_texto)

def cadastrar_usuario(clientes, nome, data_nascimento, cpf, endereco):
    for cliente in clientes:
        if cliente.cpf == cpf:
            print("Erro! Já existe um usuário cadastrado com esse CPF.")
            return
    cliente = PessoaFisica(endereco, cpf, nome, date.fromisoformat(data_nascimento))
    clientes.append(cliente)
    print("Usuário cadastrado com sucesso!")

def cadastrar_conta(clientes, contas, numero_conta, cpf):
    for cliente in clientes:
        if cliente.cpf == cpf:
            agencia = "0001"
            limite = 1000.0  # Limite padrão para todas as contas
            conta = ContaCorrente(cliente, numero_conta, agencia, limite)
            cliente.adicionar_conta(conta)
            contas.append(conta)
            print(f"Conta corrente {numero_conta} cadastrada com sucesso!")
            return numero_conta + 1
    print("Erro! Usuário não encontrado. Verifique o CPF e tente novamente.")
    return numero_conta

def listar_contas(contas):
    if not contas:
        print("Não há contas cadastradas.")
    else:
        print("\n=_=_=_=_=_=_ LISTA DE CONTAS =_=_=_=_=_=_=")
        for conta in contas:
            cliente = conta.cliente
            print(f"Agência: {conta.agencia} | Número da Conta: {conta.numero} | Cliente: {cliente.nome}")
        print("=_=_=_=_=_=_=_=_=_=_=_=_=_=_=_=_=_=_=_=_=_=_=")

def buscar_conta(contas, numero_conta):
    for conta in contas:
        if conta.numero == numero_conta:
            return conta
    return None

def depositar(conta, valor):
    if valor > 0:
        conta.depositar(valor)
    else:
        print("Operação falhou! O valor informado é inválido.")

def sacar(conta, valor):
    if valor > conta.saldo:
        print("Operação falhou! Saldo insuficiente.")
    elif conta.numero_saques >= conta.limite_saques:
        print("Operação falhou! Número máximo de saques diários excedido.")
    elif valor > 0:
        conta.sacar(valor)
        conta.numero_saques += 1
    else:
        print("Operação falhou! O valor informado é inválido.")

def visualizar_extrato(conta):
    print("\n=_=_=_=_=_=_ EXTRATO =_=_=_=_=_=_=")
    if not conta.historico.transacoes:
        print("Não foram realizadas movimentações.")
    else:
        for transacao in conta.historico.transacoes:
            if isinstance(transacao, Deposito):
                print(f"Depósito: R$ {transacao.valor:.2f}")
            elif isinstance(transacao, Saque):
                print(f"Saque: R$ {transacao.valor:.2f}")
    print(f"\nSaldo: R$ {conta.saldo:.2f}")
    print("=_=_=_=_=_=_=_=_=_=_=_=_=_=_=_=_=_=_=")

if __name__ == "__main__":
    clientes = []
    contas = []
    numero_conta = 1

    while True:
        opcao = menu()

        if opcao == '1':
            nome = input("Nome: ")
            data_nascimento = input("Data de nascimento (AAAA-MM-DD): ")
            cpf = input("CPF: ")
            endereco = input("Endereço: ")
            cadastrar_usuario(clientes, nome, data_nascimento, cpf, endereco)

        elif opcao == '2':
            cpf = input("CPF do cliente: ")
            numero_conta = cadastrar_conta(clientes, contas, numero_conta, cpf)

        elif opcao == '3':
            numero = int(input("Número da conta: "))
            conta = buscar_conta(contas, numero)
            if conta:
                valor = float(input("Valor do depósito: "))
                depositar(conta, valor)
            else:
                print("Conta não encontrada.")

        elif opcao == '4':
            numero = int(input("Número da conta: "))
            conta = buscar_conta(contas, numero)
            if conta:
                valor = float(input("Valor do saque: "))
                sacar(conta, valor)
            else:
                print("Conta não encontrada.")

        elif opcao == '5':
            numero = int(input("Número da conta: "))
            conta = buscar_conta(contas, numero)
            if conta:
                visualizar_extrato(conta)
            else:
                print("Conta não encontrada.")

        elif opcao == '6':
            listar_contas(contas)

        elif opcao == '0':
            print("Saindo...")
            break

        else:
            print("Opção inválida. Tente novamente.")
