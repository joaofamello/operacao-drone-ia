import os
import subprocess
import random


class OperacaoDrone:
    def __init__(self, tamanho=15, agua_maxima=10):
        self.tamanho = tamanho
        self.agua_maxima = agua_maxima
        self.agua_atual = agua_maxima

        # Vetor de direção do vento: (0, 1) = Leste, (0, -1) = Oeste, (-1, 0) = Norte, (1, 0) = Sul, (0, 0) = Nulo
        self.vento_direcao = (0, 1)

        # 0 = Queimado, 1 = Floresta, 2 = Fogo, 3 = Água (Rio), 4 = Fumaça (Aquecendo)
        self.grid = [[1 for _ in range(tamanho)] for _ in range(tamanho)]

        self.drone_pos = [0, 0]

        self._gerar_rios()

        focos_criados = 0
        while focos_criados < 3:
            fl = random.randint(0, tamanho - 1)
            fc = random.randint(0, tamanho - 1)
            if self.grid[fl][fc] == 1:
                self.grid[fl][fc] = 2
                focos_criados += 1

        self.grid[self.drone_pos[0]][self.drone_pos[1]] = 1

    def _gerar_rios(self):
        quantidade_rios = 3
        for _ in range(quantidade_rios):
            linha = random.randint(0, self.tamanho - 1)
            col = random.randint(0, self.tamanho - 1)
            comprimento = random.randint(3, 7)

            for _ in range(comprimento):
                if 0 <= linha < self.tamanho and 0 <= col < self.tamanho:
                    self.grid[linha][col] = 3

                dl, dc = random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
                linha += dl
                col += dc

    def definir_vento(self, dl, dc):
        self.vento_direcao = (dl, dc)

    def renderizar(self):
        if os.name == 'nt':
            subprocess.run(['cls'], shell=True)
        else:
            subprocess.run(['clear'])

        RESET = "\033[0m"
        BG_CINZA = "\033[100m"
        BG_VERDE = "\033[42m"
        BG_VERMELHO = "\033[41m"
        BG_AZUL = "\033[44m"
        BG_AMARELO = "\033[43m"
        BG_BRANCO = "\033[47m"
        TXT_PRETO = "\033[30m"

        setas_vento = {
            (0, 1): "➡️ Leste",
            (0, -1): "⬅️ Oeste",
            (-1, 0): "⬆️ Norte",
            (1, 0): "⬇️ Sul",
            (0, 0): "Nulo"
        }
        vento_str = setas_vento.get(self.vento_direcao, "Desconhecido")

        print("=== OPERAÇÃO DRONE ===")
        print(f"Nível de Água: {self.agua_atual}/{self.agua_maxima} | Vento: {vento_str}")
        print("Controles: Autônomo (Agente Heurístico)\n")

        for i in range(self.tamanho):
            linha = ""
            for j in range(self.tamanho):
                if [i, j] == self.drone_pos:
                    linha += f"{BG_BRANCO}{TXT_PRETO} D {RESET}"
                else:
                    estado_celula = self.grid[i][j]
                    if estado_celula == 0:
                        linha += f"{BG_CINZA}   {RESET}"
                    elif estado_celula == 1:
                        linha += f"{BG_VERDE}   {RESET}"
                    elif estado_celula == 2:
                        linha += f"{BG_VERMELHO}   {RESET}"
                    elif estado_celula == 3:
                        linha += f"{BG_AZUL}   {RESET}"
                    elif estado_celula == 4:
                        linha += f"{BG_AMARELO}   {RESET}"

            print(linha)
        print("\n" + "=" * 22)

    def mover_drone(self, acao):
        linha, col = self.drone_pos

        if acao == 'w' and linha > 0:
            self.drone_pos[0] -= 1
        elif acao == 's' and linha < self.tamanho - 1:
            self.drone_pos[0] += 1
        elif acao == 'a' and col > 0:
            self.drone_pos[1] -= 1
        elif acao == 'd' and col < self.tamanho - 1:
            self.drone_pos[1] += 1
        elif acao == 'e':
            if self.agua_atual > 0 and self.grid[linha][col] in [2, 4]:
                self.grid[linha][col] = 1
                self.agua_atual -= 1
        elif acao == 'r':
            if self.grid[linha][col] == 3:
                self.agua_atual = self.agua_maxima

    def espalhar_fogo(self):
        novos_aquecimentos = []
        novos_fogos = []

        for i in range(self.tamanho):
            for j in range(self.tamanho):
                if self.grid[i][j] == 4:
                    novos_fogos.append((i, j))

                elif self.grid[i][j] == 2:
                    direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                    vento_dl, vento_dc = self.vento_direcao

                    random.shuffle(direcoes)
                    for dl, dc in direcoes:
                        nl, nc = i + dl, j + dc
                        if 0 <= nl < self.tamanho and 0 <= nc < self.tamanho:
                            if self.grid[nl][nc] == 1:

                                chance_propagacao = 0.05

                                if self.vento_direcao != (0, 0):
                                    if dl == vento_dl and dc == vento_dc:
                                        chance_propagacao = 0.40
                                    elif dl == -vento_dl and dc == -vento_dc:
                                        chance_propagacao = 0.01

                                if random.random() < chance_propagacao:
                                    novos_aquecimentos.append((nl, nc))

        for l, c in novos_fogos:
            self.grid[l][c] = 2
        for l, c in novos_aquecimentos:
            self.grid[l][c] = 4

        if random.random() < 0.10:
            rl = random.randint(0, self.tamanho - 1)
            rc = random.randint(0, self.tamanho - 1)
            if self.grid[rl][rc] == 1:
                self.grid[rl][rc] = 4