import os
import math
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from constants import diagrams
from data_format import format_query


#                                _                               _
#                               (_)                             | |
#  ___  ___ ___ _ __   __ _ _ __ _  ___     __ _ _ __ __ _ _ __ | |__  ___
# / __|/ __/ _ \ '_ \ / _` | '__| |/ _ \   / _` | '__/ _` | '_ \| '_ \/ __|
# \__ \ (_|  __/ | | | (_| | |  | | (_) | | (_| | | | (_| | |_) | | | \__ \
# |___/\___\___|_| |_|\__,_|_|  |_|\___/   \__, |_|  \__,_| .__/|_| |_|___/
#                                           __/ |         | |
#                                          |___/          |_|


def _prepare_and_create_scenario_graphs(test_scenario: tuple, output_path: str) -> None:
    query = format_query(test_scenario[3].copy(), test_scenario[1]['report']['duration'], test_scenario[1]['report']['losses'], test_scenario[1]['report']['total'])
    current_scenario = (test_scenario[0], test_scenario[1], test_scenario[2], query)

    __plot_scenario_diagr1(current_scenario, output_path)
    __plot_scenario_diagr2(current_scenario, output_path)
    __plot_scenario_diagr3(current_scenario, output_path)
    __plot_scenario_diagr4(current_scenario, output_path)


def __plot_scenario_diagr1(test_scenario: tuple, output_path: str) -> None:
    if not diagrams['histogram']:
        # If no histogram should be generated, we stop here.
        return
    if  test_scenario[1]['report']['losses'] == 0:
        # If there are no losses, we stop here.
        return

    diagram_name = 'scenario-diagr1__histogram_losses'

    # Set the style
    sns.set_style("whitegrid")
    sns.set_context("paper", font_scale=1, rc={"lines.linewidth": 2})
    plt.rc('text', usetex=False)
    plt.rc('font', family='serif')

    # Fetch the data for the visualization
    query = test_scenario[3]

    # Get the data for the histogram
    differences_list = [report['difference'] for report in query]

    # Create the histogram
    # Creating the histogram
    _, ax = plt.subplots(figsize=(12, 5))
    ax.hist(differences_list, bins=range(0, max(differences_list) + 2), align='left', color=diagrams['colors']['datagramsize'].get(test_scenario[0]['connection']['datagram_size'], 'red'), edgecolor='black', alpha=0.7)

    # Labels, title, and other configurations
    ax.set_xlabel('Packet Losses per 100000 Packets (Number of Packets)')
    ax.set_ylabel('Frequency')
    ax.set_title('Frequency Analysis of Packet Losses')
    ax.set_xticks(range(0, max(differences_list) + 10, 10))
    plt.tight_layout()

    # Save the diagram
    if diagrams['output']['pdf']:
        plt.savefig(os.path.join(output_path, f'{diagram_name}.pdf'))
    if diagrams['output']['latex']:
        plt.savefig(os.path.join(output_path, f'{diagram_name}.pgf'))
    if diagrams['output']['png']:
        plt.savefig(os.path.join(output_path, f'{diagram_name}.png'), dpi=300)

    plt.close()


def __plot_scenario_diagr2(test_scenario: tuple, output_path: str) -> None:
    diagram_name = 'scenario-diagr2__packages_over_time'

    # Set the style
    sns.set_style("whitegrid")
    sns.set_context("paper", font_scale=1, rc={"lines.linewidth": 2})
    plt.rc('text', usetex=False)
    plt.rc('font', family='serif')

    # Fetch the data for the visualization
    query = test_scenario[3].copy()
    query.insert(0, {'timestamp': 0, 'total': 0, 'losses': 0, 'difference': 0})

    # Get the data for the diagram
    timestamps = [report['timestamp'] for report in query]
    totals = [report['total'] for report in query]
    received = [(report['total'] - report["losses"]) for report in query]

    # Create the diagram
    _, ax = plt.subplots(figsize=(12, 5))
    ax.fill_between(timestamps, totals, color=diagrams['colors']['paket_type']['sent'], label='Sent Packets', edgecolor='black', alpha=0.6)
    ax.fill_between(timestamps, received, color=diagrams['colors']['paket_type']['received'], label='Received Packets', edgecolor='black', alpha=0.7)
    ax.set_xlabel('Time')
    ax.set_ylabel('Packets')
    ax.set_title('Temporal Distribution of Sent and Received UDP Packets')
    ax.legend(loc='upper right', frameon=True)

    max_value = max(totals)
    plt.ylim(0, math.ceil(max_value / 0.78))

    def seconds_formatter(x, _):
        return f"{x:.0f} s"
    plt.gca().xaxis.set_major_formatter(FuncFormatter(seconds_formatter))

    plt.tight_layout()

    # Save the diagram
    if diagrams['output']['pdf']:
        plt.savefig(os.path.join(output_path, f'{diagram_name}.pdf'))
    if diagrams['output']['latex']:
        plt.savefig(os.path.join(output_path, f'{diagram_name}.pgf'))
    if diagrams['output']['png']:
        plt.savefig(os.path.join(output_path, f'{diagram_name}.png'), dpi=300)

    plt.close()


