import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

rng = np.random.default_rng(42)
X = rng.normal(size=(200, 20))
y = rng.integers(0, 2, size=200)

X_treino, X_teste, y_treino, y_teste = train_test_split(
    X, y, test_size=0.3, random_state=42
)

modelo = LogisticRegression(max_iter=1000)
modelo.fit(X_treino, y_treino)

print("Acurácia no treino:", modelo.score(X_treino, y_treino))
print("Acurácia no teste: ", modelo.score(X_teste, y_teste))