from estruturas.lista_encadeada import ListaEncadeada
from modelos.solicitacao import Solicitacao
from modelos.nave import Nave

class CentroDeControle:
    """Gerencia o fluxo de chamadas técnicas espaciais."""
    def __init__(self):
        print("Centro de Controle Espacial inicializado.")
        # Estruturas de Fila
        self.fila_triagem_emergencia = ListaEncadeada()
        self.fila_triagem_alta = ListaEncadeada()
        self.fila_triagem_normal = ListaEncadeada()
        self.filas_especialistas = {
            "Comunicações": ListaEncadeada(), "Energia": ListaEncadeada(),
            "Navegação": ListaEncadeada(), "Suporte à Vida": ListaEncadeada()
        }
        self.naves_cadastradas = {}

        # NOVO: Estruturas de dados para as estatísticas
        self.stats_solicitacoes_criadas = 0
        self.stats_atendimentos_por_prioridade = {'EMERGENCIA': 0, 'ALTA': 0, 'NORMAL': 0}
        self.stats_atendimentos_por_especialista = {'Comunicações': 0, 'Energia': 0, 'Navegação': 0, 'Suporte à Vida': 0}
        self.stats_triagens_por_operador = {'Operador-01': 0} # Preparado para múltiplos operadores no futuro

    # ALTERADO: Agora também conta as solicitações criadas.
    def adicionar_solicitacao(self, solicitacao):
        self.stats_solicitacoes_criadas += 1 # Contabiliza a criação
        if solicitacao.prioridade == "EMERGENCIA":
            self.fila_triagem_emergencia.prepend(solicitacao)
        elif solicitacao.prioridade == "ALTA":
            self.fila_triagem_alta.append(solicitacao)
        elif solicitacao.prioridade == "NORMAL":
            self.fila_triagem_normal.append(solicitacao)

    def proxima_solicitacao_para_triagem(self):
        # (Este método não precisa de alterações)
        if not self.fila_triagem_emergencia.is_empty():
            return self.fila_triagem_emergencia.remove_first()
        elif not self.fila_triagem_alta.is_empty():
            return self.fila_triagem_alta.remove_first()
        elif not self.fila_triagem_normal.is_empty():
            return self.fila_triagem_normal.remove_first()
        else:
            return None

    # NOVO: Método dedicado para contabilizar o trabalho do operador.
    def contabilizar_triagem(self, nome_operador):
        if nome_operador in self.stats_triagens_por_operador:
            self.stats_triagens_por_operador[nome_operador] += 1
        else:
            # Caso um novo operador seja adicionado no futuro
            self.stats_triagens_por_operador[nome_operador] = 1

    def enviar_para_especialista(self, solicitacao, especialidade):
        # (Este método não precisa de alterações)
        if especialidade in self.filas_especialistas:
            fila_do_especialista = self.filas_especialistas[especialidade]
            solicitacao.especialista_responsavel = especialidade
            fila_do_especialista.append(solicitacao)
            print(f"Solicitação da nave '{solicitacao.nome_nave}' enviada para o especialista em '{especialidade}'.")

    # ALTERADO: Agora também atualiza todas as estatísticas de finalização.
    def arquivar_solicitacao_na_nave(self, solicitacao_finalizada):
        nome_nave = solicitacao_finalizada.nome_nave
        if nome_nave not in self.naves_cadastradas:
            self.naves_cadastradas[nome_nave] = Nave(nome=nome_nave)
        
        nave_para_arquivar = self.naves_cadastradas[nome_nave]
        nave_para_arquivar.historico_solicitacoes.append(solicitacao_finalizada)
        print(f"Atendimento arquivado com sucesso no histórico da nave '{nome_nave}'.")

        # NOVO: Atualizando os contadores de estatísticas
        # 1. Contar por prioridade
        prioridade = solicitacao_finalizada.prioridade
        if prioridade in self.stats_atendimentos_por_prioridade:
            self.stats_atendimentos_por_prioridade[prioridade] += 1

        # 2. Contar por especialista
        especialista = solicitacao_finalizada.especialista_responsavel
        if especialista in self.stats_atendimentos_por_especialista:
            self.stats_atendimentos_por_especialista[especialista] += 1

    def consultar_historico_nave(self, nome_nave):
        return self.naves_cadastradas.get(nome_nave, None)

    # NOVO: Método para calcular a nave com mais chamados sob demanda.
    def get_nave_com_mais_chamados(self):
        if not self.naves_cadastradas:
            return "Nenhuma nave com histórico.", 0

        nave_mais_chamada = None
        max_chamados = -1

        for nome_nave, obj_nave in self.naves_cadastradas.items():
            num_chamados = len(obj_nave.historico_solicitacoes)
            if num_chamados > max_chamados:
                max_chamados = num_chamados
                nave_mais_chamada = nome_nave
        
        return nave_mais_chamada, max_chamados