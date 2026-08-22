import os
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
"""
Geração de gráficos
"""

PASTA_SCRIPT = Path(__file__).resolve().parent
PASTA_FIGURAS = PASTA_SCRIPT / "reports" / "figures"
PASTA_FIGURAS.mkdir(parents=True, exist_ok=True)

load_dotenv(PASTA_SCRIPT / ".env")

ESQUEMA = "saude"
TABELA = "dengue22_25"
ANO_INICIO, ANO_FIM = 2022, 2025

# Faixas etárias usadas no histograma (ajuste se quiser outro recorte)
FAIXAS_ETARIAS = [0, 5, 12, 18, 30, 45, 60, 75, 120]
ROTULOS_FAIXAS = ["0-4", "5-11", "12-17", "18-29", "30-44", "45-59", "60-74", "75+"]


def conectar():
    url = (
        f"postgresql+psycopg2://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}"
        f"@{os.environ['DB_HOST']}:{os.environ.get('DB_PORT', '5432')}/{os.environ['DB_NAME']}"
    )
    return create_engine(url)


def carregar_dados():
    engine = conectar()
    query = f"""
        SELECT dt_sin_pri, nu_ano, ano_nasc, cs_sexo
        FROM {ESQUEMA}.{TABELA}
        WHERE EXTRACT(YEAR FROM dt_sin_pri) BETWEEN {ANO_INICIO} AND {ANO_FIM}
    """
    df = pd.read_sql(query, engine, parse_dates=["dt_sin_pri"])

    df["ano_mes"] = df["dt_sin_pri"].dt.to_period("M")
    # idade = ano da notificação - ano de nascimento (mesma regra do dengue.md, seção 5)
    df["idade"] = df["nu_ano"] - df["ano_nasc"]
    # descarta idades implausíveis (erro de digitação de ano_nasc)
    df = df[df["idade"].between(0, 110)]

    return df


def grafico_casos_mensais(df):
    serie = df.groupby("ano_mes").size()

    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.plot(serie.index.astype(str), serie.values, color="#2a78d6", linewidth=2)
    ax.set_title("Casos de dengue notificados por mês - Goiânia (2022-2025)")
    ax.set_xlabel("Mês")
    ax.set_ylabel("Casos")
    ax.tick_params(axis="x", rotation=90, labelsize=7)
    ax.grid(axis="y", color="#e1e0d9", linewidth=0.7)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(PASTA_FIGURAS / "casos_mensais.png", dpi=150)
    plt.close(fig)


def grafico_casos_por_sexo(df):
    tabela = df.groupby(["ano_mes", "cs_sexo"]).size().unstack(fill_value=0)

    fig, ax = plt.subplots(figsize=(10, 4.5))
    if "F" in tabela.columns:
        ax.plot(tabela.index.astype(str), tabela["F"], label="Feminino", color="#d55181", linewidth=2)
    if "M" in tabela.columns:
        ax.plot(tabela.index.astype(str), tabela["M"], label="Masculino", color="#2a78d6", linewidth=2)
    ax.set_title("Casos de dengue por sexo e mês - Goiânia (2022-2025)")
    ax.set_xlabel("Mês")
    ax.set_ylabel("Casos")
    ax.tick_params(axis="x", rotation=90, labelsize=7)
    ax.grid(axis="y", color="#e1e0d9", linewidth=0.7)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend()
    fig.tight_layout()
    fig.savefig(PASTA_FIGURAS / "casos_mensais_por_sexo.png", dpi=150)
    plt.close(fig)


def grafico_distribuicao_etaria(df):
    df = df.copy()
    df["faixa_etaria"] = pd.cut(
        df["idade"], bins=FAIXAS_ETARIAS, labels=ROTULOS_FAIXAS, right=False
    )
    contagem = df["faixa_etaria"].value_counts().reindex(ROTULOS_FAIXAS)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(contagem.index, contagem.values, color="#1baf7a")
    ax.set_title("Distribuição etária dos casos de dengue - Goiânia (2022-2025)")
    ax.set_xlabel("Faixa etária")
    ax.set_ylabel("Casos")
    ax.grid(axis="y", color="#e1e0d9", linewidth=0.7)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(PASTA_FIGURAS / "distribuicao_etaria.png", dpi=150)
    plt.close(fig)

