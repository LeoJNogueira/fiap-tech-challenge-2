import pandas as pd
import numpy as np

def normalize_value(value, min_val, max_val, inverse=False):
    """Normaliza um valor para uma escala de 1 a 3."""
    if max_val == min_val:
        return 1.5  # Retorna um valor médio se não houver variação

    # Normaliza para o intervalo [0, 1]
    normalized = (value - min_val) / (max_val - min_val)

    if inverse:
        normalized = 1 - normalized

    # Mapeia para o intervalo [1, 3]
    return 1 + normalized * 2

def process_data(train_df, melh_df):
    """
    Processa e mescla os dataframes.
    """
    # Pega as culturas que já existem no train_data para não duplicar
    existing_cultures = train_df['CULTURA'].str.lower().tolist()

    # Novas linhas para adicionar
    new_rows = []

    # Encontrar min e max para normalização das colunas do data_melhorado
    min_cost = melh_df['Custo_Producao_R$/ha'].min()
    max_cost = melh_df['Custo_Producao_R$/ha'].max()

    min_prod = melh_df['Produtividade_t/ha'].min()
    max_prod = melh_df['Produtividade_t/ha'].max()

    min_water = melh_df['Requisito_Agua_mm'].min()
    max_water = melh_df['Requisito_Agua_mm'].max()

    min_return = melh_df['Retorno_Financeiro_R$/ha'].min()
    max_return = melh_df['Retorno_Financeiro_R$/ha'].max()

    for _, row in melh_df.iterrows():
        culture_name = row['Nome'].lower().replace('_', ' ')
        if culture_name not in existing_cultures:

            # Normalização
            cost_norm = normalize_value(row['Custo_Producao_R$/ha'], min_cost, max_cost, inverse=True)
            prod_norm = normalize_value(row['Produtividade_t/ha'], min_prod, max_prod)
            water_norm = normalize_value(row['Requisito_Agua_mm'], min_water, max_water, inverse=True)
            return_norm = normalize_value(row['Retorno_Financeiro_R$/ha'], min_return, max_return)

            # Ciclo de vida
            cycle_max = row['Ciclo_dias']
            cycle_min = cycle_max * 0.75 # Estimativa de 75% para o ciclo mínimo

            # Compatibilidade
            positive_comp = str(row['Compatibilidade_Positiva']).lower().replace(';', ',')
            negative_comp = str(row['Compatibilidade_Negativa']).lower().replace(';', ',')

            new_row = {
                'CULTURA': culture_name,
                'CUSTO PRODUÇÃO': round(cost_norm, 2),
                'PRODUTIVIDADE': round(prod_norm, 2),
                'CICLO DE VIDA MIN EM DIAS': int(cycle_min),
                'CICLO DE VIDA MAX EM DIAS': int(cycle_max),
                'REQUISITO DE ÁGUA': round(water_norm, 2),
                'RETORNO FINANCEIRO': round(return_norm, 2),
                'SINERGIA': 'nenhuma', # Simplificação conforme o plano
                'COMPANHEIRA': positive_comp if positive_comp != 'nan' else 'nenhuma',
                'NEUTRA': 'nenhuma', # Simplificação, poderia ser melhorado
                'ANTAGÔNICA': negative_comp if negative_comp != 'nan' else 'nenhuma',
                'ESPAÇO MÍNIMO m²': row['Espaco_Minimo_m2_por_Planta_ou_Area_minima_por_hectare']
            }
            new_rows.append(new_row)

    if new_rows:
        new_df = pd.DataFrame(new_rows)
        final_df = pd.concat([train_df, new_df], ignore_index=True)
        return final_df

    return train_df

if __name__ == "__main__":
    # Carregar os datasets
    train_data = pd.read_csv('train_data.csv')
    data_melhorado = pd.read_csv('data_melhorado.csv')

    # Processar e mesclar
    final_dataset = process_data(train_data, data_melhorado)

    # Salvar o resultado
    final_dataset.to_csv('train_data.csv', index=False)

    print("Arquivo 'train_data.csv' foi atualizado com sucesso!")
