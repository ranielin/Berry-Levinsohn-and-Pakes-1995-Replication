import numpy as np

from compute_omega import *

def bertrand_mc(delta, s, gamma, sigma, X, p, nu, D, product_markets, product_firms):
# solve for marginal costs for given values of non-linear parameters and mean utilities,
# assuming firms are setting prices in a Bertrand-Nash equilibrium
# inputs:
#   delta, vector of mean utilities of each product-market combination
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
#   product_firms, encodes the firm corresponding to each product
# output:
#   mc, vector of marginal costs of each product in each market

    omega = compute_omega(delta, gamma, sigma, X, p, nu, D, product_markets, product_firms)
    mc = p - np.matmul(np.linalg.inv(omega), s) # first-order Bertrand equilibrium condition
    mc[mc < 0] = 0.001 # ensures marginal costs are nonnegative
    return mc