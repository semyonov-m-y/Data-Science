'''
Логистическая регрессия/logit. Используется для классификации от 0 до 1, доказывается методом максимального правдоподобия (log likelihood).
ММП — это вероятность получить Y при заданных Х и найденных параметрах w.
P(i)=1/(1+e**-(b(0)+b(1)*x(1,i)+...+b(k)*x(k,i))
Сильные стороны: хорошо работает, когда гиперпараметры коррелируют с объясняющей переменной.
Слабые стороны — подходит для бинарной классификации, слабо работает при эндогенности.
'''
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression

#model fit
X, y = load_iris(return_X_y=True)
clf = LogisticRegression(random_state=0).fit(X, y)
clf.predict(X[:2, :])

#result
print(clf.predict_proba(X[:2, :]))
print(clf.score(X, y))