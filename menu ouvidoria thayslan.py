from operacoesbd import *
from mainOuvidoria import *

tiposManifestacao = {
    1: "Reclamação",
    2: "Elogio",
    3: "Melhoria"
    }

conn = criarConexao ("127.0.0.1","root","12345","ouvidoria")

#Menu principal
while True:
    print(
        "Bem-vindo à Ouvidoria Unifacisa! \n"
        "Opções: \n"
        "1) Listar manifestações cadastradas \n"
        "2) Listar manifestações por tipo\n"
        "3) Criar uma nova manifestação \n"
        "4) Exibir quantidade de manifestações\n"
        "5) Pesquisar manifestação por código\n"
        "6) Excluir manifestação por código\n"
        "7) Sair do sistema\n"
        )
    
    #Usuário digita a opção
    opcao = opcaoUser()

    #Listagem de manifestações cadastradas:
    if opcao == 1:       
        consultaListaManifestacoes = "SELECT * FROM manifestacoes"
        listaManifestacoes = listarBancoDados(conn,consultaListaManifestacoes)

        if len(listaManifestacoes) > 0:
            print("Lista de manifestações:")  
            for item in listaManifestacoes:
                print(f"Manifestação {item[0]}:\n"
                      f"- Descrição: {item[2]}\n"
                      f"- Tipo: {item[3]}\n"
                      )
        else:
            print("Não há manifestações cadastradas!.\n")
            continue
    
    #Listar manifestações por tipo:
    elif opcao == 2:
        while True:
            try:
                #User informa o tipo de manifestação que ele está buscando (Reclamação, Elogio, Melhoria)
                tipoInput = int(input("Digite 1 para Reclamações \n"
                                              "Digite 2 para Elogios \n"
                                              "Digite 3 para Melhorias \n"
                                              "Digite 4 para retornar ao menu \n"
                                              "Informe o tipo de manifestação que você está buscando: "))

                if tipoInput == 4:
                    print("Retornando ao menu...")
                    break

                userTipoInformado = tiposManifestacao.get(tipoInput)
                
                if not userTipoInformado:
                    print("Opção inválida. Tente novamente!")
                    continue
                       
            except ValueError:
                print("Erro! Número digitado é iválido!\n") 
                continue       
                                
            consultaManifestacoesTipo = "SELECT * FROM manifestacoes WHERE tipo = %s"
            dados = [userTipoInformado]
            listaManifestacoesTipo = listarBancoDados(conn,consultaManifestacoesTipo, dados)                   

            #Listagem das manifestações com as colunas "Manifestação" e "Descrição"
            if len(listaManifestacoesTipo) > 0:
                print("Lista de manifestações:")  
                for item in listaManifestacoesTipo:
                    print(f"Manifestação {item[0]}:\n"
                        f"- Descrição: {item[2]}\n"
                        )
            else:
                print("Não há manifestações cadastradas!.\n")
                continue
    
    #Criar uma nova manifestação:
    elif opcao == 3:
        print("Criar nova manifestação.")
        while True:
            try:
                #User informa o tipo de manifestação que ele quer incluir (Reclamação, Elogio, Melhoria) ou retornar ao menu
                tipoCriarInput = int(input("Digite 1 para Reclamações \n"
                                              "Digite 2 para Elogios \n"
                                              "Digite 3 para Melhorias \n"
                                              "Digite 4 para retornar ao menu \n"
                                              "Informe o tipo de manifestação que você quer adicionar: "))
                
                if tipoCriarInput == 4:
                    print("Retornando ao menu...")
                    break

                userTipoCriar = tiposManifestacao.get(tipoCriarInput)

                if not userTipoCriar:
                    print("Erro! Tente novamente!")
                    continue
                break

            except ValueError:
                print("Erro! Número digitado é iválido!\n")      

        #user informa autor, descrição e ouvidor da nova manifestação
        while True:
            autor = input("Informe o autor(a) da manifestação: ")
            descricao = input("Informe a manifestação: ")
            ouvidor = input("Informe o ouvidor(a): ")
            
            if not autor.strip() or not descricao.strip() or not ouvidor.strip():
                print("Erro. Nenhum campo pode estar vazio!")
                continue
            break

        consultaNovaManifestacao = "INSERT INTO manifestacoes (autor, descricao, tipo, ouvidor) VALUES (%s, %s, %s, %s)"
        dados = [autor, descricao, userTipoCriar, ouvidor]
        result = insertNoBancoDados(conn, consultaNovaManifestacao, dados)
        
        #feedback para o user
        if result:
            print(f"Manifestação cadastrada com sucesso!\n"
                  f"Código: {result}\n"
                  f"Autor(a): {autor}\n"
                  f"Descrição: {descricao}\n")
        else:
            print("Erro ao adicionar a manifestação. Por favor tente novamente.")
            continue

    elif opcao == 4:

        consultaQuantidadeManifestacoes = "SELECT COUNT(*) FROM manifestacoes"
        quantidadeManifestacoes = listarBancoDados(conn, consultaQuantidadeManifestacoes)
        print(f"A quantidade de manifestações cadastradas é de {quantidadeManifestacoes[0][0]}\n")

    #Pesquisar manifestação por código
    elif opcao == 5:       
        while True:
            try:
                codigoPesquisa = int(input("Informe o código a ser buscado: "))
            except ValueError:
                print("Código informado é inválido. Tente Novamente\n")
                continue
            
            consultaCodigo = "SELECT * FROM manifestacoes WHERE codigo = %s"
            dados = [codigoPesquisa]
            resultPesquisaCodigo = listarBancoDados (conn, consultaCodigo, dados)

            if not resultPesquisaCodigo:
                print("Manifestação não encontrada! Verifique o código e tente novamente.\n")
                continue

            manifestacaoEncontrada = resultPesquisaCodigo [0]

            #feedback para o user
            print(f"\n Manifestação encontrada com sucesso!\n"
                  f"Código: {manifestacaoEncontrada[0]}\n"
                  f"Tipo: {manifestacaoEncontrada[3]}\n"
                  f"Autor: {manifestacaoEncontrada[1]}\n"
                  f"Descrição: {manifestacaoEncontrada[2]}\n"
                  f"Ouvidor: {manifestacaoEncontrada[4]}\n")
            break
    
    #Excluir manifestação por código
    elif opcao == 6:
        while True:
            #User informa código:
            try:
                codigoDelete = int(input("Informe o código da manifestação a ser removida: "))
            except ValueError:
                print("Código informado é inválido. Tente Novamente\n")
                continue
            
            #Consulta se código existe no BD:
            consultaCodigoExiste = "SELECT * FROM manifestacoes WHERE codigo = %s"
            result = listarBancoDados(conn, consultaCodigoExiste, [codigoDelete])

            if not result:
                print ("Código não encontrado! Verifique e tente novamente.")
                continue
            
            #Confirma a operação com o user:
            manifestacao = result [0]
            confirmacao = input(f"Código: {manifestacao [0]}\n"
                                f"Autor: {manifestacao [1]}\n"
                                f"Descrição: {manifestacao [2]}\n"
                                "Tem certeza que deseja excluir a manifestação acima?\n"
                                "Sim (digite: s)\n"
                                "Não (digite: n)\n")
            confirmacao = confirmacao.lower().strip()
            #Exclui manifestação do BD:
            if confirmacao == "s":
                
                consultaDelete = "DELETE FROM manifestacoes WHERE codigo = %s"
                linhasAlteradas = excluirBancoDados(conn, consultaDelete, [codigoDelete])
            
                #Feedback para o user
                if linhasAlteradas == 0:
                    print("Erro! Tente novamente.")
                else:
                    print("Manifestação excluída com sucesso!")
                    break        
    
    elif opcao == 7:
        print("Agradecemos à preferência!")
        break

    encerrarConexao(conn)
