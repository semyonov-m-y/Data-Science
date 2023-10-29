#Задача предобработки данных для моделей
from pyspark.sql import SparkSession
import pyspark.sql.functions as f
from pyspark.ml.feature import HashingTF, IDF, Tokenizer
from pyspark.ml.feature import Word2Vec
from pyspark.ml.feature import CountVectorizer

#Создаем спарк-сессию
spark = SparkSession.builder.master("local[*]").appName('testForNTA').getOrCreate()

#Возьмем данные с соревнования по определению тональности текстов. Загружаем датасет
df = spark.read.format('csv').option('header', True).load('test.csv') #первая строка рассматривается как заголовок
#Для переименования столбца можем сделать его select, выделить нужный столбец и сопоставить нужный alias
# (Alias (с англ. — «псевдоним») — это имя, назначенное источнику данных в запросе при использовании выражения в качестве источника данных или для упрощения
# ввода и прочтения инструкции SQL). Переименуем столбец description_x в text
df = df.select(f.col('description_x').alias('text'))
df.show(5, vertical = True)
'''
1) Для начала рассмотрим разбивку на токены и TF-IDF (TF-IDF (от англ. TF — term frequency, IDF — inverse document frequency) — 
статистическая мера, используемая для оценки важности слова в контексте документа, являющегося частью коллекции документов или корпуса. 
Вес некоторого слова пропорционален частоте употребления этого слова в документе и обратно пропорционален частоте употребления слова во всех документах коллекции.
Мера TF-IDF часто используется в задачах анализа текстов и информационного поиска, например, как один из критериев релевантности документа поисковому запросу, 
при расчёте меры близости документов при кластеризации.)
Начинаем с набора предложений. Разбиваем каждое предложение на слова, используя Tokenizer. Для каждого предложения (набора слов) используем HashingTF-хеширование
преложения в вектор признаков. Мы используем IDF для масштабирования векторов признаков; это обычно повышает производительность при использовании текста в качестве
функции. Затем наши векторы признаков можно было бы передать алгоритму обучения.
Разобьем наш текст на отдельные токены и запишем их в столбец text_words. В Tokenizer передаем столбец входных данных и название результирующего столбца.
Далее с помощью transform модифицируем наши данные
'''
print('1) Tokens and TF-IDF')
tokenizer = Tokenizer(inputCol = 'text', outputCol = 'text_words')
data_words = tokenizer.transform(df)
#По-хорошему, надо было бы удалить ненужные символы, но не делали
#Используем хеширование, для масштабирования используем IDF
hash_tf = HashingTF(inputCol = 'text_words', outputCol = 'text_words_features', numFeatures = 20)
data_featurized = hash_tf.transform(data_words)
data_featurized.show(5)

#В features запишем конечный результат
idf = IDF(inputCol = 'text_words_features', outputCol = 'features')
idf_model = idf.fit(data_featurized)
data_scaled = idf_model.transform(data_featurized)
data_scaled.show(5)
'''
2) Теперь рассмотрим метод предобработки - Word2Vec. Он преобразует каждое слово в уникальный вектор заданного размера.На выходе получаем векторное
представление слов на естественном языке. После этого можно использовать, допустим, для расчета сходства документов или других NLP-задач.
Снова загрузим датасет:
'''
print('2) Word2Vec')
df = spark.read.format('csv').option('header', True).load('test.csv')
df = df.select(f.col('description_x').alias('text'))

#Разобьем текст сплитом, создадим 1 колонку
df = df.withColumn('text-list', (f.split(df['text'], ' ')))

#При создании Word2Vec можно задать размерность вектора. Пусть будет равен 3:
word2Vec = Word2Vec(vectorSize = 3, minCount = 0, inputCol = 'text-list', outputCol = 'result')
model = word2Vec.fit(df)
result = model.transform(df)
result.show(5)

#Убедимся, что в колонке result лежат трехмерные вектора
result.take(1)[0]['result']
'''
3)Следующий метод - CountVectorizer. Он помогает преобразовать набор документов (текстовых), в векторы количества токенов в этом тексте. Модель создаем разреженную
матрицу для наших документов. На выходе получаем таблицу со столбцами-словами, которые встречаются в тексте, а на пересечении, соотвественно , их количетву в тексте
'''
print('3) CountVectorizer')
df = spark.read.format('csv').option('header', True).load('test.csv')
df = df.select(f.col('description_x').alias('text'))
df = df.withColumn('text-list', (f.split(df['text'], ' ')))
#Необзятельный параметр minDF также влияет на процесс подбора, указывая минимальное количество (или долю, если < 1,0) документов, в которых термин должен появиться
#чтобы быть включенным в словарь

#Заполним столбцы на входе и выходе
cv = CountVectorizer(inputCol = 'text-list', outputCol = 'features')
model = cv.fit(df)
result = model.transform(df)
result.show(5, vertical = True)

#Давайте посмотрим на первую строку. Она состоит из двух разных слов, соответственно, в раздреженной матрице должно быть две единички и остальные нули
result.take(1)[0]['features']

#!!!!!ОБЯЗАТЕЛЬНО нужно останавливать спарк-сессию
spark.stop()