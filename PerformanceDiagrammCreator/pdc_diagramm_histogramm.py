from pdc_parsing import parse_timestamp_messages
import os
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mticker
import numpy as np
from scipy.interpolate import interp1d
from matplotlib.ticker import FuncFormatter
from scipy.stats import t


base_paths = [
    #'/Users/bornkessel/Developer/testresults/results/performance/output/data/01_FIN_InitTest_H/ihwk_A1_081756_211223/081756_211223_1_80'
    #'/Users/bornkessel/Developer/testresults/results/performance/output/data/01_FIN_InitTest_H/ihwk_A1_081756_211223/082156_211223_1_8080'
    '/Users/bornkessel/Developer/testresults/results/performance/output/data/S_01_FIN_SocketTypes_H/UDP_Fragment/093322_111223_1_64080'
]

diagram_name = 'NEW_campaign-diagr2__histogram'

# Set the style
sns.set_style("whitegrid")
sns.set_context("paper", font_scale=2, rc={"lines.linewidth": 2.5})
plt.rc('text', usetex=False)
plt.rc('font', family='serif')


for base_path in base_paths:
    timediff_file_path = os.path.join(base_path, 'timediff.xml')
    if not os.path.isfile(timediff_file_path):
        continue

    timediff_records = parse_timestamp_messages(timediff_file_path)

    # Create a histogram
    fig, ax = plt.subplots(figsize=(7, 6))
    sns.histplot([(record['difference']*1000000) for record in timediff_records], ax=ax, bins=950, color='#00B0F0')

    # Add a line for the mean
    mean = np.mean([(record['difference']*1000000) for record in timediff_records])
    ax.axvline(mean, color='black', linestyle='dashed', linewidth=1)

    # Add a legend with the numer of the mean
    ax.legend([r'$\mu={:.1f}$'.format(mean)], loc='upper right')

    # Set the x-axis label
    ax.set_xlabel('Latency (\u03bcs)',  fontweight='bold')
    ax.set_ylabel('Count',  fontweight='bold')

    # Adjust y-Axis to use 10^3 instead of 1000
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

    # Calculate and add the 95% confidence interval here
    # data = [(record['difference']*1000000) for record in timediff_records]
    # n = len(data)
    # m, se = np.mean(data), np.std(data)
    # h = se * t.ppf((1 + 0.99) / 2., n-1) # Does not work, nticker.t.ppf is not defined

    # Add the confidence interval to the plot with a different style than the mean line
    # ax.axvline(mean-h, color='black', linestyle='dotted', linewidth=1.2)
    # ax.axvline(mean+h, color='black', linestyle='dotted', linewidth=1.2)

    # Add a legend for the confidence interval
    # ax.legend([r'$\mu={:.1f}$'.format(mean), r'$\mu\pm{:.1f}$'.format(h)], loc='upper right')

    # Limit the x-axis to the 99% confidence interval
    ax.set_xlim([150, 300])

    # Show the plot
    #plt.savefig('{}.pdf'.format(diagram_name), bbox_inches='tight')

    # Clear the plot
    plt.clf()

    # Create a plot with the sequence number as x-axis and the difference between the timestamps as y-axis
    fig, ax = plt.subplots(figsize=(7, 6))
    sns.lineplot(x=[record['sequence'] for record in timediff_records], y=[record['difference']*1000000 for record in timediff_records], ax=ax, color='#00B0F0')

    # Set the x-axis label
    ax.set_xlabel('Sequence number',  fontweight='bold')
    ax.set_ylabel('Latency (\u03bcs)',  fontweight='bold')

    # Show the plot
    plt.show()

