#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SIMULADOR DE TELEMETRIA - ORION GROUP AEROSPACE
Telemetria do Primeiro Estágio do Foguete Orion

Descrição:
    Script que simula a trajetória do primeiro estágio do foguete Orion,
    calculando altitude, velocidade e aceleração segundo a segundo até
    o esgotamento do combustível. Gera painel de telemetria corporativo.

Autor: Orion Group Engineering Team
Data: 2026
"""

import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime


# ============================================================================
# CONFIGURAÇÕES DO FOGUETE - DADOS TÉCNICOS
# ============================================================================

class ConfiguracaoOrian:
    """Classe com configurações do foguete Orion Group"""

    # Parâmetros de massa
    MASSA_SECA_KG = 186300.0  # Massa da estrutura + motores
    MASSA_COMBUSTIVEL_INICIAL_KG = 144000.0  # Massa inicial de combustível

    # Parâmetros de propulsão
    EMPUXO_NEWTONS = 4682500.0  # Força de empuxo dos motores
    TEMPO_QUEIMA_SEGUNDOS = 89  # Tempo máximo de queima
    TAXA_QUEIMA_KG_POR_SEGUNDO = 1618.0  # Consumo de combustível

    # Parâmetros de física
    GRAVIDADE_M_S2 = 9.81  # Aceleração gravitacional
    DELTA_T = 1  # Intervalo de tempo (1 segundo)


# ============================================================================
# SIMULADOR DE TELEMETRIA
# ============================================================================

class SimuladorTelemetria:
    """
    Simulador da trajetória do foguete Orion.

    Calcula a dinâmica de voo utilizando as leis de Newton:
    - F = m * a (Segunda Lei de Newton)
    - v = v0 + a * t (Equação da velocidade)
    - s = s0 + v * t (Equação da posição)
    """

    def __init__(self, config=ConfiguracaoOrian):
        """
        Inicializa o simulador com os parâmetros do foguete.

        Args:
            config: Classe com configurações do foguete
        """
        self.config = config

        # Estados iniciais
        self.tempo = 0
        self.altitude = 0.0  # metros
        self.velocidade = 0.0  # m/s
        self.aceleracao = 0.0  # m/s²
        self.massa_combustivel = config.MASSA_COMBUSTIVEL_INICIAL_KG

        # Armazenamento de dados para gráficos
        self.dados_tempo = []
        self.dados_altitude = []
        self.dados_velocidade = []
        self.dados_aceleracao = []
        self.dados_massa = []

    def calcular_proxima_iteracao(self):
        """
        Calcula um passo da simulação (1 segundo).

        Etapas:
        1. Calcula a massa total atual (estrutura + combustível)
        2. Calcula a aceleração pela 2ª lei de Newton
        3. Atualiza a velocidade
        4. Atualiza a altitude
        5. Consome combustível
        """

        # ETAPA 1: Calcular massa total
        massa_total = self.config.MASSA_SECA_KG + self.massa_combustivel

        # ETAPA 2: Calcular aceleração (F = m * a → a = F / m)
        # Força resultante = Empuxo - Peso
        forca_resultante = self.config.EMPUXO_NEWTONS - (massa_total * self.config.GRAVIDADE_M_S2)
        self.aceleracao = forca_resultante / massa_total

        # ETAPA 3: Atualizar velocidade (v = v0 + a * Δt)
        self.velocidade += self.aceleracao * self.config.DELTA_T

        # ETAPA 4: Atualizar altitude (h = h0 + v * Δt)
        self.altitude += self.velocidade * self.config.DELTA_T

        # ETAPA 5: Consumir combustível
        self.massa_combustivel -= self.config.TAXA_QUEIMA_KG_POR_SEGUNDO * self.config.DELTA_T
        self.massa_combustivel = max(0, self.massa_combustivel)  # Garantir que não fica negativo

    def armazenar_dados(self):
        """Armazena os dados da iteração atual nas listas de dados."""
        self.dados_tempo.append(self.tempo)
        self.dados_altitude.append(self.altitude)
        self.dados_velocidade.append(self.velocidade)
        self.dados_aceleracao.append(self.aceleracao)
        self.dados_massa.append(self.config.MASSA_SECA_KG + self.massa_combustivel)

    def simular_lancamento(self):
        """
        Executa a simulação completa do lançamento.

        Simula segundo a segundo até:
        - Esgotamento do combustível, OU
        - Atingir o tempo máximo de queima
        """

        print("=" * 70)
        print("INICIANDO SIMULAÇÃO DE LANÇAMENTO - ORION GROUP")
        print("=" * 70)
        print(
            f"Massa inicial do foguete: {self.config.MASSA_SECA_KG + self.config.MASSA_COMBUSTIVEL_INICIAL_KG:.1f} kg")
        print(f"Empuxo dos motores: {self.config.EMPUXO_NEWTONS:,.0f} N")
        print(f"Tempo máximo de queima: {self.config.TEMPO_QUEIMA_SEGUNDOS} segundos")
        print("-" * 70)

        # Armazenar estado inicial
        self.armazenar_dados()

        # Loop de simulação
        while self.tempo <= self.config.TEMPO_QUEIMA_SEGUNDOS and self.massa_combustivel > 0:
            self.calcular_proxima_iteracao()
            self.tempo += 1
            self.armazenar_dados()

            # Imprimir status a cada 10 segundos
            if self.tempo % 10 == 0 or self.tempo == self.config.TEMPO_QUEIMA_SEGUNDOS:
                print(f"T+{self.tempo:3d}s | Alt: {self.altitude:10.1f}m | Vel: {self.velocidade:8.2f}m/s | " +
                      f"Ace: {self.aceleracao:7.2f}m/s² | Combustível: {self.massa_combustivel:8.1f}kg")

        print("-" * 70)
        print(f"SIMULAÇÃO CONCLUÍDA EM T+{self.tempo} segundos")
        print(f"Altitude máxima atingida: {max(self.dados_altitude):,.1f} metros")
        print(f"Velocidade máxima atingida: {max(self.dados_velocidade):,.2f} m/s")
        print("=" * 70)

    def gerar_graficos(self):
        """
        Gera painel de telemetria profissional com matplotlib.

        Cria dois subgráficos:
        - Altitude vs Tempo
        - Velocidade vs Tempo
        - Aceleração vs Tempo (bônus)

        Salva em 'graficos/telemetria_orion_flight.png'
        """

        # Criar diretório de gráficos se não existir
        if not os.path.exists('graficos'):
            os.makedirs('graficos')

        # Configurar estilo profissional
        plt.style.use('seaborn-v0_8-darkgrid')

        # Criar figura com tamanho corporativo (16:9)
        fig = plt.figure(figsize=(16, 10))
        fig.suptitle('PAINEL DE TELEMETRIA ORION GROUP - PRIMEIRO ESTÁGIO\n' +
                     f'Simulação realizada em {datetime.now().strftime("%d/%m/%Y às %H:%M:%S")}',
                     fontsize=18, fontweight='bold', color='#1a1a1a')

        # Definir cores corporativas (Orion Group)
        cor_altitude = '#FF6B35'  # Laranja
        cor_velocidade = '#004E89'  # Azul escuro
        cor_aceleracao = '#1B998B'  # Verde

        # ====== SUBGRÁFICO 1: ALTITUDE vs TEMPO ======
        ax1 = plt.subplot(2, 2, 1)
        ax1.plot(self.dados_tempo, np.array(self.dados_altitude) / 1000,
                 linewidth=2.5, color=cor_altitude, label='Altitude')
        ax1.fill_between(self.dados_tempo, 0, np.array(self.dados_altitude) / 1000,
                         alpha=0.2, color=cor_altitude)
        ax1.set_xlabel('Tempo (s)', fontsize=11, fontweight='bold')
        ax1.set_ylabel('Altitude (km)', fontsize=11, fontweight='bold')
        ax1.set_title('ALTITUDE vs TEMPO', fontsize=12, fontweight='bold', pad=10)
        ax1.grid(True, alpha=0.3, linestyle='--')
        ax1.legend(loc='upper left', fontsize=10)

        # Adicionar valor máximo
        idx_max_alt = np.argmax(self.dados_altitude)
        alt_max = self.dados_altitude[idx_max_alt] / 1000
        tempo_max_alt = self.dados_tempo[idx_max_alt]
        ax1.plot(tempo_max_alt, alt_max, 'o', color=cor_altitude, markersize=8)
        ax1.annotate(f'Máx: {alt_max:.2f} km',
                     xy=(tempo_max_alt, alt_max),
                     xytext=(10, 10), textcoords='offset points',
                     fontsize=9, fontweight='bold',
                     bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.3),
                     arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0', color=cor_altitude))

        # ====== SUBGRÁFICO 2: VELOCIDADE vs TEMPO ======
        ax2 = plt.subplot(2, 2, 2)
        ax2.plot(self.dados_tempo, self.dados_velocidade,
                 linewidth=2.5, color=cor_velocidade, label='Velocidade')
        ax2.fill_between(self.dados_tempo, 0, self.dados_velocidade,
                         alpha=0.2, color=cor_velocidade)
        ax2.set_xlabel('Tempo (s)', fontsize=11, fontweight='bold')
        ax2.set_ylabel('Velocidade (m/s)', fontsize=11, fontweight='bold')
        ax2.set_title('VELOCIDADE vs TEMPO', fontsize=12, fontweight='bold', pad=10)
        ax2.grid(True, alpha=0.3, linestyle='--')
        ax2.legend(loc='upper left', fontsize=10)

        # Adicionar valor máximo
        idx_max_vel = np.argmax(self.dados_velocidade)
        vel_max = self.dados_velocidade[idx_max_vel]
        tempo_max_vel = self.dados_tempo[idx_max_vel]
        ax2.plot(tempo_max_vel, vel_max, 'o', color=cor_velocidade, markersize=8)
        ax2.annotate(f'Máx: {vel_max:.2f} m/s',
                     xy=(tempo_max_vel, vel_max),
                     xytext=(10, -20), textcoords='offset points',
                     fontsize=9, fontweight='bold',
                     bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.3),
                     arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0', color=cor_velocidade))

        # ====== SUBGRÁFICO 3: ACELERAÇÃO vs TEMPO ======
        ax3 = plt.subplot(2, 2, 3)
        ax3.plot(self.dados_tempo, self.dados_aceleracao,
                 linewidth=2.5, color=cor_aceleracao, label='Aceleração')
        ax3.fill_between(self.dados_tempo, 0, self.dados_aceleracao,
                         alpha=0.2, color=cor_aceleracao)
        ax3.axhline(y=0, color='black', linestyle='-', linewidth=0.8, alpha=0.3)
        ax3.set_xlabel('Tempo (s)', fontsize=11, fontweight='bold')
        ax3.set_ylabel('Aceleração (m/s²)', fontsize=11, fontweight='bold')
        ax3.set_title('ACELERAÇÃO vs TEMPO', fontsize=12, fontweight='bold', pad=10)
        ax3.grid(True, alpha=0.3, linestyle='--')
        ax3.legend(loc='upper right', fontsize=10)

        # ====== SUBGRÁFICO 4: MASSA vs TEMPO ======
        ax4 = plt.subplot(2, 2, 4)
        ax4.plot(self.dados_tempo, np.array(self.dados_massa) / 1000,
                 linewidth=2.5, color='#D62828', label='Massa Total')
        ax4.fill_between(self.dados_tempo, 0, np.array(self.dados_massa) / 1000,
                         alpha=0.2, color='#D62828')
        ax4.set_xlabel('Tempo (s)', fontsize=11, fontweight='bold')
        ax4.set_ylabel('Massa (toneladas)', fontsize=11, fontweight='bold')
        ax4.set_title('MASSA DO FOGUETE vs TEMPO', fontsize=12, fontweight='bold', pad=10)
        ax4.grid(True, alpha=0.3, linestyle='--')
        ax4.legend(loc='upper right', fontsize=10)

        # Ajustar layout
        plt.tight_layout(rect=[0, 0, 1, 0.97])

        # Salvar figura
        caminho_grafico = 'graficos/telemetria_orion_flight.png'
        plt.savefig(caminho_grafico, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"\n✓ Gráfico salvo com sucesso em: {caminho_grafico}")

        # Exibir na tela
        plt.show()


# ============================================================================
# FUNÇÃO PRINCIPAL
# ============================================================================

def main():
    """Função principal que executa a simulação."""

    # Criar simulador
    simulador = SimuladorTelemetria()

    # Executar simulação
    simulador.simular_lancamento()

    # Gerar gráficos
    simulador.gerar_graficos()

    print("\n✓ Processo concluído com sucesso!")
    print("  Os dados estão prontos para integração com KSP ou outros sistemas.")


# ============================================================================
# PONTO DE ENTRADA
# ============================================================================

if __name__ == "__main__":
    main()