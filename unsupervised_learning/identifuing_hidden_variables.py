#выявление скрытых переменных в наборе данных качества вина
#сбор данных и стандартизация переменных
import pandas as pd
from sklearn import preprocessing
from sklearn.decomposition import PCA
import pylab as plt

url = 'http://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv' #загружаем набор данных
data = pd.read_csv(url, sep=";") #чтение данных в формате csv, разделенных ;
X = data[[u'fixed acidity', u'volatile acidity', u'citric acid', u'residual sugar', u'chlorides', u'free sulfur dioxide', u'total sulfur dioxide', u'density', u'pH', u'sulphates', u'alcohol']] #Х - матрица свободных переменных, которыми тут являются свойства вина (плотность, содержание алкоголя...)
y = data.quality #у - вектор, представляющий целевую переменную
X = preprocessing.StandardScaler().fit(X).transform(X) #при стандартизации данных к каждой точке применяется следующая формула: z=(x-m)/q, где z - новое наблюдаемое значение, х - старое, m - мат ожидание, q - стандартное отклонение. Результаты РСА для матрицы  
print (X)

#проведение анализа главных компонент
model = PCA() #создание экземпляра класса анализа главных компонент
results = model.fit(X) #применение РСА к свободным переменным для поиска возможности свертки их в меньшее количество переменных
Z = results.transform(X) #результат преобразуется в массив для использования вновь созданных данных
plt.plot(results.explained_variance_) #график объяснимой дисперсии переменных;в данном случае используется график каменистой осыпи
print (plt.show()) #отображение графика

#вывод компонент РСА во фрейме данных Pandas
print(pd.DataFrame(results.components_, columns=list([u'fixed acidity', u'volatile acidity', u'citric acid', u'residual sugar', u'chlorides', u'free sulfur dioxide', u'total sulfur dioxide', u'density', u'pH', u'sulphates', u'alcohol'])))
#строки полученной таблицы описывают математическую корреляцию