# A curva que mentiu sobre o salário

Código do episódio. Os dados em `dados.py` são **fictícios**.

```
pip install numpy scikit-learn matplotlib
python passo1_original.py     # roda, desenha, entrega um número errado
python passo2_diagnostico.py  # por que o número está errado
python passo3_corrigido.py    # a correção de uma linha
python passo4_backtest.py     # o teste que separa previsão de palpite
python graficos.py            # gera os gráficos do vídeo em graficos/
```

## O que cada passo mostra

| Passo | Resultado |
|---|---|
| 1. Original | R² 0,851 no treino. Previsão para 2026: R$ 17.570, abaixo do último salário real (R$ 20.000). |
| 2. Diagnóstico | Número de condição da matriz: 8,6e17. O "ajuste" para 2010, um dado de treino, dá R$ -1.579. |
| 3. Corrigido | Contando os anos a partir de 2010: R² 0,990. 2026: R$ 24.290; 2030: R$ 43.679. |
| 4. Backtest | Treinado até 2019: erra de -27% a -57%. Treinado até 2022: erra de +13% a +36%. |

## Por que o passo 1 erra

Com o ano "cru", as colunas viram 2025, 2025² (4 milhões) e 2025³ (8 bilhões).
Nessa faixa, ano, ano² e ano³ crescem quase juntos: para o computador, são
praticamente a mesma coluna repetida. A regressão descarta a curva e sobra uma
reta, que nem passa pelos próprios dados de treino.

## Na empresa

Mesma armadilha, outros nomes: projeção de custo de nuvem, crescimento de
usuários, capacidade de fila. Antes de levar uma linha de tendência para uma
reunião, três perguntas de code review:

1. O modelo acerta os próprios dados de treino? (passo 2)
2. Ele acertaria o passado se eu escondesse os últimos anos? (passo 4)
3. Que evento poderia quebrar a premissa de que o futuro se parece com o passado?
