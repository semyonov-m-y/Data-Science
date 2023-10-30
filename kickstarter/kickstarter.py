'''
На примере краудфандинг-датасета посмотрим на базовые признаки, выделим один небазовый и два разных вида таргета, а затем
запустим наш первый fit-predict. В конце урока обсудим предсказания модели и разберёмся, как они получились.
Должны научиться предсказывать соберет ли проект достатучную сумму в указанную дату.
'''
from IPython.display import Image
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

Image(filename='kickstarter.jpg')

data = pd.read_csv('ks.csv')

data.head()
data.shape

#В столбце Состояние (table_screenshot_1.png, table_screenshot_2.png) нас интересуют лишь 2 статуса - failed и successful, потому что остальных мало и не ясно что за статусы
# или проект ещё не завершён и мы по нему обучение с учителем не проведем, тк нам нужны исторические данные
data['Состояние'].value_counts()

#Отфильтруем наши данные
data = data[data['Состояние'].isin(['failed', 'successful'])]
data['Состояние'].value_counts()

#Теперь определяем что берем за таргет. Есть 2 варианта:
#1) Через классификацию, разметив объекты по статусу: те проекты, у которых успешный статус = 1, остальные = 0
#2) Через регрессию по собранному количеству денег: применить модель, а потом уже смотреть, нужная ли сумма получилась
#Построим обе модели и потом выберем какая из них лучше

#1)
data.loc[(data['Состояние'] == 'failed'), 'таргет1'] = 0 #заполнили строки с failed нулями
data['таргет1'] = data['таргет1'].fillna(1) #заполнили строки остальные единицей
#получили бинарный таргет

#теперь столбец Состояние можно удалить
data = data.drop('Состояние', axis=1)
data.head()

#2)
data = data.rename({'Собрано в долларах' : 'таргет2'}, axis=1)
#Теперь таргет1 и таргет2 - это наши ответы, а всё остальное - признаки

#Надо обработать данные, чтобы осталась лишь таблица из чисел. Чтобы получить матрицу объектов, зачастую нужно обработать сырые данные,
#то есть извлечь из имеющихся таблиц признаки там, где они не даны явно.
#Столбцы Дедлайн и Дата публикации не числа и не несут сами по себе важной для нас информации в данном случае, так как не важно проект создан в январе или августе
#Но это не значит, что надо просто убрать эти столбцы. Полезнее будет рассчитать количество времени, прошедшего между ними,
#чтобы модель понимала сколько времени обычно нужно, чтобы собрать нужную сумму. Потому что чем больше срок, тем больше вероятность, что сумма будет набрана:
data['Дедлайн'] = pd.to_datetime(data['Дедлайн'])
data['Дата публикации'] = pd.to_datetime('Дата публикации')
data['Срок'] = (data['Дедлайн'] - data['Дата публикации']).dt.days

#Добавим стоблец года, тк в течение года уже может что-то произойти, что повлияет на нас. Поэтому добавим ещё один базовый признак Год публикации
data['Год публикации'] = data['Дата публикации'].dt.year

#Часто в выборке не хватает данных, допустим, если переменных мало. Когда мы выделили базовые признаки, можем добавить их извне, предварительно подумав,
#что ещё может объяснять таргет-переменную. Например, добавим excel-таблицу (excel_screenshot_1.png) с макрокотировками акций на определенные
# даты на нефть, сахар, электричество и тд, ведь если акции растут у всех, значит в стране всё хорошо, а следовательно люди богатеют и начинают искать
# куда инвестировать. Один из вариантов, как раз стартапы на kickstarter.
Macro = pd.read_excel("macrofeatures.xlsx", engine="openpyxl")
Macro.head()

#Добавим столбец с информацией о том, какие были котировки в даты активного проекта. Возьмем не все колонки, а одну для примера, например, цену на нефть.
Macro = Macro[['Close_brent', 'dlk_cob_date']].drop_duplicates() #убираем дубликаты цен на всякий случай, тк они не нужны

#Правда ли, что на каждый день у нас будет лишь 1 цена? Чтобы такого избежать, сгруппируем данные
Macro.groupby('dlk_cob_date')['Close_brent'].count() #убеждаемся, что везде 1. Можно ещё и отсортировать
Macro['dlk_cob_date'] = pd.to_datetime(Macro['dlk_cob_date'])

#Переводим Дату публикации в формат dlk_cob_date
data['Дата публикации'] = data['Дата публикации'].astype('datetime64[ns]')

data = pd.merge(data,
         Macro,
         left_on=['Дата публикации'],
         right_on=['dlk_cob_date'],
         how='left') #используем LEFT JOIN

#Теперь много NaN значений, тк котировки были не во все даты.
#Есть стратегии обработки отсутствующих значений:
#1) Выкинуть строки с NaN. Но так мы потеряем много информации.
#2) Попытаться заполнить NaN значениями

