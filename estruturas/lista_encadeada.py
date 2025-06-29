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

    # NOVO: Método para buscar um elemento. Retorna o nó se encontrar.
    def buscar(self, valor_buscado):
        """Busca um elemento na lista e retorna o nó inteiro."""
        ponteiro = self.head
        while ponteiro:
            if ponteiro.dado == valor_buscado:
                return ponteiro
            ponteiro = ponteiro.proximo
        return None # Retorna None se não encontrar

    # NOVO: Método para remover um elemento específico.
    def remover_elemento(self, elemento):
        """Remove um elemento específico da lista."""
        if self.is_empty():
            raise ValueError("A lista está vazia.")

        # Caso o elemento a ser removido seja a cabeça da lista
        if self.head.dado == elemento:
            self.remove_first()
            return True

        # Percorre a lista para encontrar o elemento
        anterior = self.head
        ponteiro = self.head.proximo
        while ponteiro:
            if ponteiro.dado == elemento:
                # Encontrou o elemento, remove a referência a ele
                anterior.proximo = ponteiro.proximo
                self._size -= 1
                return True
            anterior = ponteiro
            ponteiro = ponteiro.proximo
        
        # Se chegou aqui, o elemento não foi encontrado
        raise ValueError(f"Elemento {elemento} não encontrado na lista.")

    def __len__(self):
        """Retorna o tamanho da lista."""
        return self._size
    
    # NOVO: Um iterador para facilitar o uso em laços for (útil na GUI)
    def __iter__(self):
        ponteiro = self.head
        while ponteiro:
            yield ponteiro.dado
            ponteiro = ponteiro.proximo

    def __str__(self):
        """Retorna uma representação em string da lista."""
        # Usa o iterador para criar a string de forma mais elegante
        return "[" + ", ".join(str(dado) for dado in self) + "]"