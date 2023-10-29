import matplotlib.pyplot as plt
import os  # функции для работы с файлами
import plotly.express as px #делаем интерактивную визуализацию
import pandas as pd  # функции для работы с таблицами
import urllib.request  # скачивание файла
import zipfile  # распаковка zip-архива

# Распаковываем архив
urllib.request.urlretrieve('https://drive.google.com/uc?export=view&id=1jbqLpNiKaDFY4ZJngrzYuWkTHOPuqsjL','dataset.zip')

with zipfile.ZipFile('dataset.zip', 'r') as zip_ref: zip_ref.extractall('dataset')

# Возьмем для сравнения первый и последний год
# 👨🏻💻 Попробуйте заменить 2015 год на 2016
data2019 = pd.read_csv('dataset/2019.csv')
data2015 = pd.read_csv('dataset/2015.csv')

# Пропишем год
data2019['Year'] = 2019
data2015['Year'] = 2015

# Посмотрим описание с помощью функции .describe()
print(data2015.describe())

# Приведем колонки к единому виду: удалим лишние колонки, переименуем отличающиеся
data2015 = data2015.drop(columns=['Region',
                                  'Dystopia Residual',
                                  'Standard Error',
                                  'Lower Confidence Interval',
                                  'Upper Confidence Interval',
                                  ],
                         errors='ignore') #если какая-то из колонок не будет найдена, не выводим ошибку

data2015 = data2015.rename(columns={
    'Country': 'Country or region',
    'Freedom': 'Freedom to make life choices',
    'Economy (GDP per Capita)': 'GDP per capita',
    'Health (Life Expectancy)': 'Healthy life expectancy',
    'Trust (Government Corruption)': 'Perceptions of corruption',
    'Happiness Rank': 'Overall rank',
    'Happiness Score': 'Score',
    'Family': 'Social support',
})

# Сделаем одинаковым порядок столбцов для наглядности - отфильтруем по списку колонок
data2015 = data2015[data2019.columns]
print(data2015)

# Корреляция - число от - 1 до 1, которое показывает, насколько два фактора А и B зависят друг от друга. Если А и B растут и падают одновременно,
# то корреляция близка или равна 1(прямая зависимость). Если А растет, когда B падает и наоборот, то корреляция близка или равна - 1(обратная зависимость)
# Если связи между поведением А и B нет, то корреляция равна 0
# 👨🏻💻 Вопрос: чему равна корреляция A и B, если B = A?
# Функция .corr() выдает таблицу попарных корреляций факторов.
# - numeric_only=True - взять для корреляции только числовые значения
correlations_table = data2019.corr(numeric_only=True)

# Выведем тепловую карту с помощью функции px.imshow
heat_map = px.imshow(correlations_table)
heat_map.show()
#Он показывает попарную корреляцию. Чем выше корреляция, тем светлее цвет. Тут у нас строго отрицательная корелляция, так как чем выше индекс счастья у страны,
#тем ближе она к 1-й строке в списке счастливых стран

# 👨🏻💻 Выведите таблицу корреляций для 2015 года. Изменилась ли картинка?

#Самая счастливая страна?
# 1. Найдем максимальное значение
max_value = data2019['Score'].max()
print(max_value)

# 2. Задаим условие фильтрации "равно максимальному значению"
data2019['Score'] == max_value
print(data2015['Score'])

# Аналогично для 2015
max_value = data2015['Score'].max()
data2015['Score'] == max_value
print(data2015['Score'])

#Тут самая счастливая страна - Швейцария. Посмотрим, что было в 2019 году
print(data2019[data2019['Country or region'] == 'Switzerland'])

#Построим графики распределения Насколько сильно разбросаны значения?
# Выберем только те столбцы, для которых интересно смотреть распределение (например, не интересны рейтинг и регион, тк не увидим по ним красивый график распределения):
interesting_columns = ['Score', 'GDP per capita', 'Social support',
                       'Healthy life expectancy', 'Freedom to make life choices', 'Generosity',
                       'Perceptions of corruption']

# Построим violin plot (диаграмма типа "скрипка"). В функцию px.violin передаем таблицу и список нужных колонок y
violin_plot = px.violin(data2019, y=interesting_columns)
violin_plot.show()

# Аналигично для графиков "ящик с усами" px.box
px_box = px.box(data2019, y=interesting_columns)
px_box.show()

# 👨🏻💻 Вернитесь к списку interesting_columns, удалите 'Score' и перезапустите ячейки с построением графиков

#Объединим данные в одну таблицу, чтобы проводить сравнительный анализ
data = pd.concat([data2015, data2019])

# Посмотрим данные для России по условию
print(data[data['Country or region'] == 'Russia'])

# 👨🏻💻 Выведите данные для любой другой страны

#Сводная таблица
#После склейки двух таблиц у нас получились 3-х-мерные данные: страна - индекс - год, и мы можем делать агрегацию в новом разрезе
score_by_year = data.pivot(index='Country or region', columns='Year', values='Score')

# Посмотрим на строчку с Россией. Для выбора строки используется .loc
# Чтобы получить однострочную таблицу, используется список внутри .loc[[...]]
print(score_by_year.loc[('Russia')])

# 👨🏻💻 Выведите данные для любой другой страны

# Найдем страну, которая больше всего выросла и сильнее всех упала в индексе счастья
score_by_year['diff'] = score_by_year[2019] - score_by_year[2015]

# Удалим строчки, в которых отсутствовали данные для какого-то из годов
score_by_year = score_by_year.dropna()

# Отсортируем данные: sort_values('diff')
print(score_by_year.sort_values('diff'))

# 👨🏻💻 Вернитесь к первой ячейке в блоке "Сводная таблица" и замените 'Score' на любой другой числовой параметр

#Какой параметр влияет на счастье больше всего? Числовые данные - это коэффициенты, показывающие, насколько фактор влияет на индекс.
# Чтобы посчитать в среднем фактор с максимальным влиянием, возьмем среднее для каждой колонки(axis=0) 👨
print(data.mean(axis=0, numeric_only=True))

# 🏻💻 Какой фактор больше всего влиял на Score?

# 👨🏻💻 Проведите такой же расчет для 2015 и 2019 года по отдельности. Изменилась ли картина?
