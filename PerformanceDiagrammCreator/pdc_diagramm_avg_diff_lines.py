from pdc_parsing import parse_performance_report
import os
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mticker
import numpy as np
from scipy.interpolate import interp1d





base_paths = [
    #'/Users/bornkessel/Developer/testresults/results/performance/output/231206_093804_8dfb44c_macOS/A_Initial/ihwk_4A_074031_061223',
    #'/Users/bornkessel/Developer/testresults/results/performance/output/231206_093804_8dfb44c_macOS/A_Initial/ihwk_4B_074804_061223',
    #'/Users/bornkessel/Developer/testresults/results/performance/output/231206_093804_8dfb44c_macOS/A_Initial/ihwk_5_080012_061223',
    #'/Users/bornkessel/Developer/testresults/results/performance/output/231206_093804_8dfb44c_macOS/A_Initial/ihwk_6_080753_061223',
    #'/Users/bornkessel/Developer/testresults/results/performance/output/231206_093804_8dfb44c_macOS/A_Initial/ihwk_7A_081535_061223',
    #'/Users/bornkessel/Developer/testresults/results/performance/output/231206_093804_8dfb44c_macOS/A_Initial/ihwk_8_083131_061223',
    #'/Users/bornkessel/Developer/testresults/results/performance/output/231206_093804_8dfb44c_macOS/A_Initial/ihwk_9_084044_061223',

    #'/Users/bornkessel/Developer/testresults/results/performance/output/231206_121730_8dfb44c_macOS/B_Initial/ihwk_4A_085845_061223',
    #'/Users/bornkessel/Developer/testresults/results/performance/output/231206_121730_8dfb44c_macOS/B_Initial/ihwk_4B_090618_061223',
    #'/Users/bornkessel/Developer/testresults/results/performance/output/231206_121730_8dfb44c_macOS/B_Initial/ihwk_5_091826_061223',
    #'/Users/bornkessel/Developer/testresults/results/performance/output/231206_121730_8dfb44c_macOS/B_Initial/ihwk_6_092559_061223',

    #'/Users/bornkessel/Developer/testresults/results/performance/output/231206_182854_8dfb44c_macOS/A_Opt1/ihwk_4A_142652_061223',
    #'/Users/bornkessel/Developer/testresults/results/performance/output/231206_182854_8dfb44c_macOS/A_Opt1/ihwk_5_144633_061223',
    #'/Users/bornkessel/Developer/testresults/results/performance/output/231206_182854_8dfb44c_macOS/A_Opt1/ihwk_6_145415_061223',

    '/Users/bornkessel/Developer/testresults/results/performance/output/231207_073018_8dfb44c_macOS/B_Opt1/ihwk_4A_064444_071223',
    '/Users/bornkessel/Developer/testresults/results/performance/output/231207_073018_8dfb44c_macOS/B_Opt1/ihwk_5_070425_071223',
    '/Users/bornkessel/Developer/testresults/results/performance/output/231207_073018_8dfb44c_macOS/B_Opt1/ihwk_6_071158_071223',

    #'/Users/bornkessel/Developer/testresults/results/performance/output/231207_094107_8dfb44c_macOS/A_Opt2/ihwk_4A_093646_071223',

    #'/Users/bornkessel/Developer/testresults/results/performance/output/231207_132743_8dfb44c_macOS/A_Opt1_Improved/ihwk_4A_132023_071223',
]
all_sorted_reports = []
combine_data = False

