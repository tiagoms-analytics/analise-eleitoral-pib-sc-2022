import os
import re
import html
import unicodedata
import pandas as pd

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))

def encontrar_arquivo(caminhos_possiveis, nome_busca):
    for caminho in caminhos_possiveis:
        if os.path.exists(caminho):
            return caminho
    for base_dir in [PASTA_SCRIPT, r"D:\Eleiçoes", r"D:\Estudos_EBAC"]:
        if os.path.exists(base_dir):
            for root, _, files in os.walk(base_dir):
                if nome_busca in files:
                    return os.path.join(root, nome_busca)
    raise FileNotFoundError(f"Não encontrei {nome_busca}. Coloque-o na pasta: {PASTA_SCRIPT}")

def normalizar(texto):
    if pd.isna(texto):
        return ""
    s = html.unescape(str(texto)).upper().strip()
    s = "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")
    s = re.sub(r"[^A-Z0-9 ]", " ", s)
    return " ".join(s.split())

# 1. Localizar os 3 arquivos
arq_tse = encontrar_arquivo([
    os.path.join(PASTA_SCRIPT, "votacao_secao_2022_SC.csv"),
    r"D:\Eleiçoes\votacao_secao_2022_SC\votacao_secao_2022_SC.csv",
], "votacao_secao_2022_SC.csv")

arq_ibge = encontrar_arquivo([
    os.path.join(PASTA_SCRIPT, "IBGE.csv"),
    r"D:\Eleiçoes\IBGE\787723dfbb0e93e9463645ecaabad245.csv",
], "IBGE.csv")

arq_renda = encontrar_arquivo([
    os.path.join(PASTA_SCRIPT, "tabela10295.csv"),
    r"D:\Eleiçoes\tabela10295.csv",
], "tabela10295.csv")

print("Lendo arquivos...")

# 2. Limpar IBGE (295 municípios exatos de SC)
with open(arq_ibge, "r", encoding="utf-8", errors="replace") as f:
    ibge_txt = html.unescape(f.read())

temp_ibge = os.path.join(PASTA_SCRIPT, "_temp_ibge.csv")
with open(temp_ibge, "w", encoding="utf-8") as f:
    f.write(ibge_txt)

df_ibge = pd.read_csv(temp_ibge, skiprows=1)
os.remove(temp_ibge)

df_ibge["Codigo_IBGE"] = pd.to_numeric(df_ibge["Código [-]"], errors="coerce")
df_ibge = df_ibge[df_ibge["Codigo_IBGE"].notna()].copy()
df_ibge["Codigo_IBGE"] = df_ibge["Codigo_IBGE"].astype(int)
df_ibge["Municipio"] = df_ibge["Município [-]"].str.strip()
df_ibge["chave_mun"] = df_ibge["Municipio"].apply(normalizar)
df_ibge["Populacao_2022"] = pd.to_numeric(df_ibge["População no último censo - pessoas [2022]"], errors="coerce")
df_ibge["PIB_Per_Capita"] = pd.to_numeric(df_ibge["PIB per capita - R$ [2023]"], errors="coerce")

# 3. Limpar Renda Domiciliar Per Capita (SIDRA Tabela 10295)
df_renda = pd.read_csv(arq_renda, sep=";", skiprows=5, encoding="utf-8-sig")
df_renda = df_renda[df_renda["Cód."].astype(str).str.startswith("42")].copy()
df_renda["Codigo_IBGE"] = df_renda["Cód."].astype(int)
df_renda["Renda_Domiciliar_Per_Capita"] = df_renda["Total"].astype(str).str.replace(",", ".").astype(float)

# 4. Ler votação do TSE em blocos (rápido) e filtrar GOVERNADOR - 1º Turno - votos nominais
cols_tse = ["NR_TURNO", "DS_CARGO", "NM_MUNICIPIO", "NR_VOTAVEL", "NM_VOTAVEL", "QT_VOTOS"]
partes_gov = []
for chunk in pd.read_csv(arq_tse, sep=";", encoding="latin1", usecols=cols_tse, chunksize=250_000):
    filtro = chunk[
        (chunk["DS_CARGO"] == "GOVERNADOR") &
        (chunk["NR_TURNO"] == 1) &
        (~chunk["NR_VOTAVEL"].isin([95, 96]))
    ]
    if not filtro.empty:
        partes_gov.append(filtro)

df_gov = pd.concat(partes_gov, ignore_index=True)

