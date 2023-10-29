import pandas as pd
from datetime import datetime

df = pd.read_csv('lesson_2_data.csv', encoding='windows-1251', sep=';')
df = df.rename(columns={'Номер' : 'number',
                        'Дата создания' : 'create_date',
                        'Дата оплаты' : 'payment_date',
                        'Title' : 'title',
                        'Статус' : 'status',
                        'Заработано' : 'money',
                        'Город' : 'city',
                        'Платежная система' : 'payment_city'})
print(df.head())
'''
Также можно было бы указать столбцы с датами
parse_dates — указывает, стоит ли воспринимать даты как даты? (по умолчанию они воспринимаются пандасом как строки)
Параметр с датами может принимать несколько значений:
       True — пытается перевести в дату первую колонку
               список колонок — пытается перевести в дату указанные в списке колонки
Например:
pd.read_csv('path_to_your.csv', encoding='Windows-1251', sep=';', parse_dates=['create_data', 'payment_data'])
'''

#ВАЖНО!!! Если считаем деньги, то лучше сначала сохранить сумму в переменную, с которой в конце рассчетов и преобразований можно всё сравнить,
# чтобы убедиться, что ничего не потеряли
all_money = df.money.sum() #выводим общую сумму всех полученных денег
print('Sum: ' + str(all_money))
print('Product (дисперсия): ' + str(df.money.product()))
print('Std (среднеквадратичное отклонение): ' + str(df.money.std()))
print('Var (дисперсия): ' + str(df.money.var()))

#Вычислим количество заказов в каждом городе по каждому курсу
#чтобы title не был индексом датафрейма, а был обычной колонкой (как money) и с ним было удобно работать, добавили as_index=False
money_by_city = (df
      .groupby(['title', 'city'], as_index=False)
      .aggregate({'money' : 'sum'})
      .sort_values('money', ascending=False)
)
'''
aggregate выше можно заменить на agg,
а выражение написать без (), просто добавив на каждой строке слэш
money_by_city = (df \
      .groupby(['title', 'city'], as_index=False) \
      .aggregate({'money' : 'sum'}) \
      .sort_values('money', ascending=False)
      )
'''
print(money_by_city)

#выгрузим полученные данные в файл, но уберем первый столбец с индексами записью index=False
money_by_city.to_csv('money_by_city.csv', index=False)
df1 = pd.read_csv('money_by_city.csv', sep=',')
print(df1.head())

#Вычислим количество полученных денег по каждому курсу
money_by_title = df \
    .query("status == 'Завершен'") \
    .groupby('title', as_index=False) \
    .aggregate({'money' : 'sum', 'number' : 'count'}) \
    .sort_values('money', ascending=False) \
    .rename(columns={'number' : 'success_orders'})
    #после агрегации number:count в столбце number отображается number.count, поэтому мы тут переименовываем не number, а number.count
print(money_by_title)
'''
В query также можно передать сразу несколько условий. Условия, которые должны выполняться одновременно, соединяются с помощью and или &: 
product_data.query("title == 'Курс обучения «Эксперт»' and status == 'Завершен'")
Когда должно удовлетворяться одно из условий – or или |:
product_data.query("title == 'Курс обучения «Эксперт»' or status == 'Завершен'")
'''
print('\n')

# ПРОВЕРКИ
#Проверим количество уникальных курсов и что запрос выше этой строки отображал их верно
print(df.title.unique())
#Выведем сколько раз каждый курс встречается в файле
print(df.title.value_counts())
'''
Также метод value_counts принимает на вход несколько параметров:
normalize – показать относительные частоты уникальных значений (по умолчанию равен False). 
dropna – не включать количество NaN (по умолчанию равен True)
bins – сгруппировать количественную переменную (например, разбить возраст на возрастные группы); 
для использования данного параметра нужно указать, на сколько групп разбить переменную
'''
print('\n')

#Проверяем, что количество денег после всех манипуляций не изменилось
print(money_by_title.money.sum())
print(all_money)
#кроме последнего знака всё сходится, поэтому можно было сделать так
if int(money_by_title.money.sum()) == int(all_money):
    print("OK")
else:
    print("ERROR")
#или округлить значения через round(all_miney, 2) - округляем значение до 2-х знаков после запятой
print('\n')

#На основе вышеописанного подготовим шаблон автовыгружатора результатов успешного рассчета в файл с актуальной датой выгрузки
today = datetime.today().strftime('%Y-%m-%d')
#Можно было ещё добавить H – час, M – минуты, S – секунды: %Y-%m-%d-%H:%M:%S
file_name = 'money_title_{}.csv'
file_name = file_name.format(today)
if int(money_by_title.money.sum()) == int(all_money):
    print("OK! File {} is written.".format(file_name))
    money_by_title.to_csv(file_name, index=False)
else:
    print("ERROR. File is not written. Check again.")
print('\n')
