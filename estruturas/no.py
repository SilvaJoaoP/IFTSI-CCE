class No:
    """Representa um nó em uma lista encadeada."""
    def __init__(self, dado):
        self.dado = dado
        self.proximo = None

    def __str__(self):
        return str(self.dado)