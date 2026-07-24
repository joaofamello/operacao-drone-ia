def calcular_distancia(pos1, pos2):
    """Calcula a Distância de Manhattan entre dois pontos."""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def encontrar_alvo(grid, drone_pos, tamanho, tipos_alvo):
    """Retorna apenas as coordenadas do alvo mais próximo."""
    alvo = None
    menor_distancia = float('inf')

    for i in range(tamanho):
        for j in range(tamanho):
            if grid[i][j] in tipos_alvo:
                dist = calcular_distancia(drone_pos, [i, j])
                if dist < menor_distancia:
                    menor_distancia = dist
                    alvo = [i, j]

    return alvo

def encontrar_alvo_com_distancia(grid, drone_pos, tamanho, tipos_alvo):
    """Retorna as coordenadas do alvo e a distância exata até ele."""
    alvo = None
    menor_dist = float('inf')

    for i in range(tamanho):
        for j in range(tamanho):
            if grid[i][j] in tipos_alvo:
                dist = calcular_distancia(drone_pos, [i, j])
                if dist < menor_dist:
                    menor_dist = dist
                    alvo = [i, j]

    return alvo, menor_dist

def obter_vetor(drone_pos, alvo_pos):
    """Retorna a direção em formato de vetor (-1, 0 ou 1) nos eixos Y e X."""
    if alvo_pos is None: return (0, 0)
    dy = 0 if alvo_pos[0] == drone_pos[0] else (1 if alvo_pos[0] > drone_pos[0] else -1)
    dx = 0 if alvo_pos[1] == drone_pos[1] else (1 if alvo_pos[1] > drone_pos[1] else -1)
    return (dy, dx)