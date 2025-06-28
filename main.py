from sistema import CentroDeControle
from modelos.solicitacao import Solicitacao
import os

def limpar_tela(): os.system('cls' if os.name == 'nt' else 'clear')
def obter_input_nao_vazio(prompt):
    while True:
        valor = input(prompt).strip();
        if valor: return valor
        else: print(">> Erro: Esta informação não pode ser deixada em branco.")
def obter_input_com_letras(prompt):
    while True:
        valor = obter_input_nao_vazio(prompt);
        if any(c.isalpha() for c in valor): return valor
        else: print(">> Erro: A informação inserida deve conter pelo menos uma letra.")
def obter_input_alfanumerico(prompt):
    while True:
        valor = obter_input_nao_vazio(prompt);
        if any(c.isalnum() for c in valor): return valor
        else: print(">> Erro: A informação inserida deve conter letras ou números.")

def exibir_menu_principal():
    print("\n--- Centro de Controle Espacial: Menu Principal ---")
    print("[1] Registrar Nova Solicitação")
    print("[2] Iniciar Triagem de Chamado (Operador)")
    print("[3] Atender Chamado (Especialista)")
    print("[4] Visualizar Filas e Status")
    print("[5] Consultar Histórico de Nave")
    print("[6] Exibir Estatísticas e Relatórios") # NOVO
    print("[0] Sair do Sistema")
    return input("Escolha uma opção: ")

