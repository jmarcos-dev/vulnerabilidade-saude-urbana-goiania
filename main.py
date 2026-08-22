"""
Análise exploratória - Dengue Goiânia 2022-2025
Fonte: PostgreSQL (tabela já filtrada para id_municip = 520870)
Gera:
  1. Média mensal geral de casos
  2. Média mensal de casos por sexo (M/F)
  3. Idade média (geral e por sexo)
  4. Tabela mensal exportada para merge posterior com dados de clima
"""

import os
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
import analise_exploratoria as ae
import gerar_graficos as gg

"""
Análise exploratória - clima Goiânia 2022-2025
Fonte: PostgreSQL (tabela já filtrada para id_municip = 520870)
Gera:
"""


"""
FIM - clima
"""



if __name__ == "__main__":
    # --- Médias mensais, por sexo e idade ---
    df_medias = ae.carregar_dados()
    tabela_mensal = ae.resumo_mensal(df_medias)
    ae.medias(df_medias, tabela_mensal)

    saida = ae.PASTA_SCRIPT / "casos_mensais_goiania.csv"
    tabela_mensal.to_csv(saida)
    print(f"\nTabela mensal salva em {saida}")

    # --- Gráficos ---
    df_graficos = gg.carregar_dados()
    print(f"\nRegistros carregados para gráficos: {len(df_graficos)}")

    gg.grafico_casos_mensais(df_graficos)
    gg.grafico_casos_por_sexo(df_graficos)
    gg.grafico_distribuicao_etaria(df_graficos)

    print(f"Gráficos salvos em: {gg.PASTA_FIGURAS}")



