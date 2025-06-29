# Importa a classe principal da nossa interface gráfica
from interface_grafica import App

# O ponto de entrada do nosso programa
if __name__ == "__main__":
    """
    Este é o único código executado quando você roda "python main.py".
    Sua única responsabilidade é:
    1. Criar uma instância da nossa aplicação gráfica (a janela principal).
    2. Iniciar o loop principal do Tkinter (app.mainloop()), que desenha a janela
       na tela e fica aguardando as interações do usuário (cliques, digitação, etc.).
    """
    
    # Cria a aplicação
    app = App()
    
    # Inicia e mantém a aplicação rodando
    app.mainloop()