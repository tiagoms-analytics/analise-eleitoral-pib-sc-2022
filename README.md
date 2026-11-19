# analise-eleitoral-pib-sc-2022

# Análise Eleitoral e Socioeconômica — Santa Catarina (2022)

## 1. Problema e Justificativa
Compreender como os indicadores econômicos locais influenciam o comportamento do eleitorado é essencial para o planejamento de políticas públicas e estratégias regionais. Este projeto analisa a relação entre o perfil econômico dos municípios catarinenses (classificados por faixas de PIB per capita) e a distribuição dos votos nas eleições de 2022, permitindo direcionar ações institucionais orientadas por dados.

## 2. Coleta de Dados
Foram utilizadas bases públicas, estruturadas (formato tabular CSV/XLSX) e não confidenciais obtidas por download direto em portais oficiais:
* **Tribunal Superior Eleitoral (TSE):** Dados abertos de votação por município em Santa Catarina nas eleições de 2022.
* **Instituto Brasileiro de Geografia e Estatística (IBGE):** Indicadores demográficos e econômicos municipais (população e PIB per capita).

## 3. Modelagem e Análise Exploratória (EDA)
* **Limpeza e Padronização:** Tratamento de valores ausentes, remoção de linhas de totalização e padronização dos nomes dos municípios para cruzamento entre as bases do TSE e do IBGE.
* **Categorização Socioeconômica:** Criação da dimensão **Faixa de PIB** (*PIB Baixo*, *PIB Médio*, *PIB Alto* e *Elite Econômica*) a partir do PIB per capita municipal.
* **Consolidação:** Cruzamento do total de votos por município com seus respectivos indicadores econômicos para visualização analítica.

## 4. Conclusões, Insights e Sugestões de Ação
* **Concentração Eleitoral:** A maior parcela dos votos de Santa Catarina concentra-se nos municípios de **PIB Médio** e **PIB Alto**, acompanhando os principais polos populacionais e econômicos do estado (como Joinville, Florianópolis, Blumenau e São José).
* **Segmentação Regional:** A divisão por faixas de PIB evidencia diferenças claras no peso eleitoral entre municípios menores de base agrária e centros industriais/tecnológicos.
* **Sugestões de Ação:** Priorizar campanhas de engajamento cívico e alocação de infraestrutura proporcionalmente à densidade eleitoral observada nas faixas de PIB Médio e Alto, adaptando pautas de desenvolvimento regional ao perfil econômico de cada grupo de municípios.

## 5. Dashboard Interativo (Looker Studio)
* **[Acessar Dashboard no Looker Studio] https://datastudio.google.com/s/hQcI3LWN5oc**
* **Interpretação das Visualizações:**
  * **Cartão de Visão Geral (`Soma de QT_VOTOS`):** Exibe o volume total de votos consolidados no estado, atualizando dinamicamente conforme os filtros aplicados.
  * **Gráfico de Colunas (`Votos por Faixa de PIB`):** Demonstra a predominância das faixas de *PIB Médio* e *PIB Alto* na composição do eleitorado catarinense.
  * **Tabela por Município:** Permite consultar individualmente cada município, sua faixa de PIB, total de votos e PIB per capita.
