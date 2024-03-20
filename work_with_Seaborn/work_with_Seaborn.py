'''
Seaborn - это расширение Matplotlib с дополнительными возможностями.
Что можно делать с помощью Seaborn?
1. Определять отношения между несколькими переменными (корреляция)
2. Соблюдать качественные переменные для агрегированных статистических данных;
3. Анализировать одномерные или двумерные распределения и сравнивать их между различными подмножествами данных;
4. Построить модели линейной регрессии для зависимых переменных;
5. Обеспечить многоуровневые абстракции, многосюжетные сетки.
Для визуализации распределения метрических переменных используются следующие типы графиков:
distplot
jointplot
rugplot
kdeplot
Можно таже визуализировать относительные распределения между парами переменных при помощи методов:
PairGrid
pairplot
FacetGrid
'''
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

tips = sns.load_dataset('tips')
tips.head()

#distplot одновременно показывает гистограмму и график плотности распределения.
sns.displot(tips['total_bill'])
#Можно оставить только гистограмму:
sns.displot(tips['total_bill'], kde=False, bins=30)
''''
Функция jointplot() показывает совместное распределение по двум переменным. Она имеет параметр kind который может 
принимать следующие значения:
“scatter”
“reg”
“resid”
“kde”
“hex”
'''
sns.jointplot(x='total_bill', y='tip', data=tips, kind='scatter')
sns.jointplot(x='total_bill',y='tip',data=tips,kind='hex')
sns.jointplot(x='total_bill', y='tip', data=tips, kind='reg')

#pairplot показывает отношения между всеми парами переменных.
sns.pairplot(tips)

sns.pairplot(tips, hue='sex', palette='Set1')

#По сути pairplot — это упрощённая версия другой функции, которая называется PairGrid.
sns.PairGrid(tips)

g = sns.PairGrid(tips)
g.map(plt.scatter)

g = sns.PairGrid(tips)
g.map_diag(plt.hist)
g.map_upper(plt.scatter)
g.map_lower(sns.kdeplot)

#Плотность распределения по двум переменным даёт нам градиент. Градиент — вектор, своим направлением указывающий
# направление наибольшего возрастания некоторой величины φ, значение которой меняется от одной точки пространства к
# другой (скалярного поля), а по величине (модулю) равный скорости роста этой величины в этом направлении.
sns.kdeplot(data=tips, y="total_bill")

#Facet Grid позволяет визуализировать совместное распределение отдельных признаков нескольких переменных.
g = sns.FacetGrid(tips, col="time", row="smoker")

g = sns.FacetGrid(tips, col="time", row="smoker")
g = g.map(plt.hist, "total_bill")

g = sns.FacetGrid(tips, col="time", row="smoker", hue='sex')
g = g.map(plt.scatter, "total_bill", "tip").add_legend()

#rugplot показывает то же, что и график плотности распределения, только в одномерной форме. Чем плотнее расположены линии,
# тем выше плотность. Лучше использовать его совместно с другими видами графиков.
sns.kdeplot(tips['tip'])
sns.rugplot(tips['tip'])

''''
Визуализация категориальных данных
В seaborn встроены функции для визуализации категориальных данных в следующих форматах:
factorplot
boxplot
violinplot
stripplot
swarmplot
barplot
countplot
В качестве тестового набора данных возьмём данные о чаевых, которые поставляются вместе с seaborn:

barplot
Первый тип визуализации — это barplot. У нас есть категориальная переменная и её цифровое значение. 
Барплот аггрегирует данные по значениям категориальной переменной и применяет определённую функцию к значениям 
соответсвующих групп цифровой переменной. По умолчанию эта функция — среднее.
'''
sns.barplot(x='sex', y='total_bill', data=tips)

#Эту функцию можно изменить в аргументе estimator:
sns.barplot(x='sex', y='total_bill', data=tips, estimator=len)
sns.countplot(x='sex', data=tips)
''''
Здесь мы считаем стандартное отклоенение.

countplot
То же самое, что и барплот, только функция уже явно задана, и она считает количество значений в каждой категории.
'''
sns.countplot(x='sex', data=tips)

''''
boxplot и violinplot
Эти два графика используются для изучения формы распределения.

boxplot
Другое название boxplot — ящик с усами или диаграмма размаха. Он был разработан Джоном Тьюки в 1970-х годах.

Такой вид диаграммы в удобной форме показывает медиану (или, если нужно, среднее), нижний и верхний квартили, 
минимальное и максимальное значение выборки и выбросы. Несколько таких ящиков можно нарисовать бок о бок, чтобы 
визуально сравнивать одно распределение с другим; их можно располагать как горизонтально, так и вертикально. 
Расстояния между различными частями ящика позволяют определить степень разброса (дисперсии) и асимметрии данных и выявить выбросы.
'''
sns.boxplot(x="day", y="total_bill", data=tips, palette='rainbow', hue='sex')