def __plot_scenario_diagr3(test_scenario: tuple, output_path: str) -> None:
    if  test_scenario[1]['report']['losses'] == 0:
        # If there are no losses, we stop here.
        return
    
    diagram_name = 'scenario-diagr3__losses_over_time'

    # Set the style
    sns.set_style("whitegrid")
    sns.set_context("paper", font_scale=1, rc={"lines.linewidth": 2})
    plt.rc('text', usetex=False)
    plt.rc('font', family='serif')

    # Fetch the data for the visualization
    query = test_scenario[3].copy()
    query.insert(0, {'timestamp': 0, 'total': 0, 'losses': 0, 'difference': 0})

    # Get the data for the diagram
    timestamps = [report['timestamp'] for report in query]
    difference = [report['difference'] for report in query]

    # Create the diagram
    _, ax = plt.subplots(figsize=(12, 5))
    ax.fill_between(timestamps, difference, color='lightgray', edgecolor='black', alpha=0.6)
    ax.set_xlabel('Time')
    ax.set_ylabel('Lost Packets')
    ax.set_title('Temporal Distribution of Packet Loss')

    def seconds_formatter(x, _):
        return f"{x:.0f} s"
    plt.gca().xaxis.set_major_formatter(FuncFormatter(seconds_formatter))

    plt.tight_layout()

    # Save the diagram
    if diagrams['output']['pdf']:
        plt.savefig(os.path.join(output_path, f'{diagram_name}.pdf'))
    if diagrams['output']['latex']:
        plt.savefig(os.path.join(output_path, f'{diagram_name}.pgf'))
    if diagrams['output']['png']:
        plt.savefig(os.path.join(output_path, f'{diagram_name}.png'), dpi=300)

    plt.close()


def __plot_scenario_diagr4(test_scenario: tuple, output_path: str) -> None:
    diagram_name = 'scenario-diagr4__packages_per_second'
    draw_packages_per_second = True

    # Set the style
    sns.set_style("whitegrid")
    sns.set_context("paper", font_scale=1, rc={"lines.linewidth": 2})
    plt.rc('text', usetex=False)
    plt.rc('font', family='serif')

    # Fetch the data for the visualization
    query = test_scenario[3]

    # Get the data for the diagram
    timestamps = [report['timestamp'] for report in query]
    package_per_second = {'sent': list(), 'received': list()}

    for idx, report in enumerate(query):
        current_timestamp = report['timestamp']
        previous_timestamp = 0 if idx == 0 else query[idx-1]['timestamp']
        diff_timestamp = current_timestamp - previous_timestamp

        diff_sent = report['total'] - (0 if idx == 0 else query[idx-1]['total'])
        diff_received = (report['total'] - report['losses']) - (0 if idx == 0 else (query[idx-1]['total'] - query[idx-1]['losses']))

        if draw_packages_per_second:
            package_per_second['sent'].append(diff_sent / diff_timestamp)
            package_per_second['received'].append(diff_received / diff_timestamp)
        else:
            package_per_second['sent'].append(diff_sent)
            package_per_second['received'].append(diff_received)

    # Create the diagram
    _, ax = plt.subplots(figsize=(12, 5))

    ax.fill_between(timestamps, package_per_second['sent'], color=diagrams['colors']['paket_type']['sent'], label='Sent Packets', edgecolor='black', alpha=0.6)
    ax.fill_between(timestamps, package_per_second['received'], color=diagrams['colors']['paket_type']['received'], label='Received Packets', edgecolor='black', alpha=0.7)

    if draw_packages_per_second:
        ax.set_title('Overview of Sent and Received UDP Packets per Second')
    else:
        ax.set_title('Overview of Sent and Received UDP Packets per Query Message')

    ax.set_ylabel('Packets per Second')
    ax.set_xlabel('Time')
    ax.legend(loc='upper right', frameon=True)

    max_value = max(package_per_second['sent'])
    min_value = min(package_per_second['received'])
    plt.ylim(min_value - 20, max_value + 20)

    def seconds_formatter(x, _):
        return f"{x:.0f} s"
    plt.gca().xaxis.set_major_formatter(FuncFormatter(seconds_formatter))

    plt.tight_layout()

    # Save the diagram
    if diagrams['output']['pdf']:
        plt.savefig(os.path.join(output_path, f'{diagram_name}.pdf'))
    if diagrams['output']['latex']:
        plt.savefig(os.path.join(output_path, f'{diagram_name}.pgf'))
    if diagrams['output']['png']:
        plt.savefig(os.path.join(output_path, f'{diagram_name}.png'), dpi=300)

    plt.close()
