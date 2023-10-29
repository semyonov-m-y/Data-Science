'''
Tobit. Применяется, когда зависимая переменная ограничена и непрерывна.
'''

from sklearn.datasets import make_regression
import matplotlib.pyplot as plt
import pandas as pd
from tobit import *

#model fit
tr = TobitModel()

#result
tr = tr.fit(x, y, cens, verbose=False)
tr.coef_