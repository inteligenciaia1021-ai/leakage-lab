import numpy as np
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline

rng = np.random.default_rng(42)
X = rng.normal(size=(100, 5000))   # 100 exemplos, 5000 colunas de ruído
y = rng.integers(0, 2, size=100)   # rótulos sorteados: nada a aprender

modelo = LogisticRegression(max_iter=1000)

# ERRADO: escolhe as colunas olhando TODOS os dados e depois valida
X_selecionado = SelectKBest(f_classif, k=20).fit_transform(X, y)
nota_errada = cross_val_score(modelo, X_selecionado, y, cv=5).mean()

# CERTO: a escolha das colunas acontece dentro de cada rodada, só com o treino
pipeline = make_pipeline(SelectKBest(f_classif, k=20), modelo)
nota_certa = cross_val_score(pipeline, X, y, cv=5).mean()

print(f"Com vazamento: {nota_errada:.3f}")
print(f"Sem vazamento: {nota_certa:.3f}")