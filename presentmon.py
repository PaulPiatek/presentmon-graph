# You do not need that many import statements, so we just import
# numpy and matplotlib using the common alias 'np' and 'plt'.
import argparse
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
from enum import Enum

class PlotType(Enum):
    ALL = 0
    RAW = 1
    MEDIAN = 2


plt.style.use('ggplot')

parser = argparse.ArgumentParser(description='Display PresentMon Data.')
parser.add_argument('-f', '--file', help='full path of the csv file containing presentmon data')
args = parser.parse_args()

# renders the raw values
def plot_raw(ax, times, values):
    raw, = ax.plot(times, values, 'g-', lw=0.3, label='raw', antialiased=1)
    return raw

# renders the median
def plot_median(ax, times, values, bins):
    x_new = np.linspace(times.min(), times.max(), bins)
    delta = x_new[1] - x_new[0]
    idx = np.digitize(times, x_new)
    running_median = [np.median(values[idx == k]) for k in range(bins)]
    median, = ax.plot(x_new - delta / 2, running_median, 'b-', lw=1, label='median', antialiased=1)
    return median

# renders the average line and min/max text
def plot_min_max_med(ax, values, max_min):
    max_ms = "{0:.1f}".format(max(values))
    min_ms = "{0:.1f}".format(min(values))
    top_98 = "{0:.1f}".format(np.nanquantile(values, 0.98))
    top_02 = "{0:.1f}".format(np.nanquantile(values, 0.02))
    average = ax.axhline(np.mean(values), label='average: ' + str(np.mean(values)),
                         color='orange',
                         alpha=0.4)
    if max_min:
        ax.text(0, 0, 'max/min: ' + max_ms + '/' + min_ms + ' | 98/2%: ' + top_98 + '/' + top_02, verticalalignment='bottom')
    return average


# renders everything
def plot(ax, times, values, bins, plottype):
    handles = []
    if plottype in {PlotType.RAW, PlotType.ALL}:
        handles.append(plot_raw(ax, times, values))
        handles.append(plot_min_max_med(ax, values, True))
    if plottype in {PlotType.MEDIAN, PlotType.ALL}:
        handles.append(plot_median(ax, times, values, bins))
        handles.append(plot_min_max_med(ax, values, False))
    ax.legend(loc='lower right', handles=handles, scatterpoints=1)
    return

# With matplotlib we define a new subplot with a certain size (10x10)
fig, axarr = plt.subplots(2, sharex=True, figsize=(14, 9), dpi=100)

# number of bins for median
total_bins = 750

# if filepath was passed as argument
if args.file:
    file_path = args.file
# otherwise select the presentmon csv-file via file dialogue
else:
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(initialdir='~', filetypes=(('Presentmon Files', '*.csv'), ('All Files', '*')))
    root.destroy()
if not file_path:
    exit(0)

# Using numpy we can use the function loadtxt to load your CSV file.
# We ignore the first line with the column names and use ',' as a delimiter.
data = np.loadtxt(file_path, delimiter=',', skiprows=1, usecols=(9, 10, 11, 12, 13, 14))

# You can access the columns directly, but let us just define them for clarity.
# This uses array slicing/indexing to cut the correct columns into variables.
time_in_seconds = data[:, 0]
ms_between_presents = data[:, 1]
ms_between_display_change = data[:, 2]
ms_in_present_api = data[:, 3]
ms_until_render_complete = data[:, 4]
ms_until_displayed = data[:, 5]

# this are the important values: time and ms between presents (could calculate this, but hey it's already there)
x = time_in_seconds
y = ms_between_presents

# calculate fps from times
fps = []
last_y = 0
for tis in y:
    fps.append(1 / (tis / 1000))

# render the frametime
plot(axarr[0], x, y, total_bins, PlotType.RAW)
axarr[0].set_title("Frametime")
axarr[0].set_ylim([0, 20])
axarr[0].set_xlim([0, max(x)])

# render the fps
plot(axarr[1], x, np.asarray(fps), total_bins, PlotType.MEDIAN)
axarr[1].set_title("FPS")
axarr[1].set_ylim([0, 300])

# show the plots
plt.tight_layout()
plt.show()
