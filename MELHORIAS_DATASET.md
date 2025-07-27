# 📊 Melhorias no Dataset de Culturas - Contexto Brasileiro

## 🎯 Objetivo das Melhorias

Aprimorar o dataset original para melhor representar a realidade agrícola brasileira, fornecendo dados mais precisos e abrangentes para o algoritmo genético de otimização de plantio.

---

## 🔄 Principais Melhorias Implementadas

### 1. **Novas Colunas Adicionadas**

- **Lucro_R$/ha**: Cálculo direto do lucro (Retorno - Custo)
- **Epoca_Plantio**: Períodos ideais de plantio no Brasil
- **Regiao_Adaptada**: Regiões brasileiras onde a cultura se adapta melhor
- **Compatibilidade_Negativa**: Culturas que competem ou prejudicam o crescimento
- **Tipo_Cultura**: Classificação agronômica (Cereal, Leguminosa, etc.)
- **pH_Solo_Min/Max**: Faixa de pH ideal para cada cultura
- **Temperatura_Min/Max_C**: Faixa de temperatura adequada

### 2. **Dados Atualizados para Contexto Brasileiro**

- **Preços e custos** baseados em valores de mercado brasileiro (2024)
- **Produtividades** ajustadas conforme dados da EMBRAPA e IBGE
- **Ciclos de cultivo** adaptados ao clima tropical/subtropical
- **Requisitos hídricos** baseados em estudos agronômicos nacionais

### 3. **Culturas Adicionadas**

- **Culturas perenes**: Café, Eucalipto, Banana, Cacau
- **Fruticultura**: Abacaxi, Melão, Melancia
- **Hortaliças**: Brócolis, expandindo opções de cultivo intensivo
- **Culturas regionais**: Adaptadas às diferentes regiões do Brasil

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

### **Restrições Mais Realistas**

- **Sazonalidade**: Época de plantio respeitada
- **Adaptação regional**: Culturas adequadas à região
- **Condições edafoclimáticas**: pH e temperatura considerados
- **Rotação de culturas**: Compatibilidade positiva/negativa

### **Diversificação de Estratégias**

- **Culturas anuais vs perenes**: Diferentes horizontes de investimento
- **Culturas de subsistência vs comerciais**: Diferentes objetivos
- **Culturas intensivas vs extensivas**: Diferentes níveis de manejo

---

## 🌱 Exemplos de Aplicação

### **Consórcio Milho-Soja**

```
Milho: Plantio Out-Dez, Compatível com Soja
Soja: Plantio Set-Nov, Compatível com Milho
Benefício: Fixação de nitrogênio + aproveitamento de espaço
```

### **Rotação Soja-Milho-Feijão**

```
Ano 1: Soja (Set-Nov) → Lucro: R$ 8.100/ha
Ano 2: Milho (Out-Dez) → Lucro: R$ 8.550/ha
Ano 3: Feijão (Abr-Jun) → Lucro: R$ 8.700/ha
```

### **Sistema Agroflorestal**

```
Eucalipto (base) + Café (sub-bosque)
Ciclo longo com retorno sustentável
Compatibilidade positiva documentada
```

---

## 🎲 Codificação Genética Sugerida

### **Representação do Indivíduo**

```python
individuo = {
    'parcela_1': {
        'cultura': 'Milho',
        'epoca': 'Out-Dez',
        'area_percentual': 0.3
    },
    'parcela_2': {
        'cultura': 'Soja',
        'epoca': 'Set-Nov',
        'area_percentual': 0.7
    }
}
```

### **Validações Automáticas**

- ✅ Compatibilidade entre culturas adjacentes
- ✅ Época de plantio adequada
- ✅ Condições edafoclimáticas atendidas
- ✅ Limite de 2 hectares respeitado

---

## 📊 Estatísticas do Dataset Melhorado

| Métrica               | Valor                   |
| --------------------- | ----------------------- |
| **Total de culturas** | 25                      |
| **Culturas anuais**   | 18                      |
| **Culturas perenes**  | 7                       |
| **Faixa de lucro**    | R$ 4.800 - R$ 79.500/ha |
| **Ciclos**            | 60 - 2.555 dias         |
| **Regiões cobertas**  | Todas as 5 regiões      |

---

## 🚀 Próximos Passos Recomendados

1. **Validação dos dados** com especialistas agronômicos
2. **Implementação de pesos** na função de fitness
3. **Testes de sensibilidade** dos parâmetros
4. **Validação com dados históricos** de produção
5. **Refinamento das compatibilidades** baseado em literatura científica

---

## 📚 Fontes de Dados

- **EMBRAPA**: Dados de produtividade e manejo
- **IBGE**: Estatísticas agrícolas nacionais
- **CONAB**: Preços e custos de produção
- **Literatura científica**: Compatibilidade entre culturas
- **Zoneamento agrícola**: Épocas de plantio por região

---

_Dataset otimizado para maximizar a eficiência do algoritmo genético na otimização de sistemas de cultivo brasileiros._
