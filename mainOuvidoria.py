from operacoesbd import *

conn = criarConexao ("127.0.0.1","root","12345","ouvidoria")

#Função para obter inteiro do user para o Menu principal
def opcaoUser():
    while True:
        try:
            opcao = int(input("Digite sua escolha: "))
            return opcao  
        except ValueError:
            print("Erro! Digite um número válido.")

#Dicionário com os tipos de manifestação (colunas do BD)
tiposManifestacao ={
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

#Função para listar manifestações
def listarManifestacoes(conn):
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
        print("Não há manifestações cadastradas!\n")

#Função para listar manifestações por tipo
def listarManifestacoesPorTipo(conn):
    while True:            
        #User informa o tipo a ser buscado
        userTipoInformado = escolherTipoManifestacao()
        if not userTipoInformado:
            print("Retornando ao menu...\n")
            break

        consultaManifestacoesTipo = "SELECT * FROM manifestacoes WHERE tipo = %s"
        dados =[userTipoInformado]
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

def criarNovaManifestacao(conn):
    print("Criar nova manifestação.")
    #User informa o tipo da nova manifestação:
    userTipoCriar = escolherTipoManifestacao()

    if not userTipoCriar:
        print("Retornando ao menu...\n")
        return

    #user informa autor, descrição e ouvidor da nova manifestação:
    while True:
        autor = input("Informe o autor(a) da manifestação: ")
        descricao = input("Informe a manifestação: ")
        ouvidor = input("Informe o ouvidor(a): ")
            
        if not autor.strip() or not descricao.strip() or not ouvidor.strip():
            print("Erro. Nenhum campo pode estar vazio!")
            return
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
        return

#Função para exibir a quantidade de manifestações
def exibirQuantidadeManifestacoes(conn):
        consultaQuantidadeManifestacoes = "SELECT COUNT(*) FROM manifestacoes"
        quantidadeManifestacoes = listarBancoDados(conn, consultaQuantidadeManifestacoes)
        print(f"A quantidade de manifestações cadastradas é de {quantidadeManifestacoes[0][0]}\n")

def pesquisaManifestacaoCodigo(conn):
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

        manifestacaoEncontrada = resultPesquisaCodigo[0]

        #feedback para o user
        print(f"\n Manifestação encontrada com sucesso!\n"
                f"Código: {manifestacaoEncontrada[0]}\n"
                f"Tipo: {manifestacaoEncontrada[3]}\n"
                f"Autor: {manifestacaoEncontrada[1]}\n"
                f"Descrição: {manifestacaoEncontrada[2]}\n"
                f"Ouvidor: {manifestacaoEncontrada[4]}\n")
        break

def excluirManifestacaoPorCodigo(conn):
    while True:
        #User informa código:
        try:
            codigoDelete = int(input("Informe o código da manifestação a ser removida (ou digite 0 para retornar ao Menu): "))
            if codigoDelete == 0:
                print("Retornando ao menu...")
                break
        except ValueError:
            print("Código informado é inválido. Tente Novamente.\n")
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
        elif confirmacao == "n":
            print("Operação cancelada.\n")
            break
        else:
            print("Entrada inválida. Digite 's' ou 'n'.\n")

