class AgenteHeuristico:
    def __init__(self):
        pass

    def calcular_distancia(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def encontrar_fogo_mais_proximo(self, grid, drone_pos, tamanho):
        fogo_mais_proximo = None
        menor_distancia = float('inf')
        for i in range(tamanho):
            for j in range(tamanho):
                if grid[i][j] == 2: # 2 representa o fogo
                    dist = self.calcular_distancia(drone_pos, [i, j])
                    if dist < menor_distancia:
                        menor_distancia = dist
                        fogo_mais_proximo = [i, j]
        return fogo_mais_proximo

    def agir(self, env):
        linha, col = env.drone_pos
        if env.agua_atual > 0 and env.grid[linha][col] == 2:
            return 'e' # apagar fogo
        if env.agua_atual == 0 and env.grid[linha][col] == 3:
            return 'r' # reabastecer no lago
        objetivo = None
        if env.agua_atual == 0:
            objetivo = env.lago_pos
        else:
            objetivo = self.encontrar_fogo_mais_proximo(env.grid, env.drone_pos, env.tamanho)
            if objetivo is None:
                return 'aguardar'

            movimentos = {
                'w': [linha - 1, col],
                'e': [linha + 1, col],
                'r': [linha, col - 1],
                'd': [linha, col + 1]
            }

            melhor_acao = None
            menor_dist = float('inf')

            for acao, (nl, nc) in movimentos.items():
                # verifica se o movimento está dentro dos limites do mapa
                if 0 <= nl < env.tamanho and 0 <= nc < env.tamanho:
                    dist = self.calcular_distancia([nl, nc], objetivo)
                    if dist < menor_dist:
                        menor_dist = dist
                        melhor_acao = acao

            return melhor_acao