sns.boxplot(data=tips, palette='rainbow', orient='h')

#Можно ввести в график третье измерение:
sns.boxplot(
    x="day", y="total_bill", hue="smoker", data=tips, palette="coolwarm")

#violinplot
#Выполняет ту же функцию, что и boxplot. По сути это два повёрнутые на 90 и -90 градусов графика плотности распределения,
# слипшиеся друг с другом.
sns.violinplot(x="day", y="total_bill", data=tips, palette='rainbow', hue='sex')

sns.violinplot(x="day", y="total_bill", data=tips, hue='sex', palette='Set1')

sns.violinplot(
    x="day", y="total_bill", data=tips, hue='sex', split=True, palette='Set1')

''''
stripplot и swarmplot
stripplot рисует диаграмму рассеяния, состоящую из одной категориальной переменной. Его можно использовать как 
самостоятельную фигуру, но лучше сочетать с другими графиками.
'''
sns.stripplot(x="day", y="total_bill", data=tips)

sns.stripplot(x="day", y="total_bill", data=tips, jitter=True)

sns.stripplot(
    x="day", y="total_bill", data=tips, jitter=True, hue='sex', palette='Set1')

sns.stripplot(
    x="day",
    y="total_bill",
    data=tips,
    jitter=True,
    hue='sex',
    palette='Set1',
    dodge=True)  # раньше назывался split

#Swarmplot представляет собой ровно то же самое, с той лишь разницей, что точки не накладываются друг на друга.
sns.swarmplot(
    x="day", y="total_bill", hue='sex', data=tips, palette="Set1", dodge=True)

#Как говорилась ранее, эти типы графиков можно комбинировать с другими. Лучше всего это делать с violinplot.
sns.violinplot(x="tip", y="day", data=tips, palette='rainbow', hue='sex')
sns.swarmplot(x="tip", y="day", data=tips, color='black', size=3)
''''
catplot (ранее factorplot)
Из документации: The default plot that is shown is a point plot, but other seaborn categorical plots can be chosen with 
the kind parameter, including box plots, violin plots, bar plots, or strip plots.
'''
sns.catplot(x='sex', y='total_bill', data=tips, kind='bar')
plt.show()
'''
#Матричные графики
#Тепловая карта
float(tips.corr())

sns.heatmap(tips.corr())
sns.heatmap(tips.corr(),cmap='coolwarm',annot=True)

#Загрузим данные о полётах:
flights = sns.load_dataset('flights')
flights.head()

#Посчитаем таблицу сопряжённости, которая покажет, какое количество пассажиров летало в различные месяцы в каждый из
# годов в промежутке от 1949 по 1960.
flights.pivot_table(values='passengers', index='month', columns='year')

pvflights = flights.pivot_table(
    values='passengers', index='month', columns='year')
sns.heatmap(pvflights)

sns.heatmap(pvflights,cmap='magma',linecolor='white',linewidths=1)

#clustermap
#Использует алгоритмы иерархической кластеризации для создания визуализации. Можно задавать различные методы кластеризации.
sns.clustermap(pvflights)

#Стили графиков
sns.countplot(x='sex', data=tips)

sns.set_style('whitegrid')  # Другие значения: darkgrid, whitegrid, dark, white, ticks
sns.countplot(x='sex', data=tips)

sns.set_style("ticks", {"xtick.major.size": 18, "ytick.major.size": 18})
sns.countplot(x='sex', data=tips)

#Все переметры стиля можно посмотреть следующим образом:
sns.axes_style()

#Если необходимо применить стиль только к одному графику, для этого следует использовать менеджер контекста with
with sns.axes_style("dark"):
    sns.countplot(x='sex', data=tips)

#Можно удалить линии осей при помощи метода despine
sns.countplot(x='sex',data=tips)
sns.despine(left=True)

#Размеры задаются так же, как и в обычном matplotlib.
plt.figure(figsize=(12, 3))
sns.countplot(x='sex', data=tips)

sns.lmplot(x='total_bill', y='tip', size=4, aspect=2, data=tips)

#Использование Seaborn совместно с matplotlib
fig, ax = plt.subplots()
sns.regplot("tip", "total_bill", data=tips, ax=ax)
ax.set_title("Заголовок")
plt.xlabel('Чаевые')
fig.savefig("filename.png", dpi=200)
'''
