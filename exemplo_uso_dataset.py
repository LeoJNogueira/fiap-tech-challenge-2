import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import random

class CulturaOptimizer:
    """
    Classe para otimização de culturas usando o dataset melhorado
    """

    def __init__(self, csv_path: str = 'data_melhorado.csv'):
        """Inicializa o otimizador carregando o dataset e pre-processando categorias"""
        self.df = pd.read_csv(csv_path)
        self.culturas = self.df.to_dict('records')
        self.area_total = 2.0  # 2 hectares em hectares

        # Mapeamento de categorias conceituais (para uso nas regras de fitness)
        self.culturas_que_produzem_sombra = {
            'Eucalipto', 'Seringueira', 'Jatobá', 'Pinus', 'Acácia', 'Coco', 'Dendê', 'Pecan',
            'Cacau', 'Banana', 'Manga', 'Abacate', 'Caju', 'Graviola', 'Pupunha', 'Guaraná',
            'Araticum', 'Laranja', 'Limão', 'Uva', 'Maçã', 'Pêssego'
            # Adicione mais conforme a necessidade e dados do seu CSV
        }
        self.culturas_anuais = {
            cultura['Nome'] for cultura in self.culturas if cultura['Ciclo_dias'] <= 365
        }
        self.culturas_adubacao_verde = {
            cultura['Nome'] for cultura in self.culturas if cultura['Tipo_Cultura'] == 'Adubacao_Verde'
        }
        self.culturas_nativas = {
            'Araticum', 'Guaraná', 'Jatobá', 'Pinhão', 'Erva_Mate'
            # Adicione mais conforme a necessidade e dados do seu CSV
        }
        self.exoticas_competitivas = {
            'Eucalipto', 'Pinus', 'Acácia' # Exemplos, baseie-se em conhecimento agronômico
            # Adicione mais se houver outras culturas no CSV que você considera "exóticas_competitivas"
        }
        self.exoticas_invasoras = set() # Se houver alguma no seu CSV, adicione aqui

    def get_cultura_data(self, nome_cultura: str) -> Dict:
        """Retorna os dados de uma cultura pelo nome."""
        for cultura in self.culturas:
            if cultura['Nome'] == nome_cultura:
                return cultura
        return None # Retorna None se a cultura não for encontrada

    def calcular_compatibilidade_score(self, cultura1_data: Dict, cultura2_data: Dict) -> float:
        """
        Calcula um score de compatibilidade entre duas culturas baseando-se nas listas e categorias.
        Returns: Score positivo para compatível, negativo para incompatível, 0 para neutro.
        """
        score = 0.0

        nome1 = cultura1_data['Nome']
        nome2 = cultura2_data['Nome']

        # Converte as strings de compatibilidade para listas
        compat_positiva1 = [c.strip() for c in str(cultura1_data.get('Compatibilidade_Positiva', '')).split(';') if c.strip()]
        compat_negativa1 = [c.strip() for c in str(cultura1_data.get('Compatibilidade_Negativa', '')).split(';') if c.strip()]

        # --- Avaliação de compatibilidade direta por nome ---
        if nome2 in compat_positiva1:
            score += 0.5 # Bônus para compatibilidade explícita
        if nome2 in compat_negativa1:
            score -= 1.0 # Penalidade para incompatibilidade explícita

        # --- Avaliação por categorias conceituais (baseado na cultura1) ---

        # Culturas de Sombra
        # Se cultura1 não se dá bem com sombra E cultura2 produz sombra
        if 'Culturas_Sombra' in compat_negativa1 and nome2 in self.culturas_que_produzem_sombra:
            score -= 0.8
        # Se cultura1 se beneficia da sombra E cultura2 produz sombra
        if 'Culturas_Sombra' in compat_positiva1 and nome2 in self.culturas_que_produzem_sombra:
            score += 0.4

        # Culturas de Cobertura
        # Se cultura1 se beneficia de culturas de cobertura E cultura2 é uma cultura de cobertura
        if 'Culturas_de_cobertura' in compat_positiva1 and nome2 in self.culturas_adubacao_verde:
            score += 0.6

        # Culturas Anuais (para perenes que são incompatíveis com anuais)
        # Se cultura1 é perene e não se dá bem com anuais E cultura2 é anual
        if cultura1_data['Ciclo_dias'] > 365 and 'Culturas_Anuais' in compat_negativa1 and nome2 in self.culturas_anuais:
            score -= 0.7

        # Exoticas Competitivas / Invasoras
        # Se cultura1 não se dá bem com exóticas competitivas E cultura2 é exótica competitiva
        if 'Exoticas_Competitivas' in compat_negativa1 and nome2 in self.exoticas_competitivas:
            score -= 1.2
        if 'Exoticas_Invasoras' in compat_negativa1 and nome2 in self.exoticas_invasoras:
            score -= 1.5 # Penalidade maior para invasoras

        # Culturas Nativas (se a compatibilidade com nativas for importante, ajustar aqui)
        # Se cultura1 se beneficia de nativas E cultura2 é nativa
        if 'Culturas_Nativas' in compat_positiva1 and nome2 in self.culturas_nativas:
             score += 0.3 # Bônus por ecossistema nativo

        # Considerar interações recíprocas (compatibilidade de c2 com c1)
        # Você pode decidir se quer que a compatibilidade seja simétrica ou não.
        # Por simplicidade, este exemplo foca principalmente na compatibilidade da cultura1 com cultura2.
        # Para simetria:
        # compat_positiva2 = [c.strip() for c in str(cultura2_data.get('Compatibilidade_Positiva', '')).split(';') if c.strip()]
        # if nome1 in compat_positiva2: score += 0.2
        # compat_negativa2 = [c.strip() for c in str(cultura2_data.get('Compatibilidade_Negativa', '')).split(';') if c.strip()]
        # if nome1 in compat_negativa2: score -= 0.5


        return score

    def validar_condicoes_climaticas(self, cultura_data: Dict, regiao_plantio: str, ph_solo: float, temp_ambiente: float) -> bool:
        """
        Valida se a cultura é adequada para a região e as condições edafoclimáticas.
        """
        # Valida Região Adaptada
        regioes_adaptadas = [r.strip() for r in str(cultura_data.get('Regiao_Adaptada', '')).split(';') if r.strip()]
        if 'Todas_Regioes' not in regioes_adaptadas and regiao_plantio not in regioes_adaptadas:
            return False

        # Valida pH do Solo
        ph_min = cultura_data.get('pH_Solo_Min')
        ph_max = cultura_data.get('pH_Solo_Max')
        if not (ph_min <= ph_solo <= ph_max):
            return False

        # Valida Temperatura
        temp_min = cultura_data.get('Temperatura_Min_C')
        temp_max = cultura_data.get('Temperatura_Max_C')
        if not (temp_min <= temp_ambiente <= temp_max):
            return False

        return True

    def gerar_individuo_aleatorio(self, regiao_predominante: str = 'Todas_Regioes', ph_medio: float = 6.5, temp_media: float = 25.0) -> List[Dict]:
        """
        Gera um indivíduo (configuração de plantio) aleatório para 2 hectares.
        Tenta respeitar o espaço mínimo e as condições climáticas iniciais.
        """
        individuo = []
        area_restante = self.area_total * 10000 # Convertendo para m2 para alocação

        # Filtra culturas viáveis para a região e condições climáticas iniciais
        culturas_viaveis = [
            c for c in self.culturas
            if self.validar_condicoes_climaticas(c, regiao_predominante, ph_medio, temp_media)
        ]

        if not culturas_viaveis:
            print(f"Aviso: Nenhuma cultura viável para a região {regiao_predominante} com pH {ph_medio} e temp {temp_media}. Gerando com todas as culturas.")
            culturas_viaveis = self.culturas # Fallback para garantir a geração de um indivíduo

        tentativas_max = 50 # Para evitar loop infinito se houver poucas culturas viáveis

        while area_restante > 0.01 * 10000 and tentativas_max > 0: # 0.01 ha = 100 m2
            cultura_escolhida = random.choice(culturas_viaveis)

            # Espaço mínimo em m2 por planta ou área mínima por hectare convertida para m2
            espaco_minimo_cultura = cultura_escolhida.get('Espaco_Minimo_m2_por_Planta_ou_Area_minima_por_hectare', 1.0) # Default para 1m2 se não especificado

            # Se for uma área mínima por hectare (indicado por um valor > 1.0, por exemplo, para florestais),
            # o espaco_minimo_cultura já é a área por planta ou unidade base.
            # Se for um valor muito pequeno, é m2 por planta. Vamos assumir que a coluna já está em m2 por planta ou m2 para a unidade base.

            # Decide uma área para esta cultura
            # Tenta pegar uma área que não seja menor que o espaço mínimo, mas que caiba na área restante

            # Para evitar que culturas com espaco_minimo muito grande dominem, ou vice-versa
            max_area_para_cultura_m2 = min(area_restante, 0.5 * self.area_total * 10000) # Máx 50% da área total por cultura

            # Certifica-se de que a área escolhida é pelo menos o espaço mínimo por planta
            if espaco_minimo_cultura > max_area_para_cultura_m2:
                tentativas_max -= 1
                continue # Não há espaço suficiente para essa cultura, tenta outra

            area_cultura_m2 = random.uniform(espaco_minimo_cultura, max_area_para_cultura_m2)

            # Arredonda para um valor razoável para evitar muitas culturas pequenas demais
            area_cultura_m2 = round(area_cultura_m2 / 100) * 100 # Arredonda para múltiplos de 100 m2 (0.01 ha)

            if area_cultura_m2 > 0:
                individuo.append({
                    'nome': cultura_escolhida['Nome'],
                    'area_m2': area_cultura_m2,
                    'epoca_plantio': cultura_escolhida['Epoca_Plantio'], # Inclui época para o indivíduo
                    'regiao_plantio': regiao_predominante, # Assume a região geral do indivíduo
                    'ph_solo': ph_medio, # Assume o pH geral do indivíduo
                    'temperatura': temp_media # Assume a temperatura geral do indivíduo
                })
                area_restante -= area_cultura_m2

            tentativas_max -= 1
            if len(individuo) >= 10: # Limita o número de culturas para um indivíduo mais gerenciável
                break

        # Ajusta a última cultura para usar a área restante se for pequena
        if area_restante > 0 and len(individuo) > 0:
            individuo[-1]['area_m2'] += area_restante

        # Converte a área de m2 para hectares
        for cultura_plantada in individuo:
            cultura_plantada['area_ha'] = cultura_plantada['area_m2'] / 10000

        return individuo

    def calcular_fitness(self, individuo: List[Dict]) -> float:
        """
        Calcula o fitness de um indivíduo (configuração de plantio).
        Um fitness maior é melhor.
        """
        lucro_total = 0.0
        produtividade_total = 0.0
        penalidade_total = 0.0
        bonus_total = 0.0
        area_total_usada = 0.0

        for i, cultura_na_parcela_i in enumerate(individuo):
            nome_cultura_i = cultura_na_parcela_i['nome']
            area_ha_i = cultura_na_parcela_i['area_ha']
            area_total_usada += area_ha_i

            dados_cultura_i = self.get_cultura_data(nome_cultura_i)
            if not dados_cultura_i:
                penalidade_total += 100000 # Penalidade alta para cultura inválida
                continue

            # --- Componentes de Lucro e Produtividade ---
            lucro_total += dados_cultura_i['Lucro_R$/ha'] * area_ha_i
            produtividade_total += dados_cultura_i['Produtividade_t/ha'] * area_ha_i

            # --- Validação de Condições Edafoclimáticas e Regionais (Penalidade) ---
            # Assume que ph_solo e temperatura estão no indivíduo ou são globais para o terreno
            if not self.validar_condicoes_climaticas(
                dados_cultura_i,
                cultura_na_parcela_i['regiao_plantio'],
                cultura_na_parcela_i['ph_solo'],
                cultura_na_parcela_i['temperatura']
            ):
                penalidade_total += 5000 * area_ha_i # Penalidade por cultura em local inadequado

            # --- Penalidade por Espaço Mínimo (considera densidade) ---
            # Se a área alocada for menor que o espaço mínimo esperado por planta
            # ou se a densidade for muito alta, dependendo da interpretação.
            # Aqui, vou usar como uma validação de que a alocação foi feita corretamente.
            # Se for para penalizar *não usar* espaço mínimo, seria diferente.
            # Para simplificar, vou assumir que 'Espaco_Minimo_m2_por_Planta_ou_Area_minima_por_hectare'
            # representa o espaço que *cada unidade* da cultura precisa, e a `area_ha_i`
            # deve ser consistente com isso (ie. a área foi alocada respeitando essa necessidade).
            # Se a intenção é que o AG evite densidades muito baixas/altas, a lógica seria mais complexa.

            # --- Avaliação de Compatibilidade entre Culturas no mesmo indivíduo ---
            for j, outra_cultura_na_parcela_j in enumerate(individuo):
                if i == j: continue # Não compare a cultura consigo mesma

                nome_outra_cultura_j = outra_cultura_na_parcela_j['nome']
                dados_outra_cultura_j = self.get_cultura_data(nome_outra_cultura_j)
                if not dados_outra_cultura_j: continue # Se a outra cultura for inválida

                compat_score = self.calcular_compatibilidade_score(dados_cultura_i, dados_outra_cultura_j)

                if compat_score < 0:
                    # Penalidade proporcional à incompatibilidade e à área das culturas envolvidas
                    penalidade_total += abs(compat_score) * 2000 * (area_ha_i + outra_cultura_na_parcela_j['area_ha'])
                elif compat_score > 0:
                    # Bônus proporcional à compatibilidade e à área
                    bonus_total += compat_score * 1000 * (area_ha_i + outra_cultura_na_parcela_j['area_ha'])

            # --- Penalidade por época de plantio inadequada para o período simulado ---
            # Esta lógica assume que o "individuo" está sendo avaliado para um momento específico do ano
            # Ou que as culturas anuais devem estar em rotação correta.
            # Por simplicidade, vou assumir que Epoca_Plantio no CSV indica o período ideal.
            # Se o indivíduo tiver uma 'epoca_simulada', poderia validar aqui.
            # Ex: se o AG tenta plantar "Milho" (Out-Dez) em "Mai-Jul" seria uma penalidade.
            # Por enquanto, a época é apenas um dado da cultura.

        # --- Penalidade por não usar a área total (se for um objetivo) ---
        if self.area_total - area_total_usada > 0.001: # Se sobrar mais de 10 m2
            penalidade_total += 5000 * (self.area_total - area_total_usada) # Penalidade por área não utilizada

        # --- Função de Fitness Principal ---
        # Combinação de lucro, produtividade, bônus e penalidades
        # Os pesos (1.0, 0.5, 0.1) devem ser ajustados conforme a prioridade do problema
        fitness = (
            1.0 * lucro_total +
            0.5 * produtividade_total - # Valorizando a produtividade também
            penalidade_total +
            bonus_total
        )
        return fitness

    def exibir_individuo(self, individuo: List[Dict]):
        """Exibe os detalhes de um indivíduo."""
        print("-" * 60)
        print("🌱 Configuração do Indivíduo:")
        lucro_total = 0
        produtividade_total = 0
        area_total_usada = 0

        for cultura_plantada in individuo:
            nome = cultura_plantada['nome']
            area_ha = cultura_plantada['area_ha']
            area_total_usada += area_ha
            dados_cultura = self.get_cultura_data(nome)

            if dados_cultura:
                lucro = dados_cultura['Lucro_R$/ha'] * area_ha
                produtividade = dados_cultura['Produtividade_t/ha'] * area_ha
                lucro_total += lucro
                produtividade_total += produtividade
                print(f"  - {nome}: {area_ha:.2f} ha (Lucro: R$ {lucro:,.2f}, Prod: {produtividade:.2f} t)")
            else:
                print(f"  - {nome}: Cultura não encontrada no dataset! ({area_ha:.2f} ha)")

        fitness = self.calcular_fitness(individuo)

        print(f"\n  Área total utilizada: {area_total_usada:.2f} ha / {self.area_total:.2f} ha")
        print(f"  Área disponível: {self.area_total - area_total_usada:.2f} ha")
        print(f"  Lucro total estimado: R$ {lucro_total:,.2f}")
        print(f"  Produtividade total estimada: {produtividade_total:,.2f} t")
        print(f"  Fitness: {fitness:,.2f}")
        print("=" * 60)

    def validar_individuo(self, individuo: List[Dict]) -> Tuple[bool, List[str]]:
        """
        Valida se um indivíduo (configuração de plantio) respeita todas as restrições.
        Retorna True se válido e uma lista de mensagens de erro se inválido.
        """
        is_valid = True
        erros = []
        area_total_usada = 0.0

        if not individuo:
            return False, ["Indivíduo vazio."]

        # 1. Validação de área total
        for cultura_na_parcela in individuo:
            area_total_usada += cultura_na_parcela.get('area_ha', 0)

        if abs(area_total_usada - self.area_total) > 0.01: # Tolerância de 0.01 ha (100 m2)
            is_valid = False
            erros.append(f"Área total utilizada ({area_total_usada:.2f} ha) difere da área total ({self.area_total:.2f} ha).")

        # 2. Validação de condições edafoclimáticas e regionais para cada cultura
        for cultura_na_parcela in individuo:
            nome_cultura = cultura_na_parcela['nome']
            dados_cultura = self.get_cultura_data(nome_cultura)
            if not dados_cultura:
                is_valid = False
                erros.append(f"Cultura '{nome_cultura}' não encontrada no dataset.")
                continue

            # Assume que ph_solo, temperatura e regiao_plantio estão no indivíduo ou são globais do terreno
            if not self.validar_condicoes_climaticas(
                dados_cultura,
                cultura_na_parcela['regiao_plantio'],
                cultura_na_parcela['ph_solo'],
                cultura_na_parcela['temperatura']
            ):
                is_valid = False
                erros.append(f"Cultura '{nome_cultura}' não se adapta às condições edafoclimáticas/regionais da parcela.")

            # 3. Validação de Espaço Mínimo (interpretação da alocação)
            espaco_minimo_cultura = dados_cultura.get('Espaco_Minimo_m2_por_Planta_ou_Area_minima_por_hectare', 0)
            area_m2_alocada = cultura_na_parcela.get('area_m2', 0)

            # Se 'Espaco_Minimo_m2_por_Planta_ou_Area_minima_por_hectare' é interpretado como 'espaço por planta':
            # E se a cultura exige um espaço mínimo que não foi fornecido pela área alocada
            # Isso é mais complexo para validar sem saber o número de plantas.
            # Uma forma simples é garantir que a área alocada seja pelo menos um múltiplo do espaço mínimo,
            # ou que não seja abaixo de um threshold razoável para a cultura.
            # Para este exemplo, vou simplificar: se o espaço mínimo é muito grande (ex: > 1m2),
            # garante que a área alocada não é trivialmente pequena.
            if espaco_minimo_cultura > 1.0 and area_m2_alocada < espaco_minimo_cultura:
                 is_valid = False
                 erros.append(f"Cultura '{nome_cultura}' requer espaço mínimo de {espaco_minimo_cultura:.2f} m2, mas área alocada é {area_m2_alocada:.2f} m2.")


        # 4. Validação de Compatibilidade (direta e categórica)
        for i, cultura_na_parcela_i in enumerate(individuo):
            nome_cultura_i = cultura_na_parcela_i['nome']
            dados_cultura_i = self.get_cultura_data(nome_cultura_i)
            if not dados_cultura_i: continue

            compat_negativa_i = [c.strip() for c in str(dados_cultura_i.get('Compatibilidade_Negativa', '')).split(';') if c.strip()]

            for j, cultura_na_parcela_j in enumerate(individuo):
                if i == j: continue

                nome_cultura_j = cultura_na_parcela_j['nome']
                dados_cultura_j = self.get_cultura_data(nome_cultura_j)
                if not dados_cultura_j: continue

                # Verifica incompatibilidade direta
                if nome_cultura_j in compat_negativa_i:
                    is_valid = False
                    erros.append(f"Incompatibilidade direta: '{nome_cultura_i}' e '{nome_cultura_j}' são incompatíveis.")

                # Verifica incompatibilidade por categorias
                # Culturas Sombra
                if 'Culturas_Sombra' in compat_negativa_i and nome_cultura_j in self.culturas_que_produzem_sombra:
                    is_valid = False
                    erros.append(f"Incompatibilidade por sombra: '{nome_cultura_i}' não tolera sombra de '{nome_cultura_j}'.")

                # Culturas Anuais vs Perenes
                if dados_cultura_i['Ciclo_dias'] > 365 and 'Culturas_Anuais' in compat_negativa_i and nome_cultura_j in self.culturas_anuais:
                    is_valid = False
                    erros.append(f"Incompatibilidade temporal: Perene '{nome_cultura_i}' não se associa bem com anual '{nome_cultura_j}'.")

                # Exoticas Competitivas
                if 'Exoticas_Competitivas' in compat_negativa_i and nome_cultura_j in self.exoticas_competitivas:
                    is_valid = False
                    erros.append(f"Incompatibilidade competitiva: '{nome_cultura_i}' não compete bem com '{nome_cultura_j}'.")

        return is_valid, erros


