import random


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

    def calcular_distancia(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def encontrar_alvo(self, grid, drone_pos, tamanho, tipos_alvo):
        alvo = None
        menor_dist = float('inf')
        for i in range(tamanho):
            for j in range(tamanho):
                if grid[i][j] in tipos_alvo:
                    dist = self.calcular_distancia(drone_pos, [i, j])
                    if dist < menor_dist:
                        menor_dist = dist
                        alvo = [i, j]
        return alvo, menor_dist

    def obter_vetor(self, drone_pos, alvo_pos):
        """Retorna a direção como um vetor simples (-1, 0 ou 1) nos eixos Y e X."""
        if alvo_pos is None: return (0, 0)
        dy = 0 if alvo_pos[0] == drone_pos[0] else (1 if alvo_pos[0] > drone_pos[0] else -1)
        dx = 0 if alvo_pos[1] == drone_pos[1] else (1 if alvo_pos[1] > drone_pos[1] else -1)
        return (dy, dx)

    def observar_estado(self, env):
        # O estado agora é focado: Ele só olha para o alvo que importa (Fogo ou Água)
        tanque = "Com_Agua" if env.agua_atual > 0 else "Vazio"

        if tanque == "Com_Agua":
            alvo_pos, dist = self.encontrar_alvo(env.grid, env.drone_pos, env.tamanho, [2, 4])
        else:
            alvo_pos, dist = self.encontrar_alvo(env.grid, env.drone_pos, env.tamanho, [3])

        dy, dx = self.obter_vetor(env.drone_pos, alvo_pos)

        # O estado agora tem apenas 18 combinações (Ex: "Com_Agua", 1, -1)
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

            # 1. Avalia se a interação foi um sucesso total (Vitória)
            if self.acao_anterior == 'e':
                if tanque_antigo == "Com_Agua" and dy_antigo == 0 and dx_antigo == 0:
                    recompensa = 100
                else:
                    recompensa = -10  # Punição por desperdiçar o turno apertando E à toa

            elif self.acao_anterior == 'r':
                if tanque_antigo == "Vazio" and dy_antigo == 0 and dx_antigo == 0:
                    recompensa = 100
                else:
                    recompensa = -10

                    # 2. Avalia a movimentação pelo delta de distância (Progresso Anti-Hack)
            else:
                if dist_atual < self.distancia_anterior:
                    recompensa = 10  # Passo perfeito na direção certa
                else:
                    recompensa = -10  # Afastou ou bateu na parede

            # Equação de Bellman
            q_antigo = self.q_table[self.estado_anterior][self.acao_anterior]
            max_q_novo = max(self.q_table[estado_atual].values())
            novo_q = q_antigo + self.alpha * (recompensa + self.gamma * max_q_novo - q_antigo)
            self.q_table[self.estado_anterior][self.acao_anterior] = novo_q

        # Decaimento do Epsilon (Fica cada vez mais inteligente e menos aleatório)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

        # Se o mapa está limpo, descansa
        if estado_atual[1] == 0 and estado_atual[2] == 0 and estado_atual[0] == "Com_Agua" and dist_atual == float(
                'inf'):
            self.estado_anterior = None
            return 'aguardar'

        # Escolhe a Ação
        if random.random() < self.epsilon:
            acao_escolhida = random.choice(self.acoes)
        else:
            acao_escolhida = max(self.q_table[estado_atual], key=self.q_table[estado_atual].get)

        self.estado_anterior = estado_atual
        self.acao_anterior = acao_escolhida
        self.distancia_anterior = dist_atual

        return acao_escolhida