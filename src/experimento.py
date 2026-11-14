import json
from pathlib import Path

import numpy as np
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline

N_AMOSTRAS = 100
N_COLUNAS = 5000
K = 20
FOLDS = 5
SEMENTES = range(50)


def rodar_uma_vez(semente):
    rng = np.random.default_rng(semente)
    X = rng.normal(size=(N_AMOSTRAS, N_COLUNAS))
    y = rng.integers(0, 2, size=N_AMOSTRAS)
    modelo = LogisticRegression(max_iter=1000)

    # ERRADO: escolhe as colunas olhando todos os dados
    X_sel = SelectKBest(f_classif, k=K).fit_transform(X, y)
    com_vazamento = cross_val_score(modelo, X_sel, y, cv=FOLDS).mean()

    # CERTO: a escolha acontece dentro de cada rodada
    pipeline = make_pipeline(SelectKBest(f_classif, k=K), modelo)
    sem_vazamento = cross_val_score(pipeline, X, y, cv=FOLDS).mean()

    return com_vazamento, sem_vazamento


def resumo(valores):
    v = np.array(valores)
    return {
        "media": round(float(v.mean()), 4),
        "minimo": round(float(v.min()), 4),
        "maximo": round(float(v.max()), 4),
        "desvio": round(float(v.std(ddof=1)), 4),
    }


def main():
    com, sem = [], []
    for semente in SEMENTES:
        a, b = rodar_uma_vez(semente)
        com.append(a)
        sem.append(b)

    resultado = {
        "configuracao": {
            "amostras": N_AMOSTRAS,
            "colunas": N_COLUNAS,
            "colunas_selecionadas": K,
            "folds": FOLDS,
            "repeticoes": len(SEMENTES),
        },
        "com_vazamento": {"notas": [round(x, 4) for x in com], **resumo(com)},
        "sem_vazamento": {"notas": [round(x, 4) for x in sem], **resumo(sem)},
    }

    destino = Path(__file__).resolve().parent.parent / "site" / "resultados.json"
    destino.write_text(json.dumps(resultado, ensure_ascii=False, indent=2), encoding="utf-8")

    for nome in ("com_vazamento", "sem_vazamento"):
        r = resultado[nome]
        print(f"{nome}: média {r['media']}  mín {r['minimo']}  máx {r['maximo']}  desvio {r['desvio']}")
    print(f"Arquivo salvo em: {destino}")


if __name__ == "__main__":
    main()