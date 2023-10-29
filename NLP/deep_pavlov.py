#Задача автоанализа постов на habr.com и нахождение в заданном тексте ответов на вопросы (Context Wuestion Answering - CQA) в сервисе HuggingFace, предлагающий множество мультиязычных предобученных NLP моделей.
#Для работы с русским языком используем DeepPavlov: 1)загрузим тексты с habr.com; 2)подготовим вопросы/ответы; 3)решим задачу CQA с помощью DeepPavlov
from urllib import request
from bs4 import BeautifulSoup
from deeppavlov import configs, build_model

#получим текст по заданному url
def getHtmlDocument(url):
    fp = request.urlopen(url)
    mybytes = fp.read()
    fp.close()
    return mybytes.decode('utf8')

def getTextFromHtml(HtmlDocunent):
    soup = BeautifulSoup(HtmlDocunent, features='html.parser')
    content = soup.find('div', {'id', 'post-content-body'})
    return content.text

#Составим набор вопросов
questions = {
    'О чём пост?',
    'Какая цель поста?',
    'Какая задача решалась?',
    'Что использовалось в работе?',
    'Какие выводы?',
    'Что использовалось?',
    'Какие алгоритмы использовались?',
    'Какой язык программирования использовали?',
    'В чём отличия?',
    'Что особенного проявилось?',
    'Какова область применения',
    'Что получено?',
    'Каков результат?',
    'Что получено в заключении?',
}

#Сделаем pip install deeppavlov, transformers и настроим deeppevlov для решения задачи CQA
#Инициализируем загрузку модели squad_ru_bert - это модель грубокого обучения на основе архитектуры BERT, обученная на наборе данных SQuAD-Ru, который содержит пары вопрос-ответ.
model = build_model('squad_ru_bert', download=True)

#Выберем посты на habr.com
paper_urls = {
    'https://habr.com/ru/articles/339914/',
    'https://habr.com/ru/articles/339915/',
    'https://habr.com/ru/articles/339916/',
}

#Воспользуемся моделью для ответы на вопросы для каждого поста из списка paper_urls
for url in paper_urls:
    content = getTextFromHtml(getHtmlDocument(url))
    for q in questions:
        answer = model([content], [q])
        if abs(answer[2] - 1) > 1e-6:
            print(q, ' ', answer[0])
