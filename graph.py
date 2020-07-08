import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
plt.rcdefaults()
import matplotlib.colors as mcolors
from operator import attrgetter


class PDGraphPeers():
    def __init__(self, data):
        self.df = pd.DataFrame(data)

    def unique_peers_counts(self):
        return self.df.groupby(['Peer'])['Date'].nunique()

    def days_per_peers(self, exclude=20):
        nu_peers = self.unique_peers_counts()
        ex_twenty_day = nu_peers[nu_peers > exclude]
        ax = sns.distplot(ex_twenty_day, kde=False, hist=True)
        ax.set(
            title='Distribution of number of days per peers excluding 20 days',
            xlabel='# of days',
            ylabel='# of peers')
        return ax

    def weekly_cohorts(self):
        self.df['datetime'] = pd.to_datetime(self.df['Date'])
        self.df['week'] = self.df['datetime'].dt.to_period('W')
        self.df['month'] = self.df['datetime'].dt.to_period('M')
        self.df['cohort'] = self.df.groupby('Peer')['datetime'].transform(
            'min').dt.to_period('W')
        df_cohort = self.df.groupby(
            ['cohort',
             'week']).agg(n_peers=('Peer', 'nunique')).reset_index(drop=False)

        df_cohort['period_number'] = (df_cohort.week - df_cohort.cohort).apply(
            attrgetter('n'))
        cohort_pivot = df_cohort.pivot_table(index='cohort',
                                             columns='period_number',
                                             values='n_peers')
        cohort_size = cohort_pivot.iloc[:, 0]
        retention_matrix = cohort_pivot.divide(cohort_size, axis=0)

        fig, ax = plt.subplots(1,
                               2,
                               figsize=(20, 16),
                               sharey=True,
                               gridspec_kw={'width_ratios': [1, 11]})

        # retention matrix
        sns.heatmap(retention_matrix,
                    mask=retention_matrix.isnull(),
                    annot=True,
                    fmt='.0%',
                    cmap='RdYlGn',
                    ax=ax[1])
        ax[1].set_title('Weekly Cohorts: Peer Retention', fontsize=16)
        ax[1].set(xlabel='# of periods', ylabel='')

        # cohort size
        cohort_size_df = pd.DataFrame(cohort_size).rename(
            columns={0: 'cohort_size'})
        white_cmap = mcolors.ListedColormap(['white'])

        fig.tight_layout()
        return sns.heatmap(cohort_size_df,
                           annot=True,
                           cbar=False,
                           fmt='g',
                           cmap=white_cmap,
                           ax=ax[0])
