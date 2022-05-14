import pandas as pd

from compute_shares import *

def contraction_mapping(delta_0, s, gamma, sigma, X, p, nu, D, product_markets, tol):
# solves for the vector of mean utilities that equates model-predicted shares
# with observed shares for given values of non-linear utility parameters
# using the BLP contraction mapping fixed-point formulation
# inputs:
#   delta_0, vector of initial guesses of product market mean utilities
#   s, vector of observed market shares of each product in each market
#   gamma, (K + 1) x L matrix of random coefficients of demographics
#   sigma, (K + 1) x (K + 1) diagonal matrix of random coefficients of 
#          unobserved heterogeneity 
#   X, matrix of observed characteristics of each product in each market
#   p, vector of prices of each product in each market
#   nu, (K + 1) x R x T array of draws r = 1, ..., R of agents' heterogeneous tastes for 
#       prices and product characteristics k = 0, ..., K in markets t = 1, ..., T
#   D, L x R x T array of demographics l = 1, ..., L of agent draws r = 1, ..., R 
#      in markets t = 1, ..., T
#   product_markets, encodes the market corresponding to each product
#   tol, tolerance level at which to stop the recursive iteration
# output:
#   delta, vector of mean utilities equating predicted shares with observed
#          shares

    error = 1.0
    delta_old = delta = delta_0

    while error > tol:
        delta_old = delta
        delta = delta_old + np.log(s) - np.log(
            compute_shares(delta_old, gamma, sigma, X, p, nu, D, product_markets)[0])
        error = np.max(np.abs(delta - delta_old))
  
    return delta