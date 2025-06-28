from .no import No # O '.' antes de 'no' indica que estamos importando do mesmo pacote/diretório

class ListaEncadeada:
    """Implementação de uma Lista Encadeada."""
    def __init__(self):
        self.head = None # A cabeça da lista, inicialmente vazia (None)
        self._size = 0

    def is_empty(self):
        """Verifica se a lista está vazia."""
        return self.head is None

    def append(self, elemento):
        """Adiciona um elemento no final da lista."""
        # Se a lista estiver vazia, o novo nó é a cabeça
        if self.is_empty():
            self.head = No(elemento)
        else:
            # Percorre a lista até encontrar o último nó
            ponteiro = self.head
            while ponteiro.proximo:
                ponteiro = ponteiro.proximo
            # Adiciona o novo nó após o último
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

    def __len__(self):
        """Retorna o tamanho da lista."""
        return self._size

    def __str__(self):
        """Retorna uma representação em string da lista."""
        if self.is_empty():
            return "[]"
        
        string_lista = "["
        ponteiro = self.head
        while ponteiro:
            string_lista += str(ponteiro.dado)
            if ponteiro.proximo:
                string_lista += ", "
            ponteiro = ponteiro.proximo
        string_lista += "]"
        return string_lista