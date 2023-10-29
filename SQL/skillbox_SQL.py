from wget import download
import pandas as pd
import sqlite3

download('https://github.com/lerocha/chinook-database/raw/master/ChinookDatabase/DataSources/Chinook_Sqlite.sqlite')

connect = sqlite3.connect("Chinook_Sqlite.sqlite")
# Создадим переменную с запросом
# Многострочные запросы можно ограничивать тройными кавычками: ''' ... '''

query = '''
-- Берем все элементы из таблицы Artist
SELECT *
FROM Artist
'''

# Данные считываем сразу в DataFrame
artists = pd.read_sql(query, connect)
print(artists)

# Посмотрим аналогично на таблицы Album и Track
albums = pd.read_sql('SELECT * FROM Album', connect)
tracks = pd.read_sql('SELECT * FROM Track', connect)
print(albums)
print(tracks)

# 👨🏻💻 Выведите таблицы Customer и Employee
#WHERE - Условия для фильтрации; SELECT - набор колонок через запятую или * FROM название таблицы WHERE условие Пример условия:
# "значение в колонке равно какому-то значению" - colname = X Еще отличия от Python: • в Python равенство проверяется через "==",
# а в SQL через "=" • в Python текст обрамляется и одинарными, и двойными кавычками, в SQL - только одинарными(двойные - для называний колонок)
# Пример: выведем названия всех таблиц, которые есть в базе данных
query = '''
SELECT
    name
FROM
    sqlite_schema
WHERE
    type ='table'
'''

pd.read_sql(query, connect)

# 👨🏻💻 Выведите из таблицы Track все композиции, для которых Composer = "Wolfgang Amadeus Mozart"
#DISTINCT, MAX, MIN, AVG Вывод уникальных значений / максимального значения в колонке / минимального значения в колонке /
# среднего SELECT distinct(имя колонки) FROM название таблицы SELECT MAX(имя колонки) FROM название таблицы SELECT MIN(имя колонки)
# FROM название таблицы SELECT MIN(имя колонки), MAX(имя колонки), AVG(имя колонки) FROM название таблицы

pd.read_sql('SELECT AVG(Bytes) from Track', connect)

# Посмотрим, какие есть жанры (таблица Genre, колонка name)
pd.read_sql('SELECT distinct(name) from Genre', connect)

# Дополнительно можем добавить сортировку с помощью ORDER BY name
pd.read_sql('SELECT distinct(name) FROM Genre ORDER BY name', connect)

# 👨🏻💻 Выведите уникальные значения для цены трека UnitPrice таблицы Track. Какой ценовой разброс?
# 👨🏻💻 Выведите максимальное и минимальное значения для Bytes таблицы Track

#JOIN Объединение таблиц.В текущей структуре таблицы ссылкъаются друг на друга с помощью колонок с идентификаторами, указывающими на номер строки в другой таблице
# Объединим в одну таблицу данные о треках и альбомах
query = '''
SELECT *
FROM Track
JOIN Album
ON Track.AlbumId = Album.AlbumId
'''
pd.read_sql(query, connect)

# Объединим в одну таблицу данные об альбомах и артистах
query = '''
SELECT *
FROM Artist
JOIN Album
ON Artist.ArtistId = Album.ArtistId
'''
pd.read_sql(query, connect)

# 👨🏻💻 Объедините все 3 таблицы в одну, чтобы можно было проследить связь трек-артист

#Группировка и функции агрегации 📝 Агрегация - функция, которая считается на наборе значений и объединяет их в одно.Например,
# взятие максимального значения или подсчет числа элементов в группе Мы можем группировать строки таблицы на основе какого -
# то значения и считать функции агрегации внутри группы 📝 COUNT - функция, которая считает количество элементов SELECT COUNT(*) FROM
# таблица SELECT COUNT(DISTINCT(колонка)) FROM таблица
# Ответим на вопрос, сколько артистов в таблице
pd.read_sql('SELECT count(*) from Artist', connect)

#Строчки с одинаковым значением в колонке агрегации объединяются в группу, и по ним сможно посчитать функцию агрегации:
# SELECT колонка агрегации, COUNT(колонка1), AVG(колонка2) FROM таблица GROUP BY колонка агрегации
# А теперь сгруппируем данные из таблицы альбомов по артистам и посмотрим, сколько альбомов у каждого артиста
query = '''
SELECT ArtistId, COUNT(title)
FROM Album
GROUP BY ArtistId
'''

pd.read_sql(query, connect)

query = '''
SELECT ArtistId, COUNT(title)
FROM Album
GROUP BY ArtistId
ORDER BY COUNT(title)
'''

pd.read_sql(query, connect)

#Ничего не понятно, давайте добавим сюда информацию о самом артисте
#Вложенные подзапросы Мы можем делать вложенные подзапросы и использовать их как таблицы SELECT... FROM( SELECT...FROM... ) ...
# Объединим запрос GROUP BY и JOIN
query = '''
SELECT name, COUNT(title)
FROM (
    SELECT *
    FROM Artist
    JOIN Album
    ON Artist.ArtistId = Album.ArtistId
)
GROUP BY name
'''

pd.read_sql(query, connect)

# Объединим запрос GROUP BY и JOIN
query = '''
SELECT name, COUNT(title)
FROM (
    SELECT *
    FROM Artist
    JOIN Album
    ON Artist.ArtistId = Album.ArtistId
)
GROUP BY name
ORDER BY COUNT(title)
'''

print(pd.read_sql(query, connect))

# 👨🏻💻 Возьмите запрос из упражнения "Объедините все 3 таблицы в одну" и выведите количество треков, написанных каждым исполнителем

# 👨🏻💻 Объедините таблицу Track и таблицу InvoiceLine. Сколько раз был куплен каждый трек? (Подсчет можно провести по колонке InvoiceID)

# 👨🏻💻 Ответьте на вопрос: какой автор наиболее коммерчески популярен? Чьи треки покупают чаще всего? Для этого понадобится объединить аж 4 таблицы :)
