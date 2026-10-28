# Declaração de Uso de IA

**Nome:** Pedro Valença Ferraz
**Data:** 27/10/2026

## Ferramenta

Assistente de IA do GitHub Copilot no VS Code.

## Prompt usado

Os dez pedidos a seguir foram enviados pelo estudante nesta conversa:

1. **Notebook e dados:** “Revise minha EDA e confira se data/clean/dataset.csv corresponde ao tratamento descrito no notebook. Aponte diferenças sem alterar os dados.”
2. **Dashboard 1:** “Revise o Dashboard 1 quanto à clareza dos filtros, da matriz de correlação e dos histogramas. Sugira melhorias coerentes com o roteiro.”
3. **Correlação:** “Explique como interpretar a matriz de correlação de Spearman deste dashboard e quais cuidados devo mencionar na apresentação.”
4. **Distribuições:** “Avalie se os histogramas permitem comparar adequadamente as variáveis selecionadas e sugira ajustes de apresentação.”
5. **Dashboard 2:** “Confira se cada KPI está definido corretamente e se as porcentagens usam um denominador adequado. Explique eventuais limitações.”
6. **Interatividade:** “Teste conceitualmente o filtro cruzado do Dashboard 2 e descreva o que deve acontecer ao selecionar um resultado ou torneio.”
7. **Validação:** “Revise os casos extremos dos filtros e dos gráficos e proponha testes para verificar que o app não falha com seleções vazias.”
8. **Acessibilidade e apresentação:** “Sugira melhorias de legibilidade, contraste, títulos e rótulos para que os dashboards sejam compreensíveis por pessoas sem familiaridade com análise de dados.”
9. **Deploy:** “Confira os requisitos e o caminho do CSV necessários para publicar este app no Streamlit Community Cloud. Liste verificações antes do deploy.”
10. **Entrega final:** “Compare os arquivos do repositório com o checklist do ROTEIRO.md e liste o que falta entregar, sem presumir que arquivos vazios estão completos.”
## O que foi aceito, modificado ou rejeitado e por quê

- **Aceito:** revisar os dashboards, os dados, as métricas, os filtros, a
  apresentação e o checklist de entrega; comparar os dados sem alterá-los,
  conforme solicitado.
- **Modificado:** os wireframes existentes são referências digitais feitas com
  auxílio de IA.
- **Rejeitado:** -

## Resultado e verificações

- Foi identificada uma divergência na coluna `mandante_venceu`: o notebook
  compara `at_result` com `HOME_WIN`, mas os rótulos existentes são `WON`,
  `LOST` e `DRAW`. O CSV calcula a coluna comparando os gols. A divergência foi
  reportada sem modificar o dataset.
- A matriz de Spearman exibe uma única correlação por par. A correlação mede
  associação monotônica entre postos, não causalidade; valores ausentes podem
  fazer com que o número de partidas varie entre pares.
- Os histogramas aceitam várias variáveis e podem ser vistos lado a lado. Como
  as variáveis têm unidades e amplitudes diferentes, a comparação deve focar
  distribuições e não alturas brutas entre gráficos; títulos e unidades devem
  permanecer claros.
- Os KPIs de resultado usam o total de partidas filtradas como denominador.
  Assim, ao filtrar por um resultado, a proporção daquele resultado passa a
  100%, o que deve ser interpretado dentro do subconjunto selecionado.
- A estrutura das seleções cruzadas do Dashboard 2 e os casos de filtros
  vazios foram inspecionados. A interação por clique ainda deve ser confirmada
  manualmente no navegador.
- O caminho relativo do CSV é incluído no app e o arquivo está no repositório.
  Antes da publicação ainda é necessário publicar no Streamlit Community Cloud
  e preencher a URL do app no README. Também falta confirmar que todos os
  arquivos da entrega estão preenchidos e substituir os wireframes digitais
  caso o roteiro exija fotos de rascunhos feitos à mão.
