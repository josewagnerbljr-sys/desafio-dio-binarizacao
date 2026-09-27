"""
Gera uma figura única com as 3 imagens lado a lado
(Original | Cinza | Binária), reproduzindo o layout mostrado
no enunciado do desafio, e salva em saida/comparativo.png
"""

import os
import sys

import matplotlib.pyplot as plt

from binarizacao import processar


def gerar_comparativo(caminho_entrada: str, limiar: int = 127, pasta_saida: str = "saida"):
    original, cinza, binaria = processar(caminho_entrada, limiar, pasta_saida)

    fig, eixos = plt.subplots(1, 3, figsize=(12, 4))

    eixos[0].imshow(original)
    eixos[0].set_title("Imagem Original")
    eixos[0].axis("off")

    eixos[1].imshow(cinza, cmap="gray", vmin=0, vmax=255)
    eixos[1].set_title("Imagem em Cinza")
    eixos[1].axis("off")

    eixos[2].imshow(binaria, cmap="gray", vmin=0, vmax=255)
    eixos[2].set_title("Imagem Binária")
    eixos[2].axis("off")

    plt.tight_layout()
    caminho_saida = os.path.join(pasta_saida, "comparativo.png")
    plt.savefig(caminho_saida, dpi=150)
    print(f"Comparativo salvo em {caminho_saida}")


if __name__ == "__main__":
    caminho = sys.argv[1] if len(sys.argv) > 1 else "imagens/entrada.png"
    limiar_escolhido = int(sys.argv[2]) if len(sys.argv) > 2 else 127
    gerar_comparativo(caminho, limiar_escolhido)
