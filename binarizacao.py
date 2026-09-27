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

import argparse
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


def calcular_limiar_otsu(imagem_cinza: Image.Image) -> int:
    """
    Calcula o limiar ótimo pelo método de Otsu (1979).

    A ideia é testar todos os limiares possíveis (0 a 255) e escolher aquele
    que **minimiza a variância intra-classe** (ou, de forma equivalente,
    maximiza a variância entre as classes de pixels "escuros" e "claros"),
    encontrando de forma automática o ponto de corte que melhor separa o
    fundo do objeto — sem precisar "chutar" um valor manualmente.
    """
    histograma, _ = np.histogram(np.array(imagem_cinza), bins=256, range=(0, 256))
    total_pixels = histograma.sum()

    soma_total = np.dot(np.arange(256), histograma)
    soma_fundo = 0.0
    peso_fundo = 0.0
    melhor_variancia = -1.0
    melhor_limiar = 0

    for limiar in range(256):
        peso_fundo += histograma[limiar]
        if peso_fundo == 0:
            continue

        peso_objeto = total_pixels - peso_fundo
        if peso_objeto == 0:
            break

        soma_fundo += limiar * histograma[limiar]
        media_fundo = soma_fundo / peso_fundo
        media_objeto = (soma_total - soma_fundo) / peso_objeto

        variancia_entre_classes = (
            peso_fundo * peso_objeto * (media_fundo - media_objeto) ** 2
        )

        if variancia_entre_classes >= melhor_variancia:
            melhor_variancia = variancia_entre_classes
            melhor_limiar = limiar

    return melhor_limiar


def processar(
    caminho_entrada: str,
    limiar: int = 127,
    pasta_saida: str = "saida",
    usar_otsu: bool = False,
):
    """Executa o pipeline completo e salva as três imagens resultantes.

    Retorna também o limiar efetivamente utilizado (útil quando `usar_otsu=True`,
    já que o valor é calculado automaticamente a partir da imagem).
    """
    os.makedirs(pasta_saida, exist_ok=True)

    imagem_original = carregar_imagem(caminho_entrada)
    imagem_cinza = converter_para_cinza(imagem_original)

    limiar_efetivo = calcular_limiar_otsu(imagem_cinza) if usar_otsu else limiar
    imagem_binaria = converter_para_binaria(imagem_cinza, limiar_efetivo)

    imagem_original.save(os.path.join(pasta_saida, "imagem_original.png"))
    imagem_cinza.save(os.path.join(pasta_saida, "imagem_cinza.png"))
    imagem_binaria.save(os.path.join(pasta_saida, "imagem_binaria.png"))

    return imagem_original, imagem_cinza, imagem_binaria, limiar_efetivo


def _construir_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Converte uma imagem colorida em níveis de cinza e binária (preto e branco)."
    )
    parser.add_argument(
        "entrada",
        nargs="?",
        default="imagens/entrada.png",
        help="Caminho da imagem de entrada (padrão: imagens/entrada.png)",
    )
    parser.add_argument(
        "limiar",
        nargs="?",
        type=int,
        default=127,
        help="Limiar manual de binarização, 0-255 (padrão: 127). Ignorado se --otsu for usado.",
    )
    parser.add_argument(
        "--otsu",
        action="store_true",
        help="Calcula o limiar automaticamente pelo método de Otsu, em vez de usar um valor fixo.",
    )
    parser.add_argument(
        "--saida",
        default="saida",
        help="Pasta onde as imagens de saída serão salvas (padrão: saida)",
    )
    return parser


if __name__ == "__main__":
    args = _construir_parser().parse_args()

    if not os.path.exists(args.entrada):
        print(f"Arquivo não encontrado: {args.entrada}")
        print("Coloque sua imagem em 'imagens/entrada.png' ou informe o caminho como argumento.")
        sys.exit(1)

    _, _, _, limiar_usado = processar(args.entrada, args.limiar, args.saida, args.otsu)

    metodo = "Otsu (automático)" if args.otsu else "manual"
    print("Processamento concluído! Imagens salvas na pasta ./{}/".format(args.saida))
    print(f" - método de limiar: {metodo} (valor usado: {limiar_usado})")
    print(f" - {args.saida}/imagem_original.png")
    print(f" - {args.saida}/imagem_cinza.png")
    print(f" - {args.saida}/imagem_binaria.png")
