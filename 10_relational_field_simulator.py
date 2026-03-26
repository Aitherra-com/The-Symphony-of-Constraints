# -*- coding: utf-8 -*-
"""
10_Relational_Field_Simulator
© 2026 AITHERRA | www.aitherra.com 
"""

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

class RelationalUniverse:
    def __init__(self, n_nodes=50, noise_level=0.01):
        self.n_nodes = n_nodes
        self.noise_level = noise_level
        # Инициализация поля (хаос)
        self.coherence = np.random.rand(n_nodes, n_nodes) * 0.1
        np.fill_diagonal(self.coherence, 1.0)

        # Инварианты (коды смысла)
        self.invariants = np.sort(np.random.rand(n_nodes))

    def update(self):
        # 1. Резонанс смыслов
        inv_diff = np.abs(self.invariants[:, None] - self.invariants[None, :])
        resonance_potential = np.exp(-inv_diff * 3)

        # 2. Сетевое усиление
        network_effect = np.dot(self.coherence, self.coherence) / (self.n_nodes * 0.5)

        # 3. Динамика
        self.coherence = 0.7 * self.coherence + 0.3 * (resonance_potential * network_effect)
        self.coherence -= np.random.rand(self.n_nodes, self.n_nodes) * self.noise_level

        # Симметрия и ограничения
        self.coherence = (self.coherence + self.coherence.T) / 2
        self.coherence = np.clip(self.coherence, 0, 1)
        np.fill_diagonal(self.coherence, 1.0)

def run_visible_simulation():
    n_nodes = 50
    universe = RelationalUniverse(n_nodes=n_nodes, noise_level=0.005)

    # Даем время на кристаллизацию
    for _ in range(200):
        universe.update()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # 1. Матрица когерентности
    im = ax1.imshow(universe.coherence, cmap='viridis', interpolation='nearest')
    ax1.set_title("Поле когерентности (Matrix)")
    plt.colorbar(im, ax=ax1)

    # 2. Эмерджентная Геометрия
    # Берем топ 10% самых сильных связей, чтобы точно что-то увидеть
    flat_values = universe.coherence[np.triu_indices(n_nodes, k=1)]
    threshold = np.percentile(flat_values, 90) # Топ 10%

    G = nx.Graph()
    for i in range(n_nodes):
        for j in range(i + 1, n_nodes):
            if universe.coherence[i, j] >= threshold:
                G.add_edge(i, j, weight=universe.coherence[i, j])

    # Если есть узлы, рисуем
    if len(G.edges) > 0:
        # Белый фон для максимальной видимости
        ax2.set_facecolor('white')
        pos = nx.kamada_kawai_layout(G) # Более стабильный алгоритм расположения

        # Рисуем ребра (черные линии)
        nx.draw_networkx_edges(G, pos, ax=ax2, edge_color='black', alpha=0.2)

        # Рисуем узлы
        node_colors = [universe.invariants[n] for n in G.nodes]
        nodes = nx.draw_networkx_nodes(G, pos, ax=ax2, node_size=100,
                                       node_color=node_colors, cmap='plasma')

        ax2.set_title("Эмерджентная Геометрия (Space)")
    else:
        ax2.text(0.5, 0.5, "Связи не найдены\nПопробуйте уменьшить шум",
                 ha='center', va='center')

    ax2.axis('on') # Включаем оси, чтобы видеть границы графика
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_visible_simulation()