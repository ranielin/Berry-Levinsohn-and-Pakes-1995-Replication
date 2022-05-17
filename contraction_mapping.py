import numpy as np

def contraction_mapping(delta_0, tol, gamma, sigma, s, X, p, product_markets, nu, D):
# solves for the vector of mean utilities that equates model-predicted shares
# with observed shares for given values of non-linear utility parameters
# using the BLP contraction mapping function
# inputs:
#   delta_0, vector of initial guesses of product market mean utilities
#   tol, tolerance level at which to stop the recursive iteration
#   gamma, (K + 1) x L matrix of random coefficients of demographics
#   sigma, (K + 1) x (K + 1) diagonal matrix of random coefficients of 
#          unobserved heterogeneity 
#   s, vector of observed market shares of each product in each market
#   X, matrix of observed product demand characteristics in each market
#   p, vector of prices of each product in each market
#   product_markets, encodes the market corresponding to each product
#   nu, (K + 1) x R x T array of draws r = 1, ..., R of agents' heterogeneous tastes for 
#       prices and product characteristics k = 0, ..., K in markets t = 1, ..., T
#   D, L x R x T array of demographics l = 1, ..., L of agent draws r = 1, ..., R 
#      in markets t = 1, ..., Tt
# output:
#   delta, vector of mean utilities equating predicted shares with observed
#          shares

    error = 1.0
    delta_old = delta = delta_0

    # iteratively update delta until ||delta - delta_old|| < tol
    while error > tol:
        delta_old = delta
        delta = delta_old + np.log(s) - np.log(
            compute_shares(delta_old, gamma, sigma, X, p, product_markets, nu, D)[0])
        error = np.max(np.abs(delta - delta_old)) 
  
    return delta

def compute_shares(delta, gamma, sigma, X, p, product_markets, nu, D):
# computes model-implied market shares given mean utilities and non-linear 
# parameters using simulated draws of individuals
# inputs:
#   delta, vector of mean utilities of each product-market combination
#   gamma, (K + 1) x L matrix of random coefficients of demographics
#   sigma, (K + 1) x (K + 1) diagonal matrix of random coefficients of 
#          unobserved heterogeneity 
#   X, matrix of observed characteristics of each product in each market
#   p, vector of prices of each product in each market
#   product_markets, encodes the market corresponding to each product
#   nu, (K + 1) x R x T array of draws r = 1, ..., R of agents' heterogeneous tastes for 
#       prices and product characteristics k = 0, ..., K in markets t = 1, ..., T
#   D, L x R x T array of demographics l = 1, ..., L of agent draws r = 1, ..., R 
#      in markets t = 1, ..., T
# output:
#   s_model, vector of model-implied shares of each product in each market
#   f_model, matrix of model-implied individual choice probabilities of each product
#            in each market conditional on values of nu_i and D_i

    K = X.shape[1] # number of product characteristics
    R = nu.shape[1] # number of simulated individuals
    s_model = np.zeros(delta.size) # initialize predicted shares
    f_model = np.zeros((delta.size, R)) # initialize choice probabilities
    
    # iterate across markets, computing shares within each market separately
    for t in np.unique(product_markets):

        # subset relevant attributes in each given market
        nu_t = nu[:, :, t-1] 
        D_t = D[:, :, t-1]
        J_t = np.where(product_markets == t)[0].size
        X_t = X[np.where(product_markets == t)[0], :]
        p_t = p[np.where(product_markets == t)[0], :]

        # mu_it is a J x R matrix of preference shocks for each product-individual combination
        mu_it =  np.matmul(np.matmul(np.concatenate((p_t, X_t), axis = 1), sigma), nu_t) - np.matmul(
            np.matmul(np.concatenate((p_t, X_t), axis = 1), gamma), D_t) 
        delta_jt = np.tile(delta[np.where(product_markets == t)[0]], R)

        # multinomial form for implied choice probabilities
        f_ijt = np.exp(delta_jt + mu_it) / (1 + np.tile(
            np.sum(np.exp(delta_jt + mu_it), axis = 0), (J_t, 1)))
        f_model[np.where(product_markets == t)[0], :] = f_ijt

        # estimate market shares as equally-weighted average across individuals
        s_jt = np.average(f_ijt, axis = 1)
        s_model[np.where(product_markets == t)[0]] = s_jt
        
    s_model = s_model[:, np.newaxis]
    return [s_model, f_model]