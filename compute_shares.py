from numpy import np

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
#   nu, K x R x T array of draws r = 1, ..., R of agents' heterogeneous tastes for 
#       product characteristics k = 1, ..., K in markets t = 1, ..., T
#   D, L x R x T array of demographics l = 1, ..., L of agent draws r = 1, ..., R 
#      in markets t = 1, ..., T
#   product_markets, encodes the market corresponding to each product
# output:
#   s_model, vector of model-implied shares of each product in each market

    s_model = np.zeros(delta.size) # initialize predicted shares
    K = X.shape[1] # number of product characteristics
    R = nu.shape[1] # number of simulated individuals
    
    # iterate across markets, computing shares within each market separately
    for t in np.unique(product_markets):

        # subset relevant attributes in each given market
        nu_t = nu[:, :, t-1] 
        D_t = D[:, :, t-1]
        J_t = np.where(product_markets == t)[0].size
        X_t = X[np.where(product_markets == t)[0], :]
        p_t = p[np.where(product_markets == t)[0], :]

        # mu_it is a J x R matrix of preference shocks for each product-individual combination
        # in general, mu_it also includes demographics from gamma, but in BLP gamma = 0 and
        # the first element of sigma is 0 because the price coefficient alpha is constant
        mu_it =  np.matmul(np.matmul(X_t, sigma[1:K+1, 1:K+1]), nu_t) 
        price_effect_it = np.tile(p_t, (1, R)) / np.tile(D_t, (J_t, 1))
        delta_jt = np.tile(delta[np.where(product_markets == t)[0]], R)

        # multinomial form for implied choice probabilities
        s_ijt = np.exp(delta_jt + mu_it - price_effect_it) / (1 + np.tile(
            np.sum(np.exp(delta_jt + mu_it - price_effect_it), axis = 0), (J_t, 1)))

        # estimate market shares as equally-weighted average across individuals
        s_jt = np.average(s_ijt, axis = 1)
        s_model[np.where(product_markets == t)[0]] = s_jt
    return s_model