# Dados de dengue - Goiânia

## 1. Objetivo

Coletar, tratar e quantificar a quantidade de casos de dengue em Goiânia entre 2022 e 2025, 
com foco em idade e sexo.

## 2. Fontes

- Fonte: SUS
- Localidade: Goiânia/GO
- Período: 2022-2025
- Frequência: Diária
- Formato original: .csv

## 3. Dados utilizados

O conjunto de dados contém registros diários das seguintes variáveis:
- id_municipio (código do múnicipio IBGE)
- Gênero (M/F)
- ano_nasc (ano de nascimento)

## 4. Armazenamento

Os dados foram importados para:
- Banco: `vulnerabilidade_saude_goiania`
- Schema: `saude`
- Tabela: `dengue22_25`

Total de registros:
174.113

Período:

01/01/2022 a 31/12/2025

## 5. Qualidade e completude

Foram realizadas verificações preliminares para avaliar:
- Quantidade total de registros;
- período das notificações;
- município dos registros;
- valores nulos;
- distribuição da variável `CS_SEXO`;
- disponibilidade de `ANO_NASC`;
- consistência das datas de notificação.

A idade dos indivíduos será obtida a partir do ano de nascimento e do ano da notificação, permitindo 
posteriormente a criação de faixas etárias para análise.

### Principais resultadops


## 6. Análise exploratória

