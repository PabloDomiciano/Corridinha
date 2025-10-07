# Corridinha Maluca

Jogo de corrida 2D feito com Python e Pygame.

Este repositório contém uma versão em desenvolvimento do jogo. As últimas mudanças trazem um menu inicial navegável por teclado e mouse, um visual de menu melhorado e suporte a highscores.

## Requisitos

- Python 3.8+
- Pygame

## Instalação

No Windows (PowerShell):

```powershell
python -m pip install -r requirements.txt
```

## Executando o Jogo

```powershell
python main.py
```

Controles do menu:
- SETAS (UP/DOWN) ou mouse para navegar
- ENTER ou clique esquerdo para selecionar
- ESC para sair

Durante o jogo:
- SETAS para mover
- SPACE para disparar foguete (se disponível)

## Notas sobre mudanças recentes
- Menu inicial com gradiente de fundo, animação de pulso no item selecionado e suporte a mouse (hover/ clique).
- `requirements.txt` limpo para conter apenas `pygame`.
- Foi instalada a dependência `pygame` no ambiente.

## Desenvolvimento
- Estrutura modular: `core/` (loop e mundo), `entities/`, `ui/`, `assets/`, `utils/`.
- `data/highscores.json` armazena as pontuações.

## Próximos passos sugeridos
- Melhorias no som (fazer fallback se áudio não estiver disponível).
- Testes unitários para `ScoreManager`.
- Adição de menu de opções (volume, tela cheia, etc.).

Contribuições são bem-vindas — abra uma issue ou PR com melhorias.