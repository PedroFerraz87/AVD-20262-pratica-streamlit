# Prompt preenchido: rascunhos de layout → esqueleto do app

Use este prompt anexando as duas imagens de referência listadas abaixo. Os
rascunhos atuais são wireframes digitais; se a atividade exigir desenhos feitos
à mão, substitua-os pelas fotos dos rascunhos finais antes de enviar.

## Contexto

Sou estudante da disciplina Análise e Visualização de Dados da Cesar School,
período 2026.2. Este projeto apresenta uma análise exploratória de partidas do
futebol brasileiro em dois dashboards Streamlit:

- **Dashboard 1 — Análise:** explorar correlações entre variáveis quantitativas
  e comparar suas distribuições.
- **Dashboard 2 — KPIs:** resumir volume de partidas, média de gols e proporção
  dos resultados, com gráficos interativos e filtros cruzados.

O dataset tratado contém 10.296 partidas e é disponibilizado no repositório em
`data/clean/dataset.csv`. Os nomes de coluna devem ser usados exatamente como
estão no CSV.

## Entrada

Considere e anexe estas duas imagens do repositório:

- Dashboard 1: `entregas/rascunho-dashboard1.png`
- Dashboard 2: `entregas/rascunho-dashboard2.png`

### Colunas disponíveis

O CSV contém as seguintes 23 colunas:

`tournament`, `home`, `home_goal`, `away_goal`, `away`, `home_corner`,
`away_corner`, `home_attack`, `away_attack`, `home_shots`, `away_shots`, `time`,
`date`, `ht_diff`, `at_diff`, `ht_result`, `at_result`, `total_corners`,
`mandante_venceu`, `jogo_com_gols`, `has_advanced_stats`, `away_shots_log`,
`periodo_jogo`.

Use como variáveis quantitativas do Dashboard 1:
`home_goal`, `away_goal`, `home_corner`, `away_corner`, `home_attack`,
`away_attack`, `home_shots`, `away_shots`, `ht_diff`, `at_diff` e
`total_corners`. Algumas estatísticas avançadas podem conter valores ausentes.
Não invente definições para campos cuja semântica não esteja clara no projeto.

Os resultados apresentados na interface devem ser derivados da comparação de
`home_goal` e `away_goal`: vitória mandante, empate ou vitória visitante.
Considere somente essas três classes ao calcular as proporções de resultado;
partidas sem resultado classificável não entram nesse denominador.

### Perguntas que os dashboards devem ajudar a responder

**Dashboard 1**

- Como as variáveis quantitativas se associam monotonicamente? Use correlação
  de Spearman e apresente cada par de variáveis uma única vez, sem valores na
  diagonal nem no triângulo repetido.
- Como se distribuem as variáveis selecionadas? Permita selecionar várias e
  mostre histogramas separados, organizados lado a lado, para facilitar a
  comparação.
- Como as seleções de torneio, equipe, resultado, período e intervalo numérico
  alteram os dados exibidos?

**Dashboard 2**

- Quantas partidas há no recorte atual e qual é a média de gols por partida?
- Qual a proporção de vitórias mandantes, empates e vitórias visitantes entre
  partidas classificáveis no recorte?
- Como os resultados se distribuem e qual é a média de gols por torneio?
- Como a média de gols por partida varia ao longo dos anos?
- Como uma seleção de resultado ou torneio nos gráficos afeta os KPIs e o outro
  gráfico, incluindo a série temporal?

### Descrição complementar dos rascunhos

- **Dashboard 1:** título e subtítulo no topo; filtros em uma barra lateral;
  área principal com correlação de um lado e distribuição do outro. A matriz
  mostra somente um valor por par. A distribuição permite múltiplas variáveis
  e dispõe os histogramas em uma grade de duas colunas.
- **Dashboard 2:** título de indicadores filtrados; cinco cartões de KPI
  (partidas, média de gols, vitórias mandantes, empates e vitórias visitantes);
  abaixo, gráfico de partidas por resultado e gráfico de média de gols por
  torneio lado a lado; em seguida, gráfico de linha com a evolução anual da
  média de gols. As seleções dos gráficos de resultado e torneio também
  filtram a série temporal. Os filtros da barra lateral atualizam os
  indicadores e os três gráficos.

## Restrições

- Use Python, Streamlit e as bibliotecas que já constam em `requirements.txt`.
  Use Plotly para os gráficos do Dashboard 1 e Altair para os gráficos
  interativos do Dashboard 2.
- Leia o CSV por meio de `load_data` em `src/data_loader.py`, que já carrega
  `data/clean/dataset.csv`; não use caminhos absolutos nem baixe dados da
  internet.
- Consulte o `app.py` existente antes de sugerir alterações. Preserve o
  comportamento que já funciona e evite reescrever o aplicativo inteiro.
- Não altere o notebook, o dataset, os rascunhos ou arquivos fora do escopo.
  Não acrescente dependências sem necessidade.
- Não invente valores de KPI, resultados, categorias ou conteúdo para os
  gráficos; os valores devem ser calculados a partir dos dados carregados.
- Trate seleções vazias e filtros sem partidas sem causar erro.
- Mantenha nomes de campos e mensagens da interface em português claro, com
  títulos e unidades identificáveis.
- Não apresente correlação como causalidade. Considere que valores ausentes
  podem afetar o número de observações usado em cada correlação.

## Formato de saída

Gere somente um esqueleto conciso para `app.py`, com a estrutura visual das duas
abas e comentários `# TODO` nos pontos onde faltarem cálculos ou gráficos.
Antes do código, liste brevemente as seções que ele conterá e quaisquer
decisões que não puderem ser inferidas dos rascunhos. Não gere dados fictícios,
não complete os TODOs com lógica inventada e não altere arquivos do projeto.
