import pandas as pd

taxi = pd.read_csv('2_taxi_nyc.csv')
print(taxi)

#Проверьте, сколько всего строк и столбцов имеется в датасете.
print(taxi.shape)

#Давайте посмотрим на типы колонок.
print(taxi.dtypes)

#Заменим пробел в названиях столбцов на знак нижнего подчеркивания.
taxi.columns = taxi.columns.str.replace(' ', '_')
print(taxi)

#Cколько раз встречается каждый из районов?
print(taxi.borough.value_counts())

#сколько раз в данных встречается район Бруклин (Brooklyn)?
print(taxi.query("borough == 'Brooklyn'").shape[0])

#Выясним общее количество поездок
print(taxi.pickups.sum())
print('\n')

#Выяснить, из какого района было совершено наибольшее количество поездок за весь период.
max_pickups_district = (taxi
      .groupby(['borough'], as_index=False)
      .aggregate({'pickups' : 'sum'})
      .sort_values('pickups', ascending=False)
      ).iloc[0]['borough'] #iloc применяется для индексирования
print(max_pickups_district)
#Также найти минимальное и максимальное значение в столбце можно с помощью функций - idxmin() и idxmax()
min_pickups = taxi.pickups.idxmin()
max_pickups = taxi.pickups.idxmax()
print(min_pickups)
print(max_pickups)
print('\n')

#Сгруппируйте данные по двум признакам: району города и является ли день выходным (колонки borough и hday).
# Сравните среднее число поездок, и выберите районы, из которых по праздникам в среднем поступает больше заказов, чем в обычные дни.
usual_day = taxi \
      .query('hday == "N"') \
      .groupby(['borough', 'hday'], as_index=False) \
      .agg({'pickups': 'mean'}) \
      .rename(columns={'pickups': 'pickups_n'})
      #после агрегации pickups:mean в столбце pickups отображается pickups.mean, поэтому мы тут переименовываем не pickups, а pickups.mean

holiday_day = taxi \
      .query('hday == "Y"') \
      .groupby(['borough', 'hday'], as_index=False) \
      .agg({'pickups': 'mean'}) \
      .rename(columns={'pickups': 'pickups_y'})

f = usual_day['pickups_n'] < holiday_day['pickups_y']
d = pd.concat([usual_day[['borough', 'hday', 'pickups_n']], holiday_day[['hday', 'pickups_y']]], axis=1)
print(d.query("pickups_y > pickups_n").values)
print('\n')

#Для каждого района посчитайте число поездок по месяцам. Отсортируйте полученные значения по убыванию и сохраните результирующий датафрейм в pickups_by_mon_bor.
#Обратите внимание, что итоговый датасет должен состоять из 3-х колонок - pickup_month, borough, pickups.
pickups_by_mon_bor = (taxi
      .groupby(['pickup_month', 'borough'], as_index=False)
      .aggregate({'pickups' : 'sum'})
      .sort_values('pickups', ascending=False)
      )
print(pickups_by_mon_bor)
print('\n')

'''
Поскольку данные о поездках в Нью-Йорке, температура представлена в градусах Фаренгейта. 
Напишите функцию temp_to_celcius, которая получает на вход колонку с температурой в °F и возвращает значения, переведенные в градусы Цельсия.
Формула:
 Celsius = ((Fahrenheit - 32) * 5.0) / 9.0
'''
def temp_to_celcius(ser):
      ser = pd.Series(ser, copy=False)
      return ((ser-32.0)*5.0)/9.0
Celsius = temp_to_celcius(taxi['temp'])
print(Celsius)