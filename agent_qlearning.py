import random

class AgenteQLearning:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=1.0, epsilon_min=0.01, epsilon_decay=0.995):
        # a tabela Q, onde o conhecimento fica armazenado
        self.q_table = {}

        # hiperparâmetros do aprendizado
        self.alpha = alpha  # Taxa de aprendizado
        self.gamma = gamma  # Fator de desconto (foco no futuro)
        self.epsilon = epsilon  # Taxa de exploração inicial (1.0 = 100% aleatório)
        self.epsilon_min = epsilon_min  # Mínimo de aleatoriedade
        self.epsilon_decay = epsilon_decay  # Velocidade que ele deixa de ser aleatório

        self.acoes = ['w', 's', 'a', 'd', 'e', 'r']

        # memória de curto prazo para a Equação de Bellman
        self.estado_anterior = None
        self.acao_anterior = None

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
        return alvo

    def obter_direcao(self, drone_pos, alvo_pos):
        if alvo_pos is None: return "Nenhum"
        if drone_pos == alvo_pos: return "No_Alvo"

        dl = alvo_pos[0] - drone_pos[0]
        dc = alvo_pos[1] - drone_pos[1]

        if abs(dl) > abs(dc):
            return "Sul" if dl > 0 else "Norte"
        else:
            return "Leste" if dc > 0 else "Oeste"

    def observar_estado(self, env):
        tanque = "Com_Agua" if env.agua_atual > 0 else "Vazio"

        fogo_pos = self.encontrar_alvo(env.grid, env.drone_pos, env.tamanho, [2, 4])
        dir_fogo = self.obter_direcao(env.drone_pos, fogo_pos)

        agua_pos = self.encontrar_alvo(env.grid, env.drone_pos, env.tamanho, [3])
        dir_agua = self.obter_direcao(env.drone_pos, agua_pos)

        return (tanque, dir_fogo, dir_agua)

    def inicializar_estado(self, estado):
        if estado not in self.q_table:
            self.q_table[estado] = {a: 0.0 for a in self.acoes}

    def calcular_recompensa(self, estado, acao):
        tanque, dir_fogo, dir_agua = estado

        # recompensas e punições finais
        if acao == 'e':
            return 100 if tanque == "Com_Agua" and dir_fogo == "No_Alvo" else -10
        if acao == 'r':
            return 100 if tanque == "Vazio" and dir_agua == "No_Alvo" else -10

        # recompensas de movimentação
        if tanque == "Com_Agua":
            if acao == 'w' and dir_fogo == "Norte": return 5
            if acao == 's' and dir_fogo == "Sul": return 5
            if acao == 'a' and dir_fogo == "Oeste": return 5
            if acao == 'd' and dir_fogo == "Leste": return 5
        else:
            if acao == 'w' and dir_agua == "Norte": return 5
            if acao == 's' and dir_agua == "Sul": return 5
            if acao == 'a' and dir_agua == "Oeste": return 5
            if acao == 'd' and dir_agua == "Leste": return 5

        # punição padrão por dar um passo errado ou inútil
        return -1

    def agir(self, env):
        estado_atual = self.observar_estado(env)
        self.inicializar_estado(estado_atual)

        # condição de descanso (Se o mapa estiver limpo)
        if estado_atual[1] == "Nenhum" and estado_atual[0] == "Com_Agua":
            self.estado_anterior = None
            return 'aguardar'

        # atualiza a Tabela Q com base no que aconteceu no turno passado (Equação de Bellman)
        if self.estado_anterior is not None:
            recompensa = self.calcular_recompensa(self.estado_anterior, self.acao_anterior)

            q_antigo = self.q_table[self.estado_anterior][self.acao_anterior]
            max_q_novo = max(self.q_table[estado_atual].values())

            # a fórmula mágica do Q-Learning:
            novo_q = q_antigo + self.alpha * (recompensa + self.gamma * max_q_novo - q_antigo)
            self.q_table[self.estado_anterior][self.acao_anterior] = novo_q

        # decaimento do Epsilon (Fica menos aleatório com o tempo)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

        # política Epsilon-Greedy (Explorar x Explorar)
        if random.random() < self.epsilon:
            acao_escolhida = random.choice(self.acoes)
        else:
            acao_escolhida = max(self.q_table[estado_atual], key=self.q_table[estado_atual].get)

        # salva o estado atual na memória para avaliar no próximo turno
        self.estado_anterior = estado_atual
        self.acao_anterior = acao_escolhida

        return acao_escolhida