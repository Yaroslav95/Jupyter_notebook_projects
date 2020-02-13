import pandas as pd

def create_df():
    '''
    Формирует датасет из 3 исходных .csv файлов (соедниение файлов, обработка невалидных данных и пропусков)
    ''' 
    df = pd.read_csv('input_files/Anketa_data.csv', sep=';', encoding='windows-1251')
    col_date=['REQUEST_DATE', 'BIRTHDATE', 'CLIENT_DATE', 'EMPL_DURATION', 'REGISTRATION_DATE_3CARD', 'FIRST_CONTRACT_DATE']
    for column in col_date:
        df[column] = pd.to_datetime(df[column].apply(lambda x: str(x)[0:10]), format='%d.%m.%Y').astype('datetime64')
        
    print('Анкетные данные ', df.shape)    
    
    df_bki = pd.read_csv('input_files/BKI_data.csv', sep=';', encoding = "utf-8", dtype= {'PMT_STR_FULL': 'str'}) 
    df_bki = df_bki.loc[lambda x: x.SUMM_LIMIT_CLOSE.notna()]
    df_bki= df_bki.drop('ID', axis=1)
    col_date=['CREATE_DATE', 'DATE_OPEN_FIRST', 'DATE_OPEN_LAST']
    for column in col_date:
        df_bki[column] = pd.to_datetime(df_bki[column].apply(lambda x: str(x)[0:10])).astype('datetime64')  
    
    print('Данные из БКИ отчета ', df_bki.shape)  
    
    df = df.merge(df_bki, on=['REQUEST_ID', 'CLIENT_ID'], how='inner')  
    print('Анкета inner merge БКИ ', df.shape)

    sc_targ = pd.read_csv('input_files/Score_target.csv', encoding = "windows-1251", sep='\t') 
    sc_targ = sc_targ.drop(['REQUEST_DATE','REQUEST_ID+', 'Выражение_1'], axis=1).loc[lambda x: ~x['12_90'].isna()]
    sc_targ.REGISTRATION_DATE = pd.to_datetime(sc_targ.REGISTRATION_DATE.apply(lambda x: str(x)[0:10])).astype('datetime64')
    print('Размерность датасета скоров и с notNAN целевой ', sc_targ.shape)
    
    df=df.merge(sc_targ, on=['CLIENT_ID', 'REQUEST_ID'], how='inner')
    df=df.drop('BANK_ID', axis=1)
    print('Итого (Анкета+БКИ+Скоры_целевая)', df.shape)
     
    #Очистка невалидных данных  
    #Убираем лишние STOPFACTORS:
    df=df[df.STOPFACTOR.isin(['Кредит предоставлен', 'Отказ по лимиту', 'Отменена клиентом', 'Отказ андеррайтинга', 'Интегральный скоринг',     'Антифрод'])] #-4809 строк
    
    #Убираем из датасета по возрасту >69 и <23 и PMT_STR_FULL, так как это были поручители и созаемщики
    df = df.loc[lambda x: ((x.REQUEST_DATE - x.BIRTHDATE).dt.days / 365.25 <= 69) & \
             ((x.REQUEST_DATE - x.BIRTHDATE).dt.days / 365.25 >= 23) & ~x.PMT_STR_FULL.isna()] #-31 строк
    
    #Выкидываем трудоспособных граждан (непенсионного возраста) с зп < 12000
    df=df.loc[lambda x: ~((x.INCOME<12000) & ((((x.REQUEST_DATE - x.BIRTHDATE).dt.days / 365.25 < 60) & (x.GENDER == 1)) \
             | (((x.REQUEST_DATE - x.BIRTHDATE).dt.days / 365.25 < 55) & (x.GENDER == 0))))] #-86 строк
    
    #Выкидываем товарищей, которые потенциально не смогут проплатить кредит 
    df=df.loc[lambda x: x.EST_NEXT_PMT_CRE_ + x.LOAN_SUM_INS / 58 < 
             x.INCOME - 10000 * (x.DEPENDENTS / (1 + (x.SPOUSE == 1).astype(int)) + 1 + (x.SPOUSE.isin([2, 3])).astype(int))] #-6457 строк
    
    #Преобразуем у пенсионеров EMPLOYEE на 3
    df.loc[lambda x: ((x.REQUEST_DATE - x.BIRTHDATE).dt.days / 365.25 > 60) & (x.GENDER == 1) & (x.EMPLOYEE.isna()), 'EMPLOYEE'] = 3 #155
    df.loc[lambda x: ((x.REQUEST_DATE - x.BIRTHDATE).dt.days / 365.25 > 55) & (x.GENDER == 0) & (x.EMPLOYEE.isna()), 'EMPLOYEE'] = 3 #551
   
    #Удаляем ненужные признаки
    df=df.drop(['TELE2_new|pr_pos_dlq_60at09', 'BEELINE|work_ver_1000m', 'МЕГАФОН|is_work2000_v2', 'BEELINE|cnt_block_6m_bin', 
                'МЕГАФОН|is_work1000_v2', 'TELE2_new|pr_mfo', 'BEELINE|work_ver_2500m', 'МЕГАФОН|is_work2000_v1', 
                'МЕГАФОН|is_home2000_v2', 'МЕГАФОН|is_work100_v1', 'BEELINE|home_ver_2500m', 'BEELINE|score_skb_uni3_pos', 
                'МЕГАФОН|BLOCK_CNT', 'МЕГАФОН|bad_address_work', 'МЕГАФОН|CIRCLE', 'TELE2_OLD|probability_cash', 
                'МЕГАФОН|OLD_SCORE', 'МЕГАФОН|is_work500_v2', 'МЕГАФОН|is_home100_v1', 'TELE2_new|pr_cash_dlq_60at09', 
                'МЕГАФОН|is_work500_v1', 'AFS|AFS_RULES_COUNT', 'BEELINE|home_ver_300m', 'МЕГАФОН|BLOCK_DUR', 
                'BEELINE|score_skb_uni3_cc', 'BEELINE|prepaid_ind', 'BEELINE|recharge_avg_6m_bin', 
                'QIWI_NEW|predictions_basis_90_v2_1', 'QIWI_NEW|predictions_basis_90_v2_2', 'BEELINE|score_skb_uni3_nan', 
                'МЕГАФОН|is_home500_v2', 'QIWI_NEW|predictions_basis_60_v3_2', 'МЕГАФОН|is_home100_v2', 'AFS|AFS_MATCH_COUNT', 
                'МЕГАФОН|is_home1000_v1', 'QIWI_NEW|predictions_basis_60_v3_1', 'TELE2_new|pr_pos_dlq_90at12', 
                'BEELINE|work_ver_500m', 'MAIL|NEW', 'QIWI_OLD|predictions_comb_v1', 'МЕГАФОН|is_home1000_v2', 
                'МЕГАФОН|bad_address_home', 'МЕГАФОН|is_work100_v2', 'BEELINE|home_ver_1000m', 'МЕГАФОН|is_home2000_v1', 
                'BEELINE|work_ver_300m', 'TELE2_OLD|probability_mfo', 'MAIL|MBALL', 'BEELINE|roam_ind', 'AFS|AFS_APPS_COUNT', 
                'МЕГАФОН|is_home500_v1', 'TELE2_new|pr_cash_dlq_90at12', 'BEELINE|bee_ind', 'МЕГАФОН|PAY_MAX', 
                'BEELINE|home_ver_1500m', 'BEELINE|client_type', 'QIWI_OLD|predictions_basis_60_v2', 'BEELINE|score_skb_uni3_cash',
                'MAIL|OLD', 'BEELINE|home_ver_500m', 'QIWI_NEW|predictions_basis_60_v3_3', 'BEELINE|hit_ind', 
                'YANDEX|yandex_score', 'BEELINE|score_skb', 'QIWI_OLD|predictions_basis_90_v1', 'score_mrg_m2', 'FPS|FPS_SCORE', 
                'BEELINE|work_ver_1500m', 'TELE2_new|pr_pos_dlq_60at06', 'TELE2_OLD|probability_card', 'BEELINE|lifetime_bin', 
                'МЕГАФОН|is_work1000_v1', 'BEELINE|all_contact', 'TELE2_new|pr_cash_dlq_60at06', 'AFS|AFS_RULE', 
                'BEELINE|lifetime_equipment', 'FPS|FPS_APPLICATIONSFOUND'],axis=1)
    
    df = df.drop(df.isna().mean().loc[lambda x:x>0.4].index, axis=1) #Удаление с кол-вом пропусков более 40%             
    
    df=df.loc[lambda x: ~x.EMPL_DURATION.isna()] #Удаляем 6 строк
    df=df.loc[lambda x: ~x.PRESENCE_CAR.isna()] #Удаляем 1 строку
    df=df.loc[lambda x: ~x.REGISTRATION_DATE.isna()] #Удаляем 6 строк
        
     #Заполняем нулями поля, так как возможно в БКИ инфа не пришла, взял кредит через сотрудника
    df.loc[:,       ['INQ_7_QTY','INQ_14_QTY','INQ_21_QTY','INQ_30_QTY','INQ_60_QTY','INQ_90_QTY','INQ_180_QTY','INQ_365_QTY','INQ_365_PLUS_QTY']]= \
      df.loc[:,['INQ_7_QTY','INQ_14_QTY','INQ_21_QTY','INQ_30_QTY','INQ_60_QTY','INQ_90_QTY','INQ_180_QTY','INQ_365_QTY','INQ_365_PLUS_QTY']].fillna(0)
    df.ABROAD = df.ABROAD.fillna(3) #1068 значений
    df.EMPL_OPF = df.EMPL_OPF.fillna(99999) #393 пропуска
    df.EMPLOYEE = df.EMPLOYEE.fillna(3) #Добавили 33 значений в класс 3
    df['FPS|MAINRULES_COUNT'] = df['FPS|MAINRULES_COUNT'].fillna(0) #28  значений
      

    for col in ['BKI|FICO3', 'BKI|4score(ECS)', 'BKI|EI', 'FICOFRAUD', 'МЕГАФОН|NEW_SCORE', 'МЕГАФОН|ALL_CLC', 'МЕГАФОН|LIFETIME_BIN',
              'MTS|Abonent', 'MTS|Ne_abonent']:
       df[col]= df[col].fillna(-999999)
     
    df = df.assign(
        REALTY=df.REALTY.map({'ЗАЕМЩИК - ЕДИНСТВЕННЫЙ СОБСТВЕННИК': 1, 'НЕТ': 0, 'ДОЛЕВАЯ/СОВМЕСТНО С СУПРУГОЙ(ОМ)': 2}) \
        .astype('float'))
      
    df=df.loc[lambda x: x.INCOME <= 600000]       #Убираем 46 чел с очень высокой зп
    df=df.loc[lambda x: x.SUMM_LIMIT < 100000000] #убираем 1 чела с кредитным лимитом 193 млн   
  
    df=df.rename(columns={'МЕГАФОН|NEW_SCORE':'MEGAFON|NEW_SCORE','МЕГАФОН|ALL_CLC':'MEGAFON|ALL_CLC',
                          'МЕГАФОН|LIFETIME_BIN':'MEGAFON|LIFETIME_BIN'})
    
    df['FPS|FPS_RULE'] = df['FPS|FPS_RULE'].fillna(0) #28 пропусков
    df=df.drop(['CLIENT_ID', 'CREATE_DATE', 'REGISTRATION_DATE_3CARD', 'STOPFACTOR'], axis=1) #STOPFACTOR
    
    #Обновление версии CRE
    df=df.drop(['EST_NEXT_PMT_CRE'], axis=1)
    df=df.rename(columns={'EST_NEXT_PMT_CRE_':'EST_NEXT_PMT_CRE'})
    
    print('Окончательная размерность исходника после удаления невалидных наблюдений', df.shape)
     
    return(df)