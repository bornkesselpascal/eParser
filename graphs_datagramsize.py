import os
import math
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator, FuncFormatter
from constants import diagrams


#      _       _                                      _                                 _
#     | |     | |                                    (_)                               | |
#   __| | __ _| |_ __ _  __ _ _ __ __ _ _ __ ___  ___ _ _______    __ _ _ __ __ _ _ __ | |__  ___
#  / _` |/ _` | __/ _` |/ _` | '__/ _` | '_ ` _ \/ __| |_  / _ \  / _` | '__/ _` | '_ \| '_ \/ __|
# | (_| | (_| | || (_| | (_| | | | (_| | | | | | \__ | |/ |  __/ | (_| | | | (_| | |_) | | | \__ \
#  \__,_|\__,_|\__\__,_|\__, |_|  \__,_|_| |_| |_|___|_/___\___|  \__, |_|  \__,_| .__/|_| |_|___/
#                        __/ |                                     __/ |         | |
#                       |___/                                     |___/          |_|


def _prepare_and_create_datagramsize_graphs(test_data: list, datagramsize: int, output_path: str) -> None:
    datagramsize_data = [test_scenario for test_scenario in test_data if test_scenario[0]['connection']['datagram_size'] == datagramsize]

    __plot_datagramsize_diagr1(datagramsize_data, datagramsize, output_path)


def __plot_datagramsize_diagr1(test_data: list, datagramsize: int, output_path: str) -> None:
    if not any(test_scenario[1]['report']['losses'] > 0 for test_scenario in test_data):
        return

    diagram_name = f'datagramsize-{datagramsize}-diagr1__losses_by_cycle'

    # Set the style
    sns.set_style("whitegrid")
    sns.set_context("paper", font_scale=1, rc={"lines.linewidth": 2})
    plt.rc('text', usetex=False)
    plt.rc('font', family='serif')

    # Fetch the data for the visualization
    cycle_times = sorted(list(set(test_scenario[0]['connection']['cycle_time'] for test_scenario in test_data)))
    loss_list = list([0]*len(cycle_times))
    total_list = list([0]*len(cycle_times))

    # Get all loss entries
    for test_scenario in test_data:
        current_cycle_time = test_scenario[0]['connection']['cycle_time']

        for idx, cycle_time in enumerate(cycle_times):
            if cycle_time == current_cycle_time:
                loss_list[idx] += test_scenario[1]['report']['losses']
                total_list[idx] += test_scenario[1]['report']['total']
                break

    ratio_list = [(loss / total)*100 for loss, total in zip(loss_list, total_list)]

    # Create a bar chart for each datagram size
    bar_width = 0.2
    index = np.arange(len(cycle_times))

    _, ax = plt.subplots(figsize=(12, 5))
    bars = ax.bar(index, ratio_list, bar_width, color=diagrams['colors']['datagramsize'].get(datagramsize, 'red'), edgecolor='black', label=f"{datagramsize} Byte", alpha=0.7)

    for entry in bars:
        yval = entry.get_height()
        plt.text(entry.get_x() + entry.get_width()/2., yval + 0.01, f"{yval:.2f}%", ha='center', va='bottom')

    # Add axis labels and titles
    ax.set_title(f'Packet Losses by Cycle Time for Datagram Size of {datagramsize} Byte')
    ax.set_xlabel('Cycle Time')
    ax.set_ylabel('Packet Loss Ratio')
    ax.set_xticks(index, [f"{(cycle_time / 1000):.1f} \u03bcs" for cycle_time in cycle_times])

    max_value = max(ratio_list)
    plt.ylim(0, math.ceil(max_value / 0.78))

    def percent_formatter(x, _):
        return f"{x:.0f}%"
    plt.gca().yaxis.set_major_formatter(FuncFormatter(percent_formatter))

    plt.tight_layout()

    # Save the diagram
    if diagrams['output']['pdf']:
        plt.savefig(os.path.join(output_path, f'{diagram_name}.pdf'))
    if diagrams['output']['latex']:
        plt.savefig(os.path.join(output_path, f'{diagram_name}.pgf'))
    if diagrams['output']['png']:
        plt.savefig(os.path.join(output_path, f'{diagram_name}.png'), dpi=300)

    plt.close()
