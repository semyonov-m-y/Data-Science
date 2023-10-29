import pandas as pd

path_to_file = '2_bookings.csv'
bookings = pd.read_csv(path_to_file, sep=';')

#Импортируйте библиотеку pandas как pd. Прочитайте датасет bookings.csv с разделителем ;. Ссылка на датасет находится в переменной path_to_file.
#Сохраните прочитанный датасет в bookings. Затем запишите первые 7 строк в переменную bookings_head.
bookings_head = bookings.head(7)
print(bookings_head)

#Проверьте, сколько всего строк и столбцов имеется в датасете.
print(len(bookings.columns))

#К какому типу относится большинство переменных?
print(bookings.dtypes.max())
print(bookings.columns)
#Приведите названия столбцов к нижнему регистру и заменив пробелы на знак нижнего подчеркивания.
bookings.columns = bookings.columns.str.replace(' ', '_')
#bookings = bookings.columns.str.lower() - если сделать так, то bookings перестанет являться dataFrame-мом, поэтому делаем:
bookings = bookings.rename(columns=str.lower)
print(bookings)
print('\n')

#Пользователи из каких стран совершили наибольшее число успешных бронирований?
# Бронирование считается успешным, если в дальнейшем не было отменено (переменная is_canceled). В качестве ответа выберите страны, входящие в топ-5.
bookings_by_countries = (bookings
    .query("is_canceled == 0")
    .groupby('country', as_index=False)
    .aggregate({'is_canceled' : 'count'})
    .sort_values('is_canceled', ascending=False)
)
print(bookings_by_countries)
print('\n')

# На сколько ночей (stays_total_nights)  в среднем бронируют отели типа City Hotel? Resort Hotel?
# Запишите полученные значения в пропуски с точностью до 2 знаков после точки.
bookings_by_nights = (bookings
    .query("hotel == 'City Hotel' or hotel == 'Resort Hotel'")
    .groupby('hotel', as_index=False)
    .aggregate({'stays_total_nights' : 'mean'})
    .sort_values('hotel', ascending=False)
)
print(round(bookings_by_nights, 2))
print('\n')

#Иногда тип номера, присвоенного клиенту (assigned_room_type), отличается от изначально забронированного (reserved_room_type).
# Такое может произойти, например, по причине овербукинга. Сколько подобных наблюдений встретилось в датасете? Отмена бронирования также считается
bookings_changed = (bookings
    .query("assigned_room_type != reserved_room_type")
    .aggregate({'assigned_room_type' : 'count'})
)
print(bookings_changed)
print('\n')

#Теперь проанализируйте даты запланированного прибытия (arrival_date_year).
# На какой месяц чаще всего оформляли бронь в 2016 году? Изменился ли самый популярный месяц в 2017?
the_most_popular_month = (bookings
    .query("arrival_date_year == 2016 or arrival_date_year == 2017")
    .groupby(['arrival_date_month', 'arrival_date_year'], as_index=False)
    .aggregate({'hotel' : 'count'})
    .sort_values('hotel', ascending=False)
)
print(the_most_popular_month)
print('\n')

#Сгруппируйте данные по годам, а затем проверьте, на какой месяц (arrival_date_month) бронирования отеля типа City Hotel отменялись чаще всего в 2015? 2016? 2017?
city_hotel_cancelled_month = (bookings
    .query("is_canceled == 1 and hotel == 'City Hotel'")
    .groupby(['arrival_date_year', 'arrival_date_month'], as_index=False)
    .aggregate({'is_canceled' : 'count'})
    .sort_values('is_canceled', ascending=False)
)
print(city_hotel_cancelled_month)
''''
или
bookings.query("is_canceled == 1 and hotel == 'City Hotel'") \
    .groupby("arrival_date_year") \
    .arrival_date_month \
    .value_counts()
'''
print('\n')

#Посмотрите на числовые характеристики трёх колонок: adults, children и babies. Какая из них имеет наибольшее среднее значение?
age_mean = bookings[['adults','children', 'babies']].mean()
print(age_mean)
print('\n')

#Создайте колонку total_kids, объединив столбцы children и babies. Для отелей какого типа среднее значение переменной оказалось наибольшим?
#City hotel – отель находится в город, Resort hotel – отель курортный. В качестве ответа укажите наибольшее среднее total_kids, округлив до 2 знаков после точки.
bookings["total_kids"] = bookings["babies"] + bookings['children']
total_kids = bookings.groupby("hotel") \
    .total_kids \
    .mean() \
    .round(2)
print(total_kids)
print('\n')

'''
Не все бронирования завершились успешно (is_canceled), поэтому можно посчитать, сколько клиентов было потеряно в процессе. 
Иными словами, посчитать метрику под названием Churn Rate. Churn rate (отток, коэффициент оттока) – это процент подписчиков 
(например, на push-уведомления от сайта), которые отписались от канала коммуникации, отказались от услуг сервиса в течение определенного периода времени. 
Иными словами, представляет собой отношение количества ушедших пользователей к общему количеству пользователей, выраженное в процентах.
В нашем случае Churn Rate - это процент клиентов, которые отменили бронирование. Давайте посмотрим, как эта метрика связана с наличием детей у клиентов!
Создайте переменную has_kids, которая принимает значение True, если клиент при бронировании указал хотя бы одного ребенка (total_kids), в противном случае – False. 
Далее проверьте, среди какой группы пользователей показатель оттока выше. 
В качестве ответа укажите наибольший % оттока, округленный до 2 знаков после точки (то есть доля 0.24563 будет 24.56% и в ответ пойдёт 24.56)
'''
bookings["has_kids"] = bookings.total_kids >0
have_children = bookings.query("has_kids == True")
have_children.shape[0]
have_no_children = bookings.query("has_kids == False")
have_no_children.shape[0]
have_children.shape[0]+have_no_children.shape[0] == bookings.shape[0]
yes_deti_canc = have_children.query("is_canceled == 1").shape[0]
no_deti_canc = have_no_children.query("is_canceled == 1").shape[0]
churn_rate =  yes_deti_canc / have_children.shape[0] *100
round(churn_rate, 2)
churn_rate_2 =  no_deti_canc / have_no_children.shape[0] *100
print(round(churn_rate_2, 2))
'''
или
bookings['has_kids'] = bookings['total_kids'] >= 1
rates = bookings.groupby('has_kids')['is_canceled'].value_counts(normalize=True)
round(rates * 100, 2)
'''
