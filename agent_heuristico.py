import heapq

class AgenteHeuristico:
    def __init__(self):
        pass

    def calcular_distancia(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def encontrar_alvo_mais_proximo(self, grid, drone_pos, tamanho, tipos_alvo):
        alvo_mais_proximo = None
        menor_distancia = float('inf')

        for i in range(tamanho):
            for j in range(tamanho):
                if grid[i][j] in tipos_alvo:
                    dist = self.calcular_distancia(drone_pos, [i, j])
                    if dist < menor_distancia:
                        menor_distancia = dist
                        alvo_mais_proximo = [i, j]

        return alvo_mais_proximo

    def agir(self, env):
        linha, col = env.drone_pos

        # interação imediata
        if env.agua_atual > 0 and env.grid[linha][col] in [2, 4]: return 'e'
        if env.agua_atual == 0 and env.grid[linha][col] == 3: return 'r'

        # definição do objetivo
        objetivo = self.encontrar_alvo_mais_proximo(env.grid, env.drone_pos, env.tamanho,
                                                    [3] if env.agua_atual == 0 else [2, 4])
        if objetivo is None: return 'aguardar'

        # cálculo de Rota (Algoritmo A* Real)
        inicio = tuple(env.drone_pos)
        objetivo_tuple = tuple(objetivo)

        open_set = []
        # tupla: (f_score, coordenada_atual, caminho_de_acoes)
        heapq.heappush(open_set, (0, inicio, []))

        g_score = {inicio: 0}
        closed_set = set()
        movimentos = {'w': (-1, 0), 's': (1, 0), 'a': (0, -1), 'd': (0, 1)}

        while open_set:
            _, atual, caminho = heapq.heappop(open_set)

            if atual == objetivo_tuple:
                return caminho[0] if caminho else 'aguardar'

            if atual in closed_set: continue
            closed_set.add(atual)

            for acao, (dl, dc) in movimentos.items():
                vizinho = (atual[0] + dl, atual[1] + dc)

                if 0 <= vizinho[0] < env.tamanho and 0 <= vizinho[1] < env.tamanho:
                    tentativa_g = g_score[atual] + 1  # custo de dar 1 passo

                    if vizinho not in g_score or tentativa_g < g_score[vizinho]:
                        g_score[vizinho] = tentativa_g
                        f_score = tentativa_g + self.calcular_distancia(vizinho, objetivo_tuple)
                        heapq.heappush(open_set, (f_score, vizinho, caminho + [acao]))

        return 'aguardar'