# D&C_CollisionCourse

**Número da Lista**: 29<br>
**Conteúdo da Disciplina**: Dividir e Conquistar<br>

## Alunos
|Matrícula | Aluno |
| -- | -- |
| 18/0016563  |  Filipe Santana Machado |
| 18/0014412  |  Cainã Valença de Freitas |

## Apresentação

https://youtu.be/H_vvSo_VCSU

[VIDEO DE APRESENTAÇÃO](https://github.com/projeto-de-algoritmos/D-C_CollisionCourse/blob/a3ee393f2ffac2e0938910107fae1976018dfb6c/presentation-video.mp4)

## Sobre 
Este projeto implementa algoritmos de [Quadtree](https://en.wikipedia.org/wiki/Quadtree) para detectar colisão entre pontos que se movem em um campo de duas dimensões. A Quadtree segmenta o campo em quadrantes que são subdivididos recursivamente até atingir um limite específico de pontos por quadrante, permitindo que as verificações de colisão sejam realizadas apenas entre pontos no mesmo ou em quadrantes adjacentes. Isso reduz significativamente o número de comparações necessárias, tornando a detecção de colisões muito mais eficiente em termos computacionais.

Por exemplo, tendo 75 pontos no campo, ao invés de todos os pontos checarem colisão com todos os pontos (totalizando 5625 checagens). Usando quadtree é possível fazer com que essas checagens de colisão para todos os pontos variem entre 140 a 200 no nosso projeto. Na interface gráfica do projeto é possível verificar o número de checagens de colisões que estão ocorrendo a cada frame e o número de pontos que estão presentes na nossa Quadtree.

## Screenshots
![image](https://github.com/projeto-de-algoritmos/D-C_CollisionCourse/assets/40258400/9d317952-9bf9-4848-9cea-bb34fa35f894)
![image](https://github.com/projeto-de-algoritmos/D-C_CollisionCourse/assets/40258400/2309207f-b498-40a8-a907-8bcba7356208)
![image](https://github.com/projeto-de-algoritmos/D-C_CollisionCourse/assets/40258400/55804614-57d2-40f2-8ef6-f02d33cdaded)
![image](https://github.com/projeto-de-algoritmos/D-C_CollisionCourse/assets/40258400/5259310d-201d-4718-ad89-6b97db0fb7c4)

<br>

#### Printscreen demo

Este ultimo screenshot é da versão de demonstração da Quadtree funcionando com muitos pontos.
Observe a quantidade de pontos e a quantidade de checagens de colisão por frame. Em cada frame são analisadas as colisões de todos os pontos.

![demo](https://github.com/projeto-de-algoritmos/D-C_CollisionCourse/assets/40258400/d9f624e0-71fd-4f58-878d-4df0ecbf1260)

## Instalação 
**Linguagem**: Python<br>
**Framework**: Pygame<br>

#### Comando de instalação

A única dependência externa do projeto, além do python, é o pygame.
Na pasta raiz do repositório basta executar:

```sh
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

ou então, use a flag --demo para acessar a demo

```sh
python -m src.game.main --demo
```

#### Como jogar

Ao executar o jogo, irá aparecer um menu e as instruções do jogo.
Selecione a dificuldade desejada clicando no botão.

Na tela do jogo irá aparecer pontos com duas circunferências. 
A circunferência vermelha representa a área de colisão dos pontos, caso duas áreas de colisão se encontre o jogo é encerrado com Game Over.
A circunferência verde representa a área de perigo dos pontos, essa área é clicável e caso seja clicada, irá inverter a velocidade de movimento do ponto clicado.

