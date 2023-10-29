from pyspark.ml.classification import GBTClassifier
from pyspark.sql import SparkSession
from pyspark.ml.feature import StringIndexer
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
'''
Apach Spark – фреймворк, предоставляющий API для выполнения распределенной обработки данных. Spark ML является основной библиотекой для разработки моделей машинного обучения в Apach Spark. Тут решаются задачи: регрессия, классификация, кластеризация, снижение размерности. Можно обрабатывать пропущенные значения и устранять выбросы. Для борьбы с переобучением использует L1 и L2 регуляризацию. Для графовых структур Apach Spark имеет модуль GraphX, а для потоковой обработки данных Spark Streeming
'''
'''
Градиентный бустинг. Это ансамбли моделей. Строятся регрессии или деревья решений и минимизируется функция потерь, как в градиентном спуске.
Используется, когда выборка помещается в память, есть смесь разных признаков.
Сильные стороны: высокая точность классификации и прогнозирования, подходит для мультиклассовой классификации, не чувствителен к выбросам,
способен решать задачи ранжирования.
Слабые стороны — требователен к ресурсам компьютера.
'''
#Датасет Titanic содержит характеристики человека (пол, возарст, билет, кабина и тд). Необходимо предсказать выжил ли человек в результате крушения корабля
spark = SparkSession.builder.appName('example').getOrCreate()
df = spark.read.csv('train_and_test2.csv', header=True, inferSchema=True)
print(df.show(10))
#Можно вывести необходимые колонки
print(df.select('Survived', 'Age', 'Parch').show(1))
#Можно посчитать сколько человек выжило, а сколько нет
print(df.groupBy('Survived').count().show())
#Сколько мужчин и сколько женщин
print(df.groupBy('Survived').pivot('Sex').count().show())
#Сколько пропущенных значений в датасете
#for col in df.columns: print(col, df.filter(df[col].isNul()).count())

#Построим модель. Используем StringIndexer для перевода текстовой фичи - пол в категориальную переменную
new_index = StringIndexer(inputCols=['Sex'], outputCols=['SexNum'])
stringIndex_model = new_index.fit(df)
df_ = stringIndex_model.transform(df).drop('Sex')

#Используем инициализацию VectorAssembler для формирования матрицы объясняющих переменных и целевой переменной. VectorAssembler формирует один векторный столбец из заданного ему на вход списка столбцов (фичей+целевой переменной). Не может работать со строковыми данными
assembler = VectorAssembler(inputCols=df_.columns[1:], outputCol='features')
df_ = assembler.setHandleInvalid("skip").transform(df_).select('features', 'Survived')

#Теперь делим выборку на тренировочную и тестовую в пропорции 70% на 30%
train_df, test_df = df_.randomSplit([0.7, 0.3])

#Обучим модель и определим метрки качества построения модели. Инициализируем экземпляр MulticlassClassificationEvaluator(), в который необходимо передать целевую переменную и метрику качества. Для оценки используем метрки accuracy. тк она является распространенной и легко применимой
evaluation = MulticlassClassificationEvaluator(labelCol='Survived', metricName='accuracy')
#Обучаем модель градиентного бустинга
gradient_boosting = GBTClassifier(labelCol='Survived')
model = gradient_boosting.fit(train_df)
pred = model.transform(test_df)
print(evaluation.evaluate(pred))