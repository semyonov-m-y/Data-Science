'''
Наивный байесовский классификатор. Формула расчета вероятности отнесения наблюдения к тому или иному классу:
P(c|d) = (P(d|c)P(c)) / P(d)
Например, нужно рассчитать вероятность, что спортивный матч состоится при условии, что погода солнечная. Исходные данные и расчеты приведены в таблице ниже:
Weather  Match not happen  Match happen
Overcast        -               4           =4/14=0.29
Rainy           3               2           =5/14=0.36
Sunny           2               3           =5/14=0.36
All             5               9
                =5/14           =9/14
                0.36            0.64
Можно посчитать по формуле (3/9) * (9/14) / (5/14) = 60%, или просто из здравого смысла 3/(2+3)=60%.
Сильные стороны — легко интерпретировать результат, подходит для больших выборок и мультиклассовой классификации.
Слабые стороны — не всегда выполняется предположение о независимости характеристик, характеристики должны составлять полную группу событий.
'''
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB

#model fit
X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=0)
gnb = GaussianNB()
y_pred = gnb.fit(X_train, y_train).predict(X_test)

#result
print("Number of mislabeled points out of a total %d points : %d" % (X_test.shape[0], (y_test != y_pred).sum()))