import os
import random
import time

class OperacaoDrone:
    def __init__(self, tamanho=10, agua_maxima=5):
        self.tamanho = tamanho
        self.agua_maxima = agua_maxima
        self.agua_atual = agua_maxima

        # 0 = Queimado/Vazio, 1 = Floresta, 2 = Fogo, 3 = Lago
        self.grid = [[1 for _ in range(tamanho)] for _ in range(tamanho)]

        # Posições iniciais
        self.drone_pos = [0, 0]
        self.lago_pos = [tamanho - 1, tamanho - 1]
        self.fogo_pos = [tamanho // 2, tamanho // 2]

        # Configuração inicial do grid
        self.grid[self.lago_pos[0]][self.lago_pos[1]] = 3
        self.grid[self.fogo_pos[0]][self.fogo_pos[1]] = 2
        self.grid[self.drone_pos[0]][self.drone_pos[1]] = 1