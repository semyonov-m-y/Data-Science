from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

# Создаем массив с текстовыми данными
data = np.array(['I love Python', 'Python is a great language'])

# Создаем экземпляр класса CountVectorizer
vectorizer = CountVectorizer()

# Токенизируем текстовые данные
tokenized_data = vectorizer.fit_transform(data)
print(tokenized_data)