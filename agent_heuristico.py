import heapq
from utils import calcular_distancia, encontrar_alvo


class AgenteHeuristico:
    def __init__(self):
        pass

    def agir(self, env):
        linha, col = env.drone_pos

        # 1. Interação imediata
        if env.agua_atual > 0 and env.grid[linha][col] in [2, 4]: return 'e'
        if env.agua_atual == 0 and env.grid[linha][col] == 3: return 'r'

        # 2. Definição do objetivo usando utils
        objetivo = encontrar_alvo(env.grid, env.drone_pos, env.tamanho, [3] if env.agua_atual == 0 else [2, 4])
        if objetivo is None: return 'aguardar'

        # 3. Cálculo de Rota (Algoritmo A*)
        inicio = tuple(env.drone_pos)
        objetivo_tuple = tuple(objetivo)

        open_set = []
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
                    tentativa_g = g_score[atual] + 1

                    if vizinho not in g_score or tentativa_g < g_score[vizinho]:
                        g_score[vizinho] = tentativa_g
                        f_score = tentativa_g + calcular_distancia(vizinho, objetivo_tuple)
                        heapq.heappush(open_set, (f_score, vizinho, caminho + [acao]))

        return 'aguardar'