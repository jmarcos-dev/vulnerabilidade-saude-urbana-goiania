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

PASTA_SCRIPT = Path(__file__).resolve().parent
load_dotenv(PASTA_SCRIPT / ".env")

# TODO: ajuste para o nome real da sua tabela mesclada no Postgres
NOME_TABELA = "saude.dengue22_25"

ANO_INICIO, ANO_FIM = 2022, 2025

# Se True, remove classi_fin = 8 (inconclusivo) da contagem de "casos".
# Ajuste conforme a definição de "caso" que você quer usar na análise.
EXCLUIR_INCONCLUSIVOS = False


def conectar():
    url = (
        f"postgresql+psycopg2://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}"
        f"@{os.environ['DB_HOST']}:{os.environ.get('DB_PORT', '5432')}/{os.environ['DB_NAME']}"
    )
    return create_engine(url)


def decodificar_idade(codigo):
    """
    Decodifica nu_idade_n (padrão SINAN).
    Primeiro dígito = unidade: 1=horas, 2=dias, 3=meses, 4=anos.
    Os 3 dígitos seguintes = valor.
    Horas/dias/meses são tratados como < 1 ano (idade_anos = 0).
    """
    if pd.isna(codigo):
        return None
    codigo = str(codigo).zfill(4)
    unidade, valor = codigo[0], int(codigo[1:])
    return valor if unidade == "4" else 0


def carregar_dados():
    engine = conectar()
    query = f"""
        SELECT dt_notific, dt_sin_pri, nu_idade_n, cs_sexo, classi_fin
        FROM {NOME_TABELA}
        WHERE EXTRACT(YEAR FROM dt_sin_pri) BETWEEN {ANO_INICIO} AND {ANO_FIM}
    """
    df = pd.read_sql(query, engine, parse_dates=["dt_notific", "dt_sin_pri"])

    if EXCLUIR_INCONCLUSIVOS:
        df = df[df["classi_fin"] != "8"]

    df["ano_mes"] = df["dt_sin_pri"].dt.to_period("M")
    df["idade_anos"] = df["nu_idade_n"].apply(decodificar_idade)
    return df


def resumo_mensal(df):
    """Contagem de casos por mês (total e por sexo)."""
    total = df.groupby("ano_mes").size().rename("casos_total")
    por_sexo = df.groupby(["ano_mes", "cs_sexo"]).size().unstack(fill_value=0)
    por_sexo.columns = [f"casos_{c.lower()}" for c in por_sexo.columns]
    return pd.concat([total, por_sexo], axis=1)


def medias(df, tabela_mensal):
    print(f"Total de registros ({ANO_INICIO}-{ANO_FIM}): {len(df)}\n")

    print("--- Média mensal geral de casos ---")
    print(round(tabela_mensal["casos_total"].mean(), 2))

    print("\n--- Média mensal de casos por sexo ---")
    for col in [c for c in tabela_mensal.columns if c.startswith("casos_") and c != "casos_total"]:
        print(f"{col}: {round(tabela_mensal[col].mean(), 2)}")

    print("\n--- Idade média ---")
    print(f"Geral: {round(df['idade_anos'].mean(), 2)}")
    print(df.groupby("cs_sexo")["idade_anos"].mean().round(2))

"""
FIM - dengue
"""