def main():
    centro_de_controle = CentroDeControle()
    while True:
        limpar_tela()
        opcao = exibir_menu_principal()

        if opcao == '1':
            # (sem alterações)
            print("\n-- Nova Solicitação --")
            while True:
                print("Prioridades: [1] EMERGENCIA, [2] ALTA, [3] NORMAL")
                p_map = {"1": "EMERGENCIA", "2": "ALTA", "3": "NORMAL"}
                p_escolha = input("Digite o número da prioridade: ");
                if p_escolha in p_map: prioridade = p_map[p_escolha]; break
                else: print(">> Erro: Opção de prioridade inválida.")
            descricao = obter_input_com_letras("Descrição inicial do problema: ")
            nova_solicitacao = Solicitacao(prioridade, descricao)
            centro_de_controle.adicionar_solicitacao(nova_solicitacao)
            input("\nSolicitação registrada com sucesso! Pressione Enter para continuar...")

        elif opcao == '2':
            # ALTERADO: Adiciona a chamada para contabilizar a triagem.
            print("\n-- Painel de Triagem do Operador --")
            solicitacao_para_triar = centro_de_controle.proxima_solicitacao_para_triagem()
            if solicitacao_para_triar:
                print(f"Atendendo solicitação ID: {str(solicitacao_para_triar.id)[:8]}")
                nome_nave = obter_input_com_letras("Nome da Nave: ")
                # ... (restante da coleta de dados não muda)
                codigo_missao = obter_input_alfanumerico("Código da Missão: ")
                setor_orbital = obter_input_nao_vazio("Setor Orbital: ")
                desc_completa = obter_input_com_letras("Descrição completa da ocorrência: ")
                while True:
                    tripulacao_str = input("Há tripulação humana envolvida (S/N)? ").upper()
                    if tripulacao_str in ['S', 'N']: tripulacao = (tripulacao_str == 'S'); break
                    else: print(">> Erro: Responda apenas com 'S' para Sim ou 'N' para Não.")
                while True:
                    print("\nEspecialidades disponíveis:")
                    esp_map = {str(i): esp for i, esp in enumerate(centro_de_controle.filas_especialistas.keys(), 1)}
                    for i, esp in esp_map.items(): print(f"[{i}] {esp}")
                    esp_escolha = input("Encaminhar para qual especialista? ")
                    especialidade = esp_map.get(esp_escolha)
                    if especialidade:
                        operador_atual = "Operador-01" # Hardcoded por enquanto
                        solicitacao_para_triar.registrar_triagem(nome_nave, codigo_missao, setor_orbital, desc_completa, tripulacao, operador_atual)
                        centro_de_controle.enviar_para_especialista(solicitacao_para_triar, especialidade)
                        # AQUI ESTÁ A MÁGICA: Contabilizando o trabalho do operador
                        centro_de_controle.contabilizar_triagem(operador_atual)
                        print(f"\nTriagem processada por {operador_atual}.")
                        break
                    else:
                        print(">> Erro: Opção de especialista inválida.")
            else:
                print("Nenhuma solicitação aguardando na fila de triagem.")
            input("\nPressione Enter para continuar...")

        # ... (Opções 3, 4, 5 não mudam)
        elif opcao == '3':
            print("\n-- Painel do Especialista --")
            while True:
                print("Selecione a sua especialidade para ver a fila de atendimento:")
                esp_map = {str(i): esp for i, esp in enumerate(centro_de_controle.filas_especialistas.keys(), 1)}
                for i, esp in esp_map.items(): print(f"[{i}] {esp} ({len(centro_de_controle.filas_especialistas[esp])} chamados)")
                esp_escolha = input("Sua especialidade (ou '0' para voltar): ")
                if esp_escolha == '0': break
                especialidade = esp_map.get(esp_escolha)
                if especialidade:
                    if not centro_de_controle.filas_especialistas[especialidade].is_empty():
                        chamado_atendido = centro_de_controle.filas_especialistas[especialidade].remove_first()
                        chamado_atendido.status = "FINALIZADA"
                        print(f"\nChamado da nave '{chamado_atendido.nome_nave}' foi atendido e finalizado com sucesso!")
                        centro_de_controle.arquivar_solicitacao_na_nave(chamado_atendido)
                    else: print("\nNão há chamados nesta fila de atendimento.")
                    break
                else: print("\n>> Erro: Especialidade inválida.")
            input("\nPressione Enter para continuar...")
        elif opcao == '4':
            print("\n-- Status Atual das Filas --")
            print("\n** FILAS DE TRIAGEM **"); print(f"EMERGÊNCIA: {len(centro_de_controle.fila_triagem_emergencia)} chamados"); print(f"ALTA: {len(centro_de_controle.fila_triagem_alta)} chamados"); print(f"NORMAL: {len(centro_de_controle.fila_triagem_normal)} chamados")
            print("\n** FILAS DE ATENDIMENTO (ESPECIALISTAS) **")
            for esp, fila in centro_de_controle.filas_especialistas.items(): print(f"{esp}: {len(fila)} chamados")
            input("\nPressione Enter para continuar...")
        elif opcao == '5':
            print("\n-- Consulta de Histórico da Nave --")
            nome_da_nave = obter_input_com_letras("Digite o nome da nave para consultar: ")
            nave_encontrada = centro_de_controle.consultar_historico_nave(nome_da_nave)
            if nave_encontrada:
                print(f"\n{'='*40}\nHistórico de Atendimentos para a {nave_encontrada}\n{'='*40}")
                if nave_encontrada.historico_solicitacoes.is_empty(): print("Nenhum atendimento registrado.")
                else: print(nave_encontrada.historico_solicitacoes)
                print("="*40)
            else: print(f"\nNenhuma nave com o nome '{nome_da_nave}' foi encontrada no sistema.")
            input("\nPressione Enter para voltar ao menu...")

        # NOVO: Lógica para a nova tela de estatísticas
        elif opcao == '6':
            print("\n--- Estatísticas e Relatórios da Sessão ---")
            print("="*45)
            # Total de solicitações criadas
            print(f"Total de Solicitações Criadas: {centro_de_controle.stats_solicitacoes_criadas}")
            print("-"*45)
            
            # Atendimentos finalizados por prioridade
            print("Atendimentos Finalizados por Prioridade:")
            for prioridade, total in centro_de_controle.stats_atendimentos_por_prioridade.items():
                print(f"  - {prioridade.title()}: {total}")
            print("-"*45)

            # Atendimentos finalizados por especialista
            print("Atendimentos Finalizados por Especialista:")
            for especialista, total in centro_de_controle.stats_atendimentos_por_especialista.items():
                print(f"  - {especialista}: {total}")
            print("-"*45)
            
            # Triagens processadas por operador
            print("Triagens Processadas por Operador:")
            for operador, total in centro_de_controle.stats_triagens_por_operador.items():
                print(f"  - {operador}: {total}")
            print("-"*45)
            
            # Nave com maior número de chamados
            nave, num_chamados = centro_de_controle.get_nave_com_mais_chamados()
            print("Nave com Maior Número de Chamados:")
            print(f"  - {nave} ({num_chamados} chamados)")
            print("="*45)

            input("\nPressione Enter para voltar ao menu...")

        elif opcao == '0':
            print("Encerrando sistema. Até logo, comandante!"); break
        else:
            input(">> Opção inválida. Pressione Enter para tentar novamente...")

if __name__ == "__main__":
    main()