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

    for _ in range(len(population)//2):
        parent1, parent2 = select_unique_parents(population)

        offspring1, offspring2 = crossover_individuals(parent1, parent2)

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
    # Get rows that are in sample2 but not in sample1
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
    # pontuação normalizada do conjunto
    W_prod = 0.6
    W_comp = 0.4

    # para cada cultura do conjunto
    # pontuação_produtividade = (produtividade/espaço minimo)
    normalized_production_score = 0
    competition_score = 0

    for s in sample.iterrows():
        production_score = (s[1]['PRODUTIVIDADE'] / s[1]['ESPAÇO MÍNIMO m²'])
        normalized_production_score += production_score

    # para cada cultura do conjunto
    # pontuação_competitividade = 0
    # +1.0 Sinérgica
    # +0.5 Companheira
    # 0.0 Neutra
    # -1.0 Antagônica

    plant_map = dict()

    for s in sample.iterrows():
        plant_map[s[1]['CULTURA']] = dict(sinergia=s[1]['SINERGIA'].split(','),
                                          companheira=s[1]['COMPANHEIRA'].split(','), neutra=s[1]['NEUTRA'].split(','),
                                          antagonica=s[1]['ANTAGÔNICA'].split(','))

    # print(plant_map)

    # score de compatibilidade
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

    # normalizar para ficar entre 0 e 1
    normalized_competition_score = 0 if competition_score <= 0 else 1 if competition_score >= 1 else competition_score

    # score = (W_prod * production_score)+(W_comp * competition_score)
    score = (W_prod * normalized_production_score) + (W_comp * normalized_competition_score)

    # penalidades

    custo_total = 0
    consumo_agua_cultura = 0
    ciclo_de_vida = []
    area_total_cultura = 0

    for s in sample.iterrows():
        custo_total += s[1]['CUSTO PRODUÇÃO']
        consumo_agua_cultura += s[1]['REQUISITO DE ÁGUA']
        area_total_cultura += s[1]['ESPAÇO MÍNIMO m²']
        ciclo_de_vida.append(s[1]['CICLO DE VIDA MAX EM DIAS'])

    # Se Custo Total > Orçamento_Máximo, então P_econômica = 0.01, senão P_econômica=1

    P_economica = 0.01 if custo_total >= orcamento_maximo else 1

    P_economica += 1 - (area_total_cultura / m2_area_disponivel)

    # Água Total > Sua_Disponibilidade_de_Água, então P_ecológica = 0.01, senão P_ecológica = 1

    P_ecologica = 0.01 if consumo_agua_cultura >= limite_agua else 1

    # ciclo de vida: verificar se o ciclo de vida mais longo cabe na janela de plantio

    if max(ciclo_de_vida) > janela_dias:
        P_ecologica += 0.5

    return score * P_economica * P_ecologica