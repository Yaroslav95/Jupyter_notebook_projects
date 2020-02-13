import numpy as np
import pandas as pd
import const.objects_file as objects_file


def div_features(df, div_pairs):
    '''
    Создание нового признака делением друг на друга существующих
    input: датасет, словарь признаков для деления
    output: дополненный датасет
    '''   
    for key in div_pairs:
        df[key+'/'+div_pairs[key]] = (df[key] / df[div_pairs[key]]).fillna(0)
    
    return df


def feature_generating(df_energy, df_plans):
    '''
    Соединение двух предобработаннных датасетов, генерация новых фичей, сдвиг фичей и целевой переменной
    output: Датасет, готовый для загрузки в модель
    '''   
    df_plans = df_plans.assign(month = lambda x: x['DateTime'].dt.month)\
                       .merge(df_energy.groupby('DateTime')['target'].mean().reset_index()\
                                         .rename(columns={'target':'target_mean'}), on='DateTime', how='inner')\
                       .assign(pkt_change = lambda x: x.target_mean.pct_change())\
                       .assign(pkt_change_2 = lambda x: x.target_mean.pct_change(periods=2))\
                       .assign(pkt_change_3 = lambda x: x.target_mean.pct_change(periods=3))\
                       .assign(MA_2 = lambda x: x.target_mean.rolling(2).mean())\
                       .assign(MA_3 = lambda x: x.target_mean.rolling(3).mean())
   
    #Сдвиг фичей с приставкой "plan", а также целевой переменной на одни сутки назад, остальные фичи нельзя использовать
    #в текущих сутках
    for col in objects_file.shift_cols:
        df_plans[col] = df_plans[col].shift(periods=-1)
    
    df = df_plans.dropna().merge(df_energy, on='DateTime', how='inner')
    df =  div_features(df, objects_file.div_cols)
    
    return df  