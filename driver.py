import numpy as np
import pandas as pd

from draw_population import *
from compute_shares import *

# load data
X = np.array(pd.read_csv("./data/estimation/X.csv")) 
product_markets = np.array(pd.read_csv("./data/estimation/product_markets.csv"))
p = np.array(pd.read_csv("./data/estimation/p.csv"))

T = np.unique(product_markets).size
K = X.shape[1]

# draw population of individuals, which are fixed during estimation, based on assumed 
# distribution of taste heterogeneity and empirical distribution of income
np.random.seed(100)

D_mean = np.array(pd.read_csv("./data/raw/meanincome.csv", header = None).iloc[:, 1])
D_var = np.tile(
    pow(pd.read_csv("./data/raw/sdincome.csv", header = None).iloc[:, 0], 2), D_mean.size)
nu_mean = 0
nu_var = 1

R = 200
nu, D = draw_population(R, T, K, nu_mean, nu_var, D_mean, D_var)
D = np.exp(D) # exponentiate log(income) 

# test computation of shares using ln(s/s0) as the vector of mean utilities 
# and ones as the sigma coefficients of the taste heterogeneity
delta = np.array(pd.read_csv("./data/estimation/s_s0.csv"))
sigma = np.identity(K+1)
s = compute_shares(delta, None, sigma, X, p, nu, D, product_markets)
# np.savetxt("s_computed.csv", s, delimiter = ",")