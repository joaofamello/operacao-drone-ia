# Operação Drone 🚁🔥

Simulador de combate a incêndios florestais desenvolvido como projeto de avaliação (Contexto I) para a disciplina de Inteligência Artificial.

Desenvolvido por **João Francisco Araújo de Mello**, Universidade Federal do Agreste de Pernambuco (UFAPE).

## Sobre o Projeto
A "Operação Drone" é um ambiente de simulação bidimensional (grid) onde um drone autônomo deve gerenciar recursos hídricos para conter o avanço estocástico de um incêndio florestal. O sistema impõe à Inteligência Artificial o desafio contínuo de equilibrar a urgência de apagar as chamas com a necessidade logística de retornar à base (lago) para reabastecimento.

O propósito central do repositório é servir como motor de simulação para a implementação, treinamento e comparação de diferentes paradigmas de agentes inteligentes.

## Agentes 
Conforme as diretrizes do Estudo Dirigido, o projeto integrará os seguintes modelos:
*   **Agente Heurístico (A*):** Planejamento dinâmico de rotas utilizando a distância de Manhattan.
*   **Agente de Aprendizado por Reforço (Q-Learning):** Tomada de decisão baseada na maximização de recompensas associadas à preservação florestal ao longo dos episódios.
*   **Algoritmo Genético:** Evolução de uma população de soluções voltadas à maximização da aptidão (fitness) do drone no cenário.

## Instalação e Execução

A fase inicial de validação lógica do ambiente foi construída de forma otimizada para execução direta no terminal, utilizando códigos de escape ANSI para a renderização da matriz de estados em blocos de cor. 

### Pré-requisitos
*   Python 3.10 ou superior.

### Passo a Passo

1. **Clone o repositório para a sua máquina local:**
   ```bash
   git clone [https://github.com/seu-usuario/operacao-drone-ia.git](https://github.com/seu-usuario/operacao-drone-ia.git)
   cd operacao-drone-ia
   
2. **(Opicional) Crie e ative um ambiente virtual:** 
   ```bash
   python -m venv venv
   source venv/bin/activate
   
3. **Execute o simulador interativo:**
   ```bash
   python environment.py
   

**Controles (Modo Manual)**
Durante a fase de testes da transição de estados, o drone pode ser operado manualmente no terminal:
- `W`, `A`, `S`, `D` - Movimentação (Cima, Esquerda, Baixo, Direita).
- `E` - Ejetar água (apaga o fogo na célula atual).
- `R` - Reabastecer (enche o tanque quando sobre o lago).
- `Q` - Encerrar a simulação.