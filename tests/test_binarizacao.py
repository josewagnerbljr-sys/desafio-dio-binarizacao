"""Testes unitários para o pipeline de binarização de imagens."""

import numpy as np
import pytest
from PIL import Image

from binarizacao import (
    calcular_limiar_otsu,
    converter_para_binaria,
    converter_para_cinza,
)


@pytest.fixture
def imagem_rgb_simples() -> Image.Image:
    """Imagem 4x4: metade preta, metade branca (RGB puro)."""
    matriz = np.zeros((4, 4, 3), dtype=np.uint8)
    matriz[:, 2:] = 255  # metade direita branca
    return Image.fromarray(matriz, mode="RGB")


def test_converter_para_cinza_retorna_modo_L(imagem_rgb_simples):
    resultado = converter_para_cinza(imagem_rgb_simples)
    assert resultado.mode == "L"
    assert resultado.size == imagem_rgb_simples.size


def test_converter_para_cinza_preserva_extremos(imagem_rgb_simples):
    cinza = converter_para_cinza(imagem_rgb_simples)
    matriz = np.array(cinza)
    assert matriz[0, 0] == 0    # área preta
    assert matriz[0, 3] == 255  # área branca


def test_converter_para_binaria_so_tem_dois_valores(imagem_rgb_simples):
    cinza = converter_para_cinza(imagem_rgb_simples)
    binaria = converter_para_binaria(cinza, limiar=127)
    valores_unicos = set(np.array(binaria).flatten().tolist())
    assert valores_unicos.issubset({0, 255})


def test_converter_para_binaria_respeita_limiar():
    # Um único nível de cinza (100) — deve virar preto com limiar 150
    # e branco com limiar 50.
    cinza = Image.fromarray(np.full((2, 2), 100, dtype=np.uint8), mode="L")

    escuro = converter_para_binaria(cinza, limiar=150)
    claro = converter_para_binaria(cinza, limiar=50)

    assert np.array(escuro).max() == 0
    assert np.array(claro).min() == 255


def test_calcular_limiar_otsu_imagem_bimodal():
    # Metade da imagem com valor 10 (escuro), metade com valor 240 (claro):
    # o limiar de Otsu deve cair claramente entre os dois grupos.
    matriz = np.zeros((10, 10), dtype=np.uint8)
    matriz[:, :5] = 10
    matriz[:, 5:] = 240
    cinza = Image.fromarray(matriz, mode="L")

    limiar = calcular_limiar_otsu(cinza)

    assert 10 < limiar < 240


def test_calcular_limiar_otsu_retorna_inteiro_no_intervalo_valido():
    matriz = np.random.default_rng(42).integers(0, 256, size=(20, 20), dtype=np.uint8)
    cinza = Image.fromarray(matriz, mode="L")

    limiar = calcular_limiar_otsu(cinza)

    assert isinstance(limiar, int)
    assert 0 <= limiar <= 255
