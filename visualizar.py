"""
Gera duas figuras a partir do processamento:

1. saida/comparativo.png
   As 3 imagens lado a lado (Original | Cinza | Binária), reproduzindo o
   layout mostrado no enunciado do desafio.

2. saida/histograma.png
   Histograma de níveis de cinza da imagem, com uma linha vertical marcando
   o limiar de binarização usado — útil para visualizar e justificar
   por que aquele ponto de corte separa bem "fundo" de "objeto".
"""

import argparse
import os

import matplotlib.pyplot as plt
import numpy as np

from binarizacao import processar


def gerar_comparativo(imagem_original, imagem_cinza, imagem_binaria, limiar, pasta_saida):
    fig, eixos = plt.subplots(1, 3, figsize=(12, 4))

    eixos[0].imshow(imagem_original)
    eixos[0].set_title("Imagem Original")
    eixos[0].axis("off")

    eixos[1].imshow(imagem_cinza, cmap="gray", vmin=0, vmax=255)
    eixos[1].set_title("Imagem em Cinza")
    eixos[1].axis("off")

    eixos[2].imshow(imagem_binaria, cmap="gray", vmin=0, vmax=255)
    eixos[2].set_title(f"Imagem Binária (limiar={limiar})")
    eixos[2].axis("off")

    plt.tight_layout()
    caminho_saida = os.path.join(pasta_saida, "comparativo.png")
    plt.savefig(caminho_saida, dpi=150)
    plt.close(fig)
    print(f"Comparativo salvo em {caminho_saida}")


def gerar_histograma(imagem_cinza, limiar, pasta_saida):
    valores = np.array(imagem_cinza).flatten()

    fig, eixo = plt.subplots(figsize=(8, 4))
    eixo.hist(valores, bins=256, range=(0, 256), color="#555555")
    eixo.axvline(limiar, color="red", linestyle="--", linewidth=2, label=f"Limiar = {limiar}")
    eixo.set_title("Histograma de níveis de cinza")
    eixo.set_xlabel("Intensidade do pixel (0-255)")
    eixo.set_ylabel("Quantidade de pixels")
    eixo.legend()

    plt.tight_layout()
    caminho_saida = os.path.join(pasta_saida, "histograma.png")
    plt.savefig(caminho_saida, dpi=150)
    plt.close(fig)
    print(f"Histograma salvo em {caminho_saida}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Gera o comparativo visual e o histograma do processo de binarização."
    )
    parser.add_argument("entrada", nargs="?", default="imagens/entrada.png")
    parser.add_argument("limiar", nargs="?", type=int, default=127)
    parser.add_argument("--otsu", action="store_true", help="Usa limiar automático de Otsu")
    parser.add_argument("--saida", default="saida")
    args = parser.parse_args()

    original, cinza, binaria, limiar_usado = processar(
        args.entrada, args.limiar, args.saida, args.otsu
    )
    gerar_comparativo(original, cinza, binaria, limiar_usado, args.saida)
    gerar_histograma(cinza, limiar_usado, args.saida)
