from pdc_parsing import parse_timestamp_messages
import os
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mticker
import numpy as np
from scipy.interpolate import interp1d

base_paths = [
    #'/Users/bornkessel/Developer/testresults/results/performance/output/231206_093804_8dfb44c_macOS/A_Initial/ihwk_1_073653_061223/073653_061223_1_80',
    #'/Users/bornkessel/Developer/testresults/results/performance/output/231206_093804_8dfb44c_macOS/A_Initial/ihwk_1_073653_061223/073723_061223_1_8900',
    '/Users/bornkessel/Developer/testresults/results/performance/output/231206_093804_8dfb44c_macOS/A_Initial/ihwk_1_073653_061223/073753_061223_1_65000',
]

diagram_name = 'campaign-diagr2__histogram'

# Set the style
sns.set_style("whitegrid")
sns.set_context("paper", font_scale=1, rc={"lines.linewidth": 2})
plt.rc('text', usetex=False)
plt.rc('font', family='serif')


for base_path in base_paths:
    timediff_file_path = os.path.join(base_path, 'timediffs.xml')
    if not os.path.isfile(timediff_file_path):
        continue

    timediff_records = parse_timestamp_messages(timediff_file_path)

    # Create a histogram
    fig, ax = plt.subplots(figsize=(4, 5))
    sns.distplot([(record['difference']*1000000) for record in timediff_records], ax=ax, kde=False, bins=100, color='#9fcc9f')

    # Add a line for the mean
    mean = np.mean([(record['difference']*1000000) for record in timediff_records])
    ax.axvline(mean, color='black', linestyle='dashed', linewidth=1)

    # Add a legend with the numer of the mean
    ax.legend([r'$\mu={:.1f}$'.format(mean)], loc='upper right')

    # Set the x-axis label
    ax.set_xlabel('Latency [\u03bcs]')
    ax.set_ylabel('Count')
    ax.set_title('Latency Distribution for a Payload Size of 65000 Bytes')

    # Limit the x axis
    ax.set_xlim(140, 260)

    # Show the plot
    plt.savefig('{}.png'.format(diagram_name), bbox_inches='tight')

