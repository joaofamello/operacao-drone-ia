import os
import subprocess
import random
import time
from agent import AgenteHeuristico


class OperacaoDrone:
    def __init__(self, tamanho=10, agua_maxima=5):
        self.tamanho = tamanho
        self.agua_maxima = agua_maxima
        self.agua_atual = agua_maxima

        # 0 = Queimado, 1 = Floresta, 2 = Fogo, 3 = Água (Rio), 4 = Fumaça (Aquecendo)
        self.grid = [[1 for _ in range(tamanho)] for _ in range(tamanho)]

        self.drone_pos = [0, 0]
        self.fogo_pos = [tamanho // 2, tamanho // 2]

        self._gerar_rios()
        self.grid[self.fogo_pos[0]][self.fogo_pos[1]] = 2
        self.grid[self.drone_pos[0]][self.drone_pos[1]] = 1

    def _gerar_rios(self):
        """Gera pequenos rios contínuos aleatórios pelo mapa."""
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


    def limpar_terminal(self):
        if os.name == 'nt':
            subprocess.run(['cls'], shell=True)
        else:
            subprocess.run(['clear'])

    def renderizar(self):
        self.limpar_terminal()

        RESET = "\033[0m"
        BG_CINZA = "\033[100m"
        BG_VERDE = "\033[42m"
        BG_VERMELHO = "\033[41m"
        BG_AZUL = "\033[44m"
        BG_AMARELO = "\033[43m"
        BG_BRANCO = "\033[47m"
        TXT_PRETO = "\033[30m"

        print("=== OPERAÇÃO DRONE ===")
        print(f"Nível de Água: {self.agua_atual}/{self.agua_maxima}")
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
            # Drone agora apaga tanto Fogo (2) quanto Fumaça (4)
            if self.agua_atual > 0 and self.grid[linha][col] in [2, 4]:
                self.grid[linha][col] = 1
                self.agua_atual -= 1

        elif acao == 'r':
            if self.grid[linha][col] == 3:
                self.agua_atual = self.agua_maxima

    def espalhar_fogo(self):
        """Sistema de estágios: Fumaça (4) vira Fogo (2); Fogo (2) cria Fumaça (4)."""
        novos_aquecimentos = []
        novos_fogos = []

        for i in range(self.tamanho):
            for j in range(self.tamanho):
                if self.grid[i][j] == 4:
                    novos_fogos.append((i, j))  # Fumaça evolui para fogo ativo

                elif self.grid[i][j] == 2:
                    direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                    random.shuffle(direcoes)
                    for dl, dc in direcoes:
                        nl, nc = i + dl, j + dc
                        if 0 <= nl < self.tamanho and 0 <= nc < self.tamanho:
                            if self.grid[nl][nc] == 1:
                                # 20% de chance de espalhar, mas começa como Fumaça
                                if random.random() < 0.3:
                                    novos_aquecimentos.append((nl, nc))

        for l, c in novos_fogos:
            self.grid[l][c] = 2
        for l, c in novos_aquecimentos:
            self.grid[l][c] = 4


if __name__ == "__main__":
    env = OperacaoDrone()
    agente = AgenteHeuristico()

    while True:
        # Vantagem Tática: O drone joga 3 turnos para cada turno do ambiente
        for _ in range(3):
            env.renderizar()
            acao = agente.agir(env)

            if acao == 'aguardar':
                print("\nFloresta salva! Aguardando novos focos...")
                time.sleep(0.5)
                break  # Sai do loop de vantagem se não há mais perigo
            elif acao:
                env.mover_drone(acao)

            time.sleep(0.25)  # Velocidade de visualização do drone
        env.espalhar_fogo()