''''scikit-learn (ранее известная, как scikits.learn, а также известная как sklearn) — библиотека, предназначенная для
машинного обучения, написанная на языке программирования Python и распространяемая в виде свободного программного обеспечения
В её состав входят различные алгоритмы, в том числе предназначенные для задач классификации, регрессионного и кластерного
анализа данных, включая метод опорных векторов, метод случайного леса, алгоритм усиления градиента, метод k-средних и DBSCAN.
Библиотека была разработана для взаимодействия с численными и научными библиотеками языка программирования Python NumPy и SciPy

train_test_split
Эта функция используется для разделения набора данных на наборы для обучения и тестирования. Она принимает набор данных,
целевую переменную и размер тестового набора в качестве параметров.'''

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.3)

''''tandardScaler
Эта функция используется для стандартизации набора данных путём вычитания среднего значения и деления на стандартное 
отклонение. Она часто используется для подготовки данных для алгоритмов, требующих стандартизированного ввода.'''''
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

''''MinMaxScaler
Эта функция используется для масштабирования набора данных до определённого диапазона (обычно от 0 до 1). Она часто 
используется для подготовки данных для алгоритмов, требующих ввода в определённом диапазоне.'''''
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

''''LabelEncoder
Эта функция используется для программирования категориальных переменных как целых чисел. Она часто используется для 
подготовки данных для алгоритмов, которые не могут обрабатывать категориальные переменные.'''''
from sklearn.preprocessing import LabelEncoder
encoder = LabelEncoder()
y_train_encoded = encoder.fit_transform(y_train)
y_test_encoded = encoder.transform(y_test)

''''OneHotEncoder
Эта функция используется для программирования категориальных переменных как двоичных векторов. Она часто используется 
для подготовки данных для алгоритмов, требующих двоичных входных данных.'''''
from sklearn.preprocessing import OneHotEncoder
encoder = OneHotEncoder()
y_train_encoded = encoder.fit_transform(y_train.reshape(- 1 , 1 ))
y_test_encoded = encoder.transform(y_test.reshape(- 1 , 1 ))

''''DecisionTreeClassifier
Эта функция используется для создания модели дерева решений. Она принимает обучающие данные и метки в качестве параметров.'''''
from sklearn.tree import DecisionTreeClassifier
clf = DecisionTreeClassifier()
#clf.fit(X_train_scaled, y_train_encoded)

''''RandomForestClassifier
Эта функция используется для создания модели случайного леса. Он принимает обучающие данные и метки в качестве параметров.'''''
from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier()
#clf.fit(X_train_scaled, y_train_encoded)

''''KMeans
Эта функция используется для создания модели кластеризации K-средних. Она принимает набор данных и количество кластеров 
в качестве параметров.'''''
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=3)
kmeans.fit(X_train_scaled)

''''LinearRegression
Эта функция используется для создания модели линейной регрессии. Она принимает обучающие данные и метки в качестве параметров.'''''
from sklearn.linear_model import LinearRegression
reg = LinearRegression()
reg.fit(X_train_scaled, y_train)

''''LogisticRegression
Эта функция используется для создания модели логистической регрессии. Она принимает обучающие данные и помечает их как 
код parameters.scssCopy.'''''
from sklearn.linear_model import LogisticRegression
clf = LogisticRegression()
#clf.fit(X_train_scaled, y_train_encoded)

''''SVM
Эта функция используется для создания модели машины опорных векторов. Она принимает обучающие данные и метки в качестве параметров.'''''
from sklearn.svm import SVC
clf = SVC()
#clf.fit(X_train_scaled, y_train_encoded)

''''NaiveBayes
Эта функция используется для создания наивной байесовской модели. Она принимает обучающие данные и метки в качестве параметров.'''''
from sklearn.naive_bayes import GaussianNB
clf = GaussianNB()
#clf.fit(X_train_scaled, y_train_encoded)

