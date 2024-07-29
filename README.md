
# A Jornada do Discípulo

![Logo do Jogo](images/game_icon.png)

A Jornada do Discípulo é um jogo educativo desenvolvido em Python, utilizando a biblioteca Pygame. O objetivo do jogo é ajudar o jogador a aprender e se divertir ao mesmo tempo, coletando itens, respondendo perguntas e evitando obstáculos para progredir através dos níveis e alcançar a maior pontuação possível.

## Funcionalidades

- Movimentação do jogador com incrementos de velocidade.
- Coleta de itens e power-ups.
- Níveis progressivos com aumento de dificuldade.
- Perguntas e respostas educativas.
- Sons e efeitos visuais para diferentes eventos do jogo.
- Sistema de pontuação e armazenamento de high scores.

## Estrutura do Projeto

```plaintext
jornada_do_discipulo/
│
├── audio.py               # Gerenciamento dos sons do jogo
├── config.py              # Configurações do jogo
├── graphics.py            # Renderização de gráficos
├── level.py               # Lógica de criação e gerenciamento de níveis
├── main.py                # Arquivo principal que executa o jogo
├── player.py              # Lógica do jogador
├── powerups.py            # Implementação dos power-ups
├── questions.py           # Gerenciamento das perguntas do jogo
├── ui.py                  # Interface do usuário
├── utils.py               # Funções utilitárias
│
├── sounds/                # Arquivos de som do jogo
│   ├── acertou.wav
│   ├── faustao-errou.wav
│   ├── damage.wav
│   ├── game_over.wav
│   ├── zerou.wav
│   ├── shield.wav
│   ├── speed.wav
│   ├── freeze.wav
│   ├── points.wav
│   ├── slow.wav
│   ├── collect.wav
│   ├── obstacle_destroyed.wav
│   ├── extra_life.wav
│   ├── explode.wav
│   ├── teleport.wav
│
├── images/                # Arquivos de imagem do jogo
│   ├── shield.png
│   ├── speed.png
│   ├── freeze.png
│   ├── points.png
│   ├── slow.png
│   ├── collect.png
│   ├── extra_life.png
│   ├── explode.png
│   ├── teleport.png
│   └── icon.png
│
├── data/                  # Arquivos de dados do jogo
│   ├── questions.xlsx
│   ├── high_scores.txt
│   └── help.txt
│
└── README.md              # Documentação do projeto
```

## Requisitos

- Python 3.8 ou superior
- Bibliotecas listadas no arquivo `requirements.txt`

## Instalação

1. Clone o repositório:

```bash
git clone https://github.com/seu_usuario/jornada_do_discipulo.git
```

2. Navegue até o diretório do projeto:

```bash
cd jornada_do_discipulo
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

## Executando o Jogo

Para iniciar o jogo, execute o arquivo `main.py`:

```bash
python main.py
```

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
