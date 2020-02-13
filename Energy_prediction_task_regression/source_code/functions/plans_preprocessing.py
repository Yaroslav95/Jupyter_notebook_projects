import re
import pandas as pd
import functions.check_date as check_date
import const.objects_file as objects_file


def plans_preprocessing(df):
    '''
    Функция предобработки файла energy:
       1) Сортировка датасета в порядке возрастания дат
       2) Проверка корректности дат временного ряда
       3) Преобразования датасета
    '''  
    df.sort_values(by='DateTime').reset_index(drop=True, inplace=True) 
    check_date.check_date(df.sort_values(by='DateTime').groupby('DateTime').size())  
    
    #Приведение значений к lower() в признаках типа object 
    #Преобразование некорректных значений в числовых признаках, приведение к типу float
    for col in df.columns[1:]:
        if col in ['product_2_status', 'product_3_status', 'product_4_status']:
            df[col] = df[col].apply(lambda x: str(x).lower())
        else:
            df[col] = df[col].apply(lambda x: re.sub(r'[^0-9.]', '', str(x)))\
                             .apply(lambda x: float(x) if x!='' else None)\
                             .fillna(method='ffill')  
    
    #Применение get_dummies для категориальных переменных, rename признаков
    df = pd.concat([df, pd.get_dummies(df[['product_2_status', 'product_3_status', 'product_4_status']],\
                    prefix=['product_2', 'product_3', 'product_4'], dummy_na=True, dtype='int')], axis=1)\
           .drop(['product_2_status', 'product_3_status', 'product_4_status'], axis=1)\
           .rename(columns=objects_file.rename_plans)
        
    return(df)