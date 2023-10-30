#В шляпе 12 шаров: четыре черных, четыре красных и четыре синих. И мы хотим написать программу, которая достает из шляпы три случайных шара.
# Шары у нас отличаются цветом, при этом эти цвета неизменны, значит их удобно представить в виде кортежа, а саму шляпу в качестве списка строк:
colors = 'black', 'red', 'blue'   # (кортеж строк)
hat = []
for color in colors:
    for i in range(4):
        hat.append(color)

#Чтобы достать шар:
import random as random_number
color = random_number.choice(hat)
print (color)

#Но нам нужно достать несколько шаров. При этом мы не возвращаем их обратно в шляпу, а это значит что элементы (шары) удаляются из списка hat.
# Три способа: 1) использовать hat.remove(color), то есть достали, например, синий шар - значит одним синим шаром в списке меньше,
# 2) выбирать шар по случайному индексу, а затем по нему же его удалять через del hat[index], 3) то же самое, но более коротким способом через hat.pop(index):
def draw_ball(hat):
    color = random_number.choice(hat)
    hat.remove(color)
    return color, hat

# или:
def draw_ball(hat):
    index = random_number.randint(0, len(hat)-1)
    color = hat[index]
    del hat[index]
    return color, hat

# или:
def draw_ball(hat):
    index = random_number.randint(0, len(hat)-1)
    color = hat.pop(index)
    return color, hat

n = int(input('How many balls are to be drawn? '))
balls = []
for i in range(n):  # n - число доставаемых шаров
    color, hat = draw_ball(hat)
    balls.append(color)
print ('Got the balls', balls)

#Продлим наше решение на более конкретную задачу, чем просто доставание из шляпы шаров: какова вероятность достать два и более черных шара из этой шляпы.
# В таком случае мы можем проделать N экспериментов и подсчитать сколько M раз мы достали не менее двух черных шаров и найти вероятность такого события как M/N.
# Один эксперимент для нас состоит в создании нового списка hat (перемешивании шаров), доставании шаров и подсчете числа черных.
# Последнее может быть легко подсчитано с помощью метода списков count, то есть в нашем случае hat.count('black').
# Тогда оставим одну понравившуюся нам функцию draw_ball(hat) и допишем нашу программу следующим образом:
import random as random_number

def draw_ball(hat):
    color = random_number.choice(hat)
    hat.remove(color)
    return color, hat

def new_hat():
    colors = 'black', 'red', 'blue'
    hat = []
    for color in colors:
        for i in range(4):
            hat.append(color)
    return hat

N = int(input('How many experiments? '))

M = 0
for e in range(N):
    hat = new_hat()
    balls = []
    for i in range(n):
        color, hat = draw_ball(hat)
        balls.append(color)
    if balls.count('black') >= 2:
        M += 1
print ('Probability:', float(M)/N)