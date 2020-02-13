#В файле содержатся константные объекты, используемые в проекте

div_cols = {'product_1_plan': 'product_1_plan_cumsum', 'product_2_plan': 'product_2_plan_cumsum',
            'product_3_plan': 'product_3_plan_cumsum', 'product_4_plan': 'product_4_plan_cumsum'}

shift_cols = ['target_mean', 'product_1_plan', 'product_1_plan_cumsum', 'product_2_plan', 
              'product_2_plan_cumsum', 'product_3_plan', 'product_3_plan_cumsum', 'product_4_plan',
              'product_4_plan_cumsum']

rename_plans = {'product_2_резерв':'product_2_reserv', 'product_2_ремонт':'product_2_repair', 
                'product_3_резерв':'product_3_reserv', 'product_3_ремонт':'product_3_repair', 
                'product_4_резерв':'product_4_reserv', 'product_4_ремонт':'product_4_repair',
                'product_2_отключение газа':'product_2_gas_off', 'product_2_ТО':'product_2_TO',
                'product_3_ТО':'product_3_TO', 'product_4_ТО':'product_4_TO'}

rename_energy = {'Фактическое собственное потребление, МВтч':'target', 
                 'Характерный день':'Character_day', 'Торговый час':'Trade_hour', 
                 'Характерный час':'Character_hour', 'Дата':'DateTime' }

drop_col_energy = ['График ППП, МВтч', 'Объем Торгового графика (скорректированное плановое почасовое потребление) МВт*час',
                  'Объем покупки МВт*час', 'В т.ч. потери, отнесенные к объему покупки',
                  'Покупка (+) / Продажа (-) на БР (BR+/-), МВтч', 'Объем покупки на БР (BR+), МВтч', 
                  'Объем продажи на БР (BR-), МВтч']