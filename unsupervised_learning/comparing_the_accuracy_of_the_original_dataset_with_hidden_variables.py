#сравнение точности исходного набора данных со скрытыми переменными
#прогнозирование качества вина до применения анализа главных компонент
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import preprocessing
from sklearn.decomposition import PCA

url = 'http://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv' #загружаем набор данных
data = pd.read_csv(url, sep=";") #чтение данных в формате csv, разделенных ;
X = data[[u'fixed acidity', u'volatile acidity', u'citric acid', u'residual sugar', u'chlorides', u'free sulfur dioxide', u'total sulfur dioxide', u'density', u'pH', u'sulphates', u'alcohol']] #Х - матрица свободных переменных, которыми тут являются свойства вина (плотность, содержание алкоголя...)
y = data.quality #у - вектор, представляющий целевую переменную
X = preprocessing.StandardScaler().fit(X).transform(X) #при стандартизации данных к каждой точке применяется следующая формула: z=(x-m)/q, где z - новое наблюдаемое значение, х - старое, m - мат ожидание, q - стандартное отклонение. Результаты РСА для матрицы
gnb = GaussianNB() #для оценки используется наивный классификатор Байеса с гауссовым распределением
fit = gnb.fit(X,y) #подгонка данных
pred = fit.predict(X) #прогнозирование для неизвестных данных
print (confusion_matrix(pred, y)) #изучение матрицы несоответствий
print (confusion_matrix(pred, y).trace()) #подсчет правильно классифицированных случаев: после проверки марицы несоответствий суммируеются все элементы диагонали (следа матрицы)
#видно, что наивный классификатор Байеса выдает 897 правильных прогнозов из 1599


#прогнозирование качества вина с наращиванием количества главных компонент
predicted_correct = [] #массив будет заполнен правильно спрогнозированными наблюдениями
for i in range(1,10): #перебор первых 10 обнаруженных главных компонент
    model = PCA(n_components = i) #создание экземпляра модели РСА с разным количеством компонентов, от 1 (1-я итерация) до 10 (10-я итерация)
    results = model.fit(X) #подгонка модели РСА по х-переменным (показателям)
    Z = results.transform(X) #Z содержит результат в форме матрицы (на самом деле массив, заполненный другими массивами)
    fit = gnb.fit(Z,y) #применение наивного классификатора Байеса с гауссовым распределением для оценки
    pred = fit.predict(Z) #прогнозирование с использованием подобранной модели
    predicted_correct.append(confusion_matrix(pred,y).trace()) #в конце каждой итерации добавляется количество правильно классифицированных наблюдений
    print (predicted_correct) #массив с добавлением в каждой итерации правильно классифицированных наблюдений
plt.plot(predicted_correct) #строим график
print (plt.show()) #выводим его
#видно, что всего с тремя скрытыми переменными классификатор лучше справляется с прогнозированием качества вина, чем с 11 исходными и что свыше 5 скрытых переменных и не нужно.
    
