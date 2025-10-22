# 🏗️ Arquitetura do Projeto Corridinha

## 📋 Visão Geral

Este documento explica a organização e hierarquia do código do jogo Corridinha, desenvolvido em Python com Pygame.

---

## 🎯 Hierarquia de Classes

### 1. Entidades (entities/)

```
BaseEntity (base.py)
    ↓
Carro (carro.py)
    ↓
    ├── Player (player.py) - Carro do jogador
    └── EnemyCar (enemy_car.py) - Carros inimigos

BasePickup (pickups/base_pickup.py)
    ↓
    ├── FuelPickup - Combustível
    ├── GhostPickup - Power-up fantasma
    └── RocketPickup - Power-up de foguete
```

**Responsabilidades por nível:**

- **BaseEntity**: Imagem, posição, desenho básico
- **Carro**: Velocidade, hitbox, colisões
- **Player**: Controles, combustível, armas, sons
- **EnemyCar**: Movimento autônomo, oscilação, troca de faixa

---

## 🎮 Sistemas Principais

### 1. GameManager (`core/game_manager.py`)
**Responsabilidade**: Orquestrador principal do jogo

```python
# Gerencia:
- Loop principal do jogo
- Estados (menu, jogo, game over, créditos)
- Delta time (dt) para framerate independente
- Pontuação e highscores
- Eventos de entrada (teclado/mouse)
```

### 2. GameWorld (`core/game_world.py`)
**Responsabilidade**: Mundo do jogo e seus elementos

```python
# Gerencia:
- Spawn de inimigos (quando e onde criar)
- Spawn de pickups (combustível, power-ups)
- Colisões entre foguetes e inimigos
- Distância percorrida (pontuação)
- Sistema de congelamento (game over)
```

### 3. Player (`entities/player.py`)
**Responsabilidade**: Controle do jogador

```python
# Sistemas:
- Movimento (teclas direcionais)
- Combustível (consumo e reabastecimento)
- Armas (disparo de foguetes)
- Power-ups (fantasma temporário)
- Sons (motor, aceleração)
```

### 4. EnemyCar (`entities/enemy_car.py`)
**Responsabilidade**: Comportamento dos inimigos

```python
# Sistemas:
- Movimento vertical (scrolling)
- Oscilação lateral (5 padrões diferentes)
- Troca de faixa (20% dos carros)
- Variação de velocidade (70-130%)
- Prevenção de colisão entre inimigos
```

---

## ⚙️ Delta Time (dt)

Todo o jogo usa **delta time** para garantir velocidade consistente independente do FPS:

```python
# Fórmula usada:
velocidade_dt = velocidade_base * 60 * dt

# Exemplo:
# Se velocidade_base = 5 pixels/frame
# Em 60 FPS: dt ≈ 0.0166s
# velocidade_dt = 5 * 60 * 0.0166 = 5 pixels/frame ✓

# Em 30 FPS: dt ≈ 0.0333s  
# velocidade_dt = 5 * 60 * 0.0333 = 10 pixels/frame ✓
# (compensa o frame mais longo)
```

**Arquivos que usam dt:**
- `game_manager.py` - Calcula e distribui dt
- `game_world.py` - Propaga para todos os elementos
- `player.py` - Movimento, combustível
- `enemy_car.py` - Movimento, oscilação
- `track.py` - Scrolling da pista
- `rocket.py` - Movimento e partículas
- Todos os pickups e efeitos visuais

---

## 📁 Estrutura de Pastas

```
Corridinha/
├── main.py              # Ponto de entrada
├── config/              # Configurações globais
│   └── constants.py     # Constantes (largura, altura, etc)
├── core/                # Lógica principal
│   ├── game_manager.py  # Gerenciador do jogo
│   └── game_world.py    # Mundo do jogo
├── entities/            # Entidades do jogo
│   ├── base.py          # Classe base
│   ├── carro.py         # Classe intermediária
│   ├── player.py        # Jogador
│   ├── enemy_car.py     # Inimigos
│   ├── track.py         # Pista
│   ├── rocket.py        # Foguetes
│   ├── explosion.py     # Explosões
│   ├── floating_text.py # Textos flutuantes
│   ├── hitbox.py        # Sistema de colisão
│   ├── pickups/         # Power-ups
│   └── effects/         # Efeitos visuais
├── ui/                  # Interface
│   ├── hud.py           # HUD do jogo
│   ├── leaderboard_screen.py
│   ├── credits_screen.py
│   └── highscore_screen.py
├── utils/               # Utilitários
│   ├── helpers.py
│   └── score_manager.py # Gerenciador de pontuações
├── img/                 # Configuração de imagens
└── assets/              # Recursos (imagens, sons)
```

---

## 🔄 Fluxo do Loop Principal

```
1. GameManager.run()
   ↓
2. Calcula delta time (dt)
   ↓
3. _handle_events() - Processa input
   ↓
4. _update(dt) - Atualiza lógica
   │
   ├─→ GameWorld.update(dt)
   │   ├─→ Track.update(dt)
   │   ├─→ Player.update(dt)
   │   ├─→ EnemyCar.update(dt) (para cada inimigo)
   │   ├─→ Pickups.update(dt)
   │   └─→ Explosion.update(dt)
   │
   └─→ Calcula pontuação
   ↓
5. _render() - Desenha tudo
   ↓
6. pygame.display.flip()
   ↓
7. clock.tick(60) - Limita a 60 FPS
   ↓
8. Volta para 1
```

---

## 🎨 Princípios de Design

### 1. **Separação de Responsabilidades**
Cada classe tem uma única responsabilidade clara:
- `GameManager` = Controla o jogo
- `GameWorld` = Gerencia entidades
- `Player` = Controla o jogador
- `EnemyCar` = Comportamento de IA

### 2. **Herança Bem Definida**
```
BaseEntity → funcionalidades básicas
    ↓
Carro → adiciona movimento e colisão
    ↓
Player/EnemyCar → comportamento específico
```

### 3. **Delta Time Consistente**
Todo movimento usa `dt` para ser independente de FPS.

### 4. **Comentários Educativos**
Código comentado como se fosse explicado para um aluno:
- O QUE faz (não só COMO)
- POR QUE foi feito assim
- Fórmulas e cálculos explicados

---

## 📊 Sistema de Pontuação

```python
# Pontuação Total = Distância + Bônus
score = (distance_traveled / 100) + bonus_score

# Onde:
# - distance_traveled: pixels percorridos
# - bonus_score: pontos de explosões (+20 por inimigo)
```

---

## 🎯 Próximos Passos (Sugestões)

1. **Adicionar mais tipos de inimigos** - Caminhões, motos, etc
2. **Novos power-ups** - Escudo, slow-motion, etc
3. **Sistema de níveis** - Dificuldade progressiva
4. **Melhorias visuais** - Partículas, sombras
5. **Multiplayer local** - Split-screen

---

## 📝 Notas para Desenvolvedores

- **Sempre use `dt`** ao adicionar novos movimentos
- **Mantenha a hierarquia** de classes clara
- **Comente código novo** de forma educativa
- **Teste em diferentes FPS** para validar dt
- **Use o padrão** existente como referência

---

**Desenvolvido por:** Pablo Henrique, Roberto Germano, Renan Gondo, Vinicius Ferrari
**Data:** Outubro 2025
