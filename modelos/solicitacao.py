# Módulo: modelos/solicitacao.py (Versão Corrigida)

import uuid
from datetime import datetime

class Solicitacao:
    """Representa uma solicitação de atendimento técnico."""
    def __init__(self, prioridade, descricao_inicial):
        # NOVO: Validação para garantir que os dados não sejam vazios na criação
        if not prioridade or not descricao_inicial.strip():
            raise ValueError("Prioridade e descrição inicial são obrigatórias.")

        self.id = uuid.uuid4()
        self.prioridade = prioridade
        self.timestamp_criacao = datetime.now()
        self.descricao_ocorrido = descricao_inicial

        # Dados a serem preenchidos na triagem
        self.nome_nave = None
        self.codigo_missao = None
        self.setor_orbital = None
        self.tripulacao_humana = None
        self.operador_triagem = None

        # Dados do atendimento especializado
        self.especialista_responsavel = None
        self.status = "AGUARDANDO_TRIAGEM"

    def registrar_triagem(self, nome_nave, codigo_missao, setor_orbital, descricao, tripulacao, operador):
        """Preenche os dados da solicitação após a triagem."""
        # NOVO: Validação para garantir que os dados da triagem não sejam vazios
        campos_obrigatorios = {
            "Nome da nave": nome_nave,
            "Código da missão": codigo_missao,
            "Setor orbital": setor_orbital,
            "Descrição": descricao,
            "Operador": operador
        }
        for nome_campo, valor_campo in campos_obrigatorios.items():
            if not valor_campo or not str(valor_campo).strip():
                raise ValueError(f"A informação '{nome_campo}' é obrigatória na triagem.")

        self.nome_nave = nome_nave
        self.codigo_missao = codigo_missao
        self.setor_orbital = setor_orbital
        self.descricao_ocorrido = descricao
        self.tripulacao_humana = tripulacao
        self.operador_triagem = operador
        self.status = "AGUARDANDO_ESPECIALISTA"

    def __str__(self):
        """Representação em string para facilitar a visualização."""
        if self.status == "AGUARDANDO_TRIAGEM":
            return f"ID: {str(self.id)[:8]} | Prioridade: {self.prioridade} | Status: {self.status}"
        else:
            return (f"Nave: {self.nome_nave} | Prioridade: {self.prioridade} | "
                    f"Descrição: {self.descricao_ocorrido[:30]}... | Status: {self.status}")