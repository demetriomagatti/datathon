from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import dendrogram
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class dendrogram_maker():
    def __init__(self,*args,**kwargs):
        # Set default parameters
        self.data = pd.DataFrame()
        self.column_list = []
        self.model = []
        self.distance_threshold = 1
        self.n_clusters = 0
        self.plot_configs = dict(figsize = (12,4),
                                 xmin = 0,
                                 xmax = 0,
                                 ymin = 0,
                                 ymax = 0,
                                 title = 'Hierarichical Clustering Dendrogram',
                                 xlabel = 'xlabel',
                                 ylabel = 'ylabel',
                                 fontsize = 10)
        # Update with provided parameters
        self.__dict__.update(kwargs)


    def preprocess_data(self):
        '''
        Drop NaN values.
        Recode categorical variables into numerical variables.
        '''
        self.data = self.data[self.column_list]
        # Drop NaN values
        self.data.dropna(inplace=True)
        # Select categorical columns
        columns_object = self.data.select_dtypes(include=['object']).columns
        self.data[columns_object] = self.data[columns_object].astype('category')
        columns_categorical = self.data.select_dtypes(include=['category']).columns
        print(columns_categorical)
        # Convert to numerical
        self.data[columns_categorical] = self.data[columns_categorical].apply(lambda x: x.cat.codes)


    def model_fit(self):
        '''
        Fit model.
        '''
        self.model = AgglomerativeClustering(distance_threshold=self.distance_threshold,
                                             n_clusters=self.n_clusters)
        self.data['cluster_ix'] = self.model.fit_predict(self.data[self.column_list])


    def plot(self):
        '''
        Dendrogram plot.
        '''
        fig,ax = plt.subplots(figsize=self.plot_configs['figsize'])

        counts = np.zeros(self.model.children_.shape[0])
        n_samples = len(self.model.labels_)
        for i, merge in enumerate(self.model.children_):
            current_count = 0
            for child_idx in merge:
                if child_idx < n_samples:
                    current_count += 1  # leaf node
                else:
                    current_count += counts[child_idx - n_samples]
            counts[i] = current_count

        linkage_matrix = np.column_stack([self.model.children_, self.model.distances_, counts]).astype(float)

        dendrogram(linkage_matrix)
        
        ax.set_xlabel(self.plot_configs['xlabel'])
        ax.set_ylabel(self.plot_configs['ylabel'])
        ax.set_title(self.plot_configs['title'])
        
        return fig