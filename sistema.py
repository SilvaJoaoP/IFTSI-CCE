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

        # Estruturas de dados para as estatísticas
        self.stats_solicitacoes_criadas = 0
        self.stats_atendimentos_por_prioridade = {'EMERGENCIA': 0, 'ALTA': 0, 'NORMAL': 0}
        self.stats_atendimentos_por_especialista = {'Comunicações': 0, 'Energia': 0, 'Navegação': 0, 'Suporte à Vida': 0}
        self.stats_triagens_por_operador = {'Operador-GUI': 0, 'Operador-01': 0}

    def adicionar_solicitacao(self, solicitacao):
        """Adiciona uma nova solicitação à fila de triagem apropriada."""
        self.stats_solicitacoes_criadas += 1
        if solicitacao.prioridade == "EMERGENCIA":
            # CORREÇÃO: Alterado de prepend() para append() para manter a ordem de chegada (FIFO).
            self.fila_triagem_emergencia.append(solicitacao)
        elif solicitacao.prioridade == "ALTA":
            self.fila_triagem_alta.append(solicitacao)
        elif solicitacao.prioridade == "NORMAL":
            self.fila_triagem_normal.append(solicitacao)
    
    def get_todas_solicitacoes_para_triagem(self):
        """
        Retorna uma lista única com todas as solicitações das filas de triagem,
        ordenadas por prioridade: Emergência, Alta, Normal.
        """
        todas = []
        for solicitacao in self.fila_triagem_emergencia:
            todas.append(solicitacao)
        for solicitacao in self.fila_triagem_alta:
            todas.append(solicitacao)
        for solicitacao in self.fila_triagem_normal:
            todas.append(solicitacao)
        return todas

    def remover_solicitacao_da_triagem(self, solicitacao_a_remover):
        """
        Busca uma solicitação específica em todas as filas de triagem e a remove.
        Utiliza o método 'remover_elemento' da ListaEncadeada.
        """
        try:
            self.fila_triagem_emergencia.remover_elemento(solicitacao_a_remover)
            return True
        except ValueError:
            pass 

        try:
            self.fila_triagem_alta.remover_elemento(solicitacao_a_remover)
            return True
        except ValueError:
            pass

        try:
            self.fila_triagem_normal.remover_elemento(solicitacao_a_remover)
            return True
        except ValueError:
            return False

    def contabilizar_triagem(self, nome_operador):
        """Contabiliza o trabalho do operador de triagem."""
        if nome_operador in self.stats_triagens_por_operador:
            self.stats_triagens_por_operador[nome_operador] += 1
        else:
            self.stats_triagens_por_operador[nome_operador] = 1

    def enviar_para_especialista(self, solicitacao, especialidade):
        """Envia uma solicitação para a fila do especialista correspondente."""
        if especialidade in self.filas_especialistas:
            fila_do_especialista = self.filas_especialistas[especialidade]
            solicitacao.especialista_responsavel = especialidade
            fila_do_especialista.append(solicitacao)
            print(f"Solicitação da nave '{solicitacao.nome_nave}' enviada para o especialista em '{especialidade}'.")

    def arquivar_solicitacao_na_nave(self, solicitacao_finalizada):
        """Arquiva uma solicitação finalizada no histórico da nave e atualiza as estatísticas."""
        nome_nave = solicitacao_finalizada.nome_nave
        if nome_nave not in self.naves_cadastradas:
            self.naves_cadastradas[nome_nave] = Nave(nome=nome_nave)
        
        nave_para_arquivar = self.naves_cadastradas[nome_nave]
        nave_para_arquivar.historico_solicitacoes.append(solicitacao_finalizada)
        print(f"Atendimento arquivado com sucesso no histórico da nave '{nome_nave}'.")

        prioridade = solicitacao_finalizada.prioridade
        if prioridade in self.stats_atendimentos_por_prioridade:
            self.stats_atendimentos_por_prioridade[prioridade] += 1

        especialista = solicitacao_finalizada.especialista_responsavel
        if especialista in self.stats_atendimentos_por_especialista:
            self.stats_atendimentos_por_especialista[especialista] += 1

    def consultar_historico_nave(self, nome_nave):
        """Consulta o histórico de uma nave específica."""
        return self.naves_cadastradas.get(nome_nave, None)

    def get_nave_com_mais_chamados(self):
        """Retorna a nave com o maior número de chamados registrados."""
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