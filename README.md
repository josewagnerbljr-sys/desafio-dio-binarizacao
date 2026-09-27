# Desafio DIO — Binarização de Imagens

Implementação em Python do algoritmo apresentado na aula, transformando uma
imagem colorida em:

1. **Níveis de cinza** (0 a 255)
2. **Imagem binarizada** (apenas 0 e 255 — preto e branco)

## 📷 Resultado

| Original | Cinza | Binária |
|---|---|---|
| ![original](saida/imagem_original.png) | ![cinza](saida/imagem_cinza.png) | ![binaria](saida/imagem_binaria.png) |

> Imagem de exemplo gerada proceduralmente (`imagens/entrada.png`) apenas
> para demonstração do pipeline. Substitua por qualquer imagem sua — o
> script funciona com qualquer `.png`/`.jpg`.

## 🧠 Como funciona

- **Escala de cinza:** cada pixel RGB é convertido para um único valor de
  luminância usando a fórmula ponderada `Y = 0.299R + 0.587G + 0.114B`
  (aplicada pelo Pillow no modo `"L"`).
- **Binarização (thresholding):** cada pixel em cinza é comparado a um
  limiar (padrão `127`). Valores `>= limiar` viram branco (`255`) e valores
  `< limiar` viram preto (`0`).

## 📂 Estrutura

```
.
├── binarizacao.py     # Pipeline principal (cinza + binária)
├── visualizar.py       # Gera o comparativo lado a lado (como no enunciado)
├── imagens/
│   └── entrada.png      # Imagem de exemplo
├── saida/               # Resultados gerados (criado automaticamente)
├── requirements.txt
└── README.md
```

## ▶️ Como executar

```bash
# instalar dependências
pip install -r requirements.txt

# gerar apenas as imagens (cinza e binária)
python binarizacao.py imagens/entrada.png 127

# gerar também o comparativo lado a lado (igual ao print do desafio)
python visualizar.py imagens/entrada.png 127
```

O segundo argumento (`127`) é o limiar de binarização — opcional, ajuste
conforme o contraste da sua imagem.

## 🛠️ Tecnologias

- Python 3
- Pillow (manipulação de imagem)
- NumPy (operações vetorizadas sobre a matriz de pixels)
- Matplotlib (visualização comparativa)

## 📚 Contexto do desafio

Desafio da trilha de Visão Computacional / Processamento de Imagens da
[DIO](https://www.dio.me/), a partir do exemplo de algoritmo de binarização
apresentado em aula.
