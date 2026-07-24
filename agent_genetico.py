import random
from environment import OperacaoDrone
from utils import calcular_distancia, encontrar_alvo, obter_vetor


class AgenteGenetico:
    def __init__(self, dna=None):
        self.acoes = ['w', 's', 'a', 'd', 'e', 'r']
        self.estados_possiveis = self._gerar_estados()

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

    def observar_estado(self, env):
        tanque = "Com_Agua" if env.agua_atual > 0 else "Vazio"
        alvo_pos = encontrar_alvo(env.grid, env.drone_pos, env.tamanho,
                                  [2, 4]) if tanque == "Com_Agua" else encontrar_alvo(env.grid, env.drone_pos,
                                                                                      env.tamanho, [3])
        dy, dx = obter_vetor(env.drone_pos, alvo_pos)
        return (tanque, dy, dx)

    def agir(self, env):
        estado_atual = self.observar_estado(env)
        return self.dna[estado_atual]


def avaliar_fitness(dna):
    fitness_total = 0

    for _ in range(3):
        env = OperacaoDrone(tamanho=15)
        agente = AgenteGenetico(dna)
        fitness_rodada = 0

        for _ in range(50):
            for _ in range(3):
                tanque = "Com_Agua" if env.agua_atual > 0 else "Vazio"
                alvo_pos = encontrar_alvo(env.grid, env.drone_pos, env.tamanho,
                                          [2, 4]) if tanque == "Com_Agua" else encontrar_alvo(env.grid, env.drone_pos,
                                                                                              env.tamanho, [3])

                dist_antes = float('inf')
                if alvo_pos:
                    dist_antes = calcular_distancia(env.drone_pos, alvo_pos)

                acao = agente.agir(env)

                if acao == 'e' and env.agua_atual > 0 and env.grid[env.drone_pos[0]][env.drone_pos[1]] in [2, 4]:
                    fitness_rodada += 500
                elif acao == 'r' and env.agua_atual == 0 and env.grid[env.drone_pos[0]][env.drone_pos[1]] == 3:
                    fitness_rodada += 500

                env.mover_drone(acao)

                if alvo_pos:
                    dist_depois = calcular_distancia(env.drone_pos, alvo_pos)
                    if dist_depois < dist_antes:
                        fitness_rodada += 5
                    else:
                        fitness_rodada -= 2

            env.espalhar_fogo()

        fitness_total += fitness_rodada

    return fitness_total / 3


def evoluir_populacao(geracoes=150, tam_pop=100):
    print("Iniciando Evolução Genética... (Isso levará poucos segundos)")
    populacao = [AgenteGenetico().dna for _ in range(tam_pop)]

    for gen in range(geracoes):
        pontuacoes = [(avaliar_fitness(dna), dna) for dna in populacao]
        pontuacoes.sort(key=lambda x: x[0], reverse=True)

        melhor_score = pontuacoes[0][0]
        if gen % 30 == 0 or gen == geracoes - 1:
            print(f"Geração {gen} | Melhor Score (Fitness): {melhor_score}")

        elite = [dna for score, dna in pontuacoes[:tam_pop // 10]]
        nova_populacao = elite.copy()

        while len(nova_populacao) < tam_pop:
            pai = random.choice(elite)
            mae = random.choice(elite)

            filho = {}
            for estado in pai.keys():
                filho[estado] = pai[estado] if random.random() > 0.5 else mae[estado]

                if random.random() < 0.05:
                    filho[estado] = random.choice(['w', 's', 'a', 'd', 'e', 'r'])

            nova_populacao.append(filho)

        populacao = nova_populacao

    print("Evolução Concluída! Super Drone criado.")
    return AgenteGenetico(populacao[0])