import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.colors as mcolors
from operator import attrgetter

class PDGraphPeers():

    def __init__(self, data):
        self.df = pd.DataFrame(data)

    def unique_peers_counts(self):
        return self.df.groupby(['Peer'])['Date'].nunique()

    def number_of_days(self, exclude=20):
        nu_peers = self.unique_peers_counts()
        ex_twenty_day = nu_peers[nu_peers > exclude]
        ax = sns.distplot(ex_twenty_day, kde=False, hist=True)
        ax.set(
            title='Distribution of number of days per peers excluding 20 days',
            xlabel='# of days', 
            ylabel='# of peers'
        )
        return ax.get_figure()
