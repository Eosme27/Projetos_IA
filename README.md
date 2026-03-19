# Projetos_IA

## Nome: Lights Out

### Descrição
- Jogo solitário  
- Jogado num tabuleiro de luzes 5x5  
- Quando o jogo começa, um número aleatório ou um padrão pré-definido de luzes são ligadas  
- Ao tocar numa luz, ela muda o estado dela e das luzes adjacentes (verticalmente e horizontalmente)  
  - Se uma luz estava desligada, ela é ligada  
  - Se uma luz estava ligada, ela é desligada  
- O objetivo do jogo é desligar todas as luzes do tabuleiro no menor tempo possível

---

## Trabalhos Semelhantes
*(adicione aqui referências ou projetos similares)*

---

## Formulação do Jogo como um Problema de Pesquisa

### Representação em estados
- `0` → luz apagada  
- `1` → luz ligada  

### Possível estado inicial

[ [0, 0, 0, 0, 0],
[0, 1, 0, 0, 0],
[1, 1, 1, 0, 0],
[0, 1, 0, 1, 0],
[0, 0, 1, 1, 1] ]

### Estado final

[ [0, 0, 0, 0, 0],
[0, 0, 0, 0, 0],
[0, 0, 0, 0, 0],
[0, 0, 0, 0, 0],
[0, 0, 0, 0, 0] ]


---

## Operação

- **Nome:** Tocar numa Luz  
- **Precondição:** o tempo ainda não acabou  
- **Efeito:** a luz que foi tocada mais as luzes adjacentes mudam de estado  
- **Custo:** 1