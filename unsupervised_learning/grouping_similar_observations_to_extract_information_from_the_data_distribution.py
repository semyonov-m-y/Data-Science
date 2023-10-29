#группировка сходных наблюдений для извлечения информации из распределения данных
#классификация ирисов (цветы)
import sklearn
from sklearn import cluster
import pandas as pd
from sklearn.datasets import load_iris

data = sklearn.datasets.load_iris() #загрузка данных с информацией об ирисах из scikit-learn
X = pd.DataFrame(data.data, columns = list(data.feature_names)) #данные ирисов преобразуются во фрейм данных pandas
print (X[:5]) #выводим первые 5 - видны длина и ширина чашечки, длина и ширина лепестка
model = cluster.KMeans(n_clusters=3, random_state=25) #инициализация кластерной модели k-средних с 3 кластерами. Значение random_state определяет случайную затравку; если не указать, тоже будет случайная. 3 кластера так как обеспечивает компромис между сложностью и быстродействием
results = model.fit(X) #подгонка модели по данным. Все переменные считаются независимыми;в неконтролируемом обучении нет целевой переменной (y)
X["cluster"] = results.predict(X) #во фрейм данных включается новая переменная с именем "cluster". В ней для каждого цвета хранится информация о принадлежности его к кластеру
X["target"] = data.target #во фрейм данных добавляется целевая переменная (y)
X["c"] = "lookatmeIamimportant" #добавляем переменную с - трюк для упрощения подсчета
print(X[:5])
classification_result = X[["cluster", "target", "c"]].groupby(["cluster", "target"]).agg("count") #выбираем столбцы cluster, target и с. Потом группируем по столбцам cluster и target. Наконец, строка группы вычисляется простым подсчетом
print (classification_result) #матрица, представляющая этот результат классификации, позволяет увидеть, насколько успешно прошла кластеризация. В кластерах 1 и 2 встречается путаница, но в общем мы получаем всего 16 (14 + 2) неверных классификаций из 150
