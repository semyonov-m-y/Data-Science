'''
1) Чтобы в Python работать с MySQL, нужно выполнить pip install pymysql
2)Если в MySQL возникает ошибка Unable to excute command chcp, то:
To resolve this problem on 64 bit system we have to follow two steps.
add environment variable path to C:\Windows\System32
we need chcp.com cmd file in C:\Windows\SysWOW64 copy it from C:\Windows\System32 path and paste in C:\Windows\SysWOW64
now close mysql workbench and reopen it.
'''

import pandas as pd
import pymysql
import pymysql.cursors
import random

#pmsql = pymysql.install_as_MySQLdb()
#сначала создаем подключение: укажите свои логин и пароль и имя схемы (переменная database)
connection = 0

def connection():
  connection = pymysql.connect(host='localhost', user='root', password='root', db='testbase', cursorclass=pymysql.cursors.DictCursor)
  return connection

def register(user_id):
  connect = connection()
  try:
    with connect.cursor() as cursor:
      result = cursor.execute(f'SELECT * FROM accounts WHERE uid={user_id}')
      if result == 0:
        cursor.execute(f'INSERT INTO accounts(uid) VALUES({user_id})')
        connect.commit()
        return 'Вы успешно зарегистрировались'

      else:
        return 'Вы уже зарегистрированны'


rand = random.randint(-2147483648, 2147483648)

print('logged')
#затем создается фиктивная база данных с клиентами и несколькими наблюдениями
nr_customers = 100
colnames = ["movie%d" %i for i in range(1, 33)]
pd.np.random.seed(2015)
generated_customers = pd.np.random.randint(0, 2, 32 * nr_customers).reshape(nr_customers, 32)
#данные сохраняются во фрейме данных Pandas, а фрейм данных сохраняется в таблице MySQL с именем cust. Если таблица уже существует, она заменяется
data = pd.DataFrame(generated_customers, columns = list(colnames))
data.to_sql('cust', connection, flavor = 'mysql', index = True, if_exists = 'replace', index_label = 'cust_id')
'''
Строка строится конкатенацией нулей (0) и единиц (1), указывающих, смотрел клиент тот или иной фильм или нет. Затем последовательность интерпретируется 
как числовое значение. Пример: двоичное число 0011 эквивалентно 3. Функция createNum() берет 8  значений, сцепляет их и преобразует в строку,
после чего преобразует двоичное представление строки в число.
'''
def createNum(x1, x2, x3, x4, x5, x6, x7, x8):
  return [int('%d%d%d%d%d%d%d%d' % (i1, i2, i3, i4, i5, i6, i7, i8), 2) for (i1, i2, i3, i4, i5, i6, i7, i8) in zip(x1, x2, x3, x4, x5, x6, x7, x8)]

#Тестирование правильности работы функции. Двоичный код 1111 эквивалентен 15 (=1*8+1*4+1*2+1*1).
#Если условие assert ложно, инициируется ошибка; в противном случае не происходит ничего
assert int('1111', 2) == 15
assert int('1100', 2) == 12
assert createNum([1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 1], [1, 0], [1, 0]) == [255, 252]

#Столбцы преобразуются в 4 битовые строки в числовой форме. Каждая битовая строка представляет 8 фильмов, 4*8=32 фильма.
#Примечание: для сокращения длины кода можно использовать 32-разрядную строку вместо 4*8.
store = pd.DataFrame()
store['bit1'] = createNum(data.movie1, data.movie2, data.movie3, data.movie4, data.movie5, data.movie6, data.movie7, data.movie8)
store['bit2'] = createNum(data.movie9, data.movie10, data.movie11, data.movie12, data.movie13, data.movie14, data.movie15, data.movie16)
store['bit3'] = createNum(data.movie17, data.movie18, data.movie19, data.movie20, data.movie21, data.movie22, data.movie23, data.movie24)
store['bit4'] = createNum(data.movie25,data.movie26, data.movie27, data.movie28, data.movie29, data.movie30, data.movie31, data.movie32)

#Определение хеш-функции (она очень похожа на функцию createNum(), только без завершающего преобразования в число и с 3 столбцами вместо 8)
def hash_fn(x1, x2, x3):
  return [b'%d%d%d' % (i, j, k) for (i, j, k) in zip(x1, x2, x3)]
