from .no import No

class ListaEncadeada:
    """Implementação de uma Lista Encadeada."""
    def __init__(self):
        self.head = None
        self._size = 0

    def is_empty(self):
        """Verifica se a lista está vazia."""
        return self.head is None

    def append(self, elemento):
        """Adiciona um elemento no final da lista."""
        if self.is_empty():
            self.head = No(elemento)
        else:
            ponteiro = self.head
            while ponteiro.proximo:
                ponteiro = ponteiro.proximo
            ponteiro.proximo = No(elemento)
        self._size += 1

    def prepend(self, elemento):
        """Adiciona um elemento no início da lista."""
        novo_no = No(elemento)
        novo_no.proximo = self.head
        self.head = novo_no
        self._size += 1

    def remove_first(self):
        """Remove e retorna o primeiro elemento da lista."""
        if self.is_empty():
            raise IndexError("A lista está vazia. Impossível remover.")
        
        elemento_removido = self.head.dado
        self.head = self.head.proximo
        self._size -= 1
        return elemento_removido

    def buscar(self, valor_buscado):
        """Busca um elemento na lista e retorna o nó inteiro."""
        ponteiro = self.head
        while ponteiro:
            if ponteiro.dado == valor_buscado:
                return ponteiro
            ponteiro = ponteiro.proximo
        return None

    def remover_elemento(self, elemento):
        """Remove um elemento específico da lista."""
        if self.is_empty():
            raise ValueError("A lista está vazia.")

        if self.head.dado == elemento:
            self.remove_first()
            return True

        anterior = self.head
        ponteiro = self.head.proximo
        while ponteiro:
            if ponteiro.dado == elemento:
                anterior.proximo = ponteiro.proximo
                self._size -= 1
                return True
            anterior = ponteiro
            ponteiro = ponteiro.proximo
        
        raise ValueError(f"Elemento {elemento} não encontrado na lista.")

    # MÉTODO CORRIGIDO: Agora ordena por prioridade E por tempo de criação.
    def inserir_ordenado_por_prioridade_e_tempo(self, solicitacao):
        """
        Insere uma solicitação na lista mantendo a ordem de prioridade e,
        dentro da mesma prioridade, a ordem de criação (mais antigo primeiro).
        EMERGENCIA (0) > ALTA (1) > NORMAL (2).
        """
        prioridade_map = {"EMERGENCIA": 0, "ALTA": 1, "NORMAL": 2}
        nova_prioridade_valor = prioridade_map.get(solicitacao.prioridade)
        novo_timestamp = solicitacao.timestamp_criacao
        novo_no = No(solicitacao)

        # Caso 1: A lista está vazia ou o novo nó deve ser a nova cabeça.
        if self.is_empty() or \
           prioridade_map.get(self.head.dado.prioridade) > nova_prioridade_valor or \
           (prioridade_map.get(self.head.dado.prioridade) == nova_prioridade_valor and self.head.dado.timestamp_criacao > novo_timestamp):
            novo_no.proximo = self.head
            self.head = novo_no
            self._size += 1
            return

        # Caso 2: Percorre a lista para encontrar o local de inserção.
        ponteiro = self.head
        while ponteiro.proximo:
            proximo_prioridade_valor = prioridade_map.get(ponteiro.proximo.dado.prioridade)
            
            # Se a prioridade do próximo nó for menor (valor numérico maior), encontramos o ponto de inserção.
            if proximo_prioridade_valor > nova_prioridade_valor:
                break
                
            # Se a prioridade for a mesma, comparamos pelo timestamp.
            # Se o próximo for mais recente (timestamp maior), encontramos o ponto de inserção.
            if proximo_prioridade_valor == nova_prioridade_valor and ponteiro.proximo.dado.timestamp_criacao > novo_timestamp:
                break
                
            ponteiro = ponteiro.proximo
        
        # Insere o novo nó após o ponteiro atual.
        novo_no.proximo = ponteiro.proximo
        ponteiro.proximo = novo_no
        self._size += 1


    def __len__(self):
        """Retorna o tamanho da lista."""
        return self._size
    
    def __iter__(self):
        ponteiro = self.head
        while ponteiro:
            yield ponteiro.dado
            ponteiro = ponteiro.proximo

    def __str__(self):
        """Retorna uma representação em string da lista."""
        return "[" + ", ".join(str(dado) for dado in self) + "]"
