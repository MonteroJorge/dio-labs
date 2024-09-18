from abc import ABC, abstractmethod
from datetime  import datetime

class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass

    @property
    def valor(self):
        pass


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
    
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(cliente, numero)

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
        excedeu_saldo = valor > self.saldo

        if excedeu_saldo:
            print("Operação falhou! Você não tem saldo suficiente.") 
        elif valor > 0:
            self._saldo -= valor
            print(f"Saque no valor de {valor:.2f} foi realizado com sucesso.")
            return True
        else:
            print(f"Operação falhou! O valor informado de {valor:.2f} é inválido.")

        return False
  
    def depositar(self, valor):
        if valor > 0:            
            self._saldo = self.saldo() + valor
            print(f"O Valor de {valor:.2f} foi depositado com sucesso.")           
        else:
            print(f"Operação falhou! O valor informado de {valor:.2f} é inválido.")
            return False
        
        return True
    

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=1000, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
        
    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print(f"Operação falhou! O valor do saque excede o limite de R$ {self.limite:.2f}.")
        elif excedeu_saques:
            print(f"Operação falhou! Somente {self.limite_saques} saques são permitidos por dia.")
        else:
            return super().sacar(valor)

        return False


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
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
            }
        )
    

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


def menu():
    emenu = """

    [d] Depositar
    [s] Sacar
    [e] Extrato
    [c] Cadastrar Cliente
    [t] Cadastrar Conta
    [l] Listar Contas
    [lc] Listar Clientes
    [q] Sair

    => Informe a opção desejada: """

    return emenu

""" def saque(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    valor = float(input("Informe o valor do saque: "))

    excedeu_saldo = valor > saldo

    excedeu_limite = valor > limite

    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")

    elif excedeu_limite:
        print(f"Operação falhou! O valor do saque excede o limite de R$ {limite:.2f}.")

    elif excedeu_saques:
        print(f"Operação falhou! Somente {limite_saques} saques são permitidos por dia.")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1

    else:
        print(f"Operação falhou! O valor informado de {valor:.2f} é inválido.")
    
    return saldo, extrato, numero_saques
"""


""" def deposito(saldo, valor, extrato, /):
    valor = float(input("Informe o valor do depósito: "))
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
    else:
        print(f"Operação falhou! O valor informado de {valor:.2f} é inválido.")
    return saldo, extrato
"""

def imprimir_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")
    

def cadastrar_cliente(lista_cliente, dict_cliente):
    nro_cpf = int(input("Informe o CPF: "))
    if nro_cpf in lista_cliente:
        print(f"Operação falhou! Cliente {nro_cpf} já cadastrado no sistema. Apenas é permitido um cadastro por CPF.")
    else:
        lista_cliente.append(nro_cpf)
        nome_cliente    = input("Informe o Nome do Cliente: ")
        data_nascimento = input("Informe a Data de Nascimento (dd/mm/yyyy): ")
        endereco        = input("Informe o Endereço: ")

        dict_cliente.update( {nro_cpf : {"nome": nome_cliente, "data_nascimento": data_nascimento, "endereco": endereco}})

    return lista_cliente, dict_cliente

def cadastrar_conta(lista_cliente, dict_cliente, nro_conta, lista_conta):
    nro_cpf = int(input("Informe o CPF: "))
    if nro_cpf not in lista_cliente:
        print(f"Operação falhou! Cliente {nro_cpf} não está cadastrado no sistema. A criação de uma conta precisa de um cliente cadastrado.")
    else:
        nro_conta += 1
        list_tmp2 = []; list_tmp2.append(nro_conta); list_tmp2.append('0001'); list_tmp2.append(nro_cpf)
        lista_conta.append(list_tmp2)
        print(f"Conta {nro_conta} cadastrada para o cliente {nro_cpf} com sucesso.")

    return dict_cliente, nro_conta, lista_conta

def listar_cliente(lista_cliente, dict_cliente):
    nro_cpf = int(input("Informe o CPF: "))
    if nro_cpf not in lista_cliente:
        print(f"Operação falhou! Cliente {nro_cpf} não está cadastrado no sistema.")
    else:
        print("\n================ DADOS DO CLIENTE ================")
        print(f"CPF do Cliente: {nro_cpf}" )
        print(f"Nome do Cliente: {dict_cliente[nro_cpf]["nome"]}")
        print(f"Data de Nascimento (dd/mm/yyyy): {dict_cliente[nro_cpf]["data_nascimento"]}")
        print(f"Endereço do Cliente: {dict_cliente[nro_cpf]["endereco"]}")
        print("====================================================")

def main():
    saldo = 0
    #limite = 1000
    extrato = ""
    numero_saques = 0
    #LIMITE_SAQUES = 3
    valor = 0
    lista_cliente = []
    lista_conta = []
    #dict_cliente = {}
    nro_conta = 0

    
    while True:
        
        opcao = input(menu()).lower()

        if opcao == "d":
            saldo, extrato = deposito(saldo, valor, extrato)
            
        elif opcao == "s":
            saldo, extrato, numero_saques = saque(saldo=saldo, valor=valor, extrato=extrato, limite=limite, numero_saques=numero_saques, \
                                                limite_saques=LIMITE_SAQUES)
            
        elif opcao == "e":
            imprimir_extrato(saldo, extrato=extrato)

        elif opcao == "c":
            lista_cliente, dict_cliente = cadastrar_cliente(lista_cliente, dict_cliente)

        elif opcao == "t":
            dict_cliente, nro_conta, lista_conta = cadastrar_conta(lista_cliente, dict_cliente, nro_conta, lista_conta)

    #    elif opcao == "l":
    #        listar_conta()
        
        elif opcao == "lc":
            listar_cliente(lista_cliente, dict_cliente)
            
        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

main()