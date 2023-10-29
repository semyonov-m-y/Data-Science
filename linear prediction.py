#выполнение модели линейного прогнозирования для полуслучайных данных
import statsmodels.api as sm
import numpy as np

predictors = np.random.random(1000).reshape(500,2) #создание случайных данных для свободных (х) и целевых переменных (у) модели. Прогностические
target = predictors.dot(np.array([0.4,0.6])) + np.random.random(500) #параметры используются для создания целевых значений, чтобы создать корреляцию
lmRegModel = sm.OLS(target,predictors) #подбор линейной регрес-
result = lmRegModel.fit() #сии для данных
print(result.summary()) #вывод статистики соответствия модели