''''GridSearchCV
Эта функция используется для выполнения поиска по сетке, чтобы найти лучшие гиперпараметры для модели. Она принимает 
модель, сетку гиперпараметров и стратегию перекрёстной проверки в качестве параметров.'''''
from sklearn.model_selection import GridSearchCV
param_grid = {'n_estimators': [10, 50, 100], 'max_depth': [2, 4, 8]}
grid_search = GridSearchCV(RandomForestClassifier(), param_grid, cv=5)
#grid_search.fit(X_train_scaled, y_train_encoded)

''''Pipeline
Эта функция используется для создания конвейера шагов предварительной обработки данных и моделирования. Она принимает 
список кортежей, где каждый кортеж содержит имя шага и соответствующую функцию.'''''
from sklearn.pipeline import Pipeline
pipe = Pipeline([( 'scaler' , StandardScaler()), ( 'clf' , RandomForestClassifier())])
pipe.fit(X_train, y_train)

''''PCA
Эта функция используется для выполнения анализа основных компонентов в наборе данных. В качестве параметра принимается 
количество компонентов.'''''
from sklearn.decomposition import PCA
pca = PCA(n_components=2)
X_train_pca = pca.fit_transform(X_train_scaled)

''''TSNE
Эта функция используется для выполнения t-распределённого стохастического встраивания соседей в набор данных. Требуется 
количество измерений для встраивания данных в качестве параметра.'''''
from sklearn.manifold import TSNE
tsne = TSNE(n_components=2)
X_train_tsne = tsne.fit_transform(X_train_scaled)

''''GradientBoostingClassifier
Эта функция используется для создания классификатора повышения градиента. Она принимает обучающие данные и метки в качестве параметров.'''''
from sklearn.ensemble import GradientBoostingClassifier
clf = GradientBoostingClassifier()
#clf.fit(X_train_scaled, y_train_encoded)

''''AdaBoostClassifier
Эта функция используется для создания классификатора AdaBoost. Она принимает обучающие данные и метки в качестве параметров.'''''
from sklearn.ensemble import AdaBoostClassifier
clf = AdaBoostClassifier()
#clf.fit(X_train_scaled, y_train_encoded)

''''Lasso
Эта функция используется для выполнения регрессии Лассо. Она принимает обучающие данные и метки в качестве параметров.'''''
from sklearn.linear_model import Lasso
reg = Lasso()
#reg.fit(X_train_scaled, y_train)

''''Ridge
Эта функция используется для выполнения регрессии Риджа. Она принимает обучающие данные и метки в качестве параметров.'''''
from sklearn.linear_model import Ridge
reg = Ridge()
#reg.fit(X_train_scaled, y_train)
''''
'''''''ElasticNet
Эта функция используется для выполнения регрессии эластичной сети. Она принимает обучающие данные и метки в качестве параметров.'''
from sklearn.linear_model import ElasticNet
reg = ElasticNet()
#reg.fit(X_train_scaled, y_train)

''''SGDClassifier
Эта функция используется для создания классификатора стохастического градиентного спуска. Она принимает обучающие данные 
и метки в качестве параметров.'''''
from sklearn.linear_model import SGDClassifier
clf = SGDClassifier()
#clf.fit(X_train_scaled, y_train_encoded)

''''KernelPCA
Эта функция используется для выполнения анализа основных компонентов ядра в наборе данных. В качестве параметров она 
принимает функцию ядра и количество компонентов, которые необходимо сохранить.'''''
from sklearn.decomposition import KernelPCA
kpca = KernelPCA(kernel='rbf', n_components=2)
X_train_kpca = kpca.fit_transform(X_train_scaled)

''''IsolationForest
Эта функция используется для создания модели изолированного леса для обнаружения аномалий. Она принимает уровень 
загрязнения и случайное начальное число в качестве параметров.'''''
from sklearn.ensemble import IsolationForest
clf = IsolationForest(contamination=0.1, random_state=42)
clf.fit(X_train_scaled)

