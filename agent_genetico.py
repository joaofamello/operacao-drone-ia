import random
from environment import OperacaoDrone


class AgenteGenetico:
    def __init__(self, dna=None):
        self.acoes = ['w', 's', 'a', 'd', 'e', 'r']
        self.estados_possiveis = self._gerar_estados()

        # Se nasce sem DNA, gera um instinto totalmente aleatório
        if dna is None:
            self.dna = {estado: random.choice(self.acoes) for estado in self.estados_possiveis}
        else:
            self.dna = dna

    def _gerar_estados(self):
        estados = []
        for tanque in ["Com_Agua", "Vazio"]:
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    estados.append((tanque, dy, dx))
        return estados

    def calcular_distancia(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def encontrar_alvo(self, grid, drone_pos, tamanho, tipos_alvo):
        alvo, menor_dist = None, float('inf')
        for i in range(tamanho):
            for j in range(tamanho):
                if grid[i][j] in tipos_alvo:
                    dist = self.calcular_distancia(drone_pos, [i, j])
                    if dist < menor_dist:
                        menor_dist = dist
                        alvo = [i, j]
        return alvo

    def obter_vetor(self, drone_pos, alvo_pos):
        if alvo_pos is None: return (0, 0)
        dy = 0 if alvo_pos[0] == drone_pos[0] else (1 if alvo_pos[0] > drone_pos[0] else -1)
        dx = 0 if alvo_pos[1] == drone_pos[1] else (1 if alvo_pos[1] > drone_pos[1] else -1)
        return (dy, dx)

    def observar_estado(self, env):
        tanque = "Com_Agua" if env.agua_atual > 0 else "Vazio"
        alvo_pos = self.encontrar_alvo(env.grid, env.drone_pos, env.tamanho,
                                       [2, 4]) if tanque == "Com_Agua" else self.encontrar_alvo(env.grid, env.drone_pos,
                                                                                                env.tamanho, [3])
        dy, dx = self.obter_vetor(env.drone_pos, alvo_pos)
        return (tanque, dy, dx)

    def agir(self, env):
        estado_atual = self.observar_estado(env)
        # O drone não pensa nem atualiza notas. Ele age puramente pelo DNA.
        return self.dna[estado_atual]


def avaliar_fitness(dna):
    """Mede a competência de um DNA rodando mapas simulados com pontuação guiada."""
    fitness_total = 0

    # Testa o mesmo DNA em 3 mapas diferentes para eliminar o fator "sorte"
    for _ in range(3):
        env = OperacaoDrone(tamanho=15)
        agente = AgenteGenetico(dna)
        fitness_rodada = 0

        for _ in range(50):  # Vida do drone dura 50 turnos
            for _ in range(3):  # Vantagem tática do drone
                # Identifica a distância antes de mover
                tanque = "Com_Agua" if env.agua_atual > 0 else "Vazio"
                alvo_pos = agente.encontrar_alvo(env.grid, env.drone_pos, env.tamanho,
                                                 [2, 4]) if tanque == "Com_Agua" else agente.encontrar_alvo(env.grid,
                                                                                                            env.drone_pos,
                                                                                                            env.tamanho,
                                                                                                            [3])

                dist_antes = float('inf')
                if alvo_pos:
                    dist_antes = agente.calcular_distancia(env.drone_pos, alvo_pos)

                acao = agente.agir(env)

                # Pontuação Massiva para o Objetivo Final (Vitória)
                if acao == 'e' and env.agua_atual > 0 and env.grid[env.drone_pos[0]][env.drone_pos[1]] in [2, 4]:
                    fitness_rodada += 500
                elif acao == 'r' and env.agua_atual == 0 and env.grid[env.drone_pos[0]][env.drone_pos[1]] == 3:
                    fitness_rodada += 500

                env.mover_drone(acao)

                # 3. Pontuação de Progresso (O segredo da evolução rápida)
                if alvo_pos:
                    dist_depois = agente.calcular_distancia(env.drone_pos, alvo_pos)
                    if dist_depois < dist_antes:
                        fitness_rodada += 5  # Ganha pontos por ir na direção certa
                    else:
                        fitness_rodada -= 2  # Perde pontos se afastar ou bater na parede

            env.espalhar_fogo()

        fitness_total += fitness_rodada

    return fitness_total / 3  # Retorna a média


def evoluir_populacao(geracoes=150, tam_pop=100):
    print("Iniciando Evolução Genética... (Isso levará poucos segundos)")
    populacao = [AgenteGenetico().dna for _ in range(tam_pop)]

    for gen in range(geracoes):
        # Avalia toda a população
        pontuacoes = [(avaliar_fitness(dna), dna) for dna in populacao]
        pontuacoes.sort(key=lambda x: x[0], reverse=True)

        melhor_score = pontuacoes[0][0]
        if gen % 30 == 0 or gen == geracoes - 1:
            print(f"Geração {gen} | Melhor Score (Fitness): {melhor_score}")

        # Seleciona os 10% melhores (Elite)
        elite = [dna for score, dna in pontuacoes[:tam_pop // 10]]
        nova_populacao = elite.copy()

        # Crossover e Mutação para preencher o resto da população
        while len(nova_populacao) < tam_pop:
            pai = random.choice(elite)
            mae = random.choice(elite)

            # Mistura os genes
            filho = {}
            for estado in pai.keys():
                filho[estado] = pai[estado] if random.random() > 0.5 else mae[estado]

                # Mutação (5% de chance de alterar o gene)
                if random.random() < 0.05:
                    filho[estado] = random.choice(['w', 's', 'a', 'd', 'e', 'r'])

            nova_populacao.append(filho)

        populacao = nova_populacao

    print("Evolução Concluída! Super Drone criado.")
    return AgenteGenetico(populacao[0])  # Retorna o campeão