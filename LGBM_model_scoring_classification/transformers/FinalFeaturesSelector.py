from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd


class FinalFeaturesSelector(BaseEstimator, TransformerMixin):
    def __init__(self, final_columns):
        self.final_columns = final_columns
        pass
        
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        X = X[self.final_columns]
        return X
