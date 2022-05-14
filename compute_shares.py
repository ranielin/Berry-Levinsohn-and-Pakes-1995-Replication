import numpy as np

def compute_shares(delta, gamma, sigma, X, p, nu, D, product_markets):
# computes model-implied market shares given mean utilities and non-linear 
# parameters using simulated draws of individuals
# inputs:
#   delta, vector of mean utilities of each product-market combination
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
# output:
#   s_model, vector of model-implied shares of each product in each market
#   s_i_model, matrix of model-implied choice probabilities of each product
#              in each market for each simulated individual

    K = X.shape[1] # number of product characteristics
    R = nu.shape[1] # number of simulated individuals
    s_model = np.zeros(delta.size) # initialize predicted shares
    s_i_model = np.zeros((delta.size, R)) # initialize choice probabilities
    
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
        s_ijt = np.exp(delta_jt + mu_it) / (1 + np.tile(
            np.sum(np.exp(delta_jt + mu_it), axis = 0), (J_t, 1)))
        s_i_model[np.where(product_markets == t)[0], :] = s_ijt

        # estimate market shares as equally-weighted average across individuals
        s_jt = np.average(s_ijt, axis = 1)
        s_model[np.where(product_markets == t)[0]] = s_jt
        
    s_model = s_model[:, np.newaxis]
    return [s_model, s_i_model]