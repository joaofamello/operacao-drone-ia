import sys

import pygame
from environment import OperacaoDrone
# from agent_heuristico import AgenteHeuristico
# from agent_qlearning import AgenteQLearning
from agent_genetico import AgenteGenetico, evoluir_populacao

# iniciando o pygame
pygame.init()

# configurações da janela
TAMANHO_BLOCO = 40
TAMANHO_GRID = 15
LARGURA = TAMANHO_BLOCO * TAMANHO_GRID
ALTURA_HUD = 80
ALTURA_TOTAL = LARGURA + ALTURA_HUD

# cores rgb
COR_FLORESTA = (34, 139, 34)
COR_FOGO = (226, 88, 34)
COR_AGUA = (30, 144, 255)
COR_FUMACA = (255, 215, 0)
COR_QUEIMADO = (105, 105, 105)
COR_DRONE = (240, 240, 240)
COR_TEXTO = (255, 255, 255)
COR_FUNDO_HUD = (25, 25, 25)

tela = pygame.display.set_mode((LARGURA, ALTURA_TOTAL))
pygame.display.set_caption("Operação Drone - IA")
fonte = pygame.font.SysFont("arial", 24, bold=True)
relogio = pygame.time.Clock()

env = OperacaoDrone(tamanho=TAMANHO_GRID)
agente = evoluir_populacao(geracoes=50, tam_pop=50)

def desenhar_ambiente(env):
    tela.fill(COR_FUNDO_HUD)

    setas_vento = {
        (0, 1): "Leste",
        (0, -1): "Oeste",
        (-1, 0): "Norte",
        (1, 0): "Sul",
        (0, 0): "Nulo"
    }
    texto_agua = fonte.render(f"Nível de Água: {env.agua_atual}/{env.agua_maxima}", True, COR_TEXTO)
    texto_vento = fonte.render(f"Vento: {setas_vento.get(env.vento_direcao, '')}", True, COR_TEXTO)

    tela.blit(texto_agua, (15, 10))
    tela.blit(texto_vento, (15, 45))

    # desenha o grid
    for i in range(env.tamanho):
        for j in range(env.tamanho):
            x = j * TAMANHO_BLOCO
            y = i * TAMANHO_BLOCO + ALTURA_HUD

            estado = env.grid[i][j]
            if estado == 0: cor = COR_QUEIMADO
            elif estado == 1: cor = COR_FLORESTA
            elif estado == 2: cor = COR_FOGO
            elif estado == 3: cor = COR_AGUA
            elif estado == 4: cor = COR_FUMACA
            else: cor = (255, 0, 255) # Rosa: se aparecer na tela, há um bug no ambiente.

            # desenha o bloco colorido e uma borda preta fina
            pygame.draw.rect(tela, cor, (x, y, TAMANHO_BLOCO, TAMANHO_BLOCO))
            pygame.draw.rect(tela, (0, 0, 0), (x, y, TAMANHO_BLOCO, TAMANHO_BLOCO), 1)

    # desenha o drone (círculo)
    dx = env.drone_pos[1] * TAMANHO_BLOCO + (TAMANHO_BLOCO // 2)
    dy = env.drone_pos[0] * TAMANHO_BLOCO + ALTURA_HUD + (TAMANHO_BLOCO // 2)
    pygame.draw.circle(tela, COR_DRONE, (dx, dy), TAMANHO_BLOCO // 2 - 4)

    pygame.display.flip()

    # loop principal da janela
rodando = True
while rodando:
    # checa se o usuário clicou no X para fechar a janela
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # vantagem tática do drone (3 turnos para cada turno de fogo)
    for _ in range(3):
        desenhar_ambiente(env)
        acao = agente.agir(env)

        if acao == 'aguardar':
            pygame.time.delay(300)
            break
        elif acao:
            env.mover_drone(acao)

        # controla a velocidade da simulação (15 quadros por segundo)
        relogio.tick(15)

    env.espalhar_fogo()

pygame.quit()
sys.exit()