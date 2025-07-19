# fiap-tech-challenge-2

# 📈 Otimização de Carteira de Ações com Algoritmo Genético

## 🎯 Objetivo do Sistema
Utilizando Algoritmos Genéticos (AGs) o sistema selecionará ativos de uma carteira de ações, otimizando o retorno esperado e minimizando o risco, conforme o perfil do investidor escolhido.

---

## 🗃️ 1. Base de Dados
- Utilizaremos dados históricos de ações da B3 (Bolsa de Valores de São Paulo) disponiveis no yfinance (Yahoo)
- Obtenção de dados históricos de ações (ex: últimos 5 anos). (ajustar tempo se precisar)
- Cálculo de métricas por ativo:
  - Retorno médio
  - Desvio padrão (risco)
  - Correlação entre ativos

---

## 🧬 2. Representação Genética
- Cada indivíduo representa uma carteira:
  - Vetor binário: `[1, 0, 1, 1, 0]` → seleção de ativos.
  - Vetor de pesos: `[0.3, 0, 0.2, 0.5, 0]` → distribuição percentual.

---

## 📐 3. Função de Fitness
- Utilizar o **Sharpe Ratio**:


Onde α e β refletem o perfil do investidor (conservador ou agressivo).

---

## 🔁 4. Processo Evolutivo
- **População inicial**: Gerada aleatoriamente.
- **Seleção**: Escolha das carteiras com melhor desempenho.
- **Crossover**: Combinação de características entre carteiras.
- **Mutação**: Alteração de ativos ou pesos para explorar novas possibilidades.

---

## 🧪 5. Avaliação e Refinamento
- Avaliação após N gerações:
- Carteira otimizada conforme critérios definidos.
- Restrições opcionais:
- Número mínimo/máximo de ativos.
- Limites por setor.
- Peso mínimo por ativo.

---

## 🧰 Ferramentas Recomendadas

| Finalidade            | Ferramenta             |
|-----------------------|------------------------|
| Dados financeiros     | `yfinance`, `pandas`   |
| Algoritmos genéticos  | `DEAP`, `PyGAD`        | 
| Análise estatística   | `numpy`, `scipy`       |
| Visualização          | `matplotlib`, `plotly` |

---

## 🚀 Próximos passos
- Definir lista de ativos brasileiros (ex: PETR4, VALE3, ITUB4).
- Coletar dados e preparar as métricas.
- Implementar e testar o AG com uma população inicial.
- Analisar os resultados e ajustar a função de fitness.
