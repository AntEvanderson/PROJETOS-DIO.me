from abc import ABC, ABCMeta, abstractclassmethod, abstractproperty 
from datetime import datetime
import textwrap

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class Pessoafisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf 

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
    
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("Operação falhou! Você não tem saldo suficiente.")
        
        elif valor > 0:
            self._saldo -= valor
            print("\nSaque realizado com sucesso! ")
            return True
        
        else:
            print("Operação falhou! O valor informado é inválido.")
        return False
    
    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            print("\nDepósito realizado com sucesso!")
        else:
            print("\nOperação falhou! O valor informado é inválido.")
            return False
        return True
    
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite = 500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
    
    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"]== Saque.__name__]
        )
        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques > self.limite_saques

        if excedeu_limite:
            print("Operação falhou! Você não tem saldo suficiente.")

        elif excedeu_saques:
            print("Operação falhou! O valor do saque excede o limite.")
        
        else:
            return super().sacar(valor)
        return False
    
    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C\C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """
    
class Historico:
    def __init__(self):
        self._transacoes = []
    
    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacoes(self, transacao):
        self.transacoes.append(
                {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime
                ("%d-%m-%Y %H:%M:%s"),
                }
        )

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor 
    
    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

def menu():
    menu = """ \n
    =============== MENU ===============
    [1] -\t Digite para Depositar
    [2] -\t Digite para Sacar
    [3] -\t Digite para o Exibir o Extrato
    [4] -\t Nova conta
    [5] -\t Listar contas
    [6] -\t Novo usuário
    [0] -\t Para Sair
    =>"""
    return input(textwrap.dedent(menu))

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [clientes for cliente in clientes if cliente.cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\nCliente não possui conta!")
        return
    # FIXME: não permite cliente escolher a conta
    return cliente[0]

def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    Cliente = filtrar_cliente(cpf, clientes)

    if not Cliente:
        print("\n Cliente não encontrado!")
        return
    
    valor = float(input("Informe o valor do depósito: "))
    Transacao = Deposito(valor)

    conta = recuperar_conta_cliente(Cliente)
    if not conta:
        return

def sacar(clientes):
    cpf = input("informe o CPF do cliente: ")
    Cliente = filtrar_cliente(cpf, clientes)

    if not Cliente:
        print("\nCliente não encontrado!")
        return
    
    valor = float(input("Informe o valor do saque: "))
    Transacao = Saque(valor)

    conta = recuperar_conta_cliente(Cliente)
    if not conta:
        return
    
    Cliente.realizar_transacao(conta, Transacao)

def exibir_extrato(clientes):
    cpf = input("Informe o CPF do Cliente: ")
    Cliente = filtrar_cliente(cpf, clientes)

    if not Cliente:
        print("\nCliente não encotrado!")
        return
    
    Conta = recuperar_conta_cliente(Cliente)
    if not Conta:
        return
    
    print("\n+=========== EXTRATO ==========")
    Transacoes = Conta.historico.transacoes

    extrato = ""
    if not Transacoes:
        extrato = "Não foram realizadas Movimentações."
    else:
        for transacao in Transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo: \n\tR$ {Conta.saldo:.2f}")
    print("\n+==============================")

def criar_cliente(Clientes):
    cpf = input("Informe o CPF (somente Número): ")
    Cliente = filtrar_cliente(cpf, Clientes)

    if Cliente:
        print("\n Já existe usuário com esse CPF! ")
        return
    
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereço = input("Informe o endereço (logradouro, nº - bairro - cidade/sigla estado): ")

    Cliente = Pessoafisica(nome = nome, data_nascimento = data_nascimento, cpf=cpf, endereco=endereço)

    Cliente.append(Cliente)

    print("\n Cliente criado com sucesso! ")

def criar_conta(numero_conta, clientes, conta):
    cpf = input("Informe o CPF do cliente: ")
    Cliente = filtrar_cliente(cpf, clientes)

    if not Cliente:
        print("Usuário não encontrado, fluxo de criação de conta encerrado! ")

    conta = ContaCorrente.nova_conta(cliente=Cliente, numero=numero_conta)
    conta.append(conta)
    Cliente.contas.append(conta)

    print("Conta criada com sucesso!")

def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))

def main():
    clientes = []
    contas = []

    while True:
        opc = menu()

        if opc == '1':
            depositar(clientes)

        elif opc == '2':
            sacar(clientes)
        
        elif opc == '3':
            exibir_extrato(clientes)

        elif opc == '4':
            criar_cliente(clientes)
        
        elif opc == '5':
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opc == '6':
            listar_contas(contas)

        elif opc == '0':
            print("Você escolheu sair, obrigado por usar nosso sistemas!")
            break

        else:
            print("Opção Inválida, por favor selecione novamente a operação desejada.")

main()
