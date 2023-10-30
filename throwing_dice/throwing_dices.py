#Пусть у нас спрашивают: какова вероятность при броске костей, чтобы по крайне мере на двух из них были шестерки? Итак, эксперимент в том,
# что кидаются четыре кости, нужное событие - не менее двух кубиков с шестью точками. Собственно, это нам и нужно записать еще раз перефразировав на Python:

import random as random_number
import numpy as np

N = int(input('Enter number of experiments: '))
M = 0
for i in range(N):
    six = 0
    r1 = random_number.randint(1, 6)
    if r1 == 6:
        six += 1
    r2 = random_number.randint(1, 6)
    if r2 == 6:
        six += 1
    r3 = random_number.randint(1, 6)
    if r3 == 6:
        six += 1
    r4 = random_number.randint(1, 6)
    if r4 == 6:
        six += 1
    if six >= 2:
        M += 1

p = float(M)/N
print('probability:', p)

#Более общая задача — ведь мы можем задать и не только число экспериментов, а, например, число бросаемых костей (ndice) и минимальное число одинаковых
# кубиков (nsix). Таким образом, мы получаем более общий и даже более короткий код, а более общие решения гораздо проще модифицировать далее:
import random as random_number
import sys

N = int(input('Number of experiments: '))
ndice = int(input('Number of dice: '))
nsix = int(input('Number of dice with six eyes: '))
M = 0
for i in range(N):
    six =0
    for j in range(ndice):
        r = random_number.randint(1, 6)
        if r == 6:
            six += 1
    if six >= nsix:
        M += 1

p = float(M)/N
print ('Probability:', p)

#Для малых вероятностей число M мало и аппроксимация M/N не очень хорошая аппроксимация, требуется большое число экспериментов,
# которые для стандартного модуля обходятся дорого, то есть долго. Конечно же, мы знаем, что при нехватке скорости надо перейти к более
# быстрым векторным операциям. Векторизация состоит в том, что мы создаем двухмерный массив случайных чисел, в котором число строк определяется
# числом экспериментов (бросков), а число столбцов — числом испытаний (костей):
eyes = np.random.randint(1, 6, (N, ndice))

#Следующий шаг — посчитать число нужных нам событий в каждом эксперименте. Для того, чтобы программа работала быстрее мы должны постараться избежать циклов.
# В предыдущем уроке мы использовали прием создания массива по выполнению условия, этот же прием мы используем ниже. Далее в полученном массиве суммируем
# элементы строк, а это нули и единицы, и в случае если число единиц равно или больше требуемому числу шестерок, то считаем, что событие произошло:
from numpy import random, sum

N = int(input('Number of experiments: '))
ndice = int(input('Number of dice: '))
nsix = int(input('Number of dice with six eyes: '))

eyes = random.randint(1, 6, (N, ndice))
compare = eyes == 6
nthrows_with_6 = sum(compare, axis=1)  # суммирование по столбцам - элементам строки (axis = 1)
nsuccesses = nthrows_with_6 >= nsix
M = sum(nsuccesses)
p = float(M)/N
print ('probability:', p)

#И подсчет при этом для большого числа экспериментов, происходит существенно быстрее.