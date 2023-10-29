#задача классификации изображений на примере распознавания цифр
from sklearn import *
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt

digits = load_digits()
y = digits.target # выбор целевой переменной
n_samples = len(digits.images) #подготовка данных. Метод reshape преобразует матричную форму
X = digits.images.reshape((n_samples, -1)) #данных. Например, он может превратить матрицу 10х10 в 100 векторов
print (X)
x_train, x_test, y_train, y_test = train_test_split(X, y, random_state=0) #разбиение данных на тестовый и тренировочный набор
gnb = GaussianNB() #выбор наивного классификатора Байеса; для оценки вероятности применяется гаусово распределение
fit = gnb.fit(x_train, y_train) #подгонка данных
predicted = fit.predict(x_test) #прогнозирование по незнакомым данным
print(confusion_matrix(y_test, predicted)) #создание матрицы несоответствий

#сравнение прогнозов с реальным числом
images_and_predictions = list(zip(digits.images, fit.predict(X))) #сохранение матрицы изображения и прогноза (в числовом виде) в одном массиве
for index, (image, prediction) in enumerate(images_and_predictions[:6]): #перебор первых 7 изображений
    plt.subplot(6, 3, index + 5) #добавление доп поддиаграммы на сетке 6х3. Можно упростить до plt.subplot(3, 2, index)
    plt.axis('off') #ось не отображается
    plt.imshow(image, cmap = plt.cm.gray_r, interpolation = 'nearest') #изображение выводится в оттенках серого
    plt.title('Prediction: %i' % prediction) #прогнозируемое значение выводится в заголовке изображения
print (plt.show()) #вывод полной диаграммы, состоящей из 6 поддиаграмм
#распознавая неправильно интерпретированные изображения, мы можем продолжить тренировку модели: каждое изображение помечается правильным числом и снова передается модели как новый тренировочный набор. Это повышает точность модели

                          
