from operacoesbd import *
from mainOuvidoria import *

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

    if opcao == 1:
        listarManifestacoes ()
        continue
    
    elif opcao == 2:
        listarManifestacoesPorCodigo()
        continue
    
    elif opcao == 3:
        criarManifestacao()
        continue
    
    elif opcao == 4:
        quantidadeManifestacoes()
        continue

    elif opcao == 5:
        pesquisarManifestacaoCodigo()
        continue

    elif opcao == 6:
        excluirManifestacao()
        continue
    
    elif opcao == 7:
        print("Agradecemos à preferência!")
        break

    encerrarConexao(conn)
