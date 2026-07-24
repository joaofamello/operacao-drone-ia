import random

class AgenteQLearning:
    def __init__(self, alpha=0.1, gamma=0.95, epsilon=1.0, epsilon_min=0.01, epsilon_decay=0.995):
        # tabela Q, onde o conhecimento fica armazenado
        self.q_table = {}

        # hiperparâmetros do aprendizado
        self.alpha = alpha                  # taxa de aprendizado
        self.gamma = gamma                  # fator de desconto (foco no futuro)
        self.epsilon = epsilon              # taxa de exploração inicial (1.0 = 100% aleatório)
        self.epsilon_min = epsilon_min      # mínimo de aleatoriedade
        self.epsilon_decay = epsilon_decay  # velocidade que ele deixa de ser aleatório

        self.acoes = ['w', 's', 'a', 'd', 'e', 'r']

        # Memória de curto prazo para a Equação de Bellman
        self.estado_anterior = None
        self.acao_anterior = None