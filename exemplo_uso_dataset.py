import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import random

class CulturaOptimizer:
    """
    Classe para otimização de culturas usando o dataset melhorado
    """

    def __init__(self, csv_path: str = 'data_melhorado.csv'):
        """Inicializa o otimizador carregando o dataset"""
        self.df = pd.read_csv(csv_path)
        self.culturas = self.df.to_dict('records')
        self.area_total = 2.0  # 2 hectares

    def calcular_compatibilidade(self, cultura1: str, cultura2: str) -> float:
        """
        Calcula score de compatibilidade entre duas culturas
        Returns: 1.0 (compatível), -1.0 (incompatível), 0.0 (neutro)
        """
        c1 = self.df[self.df['Nome'] == cultura1].iloc[0]
        c2 = self.df[self.df['Nome'] == cultura2].iloc[0]

        # Verifica compatibilidade positiva
        if cultura2 in c1['Compatibilidade_Positiva'].split(';'):
            return 1.0

        # Verifica compatibilidade negativa
        if cultura2 in c1['Compatibilidade_Negativa'].split(';'):
            return -1.0

        return 0.0

    def validar_condicoes_climaticas(self, cultura: str, regiao: str = 'SE') -> bool:
        """
        Valida se a cultura é adequada para a região
        """
        cultura_data = self.df[self.df['Nome'] == cultura].iloc[0]
        regioes_adaptadas = cultura_data['Regiao_Adaptada'].split(';')

        return regiao in regioes_adaptadas or 'Todas' in regioes_adaptadas

    def calcular_fitness(self, individuo: Dict) -> float:
        """
        Calcula fitness de um indivíduo (configuração de culturas)

        Args:
            individuo: {'cultura': str, 'area_ha': float, 'regiao': str}
        """
        fitness = 0.0
        culturas_plantadas = []

        for parcela in individuo['parcelas']:
            cultura = parcela['cultura']
            area = parcela['area_ha']

            # Dados da cultura
            cultura_data = self.df[self.df['Nome'] == cultura].iloc[0]

            # Componentes do fitness
            lucro = cultura_data['Lucro_R$/ha'] * area
            produtividade = cultura_data['Produtividade_t/ha'] * area

            # Penalidade por condições inadequadas
            if not self.validar_condicoes_climaticas(cultura, individuo['regiao']):
                lucro *= 0.5  # Reduz lucro em 50%

            fitness += lucro + (produtividade * 100)  # Peso para produtividade
            culturas_plantadas.append(cultura)

        # Bonus/penalidade por compatibilidade
        compatibilidade_score = 0
        for i, cultura1 in enumerate(culturas_plantadas):
            for j, cultura2 in enumerate(culturas_plantadas[i+1:], i+1):
                comp = self.calcular_compatibilidade(cultura1, cultura2)
                compatibilidade_score += comp * 1000  # Peso para compatibilidade

        fitness += compatibilidade_score

        return fitness

    def gerar_individuo_aleatorio(self, regiao: str = 'SE') -> Dict:
        """
        Gera um indivíduo aleatório respeitando restrições
        """
        individuo = {
            'regiao': regiao,
            'parcelas': []
        }

        area_restante = self.area_total
        num_parcelas = random.randint(1, 3)  # 1 a 3 culturas diferentes

        for i in range(num_parcelas):
            if area_restante <= 0:
                break

            # Seleciona cultura aleatória adequada à região
            culturas_validas = [
                c for c in self.culturas
                if self.validar_condicoes_climaticas(c['Nome'], regiao)
            ]

            cultura = random.choice(culturas_validas)

            # Define área (mínimo 0.2ha, máximo área restante)
            area_min = min(0.2, area_restante)
            area_max = min(1.5, area_restante)  # Máximo 1.5ha por cultura
            area = round(random.uniform(area_min, area_max), 2)

            individuo['parcelas'].append({
                'cultura': cultura['Nome'],
                'area_ha': area
            })

            area_restante -= area

        return individuo

    def exibir_individuo(self, individuo: Dict) -> None:
        """
        Exibe informações detalhadas de um indivíduo
        """
        print(f"\n🌾 CONFIGURAÇÃO DE PLANTIO - REGIÃO {individuo['regiao']}")
        print("=" * 60)

        area_total_usada = 0
        lucro_total = 0

        for i, parcela in enumerate(individuo['parcelas'], 1):
            cultura = parcela['cultura']
            area = parcela['area_ha']

            cultura_data = self.df[self.df['Nome'] == cultura].iloc[0]

            lucro_parcela = cultura_data['Lucro_R$/ha'] * area
            produtividade_parcela = cultura_data['Produtividade_t/ha'] * area

            print(f"Parcela {i}: {cultura}")
            print(f"  📏 Área: {area} ha")
            print(f"  💰 Lucro: R$ {lucro_parcela:,.2f}")
            print(f"  🌾 Produção: {produtividade_parcela:.1f} t")
            print(f"  📅 Plantio: {cultura_data['Epoca_Plantio']}")
            print(f"  🔄 Ciclo: {cultura_data['Ciclo_dias']} dias")
            print()

            area_total_usada += area
            lucro_total += lucro_parcela

        fitness = self.calcular_fitness(individuo)

        print(f"📊 RESUMO:")
        print(f"  Área total utilizada: {area_total_usada:.2f} ha")
        print(f"  Área disponível: {self.area_total - area_total_usada:.2f} ha")
        print(f"  Lucro total estimado: R$ {lucro_total:,.2f}")
        print(f"  Fitness: {fitness:,.2f}")
        print("=" * 60)

def exemplo_uso():
    """
    Exemplo de uso do dataset melhorado
    """
    print("🚀 EXEMPLO DE USO DO DATASET MELHORADO")
    print("=" * 50)

    # Inicializa otimizador
    optimizer = CulturaOptimizer()

    # Exibe estatísticas do dataset
    print(f"📊 Dataset carregado com {len(optimizer.culturas)} culturas")
    print(f"🌱 Tipos de cultura: {optimizer.df['Tipo_Cultura'].unique()}")
    print(f"🗺️ Regiões cobertas: {set([r for regioes in optimizer.df['Regiao_Adaptada'] for r in regioes.split(';')])}")

    # Gera e exibe alguns indivíduos aleatórios
    regioes = ['SE', 'CO', 'S', 'NE', 'N']

    for regiao in regioes[:3]:  # Testa 3 regiões
        individuo = optimizer.gerar_individuo_aleatorio(regiao)
        optimizer.exibir_individuo(individuo)

    # Exemplo de análise de compatibilidade
    print("\n🔗 ANÁLISE DE COMPATIBILIDADE")
    print("=" * 40)

    culturas_teste = ['Milho', 'Soja', 'Feijão', 'Algodão']

    for i, c1 in enumerate(culturas_teste):
        for c2 in culturas_teste[i+1:]:
            comp = optimizer.calcular_compatibilidade(c1, c2)
            status = "✅ Compatível" if comp > 0 else "❌ Incompatível" if comp < 0 else "⚪ Neutro"
            print(f"{c1} + {c2}: {status}")

if __name__ == "__main__":
    exemplo_uso()
