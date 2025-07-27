# 📊 Melhorias no Dataset de Culturas - Contexto Brasileiro

## 🎯 Objetivo das Melhorias

Aprimorar o dataset original para melhor representar a realidade agrícola brasileira, fornecendo dados mais precisos e abrangentes para o algoritmo genético de otimização de plantio, com foco em otimização espacial e temporal.

---

## 🔄 Principais Melhorias Implementadas

### 1. **Novas Colunas Adicionadas e Revisadas**

- **Lucro_R$/ha**: Cálculo direto do lucro (Retorno - Custo)
- **Epoca_Plantio**: Períodos ideais de plantio no Brasil (ex: "Out-Dez", "Ano_Todo", "Varias")
- **Regiao_Adaptada**: Regiões brasileiras onde a cultura se adapta melhor, padronizado (ex: "Centro-Oeste;Sudeste;Sul", "Todas_Regioes")
- **Compatibilidade_Positiva**: Culturas ou categorias agronômicas que se beneficiam do consórcio/rotação com a cultura em questão (ex: "Milho;Soja", "Culturas_de_cobertura")
- **Compatibilidade_Negativa**: Culturas ou categorias agronômicas que competem ou prejudicam o crescimento da cultura (ex: "Girassol;Algodao", "Culturas_Anuais", "Exoticas_Competitivas")
- **Tipo_Cultura**: Classificação agronômica (Cereal, Leguminosa, Frutifera, Olericola, Florestal, Oleaginosa, etc.)
- **pH_Solo_Min/Max**: Faixa de pH ideal para cada cultura
- **Temperatura_Min/Max_C**: Faixa de temperatura adequada
- **Espaco_Minimo_m2_por_Planta_ou_Area_minima_por_hectare**: Espaço mínimo necessário por planta ou área mínima por hectare para culturas de plantio denso, crucial para alocação espacial no grid.

### 2. **Dados Atualizados para Contexto Brasileiro**

- **Preços e custos** baseados em valores de mercado brasileiro (estimativas para 2024/2025)
- **Produtividades** ajustadas conforme dados da EMBRAPA, CONAB e IBGE
- **Ciclos de cultivo** adaptados ao clima tropical/subtropical
- **Requisitos hídricos** baseados em estudos agronômicos nacionais

### 3. **Culturas Adicionadas e Diversificadas**

- **Culturas perenes**: Café, Eucalipto, Banana, Cacau, Seringueira, Coqueiro, Goiaba, Abacate, Mangueira, entre outras.
- **Fruticultura**: Abacaxi, Melão, Melancia, Uva, Maçã, Pêssego, Pitaya, Caju Anão, Graviola, Maracujá, Mamão, Araticum, Pupunha, Guaraná.
- **Hortaliças e Raízes**: Alho, Cenoura, Beterraba, Pimentão, Batata, Cebola, Tomate, Alface, Brócolis, Couve-flor, Espinafre, Couve, Rabanete, Inhame, Gengibre, Couve Chinesa, Rúcula, Salsa, Cebolinha, Coentro, Batata Doce, Berinjela, Quiabo, Pepino, Abóbora.
- **Grãos e Oleaginosas**: Milho, Soja, Feijão, Sorgo, Algodão, Trigo, Cevada, Aveia, Girassol, Arroz, Grão de Bico, Lentilha, Amendoim, Gergelim, Linhaça, Centeio, Pecan.
- **Florestais**: Pinus, Acácia, Jatobá, Pinhão.
- **Culturas Específicas**: Pimenta do Reino, Erva Mate, Dendê.
- **Culturas de Adubação Verde/Forrageiras**: Girassol_de_cobertura, Crotalária, Capim_Mombaça, Capim_Brachiaria, Mandioca_forrageira.

---

## 📈 Benefícios para o Algoritmo Genético

### **Função de Fitness Mais Robusta**

```python
# Exemplo de uso das novas variáveis
fitness = (
    α * lucro_ha +
    β * produtividade +
    γ * compatibilidade_score -
    δ * custo_agua -
    ε * incompatibilidade_penalty
)
```

---

## 🛡️ Restrições Mais Realistas

- **Sazonalidade:** Época de plantio respeitada
- **Adaptação regional:** Culturas adequadas à região
- **Condições edafoclimáticas:** pH e temperatura do solo considerados
- **Rotação/Consórcio:** Compatibilidade positiva/negativa entre espécies
- **Ocupação espacial:** Respeito ao `Espaco_Minimo_m2_por_Planta_ou_Area_minima_por_hectare`

