from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd


class Clipper(BaseEstimator, TransformerMixin):
    def __init__(self, columns_binary_clip: list, columns_percent_clip: list, percent_data: float):
        self.__columns_binary_clip = columns_binary_clip
        self.__columns_percent_clip = columns_percent_clip
        self.__percent_data = percent_data
        self.__dict_clip = {}

    def fit(self, X, y=None):

        for col in self.__columns_percent_clip:
            self.__dict_clip[col] = X[col].sort_values().iloc[int(X.shape[0] * self.__percent_data)]

        return self

    def transform(self, X):
        df = pd.DataFrame(X)

        for col in self.__columns_binary_clip:
            df[col] = (df[col] != 0).astype(int)

        for col in self.__columns_percent_clip:
            df[col] = df[col].clip(0, self.__dict_clip[col])

        return df
        