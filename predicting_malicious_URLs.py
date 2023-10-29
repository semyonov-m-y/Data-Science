"""
#эмулируем ошибку при попытке загрузки большого объема данных в память
import glob
from sklearn.datasets import load_svmlight_file

files = glob.glob('C:\python-3.12.0rc1-embed-amd64\example\data science\Predicting malicious URLs\url_svmlight\*.svm') #tar файл необходимо предварительно распаковать
print ("there are %d files" % len(files)) #выводим количество файлов
X,y = load_svmlight_file(files[0], n_features=3231952) #загрузка файлов
X.todense() #данные представляют собой большую, но разреженную матрицу. Преобразование их в плотную матрицу (каждый 0 представлен в файле) приводит к ошибке нехватки памяти

Ошибка произошла при загрузке уже 1-го файла. Чтобы решить проблему, можно:
1) использовать разреженное представление данных
2) передать алгоритму сжатые данные вместо необработанных
3) применить онлайновый алгоритм для прогнозирования
Этап подготовки и очистки данных в данном случае не нужен, тк урл-адреса проходят предварительную очистку

Чтобы понять, можно ли применить 1), необходимо выяснить, действительно ли данные содержат много нулей:
print ("number of non-zero entries %2.6f" % float ((X.noz)/(float(X.shape[0])*float(X.shape[1])))
Результат = 0.000033
Данные, содержащие минимум полезной информации по сравнению с нулями называются РАЗРЕЖЕННЫМИ. Такие данные можно хранить более компактно, если использовать формат [(0,0,1),(4,4,1)] вместо [[1,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,1]]
В SVMLight этот принцип реализован

Чтобы применить 2), нужно понять размер файлов, передав процессору сжатые файлы tar.gz (архив). Файл распаковывается без записи на диск только в нужный момент.
"""
#определение размера данных
import tarfile
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import classification_report
from sklearn.datasets import load_svmlight_file
import numpy as np

uri = "C:/python-3.12.0rc1-embed-amd64/example/data science/Predicting malicious URLs/url_svmlight.tar.gz"
tar = tarfile.open(uri, "r:gz")
max_obs = 0 #количество наблюдений
max_vars = 0 #количество показателей
i = 0 #счетчик файлов
split = 5 #для демонстрации обработаем лишь первые 5 файлов
for tarinfo in tar: #все файлы весят около 2 ГБ. Нужно, чтобы файлы оставались сжатыми в памяти и распаковывалась только та часть, которая необходима для работы
    print("extracting %s,f size %s" % (tarinfo.name, tarinfo.size))
    if tarinfo.isfile():
          f = tar.extractfile(tarinfo.name) #файлы распаковываются по одному для сокращения необходимой памяти
          X,y = load_svmlight_file(f) #для загрузки конкретного файла используется вспомогательная функция load_svmlight_file()
          #обновление максимального количества наблюдений и переменных
          max_vars = np.maximum(max_vars, X.shape[0])
          max_obs = np.maximum(max_obs, X.shape[1])
    if i > split:
          break #при достижении 5-го файла останавливаем процесс
    i += 1
    print ("max X = %s, max y dimension = %s" % (max_obs, max_vars))

#теперь можно использовать сразу 1),2),3) приемы
classes = [-1,1] #целевая переменная может равняться 1 - сайт безопасен и -1 - сайт опасен
sgd = SGDClassifier(loss='log_loss') #создание стохастического градиентного классификатора
n_features=3231952 #количество показателей известно из исследования данных
split = 5
i = 0
for tarinfo in tar:
    if i > split:
        break
    if tarinfo.isfile():
        f = tar.extractfile(tarinfo.name)
        X,y = load_svmlight_file(f, n_features = n_features)
        if i < split:
            sgd.partial_fit(X, y, classes=classes) #онлайновый алгоритм. Точки данных могут передваться ему файл за файлом (пакетами)
        if i == split:
            print (classification_report(sgd.predict(X), y))
        i += 1
#при повторном прогоне кода результат может быть другим, потому что алгоритмы могут сходиться иначе
