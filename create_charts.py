from __future__ import print_function
import json
import os

import matplotlib.pyplot as plt
from matplotlib.table import Table

from cfr import CFR

label = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
rank_index_map = {
    'A': 0, 'K': 1, 'Q': 2,
    'J': 3, 'T': 4, '9': 5,
    '8': 6, '7': 7, '6': 8,
    '5': 9, '4': 10, '3': 11, '2': 12,
}
def get_color(frequency):
    if frequency >= 0.9:
        return 'green'
    elif frequency >= 0.75:
        return 'yellowgreen'
    elif frequency >= 0.5:
        return 'yellow'
    elif frequency >= 0.25:
        return 'orange'
    elif frequency >= 0.05:
        return 'orangered'
    else:
        return 'red'


def create_table(title, frequencies, save = True):
    fig, ax = plt.subplots()
    ax.set_axis_off()
    tb = Table(ax, bbox=[0, 0, 1, 1])

    nrows, ncols = len(label), len(label)
    width, height = 1.0 / ncols, 1.0 / nrows

    # Add cells
    for hand, val in frequencies.items():
        i, j = rank_index_map[hand[0]], rank_index_map[hand[1]]

        color = get_color(val)

        value_formatted = '{0:.2f}'.format(val)
        tb.add_cell(i + 1, j, width, height, text=hand,
                    loc='center', facecolor=color)

    # Row Labels...
    for i in range(len(label)):
        tb.add_cell(i + 1, -1, width, height, text=label[i], loc='right',
                    edgecolor='none', facecolor='none')
    # Column Labels...
    for j in range(len(label)):
        tb.add_cell(
            0, j, width, height / 2,
            text=label[j], loc='center', edgecolor='none', facecolor='none')
        
    # Additional labels might be needed
    ax.add_table(tb)
    iterationString = '10mil'
    iterations_title = f"({iterationString} iterations) {title}"
    plt.title(title)

    if save:
        safe_title = iterations_title.replace(' ', '_').replace('/', '_')
        filename = f"strategy_charts/{iterationString}/{safe_title}.png"
        plt.savefig(filename)
        plt.close(fig)  # Close the figure to free up memory
    return fig