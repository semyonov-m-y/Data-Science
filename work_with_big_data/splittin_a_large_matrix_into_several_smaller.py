#разбиение большой матрицы на несколько меньших
#вычисления с блочными матрицами с использованием библиотек bcolz и Dask
import dask.array as da
import bcolz as bc
import numpy as np
import dask

n = 1e4 #количество наблюдений (в экспоненциальной записи): 1е4 = 10000
n2 = int(n/2)
#создание фиктивных данных: np.arange(n).reshape(n/2, 2) создает матрицу 5000 на 2 (потому что n = 10000). bc.carray = numpy - расширение массива, которое может выгружаться на диск. Данные на нем хранятся в сжатом виде.
#rootdfr = 'ar.bcolz' - создается файл на диске при нехватке оперативной памяти. В файловой системе будет рядом с файлом fpython или в каталоге из которого запускали код. mode = 'w' - режим записи. dtype = 'float64' - храним в виде вещественного числа
ar = bc.carray(np.arange(n).reshape(n2, 2), dtype = 'float64', rootdir = 'ar.bcolz', mode = 'w')
y = bc.carray(np.arange(n2), dtype = 'float64', rootdir = 'yy.bcolz', mode = 'w')
#блочные матрицы создаются для свободных (ar) и целевых (у) переменных - это матрица разделенная на блоки. da.from_array() читает данные с диска или из оперативной памяти (в зависимости от того, где они сейчас находятся)
#chunks=(5,5): каждый блок является матрицей 5х5 (кроме ситуации, когда осталось менее 5 наблюдений или переменных)
dax = da.from_array(ar, chunks = (5, 5))
dy = da.from_array(y, chunks = (5, 5))
#ХТХ определяется как произведение матрицы на её транспонированную версию. Это структурный элемент формулы для вычислений линейной регрессии средствами матричного исчисления
XTX = dax.T.dot(dax)
#Ху - вектор у, умноженный на транспонированную матрицу Х. И снова матрица только определяется, но еще не вычисляется. Это еще один структурный элемент формулы для вычисления линейной регрессии сердствами матричного исчисления
Xy = dax.T.dot(dy)
#коэффициенты вычисляются с использованием матричной функции линейной регрессии. np.linalg.inv() в этой функции представляет ^(-1), или инвертированную матрицу. X.dot(y) - матрица Х умножается на матрицу у
coefficients = np.linalg.inv(XTX.compute()).dot(Xy.compute())
#коэффициенты также помещаются в блочную матрицу. Мы получили массив numpy на предыдущем шаге, и теперь его необходимо явно преобразовать обратно в "массив da"
coef = da.from_array(coefficients, chunks = (5, 5))
#сброс данным в памяти. Хранить большие матрицы в памяти уже не нужно
ar.flush()
y.flush()
#вычисление прогноза
predictions = dax.dot(coef).compute()
print (predictions)