#Отсортируем наш датасет по Дате публикации
data = data.sort_values('Дата публикации')

#Заполним NaN в Close_brent предыдущими значениями, тк в выходные торгов нет и соответственно для них можно брать цену пятницы
data['Close_brant'] = data['Close_brant'].fillna(method='ffill')

#Тк для самых первых значений предыдущих нет и они остались NaN, можно посмотреть какая самая первая неотсутствующая цена была и положить её вместо NaN
data['Close_brant'] = data['Close_brant'].fillna(34.41)

#Удалим ненужные нам столбцы
data = data.drop(['Дедлайн', 'Дата публикации', 'dlk_cob_date'], axis=1)
data.head()

#Так как столбец Название уникален и почти не влияет на то, проинвестируют ли в него или нет, удаляем
#Данные из столбца Страна по сути есть в столбце Валюта. А повторяющуюся информацию лучше не сохранять. То есть, если столбцы повторяются,
#или из одного можно элементарно вывести другой, один из них удаляем, тк информацию от этого не потеряем
#Столбец Инвесторов тоже удаляем, так как он напрямую влияет на таргет, но лишь во время, когда уже пройдет дэдлайн + это будет как подсказка модели,
#а нам этого не надо. Ведь для нового проекта изначально в столбце Инвесторов будет 0. И мы не можем строить модеть "подглядывая" в этот признак.
data = data.drop(['Название', 'Страна', 'Инвесторов'], axis=1)

#Научимся обрабатывать категориальные признакми (раскодируем наши категории, переведя их в числовой вид)
#Есть способы:
# 1) One-hot Encoding - для каждой категории создаем новую бинарную колонку, которая показывает объект принадлежит данной категории или нет
#Поработаем с валютой - через get_dummies создадим таблицу, в которой будет 1 в столбце лишь там, где валюта соответствует нашей и конкатенируем 2 таблицы
data = pd.concat((data, pd.get_dummies(data['Валюта'])), axis=1)
data = data.drop('Валюта', axis=1)
data.head()

#Когда используем One-hot Encoding также нужно ОБЯЗАТЕЛЬНО избавляться от одной из новосозданных колонок, отвечающих за категорию.
# Потому что модели не любят избыточную информацию. Поэтому избавимся от одного из новосозданных get_dummies столбцов (currencies_screenshot.png) -
# например столбец валюты AUD. Но мы не потеряем данные, ведь если в останых столбцах будет 0. Это нам сигнализирует, что тут была 1
data = data.drop('AUD', axis=1)

#Аналогично Валюта закодируем Главная категория
data = pd.concat((data, pd.get_dummies(data['Главная категория'])), axis=1)
data = data.drop('Главная категория', axis=1)
data.head()

#Избавимся от столбца games
data = data.drop('Games', axis=1)

#Так как категорий 159 штук, то при применении One-hot encoding мы получим 158 новых столбцов. Это чрезмерно много.
len(data['Категория'].unique())

#Поэтому используем другой способ - Mean target encoding (Счетчики) - он делает одну вещественную колонку.
#Нам не важно название категории, нам важно как она связана с нашей таргетной переменной. Поэтому для каждой категории посчитаем сколько в среднем принимает
#значение там таргет и вместо категорий положим эти средние значения. То есть, например, есть у нас 2 объекта IT с таргетом 100 и 200, то есть
#(100 + 200) / 2 = 150 - среднее значение. То есть в каждую строку с IT в столбце Категория положим значение 150.
data['Категория'] = data['Категория'].map(data.groupby(['Категория'])['таргет2'].mean())
data.head()

#Определяемся с таргетом - либо регрессия (таргет2 - сколько денег соберет), либо классификация (таргет1 - успешен проект или нет)
#Попробуем решить через регрессию, поэтому таргет1 удаляем
data = data.drop('таргет1', axis=1)

#Теперь нужно таблицу разбить на X-большое (выборку с объектами) и на Y-большое (таблицу с ответами) перед обучением модели.
#То есть явно сказать модели где лежат признаки, а где ответы.
X = data.drop('таргет2', axis=1) #в Х кладем всю таблицу, КРОМЕ переменной таргет2
Y = data['таргет2'] #в Y кладем таргет2. В Y теперь есть 2 столбца: 1-й - столбец с цифрами из Х, которые соответствуют значению в Y - 2-й столбец (XY_screenshot.png)

#!!!Теперь нужно научиться строить модель по той выборке, которую получили
#Линейная регрессия
model = LinearRegression()
model.fit(X, Y)

X['Предсказание'] = model.predict(X)
X.head()
#Если вернутся в нашему датасету до того как мы разделили X-сы и Y-ки, увидим, что таргет2 очень сильно изменился в численном значении
#Теперь нужно оценить силу алгоритма, понять может ли она и с какой достоверностью предсказывать

