#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXEMPLO DE INTEGRAÇÃO KSP - ORION GROUP
Demonstra como importar dados do Kerbal Space Program e gerar telemetria

Este arquivo mostra como você pode:
1. Exportar dados do KSP em CSV
2. Compará-los com a simulação
3. Ajustar parâmetros conforme necessário
"""

import csv
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path


# ============================================================================
# FUNÇÕES DE IMPORTAÇÃO DE DADOS KSP
# ============================================================================

def importar_csv_ksp(caminho_arquivo):
    """
    Importa dados de telemetria exportados do KSP em formato CSV.

    Formato esperado do CSV:
    tempo,altitude,velocidade,aceleracao,massa

    Args:
        caminho_arquivo (str): Caminho do arquivo CSV do KSP

    Returns:
        dict: Dicionário com listas de dados
    """

    dados = {
        'tempo': [],
        'altitude': [],
        'velocidade': [],
        'aceleracao': [],
        'massa': []
    }

    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            leitor = csv.DictReader(f)

            for linha in leitor:
                dados['tempo'].append(float(linha['tempo']))
                dados['altitude'].append(float(linha['altitude']))
                dados['velocidade'].append(float(linha['velocidade']))
                dados['aceleracao'].append(float(linha['aceleracao']))
                dados['massa'].append(float(linha['massa']))

        print(f"✓ Dados KSP carregados com sucesso!")
        print(f"  Total de pontos: {len(dados['tempo'])}")
        print(f"  Duração: {dados['tempo'][-1]:.1f}s")
        print(f"  Altitude máxima: {max(dados['altitude']) / 1000:.2f} km")

        return dados

    except FileNotFoundError:
        print(f"✗ Erro: Arquivo não encontrado: {caminho_arquivo}")
        return None
    except KeyError as e:
        print(f"✗ Erro: Coluna esperada não encontrada: {e}")
        print("  Colunas esperadas: tempo, altitude, velocidade, aceleracao, massa")
        return None


def criar_csv_exemplo(nome_arquivo='dados_ksp_exemplo.csv'):
    """
    Cria um arquivo CSV de exemplo para teste.

    Este arquivo simula dados de uma queimada real do KSP.
    """

    import os

    # Criar dados simulados de uma queimada do KSP
    dados_exemplo = [
        "tempo,altitude,velocidade,aceleracao,massa",
        "0,0,0,0,330300",
        "1,5.2,9.8,10.1,328682",
        "2,20.8,19.6,10.2,327064",
        "5,130.5,49.0,10.3,321546",
        "10,522.0,98.0,10.4,314928",
        "15,1177.5,147.0,10.5,308310",
        "20,2097.0,196.0,10.6,301692",
        "30,6615.0,294.0,10.8,288456",
        "40,13697.0,392.0,11.0,275220",
        "50,23343.0,490.0,11.2,261984",
        "60,35553.0,588.0,11.4,248748",
        "70,50327.0,686.0,11.6,235512",
        "80,67665.0,784.0,11.8,222276",
        "89,84521.0,862.0,12.0,209040",
    ]

    caminho = Path(f'dados/{nome_arquivo}')
    caminho.parent.mkdir(exist_ok=True)

    with open(caminho, 'w') as f:
        f.write('\n'.join(dados_exemplo))

    print(f"✓ Arquivo de exemplo criado: {caminho}")
    return str(caminho)


# ============================================================================
# FUNÇÕES DE COMPARAÇÃO E ANÁLISE
# ============================================================================

def comparar_simulacao_vs_ksp(dados_simulados, dados_ksp):
    """
    Compara dados da simulação com dados reais do KSP.

    Calcula desvios e diferenças percentuais.

    Args:
        dados_simulados (dict): Dados da simulação
        dados_ksp (dict): Dados importados do KSP

    Returns:
        dict: Análise comparativa
    """

    print("\n" + "=" * 70)
    print("ANÁLISE COMPARATIVA: SIMULAÇÃO vs KSP")
    print("=" * 70)

    # Verificar se têm o mesmo comprimento
    len_sim = len(dados_simulados['tempo'])
    len_ksp = len(dados_ksp['tempo'])

    print(f"\nTamanho dos datasets:")
    print(f"  Simulação: {len_sim} pontos")
    print(f"  KSP:       {len_ksp} pontos")

    # Calcular desvios
    analise = {
        'desvio_altitude_media': 0,
        'desvio_velocidade_media': 0,
        'desvio_tempo_final': abs(dados_simulados['tempo'][-1] - dados_ksp['tempo'][-1]),
        'altitude_max_sim': max(dados_simulados['altitude']),
        'altitude_max_ksp': max(dados_ksp['altitude']),
        'velocidade_max_sim': max(dados_simulados['velocidade']),
        'velocidade_max_ksp': max(dados_ksp['velocidade']),
    }

    # Interpolar dados para mesma quantidade de pontos
    min_len = min(len_sim, len_ksp)

    desvios_alt = []
    desvios_vel = []

    for i in range(min_len):
        desvio_alt = abs(dados_simulados['altitude'][i] - dados_ksp['altitude'][i])
        desvio_vel = abs(dados_simulados['velocidade'][i] - dados_ksp['velocidade'][i])

        desvios_alt.append(desvio_alt)
        desvios_vel.append(desvio_vel)

    analise['desvio_altitude_media'] = np.mean(desvios_alt)
    analise['desvio_velocidade_media'] = np.mean(desvios_vel)
    analise['desvio_altitude_max'] = max(desvios_alt)
    analise['desvio_velocidade_max'] = max(desvios_vel)

    # Imprimir resultados
    print(f"\nAltitude Máxima:")
    print(f"  Simulação: {analise['altitude_max_sim'] / 1000:,.2f} km")
    print(f"  KSP:       {analise['altitude_max_ksp'] / 1000:,.2f} km")
    print(f"  Diferença: {abs(analise['altitude_max_sim'] - analise['altitude_max_ksp']) / 1000:,.2f} km")

    print(f"\nVelocidade Máxima:")
    print(f"  Simulação: {analise['velocidade_max_sim']:,.2f} m/s")
    print(f"  KSP:       {analise['velocidade_max_ksp']:,.2f} m/s")
    print(f"  Diferença: {abs(analise['velocidade_max_sim'] - analise['velocidade_max_ksp']):,.2f} m/s")

    print(f"\nDesvios Médios:")
    print(f"  Altitude: {analise['desvio_altitude_media']:.2f} m (máximo: {analise['desvio_altitude_max']:.2f} m)")
    print(
        f"  Velocidade: {analise['desvio_velocidade_media']:.2f} m/s (máximo: {analise['desvio_velocidade_max']:.2f} m/s)")

    print("=" * 70)

    return analise


def plotar_comparacao(dados_simulados, dados_ksp, nome_saida='comparacao_ksp.png'):
    """
    Cria gráficos comparativos entre simulação e KSP.

    Args:
        dados_simulados (dict): Dados da simulação
        dados_ksp (dict): Dados do KSP
        nome_saida (str): Nome do arquivo de saída
    """

    # Criar figura com 2x2 subplots
    fig, axs = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('COMPARAÇÃO: SIMULAÇÃO vs KSP - ORION GROUP',
                 fontsize=16, fontweight='bold')

    # ====== Altitude ======
    ax = axs[0, 0]
    ax.plot(dados_simulados['tempo'], np.array(dados_simulados['altitude']) / 1000,
            label='Simulação', linewidth=2, color='#FF6B35')
    ax.plot(dados_ksp['tempo'], np.array(dados_ksp['altitude']) / 1000,
            label='KSP Real', linewidth=2, color='#004E89', linestyle='--')
    ax.set_xlabel('Tempo (s)', fontweight='bold')
    ax.set_ylabel('Altitude (km)', fontweight='bold')
    ax.set_title('ALTITUDE vs TEMPO', fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # ====== Velocidade ======
    ax = axs[0, 1]
    ax.plot(dados_simulados['tempo'], dados_simulados['velocidade'],
            label='Simulação', linewidth=2, color='#004E89')
    ax.plot(dados_ksp['tempo'], dados_ksp['velocidade'],
            label='KSP Real', linewidth=2, color='#FF6B35', linestyle='--')
    ax.set_xlabel('Tempo (s)', fontweight='bold')
    ax.set_ylabel('Velocidade (m/s)', fontweight='bold')
    ax.set_title('VELOCIDADE vs TEMPO', fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # ====== Desvio de Altitude ======
    ax = axs[1, 0]
    min_len = min(len(dados_simulados['tempo']), len(dados_ksp['tempo']))
    desvios_alt = [abs(dados_simulados['altitude'][i] - dados_ksp['altitude'][i])
                   for i in range(min_len)]
    ax.fill_between(range(min_len), desvios_alt, alpha=0.3, color='#D62828')
    ax.plot(desvios_alt, color='#D62828', linewidth=2)
    ax.set_xlabel('Ponto de Dados', fontweight='bold')
    ax.set_ylabel('Desvio (metros)', fontweight='bold')
    ax.set_title('DESVIO DE ALTITUDE (Sim vs KSP)', fontweight='bold')
    ax.grid(True, alpha=0.3)

    # ====== Desvio de Velocidade ======
    ax = axs[1, 1]
    desvios_vel = [abs(dados_simulados['velocidade'][i] - dados_ksp['velocidade'][i])
                   for i in range(min_len)]
    ax.fill_between(range(min_len), desvios_vel, alpha=0.3, color='#1B998B')
    ax.plot(desvios_vel, color='#1B998B', linewidth=2)
    ax.set_xlabel('Ponto de Dados', fontweight='bold')
    ax.set_ylabel('Desvio (m/s)', fontweight='bold')
    ax.set_title('DESVIO DE VELOCIDADE (Sim vs KSP)', fontweight='bold')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()

    # Salvar
    Path('graficos').mkdir(exist_ok=True)
    caminho = f'graficos/{nome_saida}'
    plt.savefig(caminho, dpi=300, bbox_inches='tight')
    print(f"\n✓ Gráfico de comparação salvo: {caminho}")

    plt.show()


# ============================================================================
# FUNÇÃO PRINCIPAL - DEMONSTRAÇÃO
# ============================================================================

def main():
    """
    Demonstra como integrar dados do KSP.

    Este exemplo:
    1. Cria um CSV de exemplo
    2. Importa os dados
    3. Compara com simulação
    4. Gera gráficos comparativos
    """

    print("\n" + "=" * 70)
    print("EXEMPLO DE INTEGRAÇÃO: KSP → TELEMETRIA ORION GROUP")
    print("=" * 70 + "\n")

    # PASSO 1: Criar arquivo de exemplo
    print("PASSO 1: Criando arquivo de exemplo...")
    arquivo_ksp = criar_csv_exemplo()

    # PASSO 2: Importar dados
    print("\nPASSO 2: Importando dados do KSP...")
    dados_ksp = importar_csv_ksp(arquivo_ksp)

    if dados_ksp is None:
        print("Erro ao importar dados. Encerrando.")
        return

    # PASSO 3: Importar dados da simulação (simulado aqui)
    print("\nPASSO 3: Carregando dados da simulação...")
    from main import SimuladorTelemetria

    simulador = SimuladorTelemetria()
    simulador.simular_lancamento()

    dados_simulados = {
        'tempo': simulador.dados_tempo,
        'altitude': simulador.dados_altitude,
        'velocidade': simulador.dados_velocidade,
        'aceleracao': simulador.dados_aceleracao,
        'massa': simulador.dados_massa
    }

    # PASSO 4: Comparar
    print("\nPASSO 4: Comparando resultados...")
    analise = comparar_simulacao_vs_ksp(dados_simulados, dados_ksp)

    # PASSO 5: Gerar gráficos
    print("\nPASSO 5: Gerando gráficos comparativos...")
    plotar_comparacao(dados_simulados, dados_ksp)

    print("\n✓ Processo de integração concluído com sucesso!")


# ============================================================================
# PONTO DE ENTRADA
# ============================================================================

if __name__ == "__main__":
    # Descomente a linha abaixo para testar a integração
    # main()

    print("\nESTe arquivo contém exemplos de funções para integração com KSP.")
    print("\nFunções disponíveis:")
    print("  - importar_csv_ksp(caminho)")
    print("  - comparar_simulacao_vs_ksp(sim, ksp)")
    print("  - plotar_comparacao(sim, ksp, nome_saida)")
    print("  - criar_csv_exemplo(nome)")
    print("\nPara usar, descomente 'main()' no final ou importe as funções.")