import random

def mutation(sample,df):
    remaining_rows = df[~df['CULTURA'].isin(sample['CULTURA'])]
    if not remaining_rows.empty:
        row_to_replace_idx = sample.sample(1).index[0]
        random_new_row = remaining_rows.sample(1)
        sample.loc[row_to_replace_idx] = random_new_row.iloc[0]
    return sample

def crossover(population,df):
    if len(population) < 2:
        print("Population must have at least two individuals for crossover.")
        return

    new_population = []
    # São selecionado 50% dos indivíduos (os 50% melhores)
    for _ in range(len(population)//2):
        parent1, parent2 = select_unique_parents(population)

        offspring1, offspring2 = crossover_individuals(parent1, parent2)

        # É aplicada mutação aleatória nos genes de cada nova amostra
        offspring1 = mutation(offspring1,df)
        offspring2 = mutation(offspring2,df)

        new_population.extend([offspring1, offspring2])

    return new_population


def select_unique_parents(population):
    # Sample two parents ensuring they are not the same
    parent1 = random.choice(population)
    parent2 = random.choice(population)

    # Keep selecting until the parents are unique
    while parent1.equals(parent2):  # Using .equals for pandas DataFrame comparison
        parent2 = random.choice(population)

    return parent1, parent2


def crossover_individuals(parent1, parent2):
    offspring1 = parent1.copy()
    offspring2 = parent2.copy()

    unique_to_sample1 = offspring1[~offspring1['CULTURA'].isin(offspring2['CULTURA'])]
    # Busca linhas que estão na amostra2 que não estão na amostra1
    unique_to_sample2 = offspring2[~offspring2['CULTURA'].isin(offspring1['CULTURA'])]

    if not unique_to_sample1.empty and not unique_to_sample2.empty:

        row1 = unique_to_sample1.sample(1)
        row2 = unique_to_sample2.sample(1)


        idx1 = row1.index[0]
        idx2 = row2.index[0]

        offspring1.loc[idx1] = row2.iloc[0]
        offspring2.loc[idx2] = row1.iloc[0]

        return offspring1, offspring2
    return parent1, parent2


def project_fitness_function(sample, orcamento_maximo, m2_area_disponivel, limite_agua, janela_dias):
    # pesos de cada conjunto
    W_prod = 0.6
    W_comp = 0.4

    # para cada cultura do conjunto
    # pontuação_produtividade = (produtividade/espaço minimo)
    pontuacao_producao_normalizada = 0
    competition_score = 0
    plant_map = dict()

    for s in sample.iterrows():
        pontuacao_producao = (s[1]['PRODUTIVIDADE'] / s[1]['ESPAÇO MÍNIMO m²'])
        pontuacao_producao_normalizada += pontuacao_producao

    # para cada gene da amostra
    # pontuação_competitividade = 0
    # +1.0 Sinérgica
    # +0.5 Companheira
    # 0.0 Neutra
    # -1.0 Antagônica

    # inicializa dicionário com os genes da amostra atual para validação de compatibilidade
    for s in sample.iterrows():
        plant_map[s[1]['CULTURA']] = dict(sinergia=s[1]['SINERGIA'].split(','),
                                          companheira=s[1]['COMPANHEIRA'].split(','), neutra=s[1]['NEUTRA'].split(','),
                                          antagonica=s[1]['ANTAGÔNICA'].split(','))

    # score de compatibilidade entre os genes da amostra
    for s in sample.iterrows():
        for key, value in plant_map.items():
            if s[1]['CULTURA'] == key:
                continue
            if s[1]['CULTURA'] in value['sinergia']:
                competition_score += 1.0
            if s[1]['CULTURA'] in value['companheira']:
                competition_score += 0.5
            if s[1]['CULTURA'] in value['neutra']:
                competition_score += 0.0
            if s[1]['CULTURA'] in value['antagonica']:
                competition_score -= 1.0

    normalized_competition_score = 0 if competition_score <= 0 else 1 if competition_score >= 1 else competition_score

    score = (W_prod * pontuacao_producao_normalizada) + (W_comp * normalized_competition_score)

    # Valores para cálculo de penalidades
    custo_total = 0
    consumo_agua_cultura = 0
    ciclo_de_vida = []
    area_total_cultura = 0

    # incrementa valores para as amostras de cada geração
    for s in sample.iterrows():
        custo_total += s[1]['CUSTO PRODUÇÃO']
        consumo_agua_cultura += s[1]['REQUISITO DE ÁGUA']
        area_total_cultura += s[1]['ESPAÇO MÍNIMO m²']
        ciclo_de_vida.append(s[1]['CICLO DE VIDA MAX EM DIAS'])

    # Se Custo Total > Orçamento máximo, então P_econômica = 0.01, senão P_econômica=1
    P_economica = 0.01 if custo_total >= orcamento_maximo else 1

    # utilizaçào muito grande grande de area também será punida e adicionado a penalidade econômica
    P_economica += 1 - (area_total_cultura / m2_area_disponivel)

    # Se o consumo de água total > disponibilidade de água, então P_ecológica = 0.01, senão P_ecológica = 1
    P_ecologica = 0.01 if consumo_agua_cultura >= limite_agua else 1

    # É verificado se o ciclo de vida mais longo cabe na janela de plantio caso contrário é aplicado uma taxa de penalidade proporcional
    maior_ciclo_vida = max(ciclo_de_vida)

    #Adciona penalidade se a cultura com maior tempo de produção superar o limite estabelecido
    if maior_ciclo_vida > janela_dias:
        P_ecologica += 1 - (janela_dias / maior_ciclo_vida)

    return score * P_economica * P_ecologica