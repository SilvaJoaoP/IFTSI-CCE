import uuid
# Importa a nossa estrutura de lista, que é o coração do requisito do professor.
from estruturas.lista_encadeada import ListaEncadeada

class Nave:
    """Representa uma nave espacial e seu histórico de atendimentos."""
    def __init__(self, nome):
        # Garante uma identificação única, mesmo para naves com o mesmo nome.
        self.id = uuid.uuid4()
        self.nome = nome
        # Cada nave terá sua própria lista encadeada para o histórico.
        self.historico_solicitacoes = ListaEncadeada()

    def __str__(self):
        return f"Nave: {self.nome} (ID: {str(self.id)[:8]})"