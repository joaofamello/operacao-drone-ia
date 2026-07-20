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

        # 0 = Queimado/Vazio, 1 = Floresta, 2 = Fogo, 3 = Água (Rio/Lago)
        self.grid = [[1 for _ in range(tamanho)] for _ in range(tamanho)]

        # Posições iniciais (remover o lago_pos)
        self.drone_pos = [0, 0]
        self.fogo_pos = [tamanho // 2, tamanho // 2]

        # Configuração inicial do grid
        self._gerar_rios()
        self.grid[self.fogo_pos[0]][self.fogo_pos[1]] = 2
        self.grid[self.drone_pos[0]][self.drone_pos[1]] = 1

    def _gerar_rios(self):
        """Gera pequenos rios contínuos aleatórios pelo mapa."""
        quantidade_rios = 3
        for _ in range(quantidade_rios):
            linha = random.randint(0, self.tamanho - 1)
            col = random.randint(0, self.tamanho - 1)
            comprimento = random.randint(3, 7)  # Rios de tamanho 3 a 7 blocos

            for _ in range(comprimento):
                if 0 <= linha < self.tamanho and 0 <= col < self.tamanho:
                    self.grid[linha][col] = 3

                # Escolhe uma direção aleatória para continuar "desenhando" o rio
                dl, dc = random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
                linha += dl
                col += dc

    def renderizar(self):
        """Limpa o terminal e desenha o estado atual do ambiente."""
        if os.name == 'nt': # Windows
            subprocess.run(['cls'], shell=True)
        else: # Linux/macOS
            subprocess.run(['clear'])

        # Códigos ANSI para colorir o fundo (Background)
        RESET = "\033[0m"
        BG_CINZA = "\033[100m"  # Terra queimada
        BG_VERDE = "\033[42m"  # Floresta
        BG_VERMELHO = "\033[41m"  # Fogo
        BG_AZUL = "\033[44m"  # Lago
        BG_BRANCO = "\033[47m"  # Fundo do Drone
        TXT_PRETO = "\033[30m"  # Texto do Drone

        print("=== OPERAÇÃO DRONE ===")
        print(f"Nível de Água: {self.agua_atual}")

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

            print(linha)
        print("\n"+"="*22)

    def mover_drone(self, acao):
        """Processa a ação escolhida (movimento ou interação)."""
        linha, col = self.drone_pos

        if acao == 'w' and linha > 0:
            self.drone_pos[0] -= 1
        elif acao == 's' and linha < self.tamanho - 1:
            self.drone_pos[0] += 1
        elif acao == 'a' and col > 0:
            self.drone_pos[1] -= 1
        elif acao == 'd' and col < self.tamanho - 1:
            self.drone_pos[1] += 1

        elif acao == 'e': # Jogar água
            if self.agua_atual > 0 and self.grid[linha][col] == 2:
                self.grid[linha][col] = 1 # Fogo apagado, volta a ser floresta
                self.agua_atual -= 1
                print("\n[!] Fogo apagado!")
                time.sleep(1)
            elif self.agua_atual == 0:
                print("\n[X] Sem água! Abasteça no lago.")
                time.sleep(1)

        elif acao == 'r': # Reabastecer
            if self.grid[linha][col] == 3:
                self.agua_atual = self.agua_maxima
                print("\n[!] Tanque cheio!")
                time.sleep(1)

    def espalhar_fogo(self):
        """Lógica simples para o fogo se espalhar aleatoriamente."""
        novos_fogos = []
        for i in range(self.tamanho):
            for j in range(self.tamanho):
                if self.grid[i][j] == 2: # Se tem fogo
                    direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                    random.shuffle(direcoes)
                    for dl, dc in direcoes:
                        nl, nc = i + dl, j + dc
                        if 0 <= nl < self.tamanho and 0 <= nc < self.tamanho:
                            if self.grid[nl][nc] == 1:
                                if random.random() < 0.2:
                                    novos_fogos.append((nl, nc))
                                break

        for l, c in novos_fogos:
            self.grid[l][c] = 2

if __name__ == "__main__":
    env = OperacaoDrone()
    agente = AgenteHeuristico()
    while True:
        env.renderizar()

        acao = agente.agir(env)

        if acao == 'aguardar':
            print("\nFloresta salva! Aguardando novo focos...")
            time.sleep(1)
        elif acao:
            env.mover_drone(acao)

        env.espalhar_fogo()
        time.sleep(0.5)