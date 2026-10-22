"""Passo 3: a correção de uma linha. Contar os anos a partir do primeiro ano.

Em vez de 2010, 2025 (e 2025³ ≈ 8 bilhões), o modelo vê 0, 15 (e 15³ = 3.375).
"""
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

from dados import ANOS, SALARIOS

ORIGEM = ANOS[0]
anos_desde_inicio = (ANOS - ORIGEM).reshape(-1, 1)

poly = PolynomialFeatures(degree=3)
X = poly.fit_transform(anos_desde_inicio)
modelo = LinearRegression().fit(X, SALARIOS)

print(f"R² no treino: {modelo.score(X, SALARIOS):.3f}")
for ano in (2026, 2028, 2030):
    valor = modelo.predict(poly.transform([[ano - ORIGEM]]))[0]
    print(f"Previsão para {ano}: R$ {valor:,.0f}")
