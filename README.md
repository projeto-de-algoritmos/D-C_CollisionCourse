# D&C_CollisionCourse

**Número da Lista**: 29<br>
**Conteúdo da Disciplina**: Dividir e Conquistar<br>

## Alunos
|Matrícula | Aluno |
| -- | -- |
| 18/0016563  |  Filipe Santana Machado |
| 18/0014412  |  Cainã Valença de Freitas |

## Sobre 
Este projeto implementa algoritmos de [Quadtree](https://en.wikipedia.org/wiki/Quadtree) para detectar colisão entre pontos que se movem em um campo de duas dimensões. A Quadtree segmenta o campo em quadrantes que são subdivididos recursivamente até atingir um limite específico de pontos por quadrante, permitindo que as verificações de colisão sejam realizadas apenas entre pontos no mesmo ou em quadrantes adjacentes. Isso reduz significativamente o número de comparações necessárias, tornando a detecção de colisões muito mais eficiente em termos computacionais.

Por exemplo, tendo 75 pontos no campo, ao invés de todos os pontos checarem colisão com todos os pontos (totalizando 5625 checagens). Usando quadtree é possível fazer com que essas checagens de colisão para todos os pontos variem entre 140 a 200 no nosso projeto. Na interface gráfica do projeto é possível verificar o número de checagens de colisões que estão ocorrendo a cada frame e o número de pontos que estão presentes na nossa Quadtree.

## Screenshots
Adicione 3 ou mais screenshots do projeto em funcionamento.

## Instalação 
**Linguagem**: Python<br>
**Framework**: Pygame<br>

#### Comando de instalação

A única dependência externa do projeto, além do python, é o pygame.
Na pasta raiz do repositório basta executar:

````sh
make install
```

ou

```sh
pip install -r requirements.txt
```

## Uso 

#### Execução

```sh
make run
```

ou

```sh
python -m src.game.main
```

#### Como jogar

Ao executar o jogo, irá aparecer um menu e as instruções do jogo.
Selecione a dificuldade desejada clicando no botão.

Na tela do jogo irá aparecer pontos com duas circunferências. 
A circunferência vermelha representa a área de colisão dos pontos, caso duas áreas de colisão se encontre o jogo é encerrado com Game Over.
A circunferência verde representa a área de perigo dos pontos, essa área é clicável e caso seja clicada, irá inverter a velocidade de movimento do ponto clicado.

## Outros 
Quaisquer outras informações sobre seu projeto podem ser descritas abaixo.
