# -*- coding: utf-8 -*-
"""
16_Relational_Universe_Engine
© 2026 AITHERRA | www.aitherra.com 
"""

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.gridspec import GridSpec

class RelationalEngine:
    def __init__(self, n_nodes=50):
        self.n_nodes = n_nodes
        # Поле когерентности (Материя)
        self.coherence = np.zeros((n_nodes, n_nodes))
        # Память поля (Инварианты / Призрачный Нексус)
        self.field_memory = np.zeros((n_nodes, n_nodes))
        # Смысловые коды узлов (Инварианты) - создаем кластеры для яркости
        self.invariants = np.zeros(n_nodes)
        for i in range(5): # Создаем 5 групп резонанса
            self.invariants[i*10:(i+1)*10] = i * 0.2

    def evolve_resonance(self, iterations=200):
        """Процесс самоорганизации: форсированное рождение объекта"""
        # Начальный шум + базовый резонанс
        inv_diff = np.abs(self.invariants[:, None] - self.invariants[None, :])
        # Усиливаем сродство: очень узкий и мощный пик резонанса
        resonance_mask = np.exp(-inv_diff * 10)

        # Стартовая когерентность
        temp_coh = resonance_mask * 0.5

        for _ in range(iterations):
            # Матричное произведение имитирует "транзитивность" смыслов
            # Если А знает Б, и Б знает В, то А узнает В.
            net_effect = np.matmul(temp_coh, temp_coh)
            # Нормализация, чтобы значения не улетали в бесконечность
            net_effect = net_effect / np.max(net_effect) if np.max(net_effect) > 0 else net_effect

            # Динамика: старое состояние + новые связи - энтропия
            temp_coh = 0.7 * temp_coh + 0.3 * (resonance_mask * net_effect)
            temp_coh = (temp_coh + temp_coh.T) / 2
            temp_coh = np.clip(temp_coh, 0, 1)

        self.coherence = temp_coh
        self.field_memory = self.coherence.copy()
        np.fill_diagonal(self.coherence, 1.0)

    def trigger_removal(self, decay_steps=30):
        """Удаление физического носителя и сохранение памяти поля"""
        self.coherence.fill(0)
        # Поле затухает, но сохраняет структуру
        for _ in range(decay_steps):
            self.field_memory = self.field_memory * 0.98 - (np.random.rand(self.n_nodes, self.n_nodes) * 0.001)
            self.field_memory = np.clip(self.field_memory, 0, 1)

def run_full_demonstration():
    engine = RelationalEngine(n_nodes=50)
    engine.evolve_resonance(iterations=250)

    fig = plt.figure(figsize=(16, 10))
    fig.patch.set_facecolor('white')
    gs = GridSpec(2, 2, figure=fig)

    # 1. ЖИВАЯ МАТЕРИЯ
    ax1 = fig.add_subplot(gs[0, 0])
    # Используем 'magma', но с нормализацией, чтобы видеть всё
    im1 = ax1.imshow(engine.coherence, cmap='magma', vmin=0, vmax=1)
    ax1.set_title("1. Поле когерентности (Резонанс накоплен)", fontsize=12)
    plt.colorbar(im1, ax=ax1)

    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_facecolor('#fdfdfd')
    G1 = nx.Graph()
    # Берем только сильные связи для четкой геометрии
    for i in range(engine.n_nodes):
        for j in range(i + 1, engine.n_nodes):
            if engine.coherence[i, j] > 0.5:
                G1.add_edge(i, j)

    if len(G1.nodes) > 0:
        pos = nx.kamada_kawai_layout(G1)
        nx.draw_networkx_nodes(G1, pos, ax=ax2, node_size=60, node_color=engine.invariants[list(G1.nodes)], cmap='cool', edgecolors='black')
        nx.draw_networkx_edges(G1, pos, ax=ax2, edge_color='gray', alpha=0.2)
    ax2.set_title("Эмерджентная Геометрия (Объект сформирован)", fontsize=12)
    ax2.axis('off')

    # 2. РЕЗОНАНСНАЯ ПАМЯТЬ
    engine.trigger_removal(decay_steps=50)

    ax3 = fig.add_subplot(gs[1, 0])
    # Важно: vmin/vmax помогают увидеть даже слабые значения
    im3 = ax3.imshow(engine.field_memory, cmap='hot', vmin=0, vmax=0.5)
    ax3.set_title("2. Резонансная Память (Призрачный след)", fontsize=12)
    plt.colorbar(im3, ax=ax3)

    ax4 = fig.add_subplot(gs[1, 1])
    ax4.set_facecolor('#fffafa')
    G2 = nx.Graph()
    # Адаптивный порог для призрака
    m_val = np.mean(engine.field_memory) + np.std(engine.field_memory)
    for i in range(engine.n_nodes):
        for j in range(i + 1, engine.n_nodes):
            if engine.field_memory[i, j] > m_val:
                G2.add_edge(i, j)

    if len(G2.nodes) > 0:
        pos2 = nx.spring_layout(G2, k=0.3)
        nx.draw_networkx_nodes(G2, pos2, ax=ax4, node_size=40, node_color='red', alpha=0.5)
        nx.draw_networkx_edges(G2, pos2, ax=ax4, edge_color='red', alpha=0.1)
    ax4.set_title("Призрачный Нексус (Эхо структуры)", fontsize=12)
    ax4.axis('off')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_full_demonstration()