''''DBSCAN
Эта функция используется для выполнения пространственной кластеризации приложений с шумом на основе плотности 
(DBSCAN) в наборе данных. В качестве параметров она принимает минимальное количество выборок и радиус окрестности.'''''
from sklearn.cluster import DBSCAN
dbscan = DBSCAN(min_samples=5, eps=0.5)
dbscan.fit(X_train_scaled)

''''AgglomerativeClustering
Эта функция используется для выполнения иерархической кластеризации набора данных. В качестве параметров она принимает 
количество кластеров и метод связывания.'''''
from sklearn.cluster import AgglomerativeClustering
agg = AgglomerativeClustering(n_clusters=3, linkage='ward')
agg.fit(X_train_scaled)

''''KernelDensity
Эта функция используется для оценки функции плотности вероятности набора данных с использованием оценщика плотности ядра. 
Она принимает функцию ядра и пропускную способность в качестве параметров.'''''
from sklearn.neighbors import KernelDensity
kde = KernelDensity(kernel='gaussian', bandwidth=0.1)
kde.fit(X_train_scaled)

''''GaussianMixture
Эта функция используется для моделирования гауссовой смеси в наборе данных. В качестве параметров она принимает 
количество компонентов и тип ковариации.'''''
from sklearn.mixture import GaussianMixture
gmm = GaussianMixture(n_components=3, covariance_type='full')
gmm.fit(X_train_scaled)

''''NearestNeighbors
Эта функция используется для поиска ближайших соседей в наборе данных. В качестве параметров она принимает количество 
соседей и метрику расстояния.'''''
from sklearn.neighbors import NearestNeighbors
nn = NearestNeighbors(n_neighbors=5, metric='euclidean')
nn.fit(X_train_scaled)

''''KNNClassifier
Эта функция используется для создания классификатора K ближайших соседей. Она принимает обучающие данные и метки в 
качестве параметров.'''''
from sklearn.neighbors import KNeighborsClassifier
clf = KNeighborsClassifier()
clf.fit(X_train_scaled, y_train_encoded)

''''LDA
Эта функция используется для выполнения линейного дискриминантного анализа набора данных. В качестве параметра 
принимается количество компонентов.'''''
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
lda = LinearDiscriminantAnalysis(n_components=2)
#X_train_lda = lda.fit_transform(X_train_scaled, y_train_encoded)

''''QDA
Эта функция используется для выполнения квадратичного дискриминантного анализа набора данных.'''''
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
qda = QuadraticDiscriminantAnalysis()
#qda.fit(X_train_scaled, y_train_encoded)

''''RANSACRegressor
Эта функция используется для выполнения регрессии RANSAC в наборе данных. Она принимает базовую оценку и максимальное 
количество итераций в качестве параметров.'''''
from sklearn.linear_model import RANSACRegressor
from sklearn.linear_model import LinearRegression
#ransac = RANSACRegressor(base_estimator=LinearRegression(), max_trials=100)
#ransac.fit(X_train_scaled, y_train)

''''GradientBoostingRegressor
Эта функция используется для создания модели регрессии с повышением градиента. Она принимает обучающие данные и метки 
в качестве параметров.'''''
from sklearn.ensemble import GradientBoostingRegressor
reg = GradientBoostingRegressor()
reg.fit(X_train_scaled, y_train)

''''AdaBoostRegressor
Эта функция используется для создания регрессионной модели AdaBoost. Он принимает обучающие данные и метки в качестве параметров.'''''
from sklearn.ensemble import AdaBoostRegressor
reg = AdaBoostRegressor()
reg.fit(X_train_scaled, y_train)

''''SVR
Эта функция используется для создания модели регрессии опорных векторов. Она принимает обучающие данные и метки в качестве параметров.'''''
from sklearn.svm import SVR
reg = SVR()
reg.fit(X_train_scaled, y_train)