#Тестирование функции (если обходится без ошибок, значит, функция работает). Используется лишь часть столбцов, но выбираются все наблюдения.
assert hash_fn([1, 0], [1, 1], [0, 0]) == [b'110', b'010']

store['bucket1'] = hash_fn(data.movie10, data.movie15, data.movie28)
store['bucket2'] = hash_fn(data.movie7, data.movie18, data.movie22)
store['bucket3'] = hash_fn(data.movie16, data.movie19, data.movie30)
#Сохранение информации в базе данных.
store.to_sql('movie_comparison', connection, flavor='mysql', index=True, index_label='cust_id', if_exists='replace')

#Определение функции упрощает создание индексов.Индексы ускоряют выборку данных.
def createIndex(column, cursor):
  sql = 'CREATE INDEX %s ON movie_comparison (%s);' % (column, column)
  cursor.execute(sql)

#Создание индексов по гнездам.
cursor = connection.cursor()
createIndex('bucket1', cursor)
createIndex('bucket2', cursor)
createIndex('bucket3', cursor)

#Определение функции. Функции получает 8 входных аргументов: 4 строки длины 8 для первого клиента и еще 4 строки длины 8 для второго клиента. Это позволяет
# провести параллельное сравнение 2 клиентов по 32 фильмам.
Sql = '''CREATE FUNCTION HAMMINGDISTANCE(A0 BIGINT, A1 BIGINT, A2 BIGINT, A3 BIGINT, B0 BIGINT, B1 BIGINT, B2 BIGINT, B3 BIGINT)
RETURNS INT DETERMINISTIC RETURN BIT_COUNT(A0 ^ B0) + BIT_COUNT(A1 ^ B1) + BIT_COUNT(A2 ^ B2) + BIT_COUNT(A3 ^ B3); '''

#Функция сохраняется в базе данных. Этот код может быть выполнен только один раз; при попытке повторного выполнения выдаетсяошибка: OperationalError: (1304,'FUNCTION HAMMINGDISTANCE already exists').
cursor.execute(Sql)

#Чтобы проверить эту функцию, необходимо выполнить эту команду SQL с 8 фиксированными строками. Обратите внимание на префикс "b" перед каждой строкой — это
# признак двоичных значений. Этот конкретный тест должен вернуть 3; результат означает, что строки различаются только в 3 местах.
Sql = '''Select hammingdistance(b'11111111',b'00000000',b'11011111',b'11111111',b'11111111',b'10001001',b'11011111',b'11111111')'''

pd.read_sql(Sql,connection)

customer_id = 27
sql = "select * from movie_comparison where cust_id = %s" % customer_id
cust_data = pd.read_sql(sql,connection)
'''
Мы проведем двухфазный отбор. В первой фазе выбираются клиенты, индекс которых точно совпадает с индексом выбранного клиента (проверка основана
на 9 фильмах.) Выбираемые клиенты видели (или не видели) те же 9 фильмов, что и наш клиент. Второй отбор представляет собой ранжирование, основанное
на 4-битовых строках. В нем учитываются все фильмы в базе данных.
'''
sql =  """ select cust_id,hammingdistance(bit1,bit2,bit3,bit4,%s,%s,%s,%s) as distance from movie_comparison where bucket1 = '%s' or bucket2 ='%s'
or bucket3='%s' order by distance limit 3""" %(cust_data.bit1[0],cust_data.bit2[0],cust_data.bit3[0], cust_data.bit4[0],
cust_data.bucket1[0], cust_data.bucket2[0],cust_data.bucket3[0])

#Вывод 3 клиентов, самых близких к клиенту 27. В начале списка находится сам клиент 27
shortlist = pd.read_sql(sql,connection)

#Выбор фильмов, которые видели клиенты 27, 2 и 97.
cust = pd.read_sql('select * from cust where cust_id in (27,2,97)',mc)
#Транспонирование для удобства.
dif = cust.T
#Выбор фильмов, которые клиент 27 еще не видел.
dif[dif[0] != dif[1]]

connect = connection()
connect.close()