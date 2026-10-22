"""Gera os 4 gráficos do episódio (1920x1080, fundo escuro, para o vídeo)."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter, MultipleLocator
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

from dados import ANOS, ANO_DA_TROCA, SALARIOS

SURFACE = "#1a1a19"
TEXT = "#f0efec"
TEXT_2 = "#c3c2b7"
GRID = "#3a3a37"
DADOS = "#3987e5"     # azul: o que aconteceu
MODELO = "#d95926"    # laranja: o que o modelo diz
FUTURO = "#199e70"    # verde-água: o que veio depois do corte

SAIDA = Path(__file__).parent / "graficos"
SAIDA.mkdir(exist_ok=True)
REAIS = FuncFormatter(lambda v, _: f"R$ {v/1000:.0f} mil".replace(".", ","))
ORIGEM = ANOS[0]


def ajustar(anos, salarios, centralizar=True):
    origem = ORIGEM if centralizar else 0
    poly = PolynomialFeatures(degree=3)
    modelo = LinearRegression().fit(poly.fit_transform((anos - origem).reshape(-1, 1)), salarios)
    return lambda a: modelo.predict(poly.transform((np.asarray(a, float) - origem).reshape(-1, 1)))


def base(titulo, subtitulo):
    fig, ax = plt.subplots(figsize=(19.2, 10.8), dpi=100)
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    for lado in ("left", "bottom"):
        ax.spines[lado].set_color(GRID)
    ax.tick_params(colors=TEXT_2, labelsize=20, length=0, pad=10)
    ax.grid(axis="y", color=GRID, linewidth=1)
    ax.yaxis.set_major_formatter(REAIS)
    ax.yaxis.set_major_locator(MultipleLocator(5000))
    ax.xaxis.set_major_locator(MultipleLocator(2))
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0f}"))
    fig.text(0.06, 0.93, titulo, color=TEXT, fontsize=40, weight="bold")
    fig.text(0.06, 0.875, subtitulo, color=TEXT_2, fontsize=24)
    fig.subplots_adjust(left=0.11, right=0.95, top=0.82, bottom=0.1)
    return fig, ax


def pontos(ax, anos=ANOS, salarios=SALARIOS, cor=DADOS, rotulo="Salário real"):
    ax.scatter(anos, salarios, s=180, color=cor, edgecolor=SURFACE, linewidth=2, zorder=5, label=rotulo)


def legenda(ax):
    leg = ax.legend(loc="upper left", fontsize=22, frameon=False, labelcolor=TEXT)
    return leg


def salvar(fig, nome):
    fig.savefig(SAIDA / nome, facecolor=SURFACE)
    plt.close(fig)


# 1. O modelo original: roda, desenha e erra
prever = ajustar(ANOS, SALARIOS, centralizar=False)
x = np.linspace(2010, 2026, 200)
fig, ax = base("O modelo prevê que o salário vai cair", "Polinômio de grau 3 com o ano \"cru\" (2010, 2025...)")
ax.plot(x, prever(x), color=MODELO, linewidth=3, label="Curva do modelo")
pontos(ax)
p26 = prever([2026])[0]
ax.scatter([2026], [p26], s=260, marker="D", color=MODELO, edgecolor=TEXT, linewidth=2, zorder=6)
ax.annotate(f"2026: R$ {p26:,.0f}".replace(",", "."), (2026, p26), xytext=(0, -120), ha="right",
            textcoords="offset points", color=TEXT, fontsize=24, arrowprops=dict(arrowstyle="-", color=TEXT_2))
ax.annotate("2010: R$ -1.579 (negativo!)", (2010, prever([2010])[0]), xytext=(30, -10),
            textcoords="offset points", color=TEXT, fontsize=24)
ax.axhline(0, color=TEXT_2, linewidth=1)
legenda(ax)
salvar(fig, "1-modelo-original.png")

# 2. Corrigido: ajusta bem o passado e explode no futuro
prever = ajustar(ANOS, SALARIOS)
passado, futuro = np.linspace(2010, 2025, 200), np.linspace(2025, 2030, 80)
fig, ax = base("Corrigido: ótimo no passado, perigoso no futuro", "Mesmo modelo, contando os anos a partir de 2010")
ax.plot(passado, prever(passado), color=MODELO, linewidth=3, label="Curva do modelo")
ax.plot(futuro, prever(futuro), color=MODELO, linewidth=3, linestyle=(0, (6, 4)), label="Extrapolação")
pontos(ax)
p30 = prever([2030])[0]
ax.annotate(f"2030: R$ {p30:,.0f}".replace(",", "."), (2030, p30), xytext=(-330, -10),
            textcoords="offset points", color=TEXT, fontsize=24)
legenda(ax)
salvar(fig, "2-modelo-corrigido.png")

# 3 e 4. Backtests
for corte, nome, titulo in [
    (2019, "3-backtest-2019.png", "Treinado até 2019: errou por mais da metade"),
    (2022, "4-backtest-2022.png", "Treinado até 2022: errou para o outro lado"),
]:
    treino = ANOS <= corte
    prever = ajustar(ANOS[treino], SALARIOS[treino])
    fig, ax = base(titulo, f"O modelo só viu os pontos até {corte}. Os verdes vieram depois.")
    xa = np.linspace(2010, corte, 150)
    xb = np.linspace(corte, 2025, 80)
    ax.plot(xa, prever(xa), color=MODELO, linewidth=3, label="Curva do modelo")
    ax.plot(xb, prever(xb), color=MODELO, linewidth=3, linestyle=(0, (6, 4)), label="Previsão")
    pontos(ax, ANOS[treino], SALARIOS[treino], DADOS, "O que o modelo viu")
    pontos(ax, ANOS[~treino], SALARIOS[~treino], FUTURO, "O que aconteceu depois")
    ax.axvline(corte + 0.5, color=TEXT_2, linewidth=1, linestyle=":")
    if corte == 2019:
        ax.annotate("Troca de emprego", (ANO_DA_TROCA, SALARIOS[ANOS == ANO_DA_TROCA][0]), xytext=(-260, 60),
                    textcoords="offset points", color=TEXT, fontsize=22, arrowprops=dict(arrowstyle="-", color=TEXT_2))
    legenda(ax)
    salvar(fig, nome)

print("Gráficos em", SAIDA)
