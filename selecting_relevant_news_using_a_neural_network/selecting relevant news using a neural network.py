'''
Пишем систему для рекомендации похожих новостей.
________________________________________
Наш датасет с новостями имеет темы - topic ("Спорт", "Наука и техника", ...) и тэги tag ("Футбол", "Техника", "Космос", ...).
1.	Возьмем новости, помеченные одним тэгом и разобьем на еще более маленькие группы по похожести текстов.
2.	Используем библиотеку, реализующую нейросеть архитектуры Word2Vec от gensim и готовые веса для нее от RusVectores. Преобразуем тексты в наборы чисел.
3.	Используем модели для 📝 кластеризации - разбиения набора данных на группы наиболее похожих элементов. Воспользуемся реализацией из sklearn.

'''
import nltk #для токенизации
import numpy as np
import pandas as pd
from gensim.models import KeyedVectors #представит word2vec
from nltk.tokenize import word_tokenize
from pymystem3 import Mystem #преобразование слов к начальной форме слова
from tqdm.notebook import tqdm #рисуем линии прогресса, чтобы понимать как долго что-то выполняется
from sklearn.cluster import KMeans
from wget import download

nltk.download('punkt') #загружаем дополнительные данные для библиотеки разбиения текстов на слова

# Настраиваем отображение таблиц
from IPython.display import display
pd.set_option('display.max_colwidth', 200)

# Скачиваем библиотеку для загрузки файлов pip install wget --quiet
download('https://rusvectores.org/static/models/rusvectores4/news/news_upos_cbow_600_2_2018.vec.gz','news_upos_cbow_600_2_2018.vec.gz')

#Команда %% time в начале ячейки замеряет время ее выполнения
# Скачиваем веса модели. Выполняется ≈2-3 минуты
word2vec = KeyedVectors.load_word2vec_format('news_upos_cbow_600_2_2018.vec.gz')

# Атрибут index_to_key объекта word2vec содержит список слов, на котором обучалась модель
word2vec.index_to_key

# У нашей модели есть особенность: для ее обучения к словам цепляли тэги с частью речи, например, 'год_NOUN', 'сообщать_VERB'.
# Чтобы сопоставить обычное слово и слово с тэгом из модели, составим словарь переименования.
# Метод split разбивает слово на список подслов по заданному символу
'год_NOUN'.split('_')

# В квадратных скобках из списка получаем начальный элемент (нумерация с 0)
'год_NOUN'.split('_')[0]

# Создадим словарь вида {слово: слово_ТЭГ}. В конце списка встречаются некорректные тэги, например, 'год_NOUN' 'год_PROPN'
# или ['давать_VERB', 'давать_NOUN', 'давать_ADJ', 'давать_PROPN', 'давать_NUM']
# Поэтому будем брать только первую версию слова, и если оно уже есть в словаре, перезаписывать его не будем
lemma2word = {}

for tagged_word in word2vec.index_to_key:
    word = tagged_word.split('_')[0]
    if word not in lemma2word:
        lemma2word[word] = tagged_word

lemma2word['давать']
'''
Векторизация
Для того, чтобы иметь возможность автоматически анализировать данные, нужно придать тексту числовую структуру.Для этого сделаем векторизацию.
Нам нужно пройти несколько стадий: токенизация → лемматизация → векторизация. 📝 Токенизация - процесс разбиения текста на слова(токен - 
минимальная единица язчка, имеющая смысл) 👨🏻💻 Вопрос: можно ли назвать букву токеном? 📝 
Лемматизация - получение начальной формы слова: "годы", "году" → "год" 📝 Векторизация - процесс превращения текста в набор чисел - 
векторное представление.Например, "год" → (0.1, 0, 1.2, 3) 📝 Вектор - набор чисел, например, (0.1, 0, 1.2, 3).Над векторами можно проводить 
арифметические операции аналогично числам - например, попарное сложение элементов: (1, 2, 5) + (3, 4, 0) = (4, 6, 5) или вычисление расстояния между ними. 
На основе близости векторных представлений текстов мы и будем искать похожие новости.
'''
# Пример токенизации
word_tokenize('Мороз и солнце, день чудесный', language='russian')