def exemplo_uso():
    """
    Exemplo de uso do dataset melhorado com o Algoritmo Genético
    """
    print("🚀 EXEMPLO DE USO DO DATASET MELHORADO COM VALIDAÇÕES AVANÇADAS")
    print("=" * 50)

    # Inicializa otimizador
    optimizer = CulturaOptimizer()

    # Exibe estatísticas do dataset
    print(f"📊 Dataset carregado com {len(optimizer.culturas)} culturas")
    print(f"🌱 Tipos de cultura: {optimizer.df['Tipo_Cultura'].unique()}")

    # Para regiões, é melhor processar de forma única
    todas_regioes = set()
    for regioes_str in optimizer.df['Regiao_Adaptada'].dropna():
        for reg in regioes_str.split(';'):
            todas_regioes.add(reg.strip())
    print(f"🗺️ Regiões cobertas: {todas_regioes}")
    print(f"🌲 Culturas que produzem sombra: {optimizer.culturas_que_produzem_sombra}")
    print(f"🌿 Culturas anuais (baseado no ciclo): {optimizer.culturas_anuais}")
    print(f"💚 Culturas de adubação verde: {optimizer.culturas_adubacao_verde}")
    print("-" * 50)

    # Gera e exibe alguns indivíduos aleatórios
    regioes_teste = ['Sudeste', 'Nordeste', 'Sul'] # Usar nomes completos das regiões
    ph_test = [6.0, 6.5, 7.0]
    temp_test = [22.0, 25.0, 28.0]

    for i in range(3): # Gera 3 indivíduos para teste
        regiao = random.choice(regioes_teste)
        ph = random.choice(ph_test)
        temp = random.choice(temp_test)

        print(f"\n--- Gerando Indivíduo Aleatório para Região: {regiao}, pH: {ph}, Temp: {temp} ---")
        individuo = optimizer.gerar_individuo_aleatorio(regiao, ph, temp)
        optimizer.exibir_individuo(individuo)

        # Valida o indivíduo gerado
        is_valid, erros = optimizer.validar_individuo(individuo)
        if is_valid:
            print("✅ Indivíduo Válido!")
        else:
            print("❌ Indivíduo Inválido! Erros:")
            for erro in erros:
                print(f"  - {erro}")

    # Exemplo de análise de compatibilidade detalhada
    print("\n🔗 ANÁLISE DE COMPATIBILIDADE (Exemplo)")
    print("=" * 50)

    cultura_a = optimizer.get_cultura_data('Milho')
    cultura_b = optimizer.get_cultura_data('Soja')
    cultura_c = optimizer.get_cultura_data('Eucalipto')
    cultura_d = optimizer.get_cultura_data('Pimenta_do_Reino')
    cultura_e = optimizer.get_cultura_data('Crotalária')

    if cultura_a and cultura_b:
        score_ab = optimizer.calcular_compatibilidade_score(cultura_a, cultura_b)
        print(f"Score de compatibilidade entre {cultura_a['Nome']} e {cultura_b['Nome']}: {score_ab}")

    if cultura_d and cultura_c:
        score_dc = optimizer.calcular_compatibilidade_score(cultura_d, cultura_c)
        print(f"Score de compatibilidade entre {cultura_d['Nome']} (não gosta de sombra) e {cultura_c['Nome']} (produz sombra): {score_dc}")

    if cultura_a and cultura_e:
        score_ae = optimizer.calcular_compatibilidade_score(cultura_a, cultura_e)
        print(f"Score de compatibilidade entre {cultura_a['Nome']} e {cultura_e['Nome']} (cultura de cobertura): {score_ae}")


if __name__ == "__main__":
    exemplo_uso()