'''
Probit. Отличается от логит модели тем, что предполагает нормальность распределения гиперпараметров, в то время, как логит модель предполагает логистическое распределение.
'''
import statsmodels
from statsmodels.api import Probit

#model fit
result_3 = statsmodels.discrete.discrete_model.Probit(labf_part, ind_var_probit)

#result
print(result_3.summary())