import numpy as np
import pandas as pd

from draw_population import *
from contraction_mapping import *
from compute_mc import *

# load data
X = np.array(pd.read_csv("./data/estimation/X.csv")) 
product_markets = np.array(pd.read_csv("./data/estimation/product_markets.csv"))
product_firms = np.array(pd.read_csv("./data/estimation/product_firms.csv"))
p = np.array(pd.read_csv("./data/estimation/p.csv"))
s = np.array(pd.read_csv("./data/estimation/s.csv"))

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
nu, log_y = draw_population(R, T, K, nu_mean, nu_var, D_mean, D_var)
D = 1/np.exp(log_y) # 1 / exp(log(income)) = 1/y_i

# test contraction mapping using ln(s/s0) as the initial guess
# in BLP, gamma = [alpha, 0, ..., 0]^T, sigma = diag(0, beta_nu(1), ..., beta_nu(L))
delta_0 = np.array(pd.read_csv("./data/estimation/s_s0.csv"))
sigma = np.identity(K + 1)
sigma[0, 0] = 0
gamma = np.zeros((K + 1, 1))
gamma[0] = 40
tol = 1e-12
delta = contraction_mapping(delta_0, tol, gamma, sigma, s, X, p, product_markets, nu, D)

# test computation of shares
s_model = compute_shares(delta, gamma, sigma, X, p, product_markets, nu, D)[0]
np.max(np.abs(s_model - s))

# test computation of marginal costs and share-price derivatives
mc = compute_mc(delta, gamma, sigma, s, X, p, product_markets, product_firms, nu, D)
omega = compute_omega(delta, gamma, sigma, X, p, product_markets, product_firms, nu, D)