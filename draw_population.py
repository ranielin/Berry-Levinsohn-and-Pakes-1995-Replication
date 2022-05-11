import numpy as np

def draw_population(R, T, nu_mean, nu_var, D_mean = None, D_var = None):
# generate random draws of consumer taste shocks nu_it ~ Normal(nu_mean, nu_var) and
# consumer demographics D_it ~ Normal(D_mean_t, D_var_t) in each market separately
# inputs:
#   R, number of random draws per market
#   T, number of distinct markets
#   nu_mean, mean of distribution of agents' heterogeneous tastes
#   nu_var, variance of distribution of agents' heterogeneous tastes
#   D_mean, L x T array of means of demographic variables l = 1, ..., L in markets t = 1, ..., T
#   D_var, L x T array of variance of demographic variables l = 1, ..., L in markets t = 1, ..., T
# outputs:
#   nu, R x T array of draws r = 1, ..., R of agents' heterogeneous tastes in markets t = 1, ..., T
#   D, L x R x T array of demographics l = 1, ..., L of agent draws r = 1, ..., R in markets t = 1, ..., T

    nu = np.random.normal(nu_mean, pow(nu_var, 0.5), (R, T))

    if D_mean is not None:
        if np.ndim(D_mean) == 1:
            L = 1
        else:
            L = np.shape(D_mean)[0]

        D = np.transpose(np.random.normal(D_mean, pow(D_var, 0.5), (R, L, T)), (1, 0, 2))
        return [nu, D]
    else:
        return nu