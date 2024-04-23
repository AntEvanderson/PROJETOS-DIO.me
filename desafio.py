menu = """
    
    [1] - Digite para Depositar
    [2] - Digite para Sacar
    [3] - Digite para o Exibir o Extrato
    [0] - Para Sair

print("Digite a opção desejada: ")
 =>"""

saldo = 0
limite = 500
extrato = ""
numeros_saque = 0
LIMITE_SAQUES = 3

while True:
    opcao = input(menu)    
    
    if opcao == "1":
        valor = float(input("Informe o valor do deposito: "))
        
        if valor >= 0:
            saldo += valor
            extrato += f'valor do deposito: R$ {valor:.2f}\n'
        else:
            print("Operação falhou! o valor informado é inválido.")

    elif opcao == "2":
        valor = float(input("Informe quanto deseja sacar: "))
        
        excedeu_saldo = valor > saldo
        excedeu_limite = valor > limite
        excedeu_saque = numeros_saque >= LIMITE_SAQUES 
    
        if excedeu_saldo:
            print("Operação inválida! Saldo insuficiente.")
        
        elif excedeu_limite:
            print("Operação inválida! O valor do saque excedeu o limite.")

        elif excedeu_saque:
            print("Operação Inválida! Você excedeu o número de saques.")

        elif valor > 0:
            saldo -= valor
            extrato += f'Saque: R$ {valor:.2f}\n'
            numeros_saque += 1

        else:
            print("Operação Inválida! o valor informado é inválido.")

    elif opcao == "3":
        print("\n========== EXTRATO ==========")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f'\nSaldo: R$ {saldo:.2f}')
        print("==============================")

    elif opcao == "0":
        print("Você escolheu sair, Obrigado por adquirir nossos serviços!")
        break

    else:
        print("Opção Inválida, por favor selecione novamente a operação desejada.")