for base_path in base_paths:
    performance_reports = []

    for test_scenario in os.listdir(base_path):
        test_scenario_path = os.path.join(base_path, test_scenario)
        if not os.path.isdir(test_scenario_path):
            continue

        performance_file_path = os.path.join(test_scenario_path, 'performance.xml')
        if not os.path.isfile(performance_file_path):
            continue

        performance_reports.append(parse_performance_report(performance_file_path))

    # Sort the list of dictionaries by the 'datagram_size' key, then by the 'cycle_time' key
    sorted_reports = sorted(performance_reports, key=lambda k: (int(k['basic']['datagram_size']), int(k['basic']['cycle_time'])))

    # Remove all values with datagram_size = X (only cycle_time)
    # sorted_reports = [report for report in sorted_reports if report['basic']['datagram_size'] != '8900']

    if combine_data:
        # Combine data for same datagram_size and cycle_time in all_sorted_reports
        for former_report in all_sorted_reports:
            if former_report[0]['basic']['cycle_time'] == sorted_reports[0]['basic']['cycle_time']:
                former_report.extend(sorted_reports)
                break
        else:
            # Presuming 'all_sorted_reports' is a list of sorted_reports 
            all_sorted_reports.append(sorted_reports)
    else:
        all_sorted_reports.append(sorted_reports)




# Select here what schould be on the x-axis
x_axis = 'datagram_size'
diagram_name = 'campaign-diagr1__cases_by_losses_and_datagram'

base_path_labels = [
    #"UDP", 
    "Baseline",
    #"RAW", 
    "Optimisation – Case a)",
    "PACKET", 
    #"Optimisation – Case a) and b)",
]
colors = [
    "#99ccff", # Baseline Color
    "#0000ff", # Optimisation Color
    '#000066', # Optimisation2 Color
    'blue',
    'black'
]

interpolation = False
jitter = False




# Set the style
sns.set_style("whitegrid")
sns.set_context("paper", font_scale=1, rc={"lines.linewidth": 2})
plt.rc('text', usetex=False)
plt.rc('font', family='serif')

# Create the plot
fig, ax = plt.subplots(figsize=(12, 5))

# Use a FuncFormatter to add 's' to y-axis labels
formatter = mticker.FuncFormatter(lambda y, _: f'{y:.0f} \u03bcs')
ax.yaxis.set_major_formatter(formatter)
ax.set_ylim(bottom=0, top=600)




# Iterate over each sorted_reports structure and plot them
for sorted_reports in all_sorted_reports:
    # Extract the data for the current sorted_reports structure
    x_axis_values = [int(report['basic'][x_axis]) for report in sorted_reports]
    y_axis_values = [(float(report['timestamps']['maximum_difference'])*1000000) for report in sorted_reports]
    jitter_values = [(float(report['timestamps']['jitter'])*1000000) for report in sorted_reports]
    jitter_values[0] = jitter_values[1]

    if interpolation:
        x_new = np.linspace(min(x_axis_values), max(x_axis_values), 300)  # Increase number for more smoothness
        f = interp1d(x_axis_values, y_axis_values, kind='cubic')
        y_smooth = f(x_new)
    else:
        x_new = x_axis_values
        y_smooth = y_axis_values
    
    # Plot the current dataset
    if jitter:
        plt.errorbar(x_axis_values, y_axis_values, yerr=jitter_values, label=base_path_labels[all_sorted_reports.index(sorted_reports)], fmt='-.s', color=colors[all_sorted_reports.index(sorted_reports)])
    else:
        plt.plot(x_new, y_smooth, label=base_path_labels[all_sorted_reports.index(sorted_reports)])

# Label the axes
plt.title('Worst Case Latency of a UDP socket with different Payload Sizes and a Cycle Time of 1 \u03bcs')
plt.ylabel('Latency [\u03bcs]')

# Add a unti to the x-axis
if x_axis == 'datagram_size':
    plt.xlabel('Payload Size [Byte]')
    formatter2 = mticker.FuncFormatter(lambda y, _: f'{y:.0f} Byte')
    ax.xaxis.set_major_formatter(formatter2)
    ax.set_xlim(left=0, right=8510)
elif x_axis == 'cycle_time':
    plt.xlabel('Cycle Time [\u03bcs]')
    formatter2 = mticker.FuncFormatter(lambda y, _: f'{y:.0f} \u03bcs')
    ax.xaxis.set_major_formatter(formatter2)
    ax.set_xlim(left=0, right=102)

# Add the legend to distinguish the different datasets
# Legend should be below the plot in the middle
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)

# Save the figure
plt.savefig('{}.png'.format(diagram_name), bbox_inches='tight')