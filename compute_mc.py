import numpy as np

from contraction_mapping import compute_shares

def compute_mc(delta, gamma, sigma, s, X, p, product_markets, product_firms, nu, D):
# solve for marginal costs for given values of non-linear parameters and mean utilities,
# assuming firms are setting prices in a Bertrand-Nash equilibrium
# inputs:
#   delta, vector of mean utilities of each product-market combination
#   gamma, (K + 1) x L matrix of random coefficients of demographics
#   sigma, (K + 1) x (K + 1) diagonal matrix of random coefficients of 
#          unobserved heterogeneity 
#   s, vector of observed market shares of each product in each market
#   X, matrix of observed characteristics of each product in each market
#   p, vector of prices of each product in each market
#   product_markets, encodes the market corresponding to each product
#   product_firms, encodes the firm corresponding to each product
#   nu, (K + 1) x R x T array of draws r = 1, ..., R of agents' heterogeneous tastes for 
#       prices and product characteristics k = 0, ..., K in markets t = 1, ..., T
#   D, L x R x T array of demographics l = 1, ..., L of agent draws r = 1, ..., R 
#      in markets t = 1, ..., T
# output:
#   mc, vector of marginal costs of each product in each market

    omega = compute_omega(delta, gamma, sigma, X, p, product_markets, product_firms, nu, D)
    mc = p - np.matmul(np.linalg.inv(omega), s) # first-order Bertrand equilibrium condition
    mc[mc < 0] = 0.001 # ensures marginal costs are nonnegative
    return mc

def compute_omega(delta, gamma, sigma, X, p, product_markets, product_firms, nu, D):
# computes derivatives of shares with respect to prices given mean utilities 
# and non-linear parameters using simulated draws of individuals
# inputs:
#   delta, vector of mean utilities of each product-market combination
#   gamma, (K + 1) x L matrix of random coefficients of demographics
#   sigma, (K + 1) x (K + 1) diagonal matrix of random coefficients of 
#          unobserved heterogeneity 
#   X, matrix of observed characteristics of each product in each market
#   p, vector of prices of each product in each market
#   product_markets, encodes the market corresponding to each product
#   product_firms, encodes the firm corresponding to each product
#   nu, (K + 1) x R x T array of draws r = 1, ..., R of agents' heterogeneous tastes for 
#       prices and product characteristics k = 0, ..., K in markets t = 1, ..., T
#   D, L x R x T array of demographics l = 1, ..., L of agent draws r = 1, ..., R 
#      in markets t = 1, ..., T
# output:
#   omega, matrix where entry [j, k] is the (negative) derivative of share j with 
#   respect to price k if the two products are produced by the same firm in the same 
#   market, and zero otherwise

    omega = np.zeros((X.shape[0], X.shape[0]))
    f_model = compute_shares(delta, gamma, sigma, X, p, product_markets, nu, D)[1]

    # iterate through markets, computing share-price derivatives separately in each
    # market
    for t in np.unique(product_markets):
        f_t = product_firms[np.where(product_markets == t)[0]] # list of firms in market t
        D_t = D[:, :, t-1] # simulated consumer demographics in market t
        alpha = np.matmul(gamma[0, :], D_t) # simulated price coefficients alpha_i

        # iterate through each firm in market t
        for f in np.unique(f_t):
            # get indices of other products produced by firm f in market t
            f_idx = np.intersect1d(
                np.where(product_markets == t)[0], np.where(product_firms == f)[0])

            # compute -ds_j/dp_k 
            for j in f_idx:
                for k in f_idx:
                    if j == k:
                        omega[j, k] = np.average(alpha * f_model[j, :] * (1 - f_model[j, :]))
                    else:
                        omega[j, k] = np.average(- alpha * f_model[j, :] * f_model[k, :])

    return omega