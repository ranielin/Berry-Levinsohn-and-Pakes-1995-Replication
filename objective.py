import numpy as np
import scipy.linalg

from contraction_mapping import *
from compute_mc import *

def objective(theta_2, phi, delta_0, tol, s, X, W, p, Z, Z_s, product_markets, product_firms, nu, D):
# compute GMM objective function
# inputs:
#   phi, GMM weighting matrix
#   delta_0, vector of initial guesses of product market mean utilities
#   tol, tolerance level at which to stop the contraction mapping iteration
#   theta_2, vector of nonlinear parameters
#   s, vector of observed market shares of each product in each market
#   X, matrix of observed characteristics of each product in each market
#   W, matrix of observed supply-side cost shifters in each market
#   p, vector of prices of each product in each market
#   Z, matrix of demand-side instruments
#   Z_s, matrix of supply-side instruments
#   product_markets, encodes the market corresponding to each product
#   product_firms, encodes the firm corresponding to each product
#   nu, (K + 1) x R x T array of draws r = 1, ..., R of agents' heterogeneous tastes for 
#       prices and product characteristics k = 0, ..., K in markets t = 1, ..., T
#   D, L x R x T array of demographics l = 1, ..., L of agent draws r = 1, ..., R 
#      in markets t = 1, ..., Tt
# output:
#   val, value of GMM objective function at the given parameters

    obs = X.shape[0] # number of total observations
    K = X.shape[1] # number of product characteristics
    K_s = W.shape[1] # number of cost-shifters

    # set gamma = [alpha, 0, ..., 0]^T, sigma = diag(0, beta_nu(1), ..., beta_nu(L))
    gamma = np.zeros((K + 1, 1))
    gamma[0] = theta_2[0]

    sigma = np.zeros((K + 1, K + 1))
    np.fill_diagonal(sigma, np.append([0], theta_2[1:(K + 1)]))

    # solve for mean utilities and marginal costs at the given non-linear parameters
    delta = contraction_mapping(delta_0, tol, gamma, sigma, s, X, p, product_markets, nu, D)
    log_mc = np.log(compute_mc(delta, gamma, sigma, s, X, p, product_markets, product_firms, nu, D))

    # combine demand-side and supply-side data and instruments
    X_full = scipy.linalg.block_diag(X, W) # product characteristics + cost-shifters
    Z_full = scipy.linalg.block_diag(Z, Z_s) # demand-side instruments + supply-side instruments
    delta_full = np.vstack([delta, log_mc]) # mean utilities + log(marginal costs)

    # IV projection to recover linear parameters
    theta_1 = np.linalg.inv(X_full.T @ Z_full @ np.linalg.inv(phi) @ Z_full.T @ X_full) @ (
        X_full.T @ Z_full @ np.linalg.inv(phi) @ Z_full.T @ delta_full) 

    # structural errors
    xi = delta_full - X_full @ theta_1

    # GMM objective function value
    g = (1 / obs) * Z_full.T @ xi
    val = float(g.T @ np.linalg.inv(phi) @ g)

    print(theta_2, val)
    return val
