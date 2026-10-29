# Justificativa das métricas — Dashboard 2

## Contexto de leitura

Os indicadores e gráficos consideram os filtros da barra lateral. As seleções
feitas nos gráficos de resultado e de torneio também filtram os indicadores e o
outro gráfico. As porcentagens de resultado usam como denominador somente
partidas com placar disponível e resultado classificável.

O dashboard apresenta três visuais complementares: quantidade de partidas por
resultado, média de gols por torneio e evolução anual da média de gols. A
seleção de resultado ou torneio também atualiza a série temporal.

## Métrica 1: Partidas analisadas

- **Variável:** uma linha por partida no dataset; o número exibido é a
  quantidade de linhas após os filtros ativos.
- **O que mede:** o tamanho do conjunto de partidas analisado.
- **Por que foi escolhida:** informa o volume que dá contexto às médias e
  porcentagens exibidas ao lado.
- **Público-alvo:** pessoas interessadas em comparar o desempenho de equipes e
  torneios, mesmo sem conhecimento técnico de análise de dados.
- **Qual decisão pode ser apoiada por essa métrica?** avaliar se o recorte de
  partidas é amplo o bastante para uma comparação ou se é preciso ajustar os
  filtros.
- **O que comunica ao público-alvo:** quantas partidas estão incluídas no
  recorte atual.

## Métrica 2: Média de gols por partida

- **Variável:** `home_goal` + `away_goal`.
- **O que mede:** a média da soma dos gols do mandante e do visitante por
  partida no recorte atual.
- **Por que foi escolhida:** resume o nível de gols sem exigir que o público
  compare cada partida individualmente.
- **Público-alvo:** pessoas interessadas em entender se os jogos do recorte
  tendem a ter mais ou menos gols.
- **Qual decisão pode ser apoiada por essa métrica?** comparar o perfil de gols
  entre torneios ou resultados selecionados.
- **O que comunica ao público-alvo:** quantos gols, em média, foram marcados em
  cada partida do recorte.

## Métrica 3: Vitórias do mandante

- **Variável:** resultado calculado pela comparação entre `home_goal` e
  `away_goal`.
- **O que mede:** a proporção de partidas classificáveis em que o mandante
  marcou mais gols que o visitante.
- **Por que foi escolhida:** permite observar a frequência de vitórias de quem
  joga em casa e compará-la com empates e vitórias visitantes.
- **Público-alvo:** pessoas interessadas em resultados e na possível vantagem
  de jogar em casa.
- **Qual decisão pode ser apoiada por essa métrica?** comparar a frequência de
  vitórias mandantes entre recortes de torneios e partidas.
- **O que comunica ao público-alvo:** que parcela das partidas com placar
  classificável terminou com vitória do mandante.

## Métrica 4: Empates

- **Variável:** resultado calculado pela comparação entre `home_goal` e
  `away_goal`.
- **O que mede:** a proporção de partidas classificáveis em que mandante e
  visitante marcaram o mesmo número de gols.
- **Por que foi escolhida:** completa a distribuição dos resultados e evita
  reduzir a leitura apenas a vitórias.
- **Público-alvo:** pessoas interessadas na frequência de cada tipo de
  resultado.
- **Qual decisão pode ser apoiada por essa métrica?** identificar recortes em
  que empates são mais comuns para orientar comparações de perfil competitivo.
- **O que comunica ao público-alvo:** que parcela das partidas terminou sem um
  vencedor.

## Métrica 5: Vitórias do visitante

- **Variável:** resultado calculado pela comparação entre `home_goal` e
  `away_goal`.
- **O que mede:** a proporção de partidas classificáveis em que o visitante
  marcou mais gols que o mandante.
- **Por que foi escolhida:** junto das vitórias mandantes e dos empates, mostra
  a distribuição completa dos resultados.
- **Público-alvo:** pessoas interessadas em resultados e em comparar o
  desempenho de equipes visitantes.
- **Qual decisão pode ser apoiada por essa métrica?** comparar resultados de
  equipes visitantes entre torneios ou outros recortes dos filtros.
- **O que comunica ao público-alvo:** que parcela das partidas com placar
  classificável terminou com vitória do visitante.
