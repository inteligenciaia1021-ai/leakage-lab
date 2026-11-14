import json
from pathlib import Path

import pytest

from experimento import resumo, rodar_uma_vez

SEMENTES_TESTE = range(10)


def test_resumo_calcula_estatisticas():
    r = resumo([0.5, 0.7])
    assert r["media"] == pytest.approx(0.6)
    assert r["minimo"] == 0.5
    assert r["maximo"] == 0.7
    assert r["desvio"] == pytest.approx(0.1414, abs=1e-4)


def test_mesma_semente_gera_mesmo_resultado():
    assert rodar_uma_vez(0) == rodar_uma_vez(0)


def test_vazamento_infla_a_nota():
    notas = [rodar_uma_vez(s) for s in SEMENTES_TESTE]
    media_com = sum(c for c, _ in notas) / len(notas)
    media_sem = sum(s for _, s in notas) / len(notas)
    assert media_com > media_sem + 0.20


def test_sem_vazamento_fica_perto_de_um_palpite():
    notas = [rodar_uma_vez(s)[1] for s in SEMENTES_TESTE]
    media_sem = sum(notas) / len(notas)
    assert 0.40 < media_sem < 0.60


def test_resultados_json_tem_a_estrutura_esperada():
    caminho = Path(__file__).resolve().parent.parent / "site" / "resultados.json"
    dados = json.loads(caminho.read_text(encoding="utf-8"))
    assert set(dados) == {"configuracao", "com_vazamento", "sem_vazamento"}
    assert len(dados["com_vazamento"]["notas"]) == dados["configuracao"]["repeticoes"]
    assert len(dados["sem_vazamento"]["notas"]) == dados["configuracao"]["repeticoes"]