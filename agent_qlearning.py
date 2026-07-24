import random
from utils import calcular_distancia, encontrar_alvo_com_distancia, obter_vetor

class AgenteQLearning:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=1.0, epsilon_min=0.01, epsilon_decay=0.995):
        self.q_table = {}
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.acoes = ['w', 's', 'a', 'd', 'e', 'r']

        self.estado_anterior = None
        self.acao_anterior = None
        self.distancia_anterior = float('inf')

    def observar_estado(self, env):
        tanque = "Com_Agua" if env.agua_atual > 0 else "Vazio"

        # Usa a função do utils que retorna distância simultaneamente
        if tanque == "Com_Agua":
            alvo_pos, dist = encontrar_alvo_com_distancia(env.grid, env.drone_pos, env.tamanho, [2, 4])
        else:
            alvo_pos, dist = encontrar_alvo_com_distancia(env.grid, env.drone_pos, env.tamanho, [3])

        dy, dx = obter_vetor(env.drone_pos, alvo_pos)
        return (tanque, dy, dx), dist

    def inicializar_estado(self, estado):
        if estado not in self.q_table:
            self.q_table[estado] = {a: 0.0 for a in self.acoes}

    def agir(self, env):
        estado_atual, dist_atual = self.observar_estado(env)
        self.inicializar_estado(estado_atual)

        if self.estado_anterior is not None:
            tanque_antigo, dy_antigo, dx_antigo = self.estado_anterior
            recompensa = 0

            if self.acao_anterior == 'e':
                if tanque_antigo == "Com_Agua" and dy_antigo == 0 and dx_antigo == 0:
                    recompensa = 100
                else:
                    recompensa = -10

            elif self.acao_anterior == 'r':
                if tanque_antigo == "Vazio" and dy_antigo == 0 and dx_antigo == 0:
                    recompensa = 100
                else:
                    recompensa = -10

            else:
                if dist_atual < self.distancia_anterior:
                    recompensa = 10
                else:
                    recompensa = -10

            q_antigo = self.q_table[self.estado_anterior][self.acao_anterior]
            max_q_novo = max(self.q_table[estado_atual].values())
            novo_q = q_antigo + self.alpha * (recompensa + self.gamma * max_q_novo - q_antigo)
            self.q_table[self.estado_anterior][self.acao_anterior] = novo_q

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

        if estado_atual[1] == 0 and estado_atual[2] == 0 and estado_atual[0] == "Com_Agua" and dist_atual == float('inf'):
            self.estado_anterior = None
            return 'aguardar'

        if random.random() < self.epsilon:
            acao_escolhida = random.choice(self.acoes)
        else:
            acao_escolhida = max(self.q_table[estado_atual], key=self.q_table[estado_atual].get)

        self.estado_anterior = estado_atual
        self.acao_anterior = acao_escolhida
        self.distancia_anterior = dist_atual

        return acao_escolhida