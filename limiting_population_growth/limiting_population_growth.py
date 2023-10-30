#В Китае уже в течение нескольких лет супружеским парам разрешено иметь только одного ребенка. Однако успех в проведении этой политики
# ограничивается рядом факторов. Одна из проблем в том, что семьи чаще оставляют сыновей, которые могут помочь семье,
# и отсюда все сильнее растет доля мужского населения. Отсюда альтернативная политика в том, что семьям разрешается завести дочь пока не родится сын.
# Мы можем промоделировать эту ситуацию и посмотреть как будет расти численность в таком обществе. Поскольку мы работаем с большой популяцией,
# сразу зададимся тем, что поиск решения будем искать в векторизованном варианте.
#Представим, у нас есть n индивидуумов, назовем их parents, которым мы придаем некоторые равномерно распределенные случайные значения.
# Далее из статистических данных мы знаем долю мужчин (male_portion), и всех индивидуумов, у которых их случайное число меньше male_portion,
# считаем мужчинами и присваиваем значение 1, а у кого выше — женщинами и присваиваем значение 2. Чтобы код было удобнее читать, введем константы
# MALE=1 и FEMALE=2. Наша задача в том, чтобы посмотреть как меняется массив parents для каждого нового поколения при учете двух указанных политик.
# Итак, создаем исходный массив:
from numpy import random, zeros

N = 1000000
male_portion = 0.51
fertility = 0.92
law_breakers = 0.06
wanted_children = 6
n=0
generations = 10
r = random.random(n)
parents = zeros(n, int)  # массив нулей размером n
MALE = 1; FEMALE = 2
parents[r <  male_portion] = MALE
parents[r >= male_portion] = FEMALE

#Число потенциально возможных супружеских пар это минимум от числа мужчин и числа женщин. Однако, даже если мы посчитаем, что все эти пары сложатся,
# то все равно только часть из них дадут детей. При учете политики «одна семья — один ребенок» получаем:
males = len(parents[parents==MALE])  # число мужчин
females = len(parents) - males       # число женщин
couples = min(males, females)        # число потенциальных супружеских пар
n = int(fertility*couples)   # пары, родившие ребенка, fertility - рождаемость

# следующее поколение
r = random.random(n)
children  =  zeros(n, int)
children[r <  male_portion] = MALE
children[r >= male_portion] = FEMALE

#Код, написанный для рождении нового поколения будет нужен при каждой новой генерации.
# Поэтому эти инструкции более естественно заключить в соответствующую функцию:
def get_children(n, male_portion, fertility):
    n = int(fertility*n)
    r = random.random(n)
    children = zeros(n, int)
    children[r <  male_portion] = MALE
    children[r >= male_portion] = FEMALE
    return children

#При условии более мягкой политики, назовем ее «политикой одного сына», родители могут рожать детей, пока у них не появится сын.
# В рамках нашей оценочной задачи будем упрощенно считать, что они так и делают:
# сначала обычное
children = get_children(couples, male_portion, fertility)
# в случае, если дочь:
daughters = children[children == FEMALE]
while len(daughters) > 0:
    new_children = get_children(len(daughters), male_portion, fertility)
    children = str.concatenate((children, new_children))
    daughters = new_children[new_children == FEMALE]

#Накопленный опыт мы можем представить в виде общей функции анализа популяции для обеих политик:
def advance_generation(parents, policy='one child',
                       male_portion=0.5, fertility=1.0,
                       law_breakers=0, wanted_children=4):

    males = len(parents[parents==MALE])
    females = len(parents) - males
    couples = min(males, females)

    if policy == 'one child':
        # у каждой пары только один ребенок:
        children = get_children(couples, male_portion, fertility)
        max_children = 1
    elif policy == 'one son':
        # каждая пара продолжает рожать детей до тех пор, пока у них не будет сына

        children = get_children(couples, male_portion, fertility)
        max_children = 1
        daughters = children[children == FEMALE]
        while len(daughters) > 0:
            new_children = get_children(len(daughters), male_portion, fertility)
            children = concatenate((children, new_children))
            daughters = new_children[new_children == FEMALE]
            max_children += 1

    # кроме того часть граждан нарушает закон и имеет столько детей, сколько хочет (wanted_children)
    illegals = get_children(int(len(children)*law_breakers)*wanted_children, male_portion, fertility=1.0)
    children = concatenate((children, illegals))
    return children, max_children

#Законченная программа с заданием исходных данных тогда будет выглядеть так:
from numpy import random, concatenate, zeros
MALE = 1;  FEMALE = 2

def get_children(n, male_portion, fertility):
    n = int(fertility*n)
    r = random.random(n)
    children = zeros(n, int)
    children[r <  male_portion] = MALE
    children[r >= male_portion] = FEMALE
    return children

def advance_generation(parents, policy='one child',
                       male_portion=0.5, fertility=1.0,
                       law_breakers=0, wanted_children=4):

    males = len(parents[parents==MALE])
    females = len(parents) - males
    couples = min(males, females)

    if policy == 'one child':
        # у каждой пары только один ребенок:
        children = get_children(couples, male_portion, fertility)
        max_children = 1
    elif policy == 'one son':
        # каждая пара продолжает рожать детей до тех пор, пока у них не будет сына

        children = get_children(couples, male_portion, fertility)
        max_children = 1
        daughters = children[children == FEMALE]
        while len(daughters) > 0:
            new_children = get_children(len(daughters), male_portion, fertility)
            children = concatenate((children, new_children))
            daughters = new_children[new_children == FEMALE]
            max_children += 1

    # кроме того часть граждан нарушает закон и имеет столько детей, сколько хочет (wanted_children)
    illegals = get_children(int(len(children)*law_breakers)*wanted_children, male_portion, fertility=1.0)
    children = concatenate((children, illegals))
    return children, max_children

# начнем с "идеального поколения" родителей:
start_parents = get_children(N, male_portion=0.5, fertility=1.0)
parents = start_parents.copy()
print ('one child policy, start: %d' % len(parents))
for i in range(generations):
    parents, mc = advance_generation(parents, 'one child',
                                     male_portion, fertility,
                                     law_breakers, wanted_children)
    print ('%3d: %d' % (i+1, len(parents)))

parents = start_parents.copy()
print ('one son policy, start: %d' % len(parents))
for i in range(generations):
    parents, mc = advance_generation(parents, 'one son',
                                     male_portion, fertility,
                                     law_breakers, wanted_children)
    print ('%3d: %d (max children in a family: %d)' % (i+1, len(parents), mc))