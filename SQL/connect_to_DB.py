import pymysql.cursors
import random

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

  finally:
    connect.close()

rand = random.randint(-2147483648, 2147483648)

print('logged')