---

## 🌾 Diversificação de Estratégias

- **Culturas anuais vs perenes:** Diferentes horizontes de investimento e manejo
- **Culturas de subsistência vs comerciais:** Diferentes objetivos de produção
- **Culturas intensivas vs extensivas:** Diferentes níveis de manejo e densidade
- **Uso do solo:** Inclusão de forrageiras e culturas de adubação verde para sistemas integrados

---

## 🌱 Exemplos de Aplicação

### Consórcio Milho-Soja (ou Milho-Feijão)

- **Milho:** Plantio Out-Dez, compatível com Soja/Feijão
- **Soja/Feijão:** Plantio Set-Nov/Abr-Jun, compatível com Milho
- **Benefício:** Fixação de nitrogênio (leguminosa) + aproveitamento de espaço e recursos

### Rotação Soja-Milho-Feijão

- **Ano 1:** Soja (Set-Nov) → Lucro: ~R$ 8.100/ha
- **Ano 2:** Milho (Out-Dez) → Lucro: ~R$ 8.550/ha
- **Ano 3:** Feijão (Abr-Jun) → Lucro: ~R$ 8.700/ha
- **Benefício:** Manejo de pragas/doenças, melhoria do solo e diversificação de renda

### Sistema Agroflorestal (SAF)

- **Eucalipto (base) + Café (sub-bosque)** ou **Cacau + Banana**
- **Ciclo longo** com retorno sustentável e otimização de diferentes extratos (sombra/sol)
- **Compatibilidade positiva** documentada para coexistência

---

## 🎲 Codificação Genética Sugerida

### Representação do Indivíduo

```python
individuo = {
    'parcela_1': {
        'cultura': 'Milho',
        'epoca': 'Out-Dez',
        'area_percentual': 0.3,  # Ou área em m2
        'regiao_especifica': 'Sudeste'  # Se o grid tiver granularidade regional
    },
    'parcela_2': {
        'cultura': 'Soja',
        'epoca': 'Set-Nov',
        'area_percentual': 0.7,
        'regiao_especifica': 'Centro-Oeste'
    }
}
```

### Validações Automáticas

- ✅ Compatibilidade entre culturas adjacentes ou em rotação
- ✅ Época de plantio adequada para a região e período
- ✅ Condições edafoclimáticas (pH, temperatura) atendidas pela cultura e pela parcela
- ✅ Limite de 2 hectares respeitado na soma das áreas
- ✅ `Espaco_Minimo_m2_por_Planta` respeitado dentro das parcelas

---

## 📊 Estatísticas do Dataset Melhorado (Estimativa Atual)

| Métrica                | Valor                        |
|------------------------|------------------------------|
| Total de culturas      | ~50+                         |
| Culturas anuais        | ~35                          |
| Culturas perenes/longo ciclo | ~15+                  |
| Faixa de lucro         | R$ 0 - R$ 60.000/ha (aprox.) |
| Ciclos                 | 30 - 7.300 dias              |
| Regiões cobertas       | Todas as 5 regiões do Brasil |

---

## 🚀 Próximos Passos Recomendados

1. Validação final dos dados com especialistas agronômicos para ajuste fino de valores específicos
2. Implementação de pesos mais sofisticados na função de fitness para diferentes objetivos (ex: priorizar lucro, sustentabilidade, biodiversidade)
3. Testes de sensibilidade dos parâmetros do algoritmo genético e do dataset
4. Validação com dados históricos de produção e custos em cenários reais, se disponíveis
5. Refinamento das lógicas de compatibilidade para cenários mais complexos (ex: profundidade de raízes, demanda por nutrientes)

---

## 📚 Fontes de Dados

- **EMBRAPA:** Dados de produtividade, manejo e zoneamento agrícola
- **IBGE:** Estatísticas agrícolas nacionais
- **CONAB:** Preços e custos de produção
- **Literatura científica e agronômica:** Compatibilidade entre culturas, requisitos edafoclimáticos
- **Zoneamento Agrícola de Risco Climático (ZARC):** Épocas de plantio por região

---

_Dataset otimizado para maximizar a eficiência do algoritmo genético na otimização de sistemas de cultivo brasileiros._
