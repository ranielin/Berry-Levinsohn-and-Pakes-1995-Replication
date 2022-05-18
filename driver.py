import numpy as np
import pandas as pd
import scipy.linalg
import scipy.optimize

from draw_population import *
from contraction_mapping import *
from compute_mc import *
from objective import *

np.random.seed(123)

# load data 
X = np.array(pd.read_csv("./data/estimation/X.csv")) # product characteristics
W = np.array(pd.read_csv("./data/estimation/W.csv")) # cost-shifters
product_markets = np.array(
    pd.read_csv("./data/estimation/product_markets.csv")) # market of each product
product_firms = np.array(
    pd.read_csv("./data/estimation/product_firms.csv")) # firm producing each product
p = np.array(pd.read_csv("./data/estimation/p.csv")) # prices
s = np.array(pd.read_csv("./data/estimation/s.csv")) # observed shares
Z = np.array(pd.read_csv("./data/estimation/Z.csv")) # demand-side instruments
Z_s = np.array(pd.read_csv("./data/estimation/Z_s.csv")) # supply-side instruments

obs = X.shape[0] # number of total observations
T = np.unique(product_markets).size # number of markets
K = X.shape[1] # number of characteristics per product
K_s = W.shape[1] # number of cost-shifters
M = Z.shape[1] # number of demand-side instruments
M_s = Z_s.shape[1] # number of supply-side instruments

# generate random draws separately in each market
D_mean = np.array(pd.read_csv("./data/raw/meanincome.csv", header = None).iloc[:, 1])
D_var = np.tile(
    pow(pd.read_csv("./data/raw/sdincome.csv", header = None).iloc[:, 0], 2), D_mean.size)
nu_mean = 0
nu_var = 1

R = 500 # number of simulations per market
nu, log_y = draw_population(R, T, K, nu_mean, nu_var, D_mean, D_var)
D = 1/np.exp(log_y) # 1 / exp(log(income)) = 1/y_i

# two-step feasible GMM estimation
# step 1: generate initial estimates using identity weighting matrix
delta_0 = np.array(pd.read_csv("./data/estimation/s_s0.csv"))
theta_2_start = np.array(pd.read_csv("./data/raw/theta_2_start.csv"))[:, 1]
tol = 1e-12
bounds = ((0, np.inf),) * theta_2_start.shape[0]
phi = np.identity(M + M_s)

gmm_1 = scipy.optimize.minimize(objective, theta_2_start, args = (
    phi, delta_0, tol, s, X, W, p, Z, Z_s, product_markets, product_firms, nu, D
    ), method = 'L-BFGS-B', bounds = bounds, options = {
        'maxiter': 1000, 'maxfun': 1000, 'eps': 1e-3}, tol = 1e-4)

theta_2_initial = gmm_1.x
theta_2_initial_df = pd.DataFrame(theta_2_initial)
theta_2_initial_df.insert(0, "var", [
    "alpha_price", "sigma_constant", "sigma_hpwt", "sigma_air", "sigma_mpd", "sigma_size"])
theta_2_initial_df.rename({0:'est'}, axis = 1, inplace = True)
theta_2_initial_df.to_csv("./output/gmm_1_nonlinear_estimates.csv", sep = ",", index = False)

# re-estimate weighting matrix using initial parameter estimates
gamma = np.zeros((K + 1, 1))
gamma[0] = theta_2_initial[0]

sigma = np.zeros((K + 1, K + 1))
np.fill_diagonal(sigma, np.append([0], theta_2_initial[1:(K + 1)]))

delta = contraction_mapping(delta_0, tol, gamma, sigma, s, X, p, product_markets, nu, D)
log_mc = np.log(compute_mc(delta, gamma, sigma, s, X, p, product_markets, product_firms, nu, D))

X_full = scipy.linalg.block_diag(X, W) # product characteristics + cost-shifters
Z_full = scipy.linalg.block_diag(Z, Z_s) # demand-side instruments + supply-side instruments
delta_full = np.vstack([delta, log_mc]) # mean utilities + log(marginal costs)

theta_1 = np.linalg.inv(X_full.T @ Z_full @ np.linalg.inv(phi) @ Z_full.T @ X_full) @ (
    X_full.T @ Z_full @ np.linalg.inv(phi) @ Z_full.T @ delta_full) # IV projection

xi = delta_full - X_full @ theta_1 # structural errors
g_jt = Z_full *  xi # obs x (M + M_s) matrix, each row is g_jt for a unique j, t observation

phi = (1 / obs) * g_jt.T @ g_jt # sample variance-covariance matrix of g_jt vectors 
np.savetxt("./output/gmm_phi_estimate.csv", phi, delimiter=",")

# step 2: re-estimate parameters with re-calculated weighting matrix
gmm_2 = scipy.optimize.minimize(objective, theta_2_start, args = (
    phi, delta_0, tol, s, X, W, p, Z, Z_s, product_markets, product_firms, nu, D
    ), method = 'L-BFGS-B', bounds = bounds, options = {
        'maxiter': 1000, 'maxfun': 1000, 'eps': 1e-3}, tol = 1e-4)

theta_2_final = gmm_2.x
theta_2_final_df = pd.DataFrame(theta_2_final)
theta_2_final_df.insert(0, "var", [
    "alpha_price", "sigma_constant", "sigma_hpwt", "sigma_air", "sigma_mpd", "sigma_size"])
theta_2_final_df.rename({0:'est'}, axis = 1, inplace = True)
theta_2_final_df.to_csv("./output/gmm_2_nonlinear_estimates.csv", sep = ",", index = False)

# extract linear parameters
gamma = np.zeros((K + 1, 1))
gamma[0] = theta_2_final[0]

sigma = np.zeros((K + 1, K + 1))
np.fill_diagonal(sigma, np.append([0], theta_2_final[1:(K + 1)]))

delta = contraction_mapping(delta_0, tol, gamma, sigma, s, X, p, product_markets, nu, D)
log_mc = np.log(compute_mc(delta, gamma, sigma, s, X, p, product_markets, product_firms, nu, D))

X_full = scipy.linalg.block_diag(X, W) # product characteristics + cost-shifters
Z_full = scipy.linalg.block_diag(Z, Z_s) # demand-side instruments + supply-side instruments
delta_full = np.vstack([delta, log_mc]) # mean utilities + log(marginal costs)

theta_1_final = np.linalg.inv(X_full.T @ Z_full @ np.linalg.inv(phi) @ Z_full.T @ X_full) @ (
    X_full.T @ Z_full @ np.linalg.inv(phi) @ Z_full.T @ delta_full) # IV projection
theta_1_final_df = pd.DataFrame(theta_1_final)
theta_1_final_df.insert(0, "var", [
    "beta_constant", "beta_hpwt", "beta_air", "beta_mpd", "beta_size", "gamma_constant",
    "gamma_ln_hpwt", "gamma_air", "gamma_ln_mpg", "gamma_ln_size", "gamma_trend"])
theta_1_final_df.rename({0:'est'}, axis = 1, inplace = True)
theta_1_final_df.to_csv("./output/gmm_2_linear_estimates.csv", sep = ",", index = False)