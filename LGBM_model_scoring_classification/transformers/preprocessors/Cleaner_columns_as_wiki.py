from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd


class Cleaner_columns_as_wiki(BaseEstimator, TransformerMixin):
    def __init__(self, columns_as_wiki):
        self.columns_as_wiki = columns_as_wiki
        
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        df_clean = X[self.columns_as_wiki]
        return df_clean
