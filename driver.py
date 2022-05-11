import numpy as np
import pandas as pd

from draw_population import *

D_mean = np.array(pd.read_csv("./data/raw/meanincome.csv", header = None).iloc[:, 1])
D_var = np.tile(pow(pd.read_csv("./data/raw/sdincome.csv", header = None).iloc[:, 0], 2), D_mean.size)
nu_mean = 0
nu_var = 1
T = D_mean.size
R = 200

nu, D = draw_population(R, T, nu_mean, nu_var, D_mean, D_var)

