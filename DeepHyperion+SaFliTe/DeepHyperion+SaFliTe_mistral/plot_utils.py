import matplotlib.pyplot as plt
import seaborn as sns

from matplotlib.offsetbox import OffsetImage
import numpy as np
import os
import pandas as pd

def plot_heatmap(data, 
                ylabel,
                xlabel,                                   
                minimization=False,
                savefig_path=None,
                 ):
    plt.clf()
    plt.cla()

    ser = pd.Series(list(data.values()),
                  index=pd.MultiIndex.from_tuples(data.keys()))
    df = ser.unstack().fillna(0)
    df = ser.unstack().fillna(np.inf)

    # figure
    fig, ax = plt.subplots(figsize=(8, 8))

    cmap = sns.cubehelix_palette(as_cmap=True)

    # Set the color for the under the limit to be white (0.0) so empty cells are not visualized
    # cmap.set_under('-1.0')
    # Plot NaN in white
    cmap.set_bad(color='white')    
    
    ax = sns.heatmap(df, vmin=0, vmax=6)
    ax.invert_yaxis()
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    # get figure to save to file
    if savefig_path:
        ht_figure = ax.get_figure()
        fig_name = savefig_path+"/heatmap_"+xlabel+"_"+ylabel
        print(os.path.abspath(fig_name))
        ht_figure.savefig(fig_name)


    plt.clf()
    plt.cla()
    plt.close()
 
    


def getImage(path):
    return OffsetImage(plt.imread(path))

