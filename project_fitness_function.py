def project_fitness_function(sample, orcamento_maximo, m2_area, limite_agua, janela_dias):
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
    normalized_competition_score = 0 if competition_score < 0 else 1 if competition_score > 1 else competition_score
    print('comp: ', normalized_competition_score)

    # score = (W_prod * production_score)+(W_comp * competition_score)
    score = (W_prod * normalized_production_score) + (W_comp * competition_score)

    print(score)

    # penalidades

    custo_total = 0
    agua_total = 0
    ciclo_de_vida = []
    area_total = 0

    for s in sample.iterrows():
        custo_total += s[1]['CUSTO PRODUÇÃO']
        agua_total += s[1]['REQUISITO DE ÁGUA']
        area_total += s[1]['ESPAÇO MÍNIMO m²']
        ciclo_de_vida.append(s[1]['CICLO DE VIDA MAX EM DIAS'])

    # Se Custo Total > Orçamento_Máximo, então P_econômica = 0.01, senão P_econômica=1

    P_economica = 0.01 if custo_total >= orcamento_maximo else 1

    P_economica += 1 - (area_total / m2_area)

    # Água Total > Sua_Disponibilidade_de_Água, então P_ecológica = 0.01, senão P_ecológica = 1

    P_ecologica = 0.01 if agua_total >= limite_agua else 1

    # ciclo de vida: verificar se o ciclo de vida mais longo cabe na janela de plantio

    if max(ciclo_de_vida) > janela_dias:
        P_ecologica += 0.5

    fitness = score * P_economica * P_ecologica

    print(fitness)