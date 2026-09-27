"""
Desafio DIO - Binarização de Imagens
=====================================

Converte uma imagem colorida para:
  1) Níveis de cinza (0 a 255)
  2) Imagem binarizada / preto e branco (apenas 0 e 255)

Uso:
    python binarizacao.py [caminho_da_imagem] [limiar]

Exemplos:
    python binarizacao.py
    python binarizacao.py imagens/entrada.png
    python binarizacao.py imagens/entrada.png 140
"""

import os
import sys

import numpy as np
from PIL import Image


def carregar_imagem(caminho: str) -> Image.Image:
    """Carrega uma imagem do disco e garante que está em RGB."""
    return Image.open(caminho).convert("RGB")


def converter_para_cinza(imagem: Image.Image) -> Image.Image:
    """
    Converte uma imagem RGB para níveis de cinza (0 a 255).

    Usa a fórmula de luminância ponderada (a mesma aplicada internamente
    pelo Pillow no modo "L"): Y = 0.299R + 0.587G + 0.114B
    """
    return imagem.convert("L")


def converter_para_binaria(imagem_cinza: Image.Image, limiar: int = 127) -> Image.Image:
    """
    Converte uma imagem em níveis de cinza para binária (0 e 255).

    Todo pixel com valor >= limiar vira 255 (branco).
    Todo pixel com valor <  limiar vira 0   (preto).
    """
    matriz = np.array(imagem_cinza)
    matriz_binaria = np.where(matriz >= limiar, 255, 0).astype(np.uint8)
    return Image.fromarray(matriz_binaria, mode="L")


def processar(caminho_entrada: str, limiar: int = 127, pasta_saida: str = "saida"):
    """Executa o pipeline completo e salva as três imagens resultantes."""
    os.makedirs(pasta_saida, exist_ok=True)

    imagem_original = carregar_imagem(caminho_entrada)
    imagem_cinza = converter_para_cinza(imagem_original)
    imagem_binaria = converter_para_binaria(imagem_cinza, limiar)

    imagem_original.save(os.path.join(pasta_saida, "imagem_original.png"))
    imagem_cinza.save(os.path.join(pasta_saida, "imagem_cinza.png"))
    imagem_binaria.save(os.path.join(pasta_saida, "imagem_binaria.png"))

    return imagem_original, imagem_cinza, imagem_binaria


if __name__ == "__main__":
    caminho = sys.argv[1] if len(sys.argv) > 1 else "imagens/entrada.png"
    limiar_escolhido = int(sys.argv[2]) if len(sys.argv) > 2 else 127

    if not os.path.exists(caminho):
        print(f"Arquivo não encontrado: {caminho}")
        print("Coloque sua imagem em 'imagens/entrada.png' ou informe o caminho como argumento.")
        sys.exit(1)

    processar(caminho, limiar_escolhido)
    print("Processamento concluído! Imagens salvas na pasta ./saida/")
    print(" - saida/imagem_original.png")
    print(" - saida/imagem_cinza.png")
    print(" - saida/imagem_binaria.png")