mapa_partidos = {
    22: "PL", 13: "PT", 10: "REPUBLICANOS", 44: "UNIÃO", 11: "PP",
    30: "NOVO", 12: "PDT", 16: "PSTU", 29: "PCO", 90: "PROS"
}
df_gov["Partido"] = df_gov["NR_VOTAVEL"].map(mapa_partidos).fillna(df_gov["NR_VOTAVEL"].astype(str))
df_gov["chave_mun"] = df_gov["NM_MUNICIPIO"].apply(normalizar)

# Agregar por município e por partido
votos_mun = df_gov.groupby("chave_mun", as_index=False)["QT_VOTOS"].sum().rename(columns={"QT_VOTOS": "Total_Votos_Gov_1T"})
votos_part_long = df_gov.groupby(["chave_mun", "Partido", "NM_VOTAVEL"], as_index=False)["QT_VOTOS"].sum().rename(columns={"NM_VOTAVEL": "Candidato", "QT_VOTOS": "Votos_Partido"})
votos_part_wide = df_gov.pivot_table(index="chave_mun", columns="Partido", values="QT_VOTOS", aggfunc="sum", fill_value=0).reset_index()

# 5. Classificações Socioeconômicas
def classificar_pib(v):
    if v < 42000:
        return "1. PIB Baixo (< R$ 42 mil)"
    elif v < 68000:
        return "2. PIB Médio (R$ 42 mil a R$ 68 mil)"
    elif v < 100000:
        return "3. PIB Alto (R$ 68 mil a R$ 100 mil)"
    else:
        return "4. Elite Econômica (> R$ 100 mil)"

def classificar_renda(v):
    if v < 1700:
        return "1. Baixa Renda (< R$ 1.700)"
    elif v < 2200:
        return "2. Média Renda (R$ 1.700 a R$ 2.200)"
    else:
        return "3. Alta Renda (> R$ 2.200)"

# 6. Montar Aba 1: Municipios_295
base_mun = (
    df_ibge[["Codigo_IBGE", "Municipio", "chave_mun", "Populacao_2022", "PIB_Per_Capita"]]
    .merge(df_renda[["Codigo_IBGE", "Renda_Domiciliar_Per_Capita"]], on="Codigo_IBGE", how="left")
    .merge(votos_mun, on="chave_mun", how="left")
    .merge(votos_part_wide, on="chave_mun", how="left")
)

base_mun["Faixa_de_PIB"] = base_mun["PIB_Per_Capita"].apply(classificar_pib)
base_mun["Faixa_de_Renda"] = base_mun["Renda_Domiciliar_Per_Capita"].apply(classificar_renda)
base_mun["Votos_Por_Habitante_Pct"] = (base_mun["Total_Votos_Gov_1T"] / base_mun["Populacao_2022"]) * 100

for p in ["PL", "PT", "REPUBLICANOS", "UNIÃO", "PP", "NOVO", "PDT"]:
    if p in base_mun.columns:
        base_mun[f"Pct_{p}"] = (base_mun[p] / base_mun["Total_Votos_Gov_1T"]) * 100

# 7. Montar Aba 2: Partidos_Por_Municipio
base_partidos = (
    base_mun[["Codigo_IBGE", "Municipio", "chave_mun", "Faixa_de_PIB", "Faixa_de_Renda", "Total_Votos_Gov_1T"]]
    .merge(votos_part_long, on="chave_mun", how="inner")
)
base_partidos["Pct_Votos_Municipio"] = (base_partidos["Votos_Partido"] / base_partidos["Total_Votos_Gov_1T"]) * 100

base_mun = base_mun.drop(columns=["chave_mun"]).sort_values("Municipio")
base_partidos = base_partidos.drop(columns=["chave_mun"]).sort_values(["Municipio", "Votos_Partido"], ascending=[True, False])

assert len(base_mun) == 295, f"Erro: esperado 295 municípios, obtido {len(base_mun)}"
assert base_mun["Total_Votos_Gov_1T"].isna().sum() == 0, "Erro: existem municípios sem votos!"

saida = os.path.join(PASTA_SCRIPT, "Base_Limpa_SC_2022.xlsx")
with pd.ExcelWriter(saida, engine="openpyxl") as writer:
    base_mun.to_excel(writer, sheet_name="Municipios_295", index=False)
    base_partidos.to_excel(writer, sheet_name="Partidos_Por_Municipio", index=False)

print("\nSUCESSO ABSOLUTO!")
print(f"Arquivo salvo em: {saida}")
print(f"Total de municípios: {len(base_mun)} (zero vazios)")
print(f"Total oficial de votos nominais (Governador 1T): {int(base_mun['Total_Votos_Gov_1T'].sum()):,}".replace(",", "."))