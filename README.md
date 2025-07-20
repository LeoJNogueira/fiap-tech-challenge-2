# fiap-tech-challenge-2

# 🌾 Otimização de Eficiência de Plantio com Algoritmo Genético

## 🎯 Objetivo
Utilizar Algoritmo Genético para definir a configuração ideal de culturas em uma área agrícola de 2 hectares, maximizando produtividade e minimizando competição entre espécies, respeitando condições ecológicas e econômicas.

---

## 🧩 Etapas do Projeto

### 1. Definição das Culturas
- Culturas disponíveis:
  - Milho, feijão, soja, sorgo, mandioca, etc.
- Parâmetros de cada cultura:
  - Produtividade estimada por hectare
  - Ciclo de crescimento
  - Quantidade de água necessária (parametrizar custo por m³)
  - Compatibilidade com outras espécies (consórcio ou competição)

---

### 2. Modelagem da Área
- Divisão da área em células (grid) ou parcelas
- Atributos das parcelas:
  - Coeficiente de Umidade do solo

---

### 3. Codificação Genética
- Cada indivíduo representa uma configuração de culturas
- Exemplos:
  - Vetor simples: `[milho, soja, mandioca, feijão]`
  - Matriz para representar o grid da área

---

### 4. Função de Fitness
- Avaliação dos indivíduos com múltiplos critérios:
  - Produção estimada
  - Compatibilidade ecológica
  - Custo operacional
  - Lucro financeiro esperado
- Fórmula exemplo: Fitness = α × produção + β × lucro - γ × competição



---

### 5. Algoritmo Genético
- **População inicial**: configurações aleatórias
- **Seleção**: indivíduos com maior fitness
- **Crossover**: combinação de culturas entre indivíduos
- **Mutação**: alteração aleatória de culturas em parcelas
- **Restrições**:
  - Evitar culturas incompatíveis lado a lado
  - Respeitar calendário agrícola e época de plantio (desejavel)
  - Limitar número de culturas por hectare até 2
  - Retorno financeiro mínimo por hectare
  - Custo de produção máximo por hectare

---

## 🔬 Dados Necessários

- Tabelas agronômicas:
- Produtividade média
- Preço de mercado
- Compatibilidade

---

## 🧰 Ferramentas Recomendadas

| Finalidade                  | Ferramenta              |
|-----------------------------|-------------------------|
| Dados agronômicos           | EMBRAPA, IBGE, FAO      |
| Algoritmo Genético          | `DEAP`, `PyGAD`         |
| Geoprocessamento / Grid     | `geopandas`, `shapely`  |
| Visualização de mapas       | `folium`, `matplotlib`  |
| Otimização multivariada     | `SciPy`, `sklearn`      |

---

## 🚀 Próximos Passos

1. Culturas possíveis (Carlos)
2. Coletar os dados necessários e preparar o grid (Carlos)
3. Implementar o AG com representação genética adequada (Dan / Leo / Carlos)
4. Testar e refinar a função de fitness (Dan)
5. Validação de comparação com dados históricos (Leo)


## Definindo Culturas
- Quais variavies precismos saber para compatibilizar culturas
- Qual o requisito de produção de cada cultura
- Qual o custo de produção de cada cultura
- Qual o ciclo de vida de cada cultura
- Qual o requisito de água de cada cultura
- Qual o retorno financeiro de cada cultura


Induviduo [CUSTO PRODUÇÃO, PRODUTIVIDADE, CICLO DE VIDA, REQUISITO DE ÁGUA, RETORNO FINANCEIRO, COMPATIBILIDADE]