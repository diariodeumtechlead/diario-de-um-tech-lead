"""Passo 1: o código como um júnior (ou eu, anos atrás) escreveria.

Roda sem erro, desenha uma curva bonita e entrega um número.
O problema é que o número está errado, e nada avisa.
"""
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

from dados import ANOS, SALARIOS

poly = PolynomialFeatures(degree=3)
X = poly.fit_transform(ANOS.reshape(-1, 1))   # usa o ano "cru": 2010, 2025...

modelo = LinearRegression().fit(X, SALARIOS)

previsao_2026 = modelo.predict(poly.transform([[2026]]))[0]
print(f"R² no treino: {modelo.score(X, SALARIOS):.3f}")
print(f"Último salário real (2025): R$ {SALARIOS[-1]:,.0f}")
print(f"Previsão para 2026:          R$ {previsao_2026:,.0f}")
