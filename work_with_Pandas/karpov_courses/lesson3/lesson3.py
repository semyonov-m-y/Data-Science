#Задача: найти выборку лояльных пользователей, чтобы сделать именно им скидку на продукты брэндов
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('lesson_3_data_1_.csv', encoding='windows-1251', sep=',')
user_df = df[['tc', 'art_sp']]
print(user_df.head())
user_df = user_df.rename(columns={'tc' : 'user_id', 'art_sp' : 'brand_info'})
print('\n')

#ПОДГОТОВИМ ДАННЫЕ
#Напишем функцию, которая разделяет строку brand_info по пробелу, создавая список элементов и возвращает последний элемент (брэнд компании)
def split_brand(brand_name_data):
    return brand_name_data.split(' ')[-1]
#иначе функцию можно записать как user_df.brand_info.apply(lambda x: x.split(' ')[-1])

#Вставим эту функцию в apply (apply — применяет переданную в него функцию ко всем колонкам вызванного датафрейма.)
# и параллельно создадим новый столбец brand_name, куда и вставим наши данные
#Чтобы применить функцию к одной колонке датафрейма, можно выбрать её перед применением apply
user_df['brand_name'] = user_df.brand_info.apply(split_brand)
print(user_df.head())
print('\n')

#ПРОВЕДЕМ ИССЛЕДОВАТЕЛЬСКИЙ АНАЛИЗ
user_purchases = (user_df
        .groupby('user_id', as_index=False)
        .agg({'brand_name' : 'count'})
        .rename(columns={'brand_name' : 'purchases'})
)
print(user_purchases)
print('\n')

#Выясним общее количество покупателей
print(user_purchases.shape)

#Выясним медианное количество покупок
print(user_purchases.purchases.median())
#Это же можно посмотреть через describe по строке 50%
print(user_purchases.describe())
#Видим, что 25% пользователей совершило более 5 покупок, поэтому можно в user_purchases добавить .query('purchases >= 5')
#если решаем, что именно они подойдут для программы лояльности
user_purchases = (user_df
        .groupby('user_id', as_index=False)
        .agg({'brand_name' : 'count'})
        .rename(columns={'brand_name' : 'purchases'})
        .query('purchases >= 5')
)
print(user_purchases)
print('\n')

#Выведем список уникальных покупок пользователей
users_unique_brand = (user_df
        .groupby('user_id', as_index=False)
        .agg({'brand_name' : pd.Series.nunique}) #используем nunique, поскольку DataFrame.nunique пропускает пропущенные значения (NaN) и считает количество уникальных значений, тк у него параметр по умолчанию dropna=True, функция Series.unique — нет. Она возвращает сами значения, а не количество
        .rename(columns={'brand_name' : 'unique_brands'})
)
print(users_unique_brand)
print('\n')

#Теперь выведем пользователей и бренды, у которых они сделали покупки, потом отсортируем по убыванию
#а так как у каждого пользователя любимый бренд будет отображаться первой строкой, то применим head(1), чтобы вывести только её
brand_by_user = (user_df
        .groupby(['user_id', 'brand_name'], as_index=False)
        .agg({'brand_info' : 'count'}) #чтобы не переименовывать brand_name.count, агрегируем по любому другому полю, например brand_info
        .sort_values(['user_id', 'brand_info'], ascending=[False, False]) #тк сортируем по 2-м значениям, то и ascending указываем для каждого
        .groupby('user_id')
        .head(1)
        .rename(columns={'brand_name' : 'favorite_brand', 'brand_info' : 'favorite_brand_purchases'})
)
print(brand_by_user)
print('\n')
'''
Индекс — это лейбл строки в таблицы, по умолчанию является её номером. А имена колонок — лейблы, по которым мы можем обращаться к каждому из столбцов.
У датафрейма есть 2 атрибута index и columns, позволяющие получить доступ к соответствующей информации в виде array (на самом деле, не совсем array)
1) Сброс индекса: Иногда вам может захотеться перевести индекс датафрэйма в колонку.  Для этого существует метод reset_index. 
Индексом становится дефолтная последовательность чисел от 0 до числа строк - 1.
df.reset_index()
2) Удаление индекса: Аргумент drop отвечает за то, нужно ли переводить индекс в колонку, или убрать его из таблицы:
df.reset_index(drop=True)
3) Поиск пустых значений: isna — это метод, с помощью которого можно быстро найти пропущенные значения в датафрейме:
Применив его, на выходе мы получаем датафрэйм той же размерности, где в каждой ячейке True или False — в зависимости от того, было ли значение пропущено:
df.isna()
В связке с ним можно использовать, например, sum, чтобы посмотреть на число NA в разных колонках:
df.isna().sum()
'''
print(brand_by_user.index)
print(brand_by_user.columns)

#Теперь соединим наши три датафрейма по ключу (столбец user_id) через INNER JOIN (идет по умолчанию, поэтому how='inner' можно не писать),
# то есть объединим только юзеров, у которых более 5 покупок, которые сделали уникальные покупки и их любимые бренды
loyalty_df = (user_purchases
              .merge(users_unique_brand, on='user_id', how='inner')
              .merge(brand_by_user, on='user_id', how='inner'))
print(loyalty_df)
print('\n')

#Найдем лояльным покупателей, которые выбирают лишь 1 бренд
loyal_users = loyalty_df[loyalty_df.unique_brands == 1]
print(loyal_users)
print('\n')

#Посчитаем какая доля от всех покупок пришлась на любимый бренд
loyalty_df['loyalty_score'] = loyalty_df.favorite_brand_purchases / loyalty_df.purchases
print(loyalty_df.head())

#Нарисуем график распределения loyalty_score. kde=False, чтобы убрать линию
#ax = sns.displot(loyalty_df.loyalty_score, kde=True)
#plt.show()

#Выясним сколько лояльных клиентов в нашей выборке приходится на каждый бренд
brands_loyalty = (loyalty_df.groupby('favorite_brand', as_index=False)
          .agg({'loyalty_score' : 'median', 'user_id' : 'count'})
 )
ax1 = sns.barplot(x = 'favorite_brand', y = 'user_id', data = brands_loyalty)
plt.show()
#Изменить размер графика в формате (ширина, высота) - plt.figure(figsize=(6, 9))
#Сохранить график можно с помощью savefig , где аргумент — путь к сохраняемой картинке (желаемое название и формат): plt.savefig('1.jpg')
