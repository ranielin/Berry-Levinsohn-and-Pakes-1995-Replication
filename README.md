# Berry, Levinsohn, and Pakes (1995) Replication

Replication of the estimation of demand for automobiles in [Berry, Levinsohn, and Pakes (1995)](https://www.econometricsociety.org/publications/econometrica/1995/07/01/automobile-prices-market-equilibrium). The code provided replicates the point estimates of all linear and non-linear parameters (the first "parameter estimates" column of Table IV) in BLP (1995).

This replication is for expository purposes, i.e., to convey the basic fundamentals of the BLP demand estimation routine in an easy to understand format, and may not incorporate the most up-to-date practices for demand estimation. For practical uses of demand estimation, the following resources may be helpful:
* [Conlon and Gortmaker (2020)](https://chrisconlon.github.io/site/pyblp.pdf) and associated [PyBLP](https://pyblp.readthedocs.io/en/stable/index.html) Python library for what is, to my knowledge, the current best practices for the estimation of demand in differentiated products industries
* [Nevo (2000)](https://onlinelibrary.wiley.com/doi/10.1111/j.1430-9134.2000.00513.x) for a well-known "practitioner's guide" that provides additional tips and guidance on the implementation of BLP
* [Berry and Haile (2021)](http://www.econ.yale.edu/~pah29/Foundations.pdf) for a broader overview of demand estimation and associated IO literature

### Data and Instruments

Market-level data from BLP (1995) is obtained from the [hdm](https://cran.r-project.org/web/packages/hdm/index.html) (high-dimensional metrics) package for R. Census CPS data on the empirical distribution of income from 1971 to 1990 is obtained from [Gentzkow and Shapiro (2016)](https://web.stanford.edu/~gentzkow/research/blp_replication.zip)'s BLP replication repository.

Following BLP (1995) directly, there are three sets of instruments used for the demand-side: exogenous product characteristics themselves (i.e., non-price attributes), sums of the characteristics of other products produced by the same firm in the same market, and sums of the characteristics of products produced by other rival firms in the same market.

Supply-side instruments are similarly constructed, and include exogenous cost shifters, sums of the cost-shifters of other products produced by the same firm in the same market, sums of the cost-shifters of products produced by other rival firms in the same market, as well as the demand variable excluded from the pricing equation (miles per dollar). Following the [PyBLP data documentation](https://pyblp.readthedocs.io/en/stable/_api/pyblp.data.html#module-pyblp.data), the supply-side "rival" instrument corresponding to the "trend" variable is discarded due to near-perfect collinearity. 

### Simulating Market Shares

Prior to estimation, 500 random draws are taken in each market. The random draws are simulated random taste shocks, from a standard normal distribution, and incomes, which are derived empirically from estimating the distribution of income using Census data. 

Model-implied market shares are approximated as the average of share probabilities taken across the simulated draws. Note that this is a simpler approach than the original procedure used in BLP (1995), which incorporates importance sampling to reduce simulation error.

### Contraction Mapping

For given values of the non-linear parameters, product and price characteristics, simulated draws, and observed market shares, the iterative contraction mapping from BLP (1995) is applied with the logarithm of the ratio of observed market shares to the observed outside share used as the starting guess. The iteration is applied with a tolerance of 10e-12.

As shown in BLP (1995), this sequence of mean utilities converges to the unique vector of mean utilities equating model-implied market shares with observed market shares. 

### Recovering Marginal Costs

Similar to the simulation of market shares, share-price derivatives are numerically approximated by averaging across simulated draws. Firms are assumed to set prices in a static Bertrand-Nash equilibrium. From the first-order optimality condition, marginal costs are recovered given the observed price vector, market shares, and an ownership matrix whose (j, k)'th entry is equal to the share-price derivative of product j with respect to the price of product k if the two products are produced by the same firm in the same market and 0 otherwise.

### Estimation

Model parameters are estimated using two-step GMM. The objective function is computed by interacting demand or supply instruments with the corresponding model-implied demand or supply structural errors and applying an appropriate weight matrix. As described in Nevo (2000), the linear parameters can be recovered given the non-linear parameters using an IV projection, so it is sufficient to maximize over the non-linear parameters.

Estimation proceeds in two steps. In the first step, parameters are estimated using the identity weight matrix to obtain a consistent estimate of the optimal GMM weight matrix. In the second step, the parameters are re-estimated using the estimated optimal weight matrix to obtain the final estimates. In BLP (1995), observations are instead grouped by distinct automobile models and the GMM vectors are constructed for each model rather than for each distinct product-market combination. In their approach, the weight matrix is taken to be the sample variance-covariance matrix of model vectors rather than individual product-market vectors. It is straightforward to adapt this code in a similar way, if desired.

Optimization is performed using the L-BFGS-B gradient-based search routine. The original parameter estimates published in BLP (1995) are used as the starting search values and all non-linear parameters are constrained to be non-negative.