''''DecisionTreeRegressor
Эта функция используется для создания регрессионной модели дерева решений. Она принимает обучающие данные и метки в качестве параметров.'''''
from sklearn.tree import DecisionTreeRegressor
reg = DecisionTreeRegressor()
reg.fit(X_train_scaled, y_train)

''''RandomForestRegressor
Эта функция используется для создания модели регрессии случайного леса. Она принимает обучающие данные и метки в качестве параметров.'''''
from sklearn.ensemble import RandomForestRegressor
reg = RandomForestRegressor()
reg.fit(X_train_scaled, y_train)

''''PolynomialFeatures
Эта функция используется для создания полиномиальных признаков из набора данных. В качестве параметра принимает степень многочлена.'''''
from sklearn.preprocessing import PolynomialFeatures
poly = PolynomialFeatures(degree=2)
X_train_poly = poly.fit_transform(X_train_scaled)

''''TruncatedSVD
Эта функция используется для выполнения усечённого разложения по сингулярным значениям в наборе данных. 
В качестве параметра требуется количество компонентов, которые необходимо сохранить.'''''
from sklearn.decomposition import TruncatedSVD
svd = TruncatedSVD(n_components=2)
X_train_svd = svd.fit_transform(X_train_scaled)

''''NMF
Эта функция используется для выполнения неотрицательной матричной факторизации набора данных. Она принимает количество 
компонентов для извлечения в качестве кода parameter.scssCopy'''''
from sklearn.decomposition import NMF
nmf = NMF(n_components=2)
X_train_nmf = nmf.fit_transform(X_train_scaled)

''''Binarizer
Эта функция используется для бинаризации набора данных на основе порогового значения. Она принимает пороговое значение 
в качестве параметра.'''''
from sklearn.preprocessing import Binarizer
binarizer = Binarizer(threshold=0.5)
X_train_binarized = binarizer.fit_transform(X_train_scaled)

''''LabelBinarizer
Эта функция используется для бинаризации категориальных переменных как бинарных векторов. Она часто используется для 
подготовки данных для алгоритмов, требующих двоичных входных данных.'''''
from sklearn.preprocessing import LabelBinarizer
binarizer = LabelBinarizer()
y_train_binarized = binarizer.fit_transform(y_train)

''''MultiLabelBinarizer
Эта функция используется для бинаризации нескольких категориальных переменных как бинарных векторов. Она часто 
используется для подготовки данных для алгоритмов, требующих двоичных входных данных.'''''
from sklearn.preprocessing import MultiLabelBinarizer
binarizer = MultiLabelBinarizer()
#y_train_binarized = binarizer.fit_transform(y_train)

''''LabelPropagation
Эта функция используется для распространения меток в наборе данных. В качестве параметров она принимает функцию ядра 
и количество итераций.'''''
from sklearn.semi_supervised import LabelPropagation
propagation = LabelPropagation(kernel='knn', max_iter=100)
propagation.fit(X_train_scaled, y_train)

''''LabelSpreading
Эта функция используется для распространения меток в наборе данных. В качестве параметров она принимает функцию ядра и 
количество итераций.'''''
from sklearn.semi_supervised import LabelSpreading
spreading = LabelSpreading(kernel='knn', max_iter=100)
spreading.fit(X_train_scaled, y_train)

''''CalibratedClassifierCV
Эта функция используется для калибровки вероятностей классификатора. В качестве параметров она принимает базовый 
классификатор и метод калибровки.'''''
from sklearn.calibration import CalibratedClassifierCV
from sklearn.linear_model import LogisticRegression
clf = LogisticRegression()
calibrated_clf = CalibratedClassifierCV(clf, cv=5, method='sigmoid')
#calibrated_clf.fit(X_train_scaled, y_train_encoded)

''''DummyClassifier
Эта функция используется для создания фиктивного классификатора, который прогнозирует с использованием простой стратегии. 
Она принимает стратегию в качестве параметра.'''''
from sklearn.dummy import DummyClassifier
dummy = DummyClassifier(strategy='most_frequent')
#dummy.fit(X_train_scaled, y_train_encoded)