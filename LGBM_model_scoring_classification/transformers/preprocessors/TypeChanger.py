from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd


class TypeСhanger(BaseEstimator, TransformerMixin):
    def __init__(self, to_default_int=[], to_default_str=[], to_date=[], to_int=[], to_str=[], to_float=[]):
        self.to_default_int = to_default_int
        self.to_default_str = to_default_str
        self.to_date = to_date
        self.to_int = to_int
        self.to_str = to_str
        self.to_float = to_float
             
    def fit(self, X, y=None):
        return self
     
    def transform(self, X):
        transform_data=X.copy()  
        
        for column in self.to_default_int:
            transform_data.loc[:, column] = transform_data.loc[:, column].replace({0:-999999})    
        for column in self.to_default_str:
            transform_data.loc[:, column] = transform_data.loc[:, column].replace({'NOT FOUND':-999999}) 
        for column in self.to_date:
            transform_data.loc[:,column] = pd.to_datetime(transform_data.loc[:, column])
        for column in self.to_int:
            transform_data.loc[:, column] = transform_data.loc[:,column].apply(pd.to_numeric, downcast='integer')
        for column in self.to_str:
            transform_data.loc[:,column] = transform_data.loc[:, column].astype(str)
        for column in self.to_float:
            transform_data.loc[:,column] = transform_data.loc[:, column].apply(pd.to_numeric)
    
        return(transform_data)
