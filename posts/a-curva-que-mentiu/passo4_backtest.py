"""Passo 4: o teste que separa previsão de palpite. Backtest.

Finge que estamos no passado: treina só com os anos até um corte
e compara a previsão com o que aconteceu de verdade depois.
"""
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

from dados import ANOS, SALARIOS

ORIGEM = ANOS[0]


def backtest(ano_de_corte: int) -> None:
    treino = ANOS <= ano_de_corte
    poly = PolynomialFeatures(degree=3)
    X_treino = poly.fit_transform((ANOS[treino] - ORIGEM).reshape(-1, 1))
    modelo = LinearRegression().fit(X_treino, SALARIOS[treino])

    print(f"\nTreinando só até {ano_de_corte}:")
    for ano, real in zip(ANOS[~treino], SALARIOS[~treino]):
        previsto = modelo.predict(poly.transform([[ano - ORIGEM]]))[0]
        erro = (previsto - real) / real * 100
        print(f"  {ano}: previsto R$ {previsto:>7,.0f} | real R$ {real:>7,.0f} | erro {erro:+.0f}%")


backtest(2019)   # antes da troca de emprego
backtest(2022)   # logo depois da troca
