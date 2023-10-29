import pandas as pd
from sklearn.preprocessing import OneHotEncoder

# Создаем датафрейм с категориальными данными
data = pd.DataFrame({'color': ['red', 'green', 'blue', 'yellow']})

# Создаем экземпляр класса OneHotEncoder
encoder = OneHotEncoder()

# Преобразуем категориальные признаки в бинарные векторы
encoded_data = encoder.fit_transform(data[['color']])
print(encoded_data)