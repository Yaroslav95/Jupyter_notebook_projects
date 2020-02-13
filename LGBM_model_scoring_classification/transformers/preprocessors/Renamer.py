from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd


class Renamer(BaseEstimator, TransformerMixin):
    def __init__(self, renaming_dict):
        self.renaming_dict = renaming_dict
        
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        renamed_data = X.rename(columns=self.renaming_dict)
        return renamed_data
