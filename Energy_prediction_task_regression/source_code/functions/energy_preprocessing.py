import functions.check_date as check_date
import const.objects_file as objects_file


def energy_preprocessing(df):
    '''
    Функция предобработки файла energy:
       1) Сортировка датасета в порядке возрастания дат
       2) Проверка корректности дат временного ряда
       3) Преобразования датасета
    '''  
    df.sort_values(by='Дата').reset_index(drop=True, inplace=True)  
    check_date.check_date(df.sort_values(by=['Дата','Торговый час']).groupby('Дата').size())
       
    df = df.rename(columns=objects_file.rename_energy)\
           .assign(Character_day = lambda x: x['Character_day'].map({'рабочий день':0, 'выходной':1}))\
           .assign(Character_hour = lambda x: x['Character_hour'].map({'полупик':0, 'минимум':1,'пик':2}).astype('int'))\
           .assign(target = lambda x: x['target'].apply(lambda x: float(str(x).replace(',', '.'))))\
           .drop(objects_file.drop_col_energy, axis=1)\
  
    return df