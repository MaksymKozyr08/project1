import matplotlib.pyplot as plt
import networkx as nx

# Налаштування вікна
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))


def draw_perfect_automaton(edges, start, finals, title, ax, pos_modifier):
    G = nx.MultiDiGraph()
    for u, v, label in edges:
        G.add_edge(u, v, label=label)

    # Фіксоване ручне розташування вузлів, щоб лінії не перетиналися
    if pos_modifier == 20:
        pos = {"a0": (0, 0), "a1": (2, 1), "a2": (4, 0)}
    else:
        pos = {"a0": (0, 0), "a1": (3, 0)}

    # Базові вузли
    nx.draw_networkx_nodes(
        G, pos, node_size=2000, node_color="#fff2cc", edgecolors="#d6b656", linewidths=2, ax=ax
    )

    # Подвійне коло для фінальних станів (малюємо поверх ширший контур)
    nx.draw_networkx_nodes(
        G, pos, nodelist=finals, node_size=2600, node_color="none", edgecolors="#385723", linewidths=2.5, ax=ax
    )

    # Текст всередині вузлів
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight="bold", font_family="Arial", ax=ax)

    # Малюємо стрілки вручну з вигинами, щоб туди-сюди не злипалися
    for u, v, label in edges:
        # Розрахунок вигину: якщо в себе — велика петля, якщо зустрічні — вигинаємо в різні боки
        if u == v:
            rad = 0.4
        elif (v, u) in [(edge[0], edge[1]) for edge in edges if edge[0] != edge[1]]:
            rad = 0.25 if u < v else 0.25  # симетричний вигин зустрічних дуг
        else:
            rad = 0.1

        connectionstyle = f"arc3,rad={rad}" if u != v else "arc,rad=40"

        # Малюємо стрілку
        arrow = ax.annotate(
            "",
            xy=pos[v],
            xytext=pos[u],
            arrowprops=dict(
                arrowstyle="-|>",
                color="#434343",
                lw=2,
                connectionstyle=connectionstyle,
                mutation_scale=20,
                shrinkA=32,  # відступ від центра початку
                shrinkB=38,  # відступ від контуру фінішу
            ),
        )

        # Обчислення зміщення тексту міток (текст виноситься ЗА лінію, щоб не наповзав)
        mid_x = (pos[u][0] + pos[v][0]) / 2
        mid_y = (pos[u][1] + pos[v][1]) / 2

        if u == v:  # для петель зміщуємо текст строго вгору
            txt_x, txt_y = pos[u][0], pos[u][1] + 0.45
        else:  # для дуг зміщуємо текст перпендикулярно до вигину лінії
            offset = 0.15 if u < v else -0.15
            txt_x, txt_y = mid_x, mid_y + offset

        ax.text(
            txt_x,
            txt_y,
            label,
            fontsize=12,
            color="#b02a37",
            weight="bold",
            ha="center",
            va="center",
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.7),
        )

    ax.set_title(title, fontsize=14, fontweight="bold", pad=20)
    ax.axis("off")


# --- Дані Задача 20 ---
edges_20 = [("a0", "a0", "0"), ("a0", "a1", "1"), ("a1", "a2", "0"), ("a2", "a2", "0"), ("a2", "a1", "1")]
draw_perfect_automaton(edges_20, "a0", ["a0", "a2"], "Задача 20: Непарна кількість '0' між '1'", ax1, 20)

# --- Дані Задача 21 ---
edges_21 = [("a0", "a0", "1"), ("a0", "a1", "0"), ("a1", "a1", "0"), ("a1", "a0", "1")]
draw_perfect_automaton(edges_21, "a0", ["a1"], "Задача 21: Двійкові парні числа", ax2, 21)

plt.tight_layout()
plt.show()