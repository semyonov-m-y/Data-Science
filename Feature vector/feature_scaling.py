from sklearn.preprocessing import MinMaxScaler
import numpy as np

# Создаем массив с числовыми данными
data = np.array([[1, 10], [2, 20], [3, 30], [4, 40]])

# Создаем экземпляр класса MinMaxScaler
scaler = MinMaxScaler()

# Масштабируем числовые признаки в заданный диапазон (например, [0, 1])
scaled_data = scaler.fit_transform(data)
print(scaled_data)