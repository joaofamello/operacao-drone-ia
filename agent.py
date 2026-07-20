class AgenteHeuristico:
    def __init__(self):
        pass

    def calcular_distancia(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def encontrar_alvo_mais_proximo(self, grid, drone_pos, tamanho, tipo_alvo):
        alvo_mais_proximo = None
        menor_distancia = float('inf')

        for i in range(tamanho):
            for j in range(tamanho):
                if grid[i][j] == tipo_alvo:
                    dist = self.calcular_distancia(drone_pos, [i, j])
                    if dist < menor_distancia:
                        menor_distancia = dist
                        alvo_mais_proximo = [i, j]

        return alvo_mais_proximo

    def agir(self, env):
        linha, col = env.drone_pos

        # 1. Interação imediata
        if env.agua_atual > 0 and env.grid[linha][col] == 2:
            return 'e'  # apagar fogo
        if env.agua_atual == 0 and env.grid[linha][col] == 3:
            return 'r'  # reabastecer no rio

        # 2. Definição do objetivo
        objetivo = None
        if env.agua_atual == 0:
            # Procura a água (3) mais próxima
            objetivo = self.encontrar_alvo_mais_proximo(env.grid, env.drone_pos, env.tamanho, 3)
            # Contingência caso o mapa seja gerado sem nenhuma água
            if objetivo is None:
                return 'aguardar'
        else:
            # Procura o fogo (2) mais próximo
            objetivo = self.encontrar_alvo_mais_proximo(env.grid, env.drone_pos, env.tamanho, 2)
            if objetivo is None:
                return 'aguardar'

        # 3. Cálculo de Rota
        movimentos = {
            'w': [linha - 1, col],
            's': [linha + 1, col],
            'a': [linha, col - 1],
            'd': [linha, col + 1]
        }

        melhor_acao = None
        menor_dist = float('inf')

        for acao, (nl, nc) in movimentos.items():
            if 0 <= nl < env.tamanho and 0 <= nc < env.tamanho:
                dist = self.calcular_distancia([nl, nc], objetivo)
                if dist < menor_dist:
                    menor_dist = dist
                    melhor_acao = acao

        return melhor_acao