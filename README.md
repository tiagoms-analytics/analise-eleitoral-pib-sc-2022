# Análise Eleitoral e Socioeconômica — Santa Catarina (2022)

## 1. Problema e Justificativa
* **Problema:** Análises eleitorais regionais frequentemente observam apenas o volume absoluto de votos por município, desconsiderando como a estrutura produtiva (PIB per capita) e a renda domiciliar per capita influenciam a distribuição proporcional dos votos e a participação do eleitorado.
* **Relevância:** Santa Catarina possui 295 municípios com perfis econômicos bastante distintos — desde polos portuários e industriais de altíssimo PIB per capita até municípios de pequeno porte com menor renda domiciliar.
* **Solução via Dados:** Integrar os resultados oficiais do TSE aos indicadores econômicos e demográficos do IBGE permite analisar proporções (votos por habitante e participação percentual de cada partido por faixa econômica), gerando insumos objetivos para planejamento regional e políticas públicas.

## 2. Coleta e Fontes de Dados
Foram utilizadas exclusivamente bases públicas, oficiais e estruturadas:
* **Tribunal Superior Eleitoral (TSE):** Votação nominal por seção/município nas Eleições Gerais de 2022 (`votacao_secao_2022_SC.csv` e `consulta_cand_2022_SC.csv`), filtrada exclusivamente para o cargo de **Governador (1º turno)**, totalizando **4.072.810 votos nominais** válidos em Santa Catarina (eliminando dupla contagem entre cargos simultâneos).
* **Instituto Brasileiro de Geografia e Estatística (IBGE):** População residente (Censo 2022) e PIB per capita municipal [2023] (`IBGE.csv`), além do rendimento nominal médio mensal domiciliar per capita [2022] (`tabela10295.csv` — SIDRA).

## 3. Tratamento, Modelagem e Critérios de Corte (EDA)
Todo o pipeline de limpeza e cruzamento foi automatizado em Python (`projeto_eleicao.py`), gerando a base consolidada `Base_Limpa_SC_2022.xlsx`:
* **Integridade dos 295 Municípios:** Remoção de linhas de totalização (`Total Geral`), exclusão de notas de rodapé HTML do arquivo do IBGE e normalização de caracteres/acentuação para cruzamento exato dos **295 municípios catarinenses** (`4200051` a `4220000`), resultando em **zero registros nulos ou duplicados**.
* **Estatísticas Adequadas:** Utilização de **média e mediana** (em substituição à soma) para avaliar PIB per capita e renda domiciliar per capita por grupo.
* **Critérios de Corte das Faixas de PIB per capita** (definidos a partir da distribuição quartílica estadual — Q1 = R$ 42.061 | Mediana = R$ 52.591 | Q3 = R$ 68.149 | P95 = R$ 103.423):
  * **1. PIB Baixo (< R$ 42.000):** 73 municípios (24,75% dos municípios; 10,18% da população; média de R$ 34.463,61).
  * **2. PIB Médio (R$ 42.000 a R$ 67.999):** 147 municípios (49,83% dos municípios; 50,02% da população; média de R$ 53.046,23).
  * **3. PIB Alto (R$ 68.000 a R$ 99.999):** 58 municípios (19,66% dos municípios; 33,63% da população; média de R$ 79.296,28).
  * **4. Elite Econômica (> R$ 100.000):** 17 municípios (5,76% dos municípios; 6,17% da população; média de R$ 129.628,42 — inclui polos portuários e industriais como Araquari com R$ 218.625,97 e Itajaí com R$ 182.522,93).
* **Critérios de Corte das Faixas de Renda Domiciliar Per Capita:** Baixa Renda (< R$ 1.700; 80 municípios), Média Renda (R$ 1.700 a R$ 2.199; 148 municípios) e Alta Renda (> R$ 2.200; 67 municípios).

## 4. Insights Proporcionais e Sugestões de Ação
1. **Descolamento entre PIB per capita e Renda Domiciliar na Elite Econômica:** Embora os 17 municípios da faixa **Elite Econômica** apresentem PIB per capita médio de **R$ 129.628,42**, sua **renda domiciliar média é de R$ 1.911,71** — inferior à média dos municípios de **PIB Alto (R$ 2.088,97)** e **PIB Médio (R$ 2.014,41)**. Isso ocorre porque o indicador de PIB per capita concentra grandes operações industriais, portuárias e agroindustriais que não se convertem automaticamente em maior renda média distribuída às famílias locais.
2. **Concentração Demográfica e Eleitoral nas Faixas Intermediárias:** As faixas de **PIB Médio** e **PIB Alto** concentram juntas **83,65% da população catarinense** (205 municípios), sendo decisivas para o resultado estadual no 1º turno, enquanto a análise proporcional por partido (gráfico 100% empilhado) permite comparar o desempenho relativo de **PL, PT, REPUBLICANOS, UNIÃO e PP** independentemente do tamanho populacional de cada grupo.
3. **Recomendações Estratégicas:**
   * **Políticas Públicas e Infraestrutura:** Priorizar investimentos em serviços públicos, mobilidade e infraestrutura eleitoral nos municípios de **PIB Baixo** e rápido crescimento populacional (especialmente no litoral), onde a baixa arrecadação per capita pressiona o atendimento ao cidadão.
   * **Planejamento Regional Segmentado:** Diferenciar estratégias para polos industriais/portuários (alto PIB per capita, renda domiciliar moderada) e centros urbanos de serviços/tecnologia (alta renda domiciliar), evitando tratar municípios economicamente distintos com diagnósticos homogêneos.

## 5. Dashboard Interativo (Looker Studio)
* **[Acessar Dashboard Interativo no Looker Studio](https://datastudio.google.com/s/kt5pTAQm3Ik)**
* **Recursos do Painel:** Cartões de visão geral com contagem exata dos 295 municípios e médias econômicas, filtro interativo de **Faixa de PIB**, gráfico de barras empilhadas 100% com a proporção partidária por faixa econômica e tabelas detalhadas com indicadores proporcionais.
