#Função para obter inteiro do user para o Menu principal
def opcaoUser():
    while True:
        try:
            opcao = int(input("Digite sua escolha: "))
            return opcao  
        except ValueError:
            print("Erro! Digite um número válido.")

#Dicionário com os tipos de manifestação (colunas do BD)
tiposManifestacao = {
    1: "Reclamação",
    2: "Elogio",
    3: "Melhoria"
    }

#Função para obter do user o tipo de manifestação que ele está buscando (Reclamação, Elogio, Melhoria) ou redirecioná-lo ao Menu Principal
def escolherTipoManifestacao():
    while True:
        try:
            tipoInput = int(input(
                                    "Digite 1 para Reclamações \n"
                                    "Digite 2 para Elogios \n"
                                    "Digite 3 para Melhorias \n"
                                    "Digite 4 para retornar ao menu \n"
                                    "Informe o tipo de manifestação que você está buscando: "
                                    ))
            if tipoInput == 4:
                return None
            
            userTipoInformado = tiposManifestacao.get(tipoInput)

            if userTipoInformado:
                return userTipoInformado
            else:
                print("Opção inválida. Tente novamente!\n")
        except ValueError:
            print("Entrada inválida. Digite um número de 1 a 4.\n")