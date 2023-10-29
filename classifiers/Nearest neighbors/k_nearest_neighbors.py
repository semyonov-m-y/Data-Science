#выполнение классификации методом k ближайших соседей для полуслучайных данных
from sklearn import neighbors
from sklearn import metrics
import numpy as np

predictors = np.random.random(1000).reshape(500,2) #создание случайных свободных данных
target = np.around(predictors.dot(np.array([0.4,0.6])) + np.random.random(500)) #и полуслучайных целевых данных на основании свободных
clf = neighbors.KNeighborsClassifier(n_neighbors=10) #классификация по 
knn = clf.fit(predictors,target) #модели 10 случайных соседей
knn.score(predictors,target) #получение метрики соответствия модели: какой процент классификации был правильным?
prediction = knn.predict(predictors)
print(metrics.confusion_matrix(target, prediction))
