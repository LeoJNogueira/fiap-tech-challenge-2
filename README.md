# fiap-tech-challenge-2

# 🌾 Otimização de Eficiência de Plantio com Algoritmo Genético

## 🎯 Objetivo

Utilizar Algoritmo Genético para definir a configuração ideal de culturas em uma área agrícola de 2 hectares, maximizando produtividade e lucro financeiro, minimizando custos e competição entre espécies, e respeitando rigorosamente as condições ecológicas, temporais e espaciais.

---

## 🧩 Etapas do Projeto

### 1. Definição e Enriquecimento das Culturas

- **Culturas disponíveis**: Uma vasta gama, incluindo cereais, leguminosas, tubérculos, fibras, frutíferas (perenes e anuais), hortaliças, florestais, oleaginosas, especiarias, e culturas para adubação verde/forrageiras.
- **Parâmetros de cada cultura**:
  - Produtividade estimada por hectare (`Produtividade_t/ha`)
  - Ciclo de crescimento (`Ciclo_dias`)
  - Quantidade de água necessária (`Requisito_Agua_mm`)
  - Custo de produção por hectare (`Custo_Producao_R$/ha`)
  - Retorno financeiro esperado por hectare (`Retorno_Financeiro_R$/ha`)
  - Lucro financeiro por hectare (`Lucro_R$/ha`)
  - Compatibilidade com outras espécies (consórcio ou competição) (`Compatibilidade_Positiva`, `Compatibilidade_Negativa`)
  - Tipo de cultura (`Tipo_Cultura`)
  - Faixa de pH ideal do solo (`pH_Solo_Min/Max`)
  - Faixa de temperatura ideal (`Temperatura_Min/Max_C`)
  - Espaço mínimo necessário por planta ou área mínima por hectare (`Espaco_Minimo_m2_por_Planta_ou_Area_minima_por_hectare`)
  - Época de plantio (`Epoca_Plantio`)
  - Região brasileira adaptada (`Regiao_Adaptada`)

---

### 2. Modelagem da Área

- **Divisão da área em células (grid) ou parcelas**: Permite a alocação espacial das culturas.
- **Atributos das parcelas**:
  - Coeficiente de Umidade do solo (a ser implementado/simulado)
  - pH do solo (a ser implementado/simulado para cada parcela)
  - Temperatura média (a ser implementado/simulado para cada parcela)
  - Região geográfica da parcela.

---

### 3. Codificação Genética

- **Cada indivíduo representa uma configuração de culturas para a área total.**
- **Representação**: Uma matriz para representar o grid da área, onde cada célula contém informações sobre a cultura, sua época de plantio e/ou rotação.

---

### 4. Função de Fitness

- **Avaliação dos indivíduos com múltiplos critérios**:
  - Produção estimada.
  - Compatibilidade ecológica e temporal.
  - Custo operacional.
  - Lucro financeiro esperado.
  - Otimização do uso do espaço.
- **Fórmula exemplo**: Fitness = α × lucro + β × produtividade - γ × custo_agua - δ × incompatibilidade_penalty + ε × compatibilidade_score.

---

### 5. Algoritmo Genético

- **População inicial**: configurações aleatórias de culturas dentro das parcelas.
- **Seleção**: indivíduos com maior fitness são selecionados para reprodução.
- **Crossover**: combinação de culturas entre indivíduos para gerar novas configurações.
- **Mutação**: alteração aleatória de culturas ou parâmetros em parcelas para explorar novas soluções.
- **Restrições**:
  - Evitar culturas incompatíveis lado a lado ou em sequência temporal.
  - Respeitar calendário agrícola e época de plantio.
  - Limitar o número total de culturas ou a proporção de área por cultura (se aplicável, para diversificação).
  - Limite da área total de 2 hectares para o plantio.
  - Respeitar requisitos de pH, temperatura e umidade do solo por cultura.
  - Considerar o espaço mínimo necessário por planta/cultura.

---

## 🔬 Dados Necessários

- **Tabelas agronômicas detalhadas**:
  - Produtividade média.
  - Preço de mercado.
  - Compatibilidade.
  - Ciclo de vida.
  - Requisito de água.
  - Custo de produção.
  - Retorno financeiro.
  - pH do solo, temperatura, época de plantio e região adaptada.
  - Espaço mínimo.

---

## 🧰 Ferramentas Recomendadas

| Finalidade                  | Ferramenta              |
|-----------------------------|-------------------------|
| Dados agronômicos           | EMBRAPA, IBGE, CONAB    |
| Algoritmo Genético          | `DEAP`, `PyGAD`         |
| Geoprocessamento / Grid     | `geopandas`, `shapely`  |
| Visualização de mapas       | `folium`, `matplotlib`  |
| Otimização multivariada     | `SciPy`, `sklearn`      |

---

## 🚀 Próximos Passos

1. **Enriquecimento e Validação dos Dados Agronômicos**: Concluir a coleta e validação dos dados de todas as culturas, garantindo consistência e precisão.
2. **Modelagem do Grid/Área**: Definir a estrutura do grid e os atributos associados a cada célula (pH, umidade, região).
3. **Implementação do Algoritmo Genético**: Codificar o AG com a representação genética e as operações de seleção, crossover e mutação.
4. **Desenvolvimento da Função de Fitness**: Implementar a função de fitness considerando todos os critérios de otimização e restrições.
5. **Testes, Refinamento e Validação**: Realizar testes extensivos, refinar parâmetros do AG e validar os resultados com dados históricos ou simulações realistas.

---

## Definindo Culturas (Parâmetros Essenciais no Dataset)

- Quais variáveis precisamos saber para compatibilizar culturas? `Compatibilidade_Positiva`, `Compatibilidade_Negativa`.
- Qual o requisito de produção de cada cultura? `Produtividade_t/ha`.
- Qual o custo de produção de cada cultura? `Custo_Producao_R$/ha`.
- Qual o ciclo de vida de cada cultura? `Ciclo_dias`.
- Qual o requisito de água de cada cultura? `Requisito_Agua_mm`.
- Qual o retorno financeiro de cada cultura? `Retorno_Financeiro_R$/ha`, `Lucro_R$/ha`.
- Qual o tipo de solo e temperatura? `pH_Solo_Min/Max`, `Temperatura_Min/Max_C`.
- Qual a época e região de plantio? `Epoca_Plantio`, `Regiao_Adaptada`.
- Qual o espaço mínimo necessário? `Espaco_Minimo_m2_por_Planta_ou_Area_minima_por_hectare`.

Indivíduo: Uma configuração completa das culturas alocadas em um grid ou parcelas, considerando todos os parâmetros relevantes e respeitando as restrições.
