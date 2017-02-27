# You do not need that many import statements, so we just import
# numpy and matplotlib using the common alias 'np' and 'plt'.
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog

plt.style.use('ggplot')


def plot(ax, times, values, bins, text):
    x_new = np.linspace(times.min(), times.max(), bins)

    delta = x_new[1] - x_new[0]
    idx = np.digitize(times, x_new)

    running_median = [np.median(values[idx == k]) for k in range(bins)]

    ax.scatter(times, values, color='g', alpha=0.3)
    ax.plot(x_new - delta / 2, running_median, 'b-', lw=2)
    ax.legend(loc='lower right')
    return


def plot_min_max_med(ax, values, text):
    max_ms = max(values)
    min_ms = min(values)
    ax.text(0, 1, 'max/min ' + text + ' ' + str(max_ms) + '/' + str(min_ms), verticalalignment='center')

    ax.axhline(np.mean(values), label='average: ' + str(np.mean(values)),
                  alpha=0.4,
                  color='orange')
    ax.legend(loc='lower right')
    return


# With matplotlib we define a new subplot with a certain size (10x10)
fig, ax = plt.subplots(2, sharex=True)

# number of bins for median
total_bins = 500

# selct the presentmon csv-file
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename(initialdir='~', filetypes=(('Presentmon Files', '*.csv'), ('All Files', '*')))

# Using numpy we can use the function loadtxt to load your CSV file.
# We ignore the first line with the column names and use ',' as a delimiter.
# data = np.loadtxt('/home/paul/Schreibtisch/test.csv', delimiter=',', skiprows=1, usecols=(9, 10, 11, 12, 13, 14))
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
last_y=0
for tis in y:
    fps.append(1 / (tis / 1000))

text="Frametime"
plot(ax[0], x, y, total_bins, text)
plot_min_max_med(ax[0], y, text)
ax[0].set_title(text)
ax[0].set_ylim([0,20])
ax[0].set_xlim([0,max(x)])

text="FPS"
plot(ax[1], x, np.asarray(fps), total_bins, text)
plot_min_max_med(ax[1], fps, text)
ax[1].set_title(text)
ax[1].set_ylim([0,300])


# Show the legend
# plt.ylim([0, 200])
plt.tight_layout()
plt.show()
