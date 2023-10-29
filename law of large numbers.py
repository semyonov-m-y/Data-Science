#Закон больших чисел (ЗБЧ) говорит, что при увеличении количества попыток случайная величина стремится к своему математическому ожиданию — всё усредняется.
import random
import matplotlib.pyplot as plt


total_flips = 0
numerical_probability = []
H_count = 0

for i in range(0,5000):
    new_flip = random.choices(['H', 'T'], weights=[0.5, 0.5])
    total_flips = total_flips + 1
    if new_flip == ['H']: # внимание: функция choices возвращает список, а не строку ‘H’ или ‘T’!
         H_count = H_count + 1
         numerical_probability.append(H_count/total_flips)
         
# рисуем график
plt.plot(numerical_probability)
print(plt.xlabel("Количество бросков"))
print(plt.ylabel("Численная вероятность"))