# mystem - инструмент для лемматизации
mystem = Mystem()

# Функция получения тэгированной формы слова из модели Word2Vec
def get_w2v_word(word):
    # Получаем начальную форму слова
    lemma = mystem.lemmatize(word)[0]
    # Берем тэгированную форму из составленного ранее словаря
    w2v_word = lemma2word.get(lemma)
    return w2v_word

get_w2v_word("Мороз")
get_w2v_word("даю")

# Функция получения векторного представления слова из модели Word2Vec
def vectorize_sentence(txt):
    words = word_tokenize(txt, language='russian')
    vectors = []
    for word in words:
        tagged_word = get_w2v_word(word)
        if tagged_word is not None:
            vector = word2vec[tagged_word] #получаем векторное представление, то есть веса
            vectors.append(vector)
    return np.mean(vectors, axis=0) #по вертикали в таблице считаем не общее одно среднее значение, а каждое, чтобы получить 1 вектор, схлопнув множество векторов в 1
#получили представление списком из 600 чисел, малые по модулю и в -2/-3/-4 степени
vectorize_sentence('Мороз и солнце, день чудесный')

#Возьмем данные о новостях с Lenta.ru
data = pd.read_csv('https://raw.githubusercontent.com/anastasiarazb/skillbox_nlp_demo/master/lenta_example.csv',sep=',')

# Выведем списки тем и тэгов со счетчиком числа статей в этих группах. Функция groupby по списку колонок ['topic', 'tags'] группирует данные,
# а count() - дает количество записей в каждой группе
data.groupby(['topic', 'tags']).count()

# В теме 'Экономика' возьмем тэг 'undefined' и исследуем новости в нем
data_tag = data[
    (data['topic'] == 'Экономика')
    & (data['tags'] == 'undefined')
    ].copy()

# 👨🏻💻 Попробуйте другую комбинацию темы и тэга, напр. "Наука и техника"+"Техника"
data_tag.shape

# Представим заголовки и тексты в виде чисел с помощью
# объединения векторных представлений, полученных с помощью
# vectorize_sentence для каждого в отдельности
# Операция + для двух списков объединяет их: [1, 2] + [3, 4] = [1, 2, 3, 4]
vectors = []

for title, text in tqdm(data_tag[['title', 'text']].values):
    vector = vectorize_sentence(title) + vectorize_sentence(text)
    vectors.append(vector)

# 👨🏻💻 Попробуйте использовать только 1 элемент статьи, только текст
#    или только заголовок
#    (для этого в цикле надо будет оставить в vector, например,
#    только vectorize_sentence(text))
vectors = np.array(vectors)

#Кластеризация 📝 Кластеризация - объединение похожих объектов в группы. Есть различные методы кластеризации, мы будем пользоваться библиотекой sklearn

from sklearn.cluster import SpectralClustering, KMeans

clusterizer = SpectralClustering(n_clusters=8, n_init=10, random_state=42)

# 👨🏻💻 Попробуйте другую модель кластеризации, например, KMeans.
#    Описание различных методов: https://scikit-learn.org/stable/modules/clustering.html
# 👨🏻💻 Попробуйте заменить параметры, например, установить n_clusters=10. Есть ли какие-то идеи, как правильно выбрать количество кластеров?
clusterizer.fit(vectors)

# Добавим разметку с номером кластера clusterizer.labels_ как новую колонку в данные 'label' в таблицу data_tag
data_tag['label'] = clusterizer.labels_

data_tag.head(5)

# Набор меток data_tag['label'].unique() отсортируем через sorted() и для каждой метки выведем label и подтаблицу строк с этой
# меткой кластера data_tag[data_tag['label'] == label]
for label in sorted(data_tag['label'].unique()):
    print(label)
    display(data_tag[data_tag['label'] == label])
