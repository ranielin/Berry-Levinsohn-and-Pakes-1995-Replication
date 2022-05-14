import numpy as np

from compute_shares import *

def compute_omega(delta, gamma, sigma, X, p, nu, D, product_markets, product_firms):
# computes derivatives of shares with respect to prices given mean utilities 
# and non-linear parameters using simulated draws of individuals
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
#   product_firms, encodes the firm corresponding to each product
# output:
#   omega, matrix where entry [i, j] is the (negative) derivative of share i with 
#   respect to price j if the two products are produced by the same firm in the same 
#   market, and zero otherwise

    omega = np.zeros((X.shape[0], X.shape[0]))
    s_i_model = compute_shares(delta, gamma, sigma, X, p, nu, D, product_markets)[1]

    # iterate through markets, computing share-price derivatives separately in each
    # market
    for t in np.unique(product_markets):
        f_t = product_firms[np.where(product_markets == t)[0]] # list of firms in market t
        D_t = D[:, :, t-1] # simulated conumser demographics in market t
        alpha = np.matmul(gamma[0, :], D_t) # simulated price coefficients alpha_i

        # iterate through each firm in market t
        for f in np.unique(f_t):
            # get indices of other products produced by firm f in market t
            f_idx = np.intersect1d(
                np.where(product_markets == t)[0], np.where(product_firms == f)[0])

            # compute -ds_i/dp_j 
            for i in f_idx:
                for j in f_idx:
                    if i == j:
                        omega[i, j] = np.average(alpha * s_i_model[i, :] * (1 - s_i_model[i, :]))
                    else:
                        omega[i, j] = np.average(- alpha * s_i_model[i, :] * s_i_model[j, :])

    return omega