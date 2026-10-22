"""Passo 2: não confiar no número. Ir olhar o que o modelo aprendeu.

Três perguntas de code review:
1. O ajuste faz sentido nos próprios dados de treino?
2. Quais coeficientes ele aprendeu?
3. A matriz de entrada é "bem comportada"? (número de condição)
"""
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

from dados import ANOS, SALARIOS

poly = PolynomialFeatures(degree=3)
X = poly.fit_transform(ANOS.reshape(-1, 1))
modelo = LinearRegression().fit(X, SALARIOS)

print("Colunas de uma linha de X (1, ano, ano², ano³):")
print(X[-1])
print(f"\nNúmero de condição de X: {np.linalg.cond(X):.1e}")
print("Coeficientes aprendidos:", modelo.coef_)

ajuste = modelo.predict(X)
print(f"\nSalário 'previsto' para {ANOS[0]} (dado de treino!): R$ {ajuste[0]:,.0f}")
print(f"Salário real em {ANOS[0]}:                     R$ {SALARIOS[0]:,.0f}")
