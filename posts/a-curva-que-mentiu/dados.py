"""Carreira FICTÍCIA de uma pessoa desenvolvedora.

Os números são inventados para o episódio. Não são dados reais de ninguém.
O formato imita uma carreira comum: crescimento lento até 2019 e uma troca
de emprego em 2020 que muda o ritmo.
"""
import numpy as np

ANOS = np.array([2010, 2012, 2013, 2015, 2016, 2018, 2019,
                 2020, 2021, 2022, 2023, 2024, 2025])

SALARIOS = np.array([1800, 2400, 2700, 3500, 3900, 4800, 5300,
                     8000, 10500, 13000, 15000, 17500, 20000], dtype=float)

ANO_DA_TROCA = 2020  # o "evento" que nenhum modelo enxerga antes de acontecer
