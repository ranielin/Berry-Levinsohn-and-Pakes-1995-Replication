# Berry, Levinsohn, and Pakes (1995) Replication

Replication of the estimation of demand for automobiles in [Berry, Levinsohn, and Pakes (1995)](https://www.econometricsociety.org/publications/econometrica/1995/07/01/automobile-prices-market-equilibrium). The code provided replicates the point estimates of all linear and non-linear parameters (the first "parameter estimates" column of Table IV) in BLP (1995).

This replication is for expository purposes, i.e., to convey the basic fundamentals of the BLP demand estimation routine in an easy to understand format, and may not incorporate the most up-to-date practices for demand estimation. For practical uses of demand estimation, the following resources may be helpful:
* [Conlon and Gortmaker (2020)](https://chrisconlon.github.io/site/pyblp.pdf) and associated [PyBLP](https://pyblp.readthedocs.io/en/stable/index.html) Python library for what is, to my knowledge, the current best practices for the estimation of demand in differentiated products industries
* [Nevo (2000)](https://onlinelibrary.wiley.com/doi/10.1111/j.1430-9134.2000.00513.x) for a well-known "practitioner's guide" that provides additional tips and guidance on the implementation of BLP
* [Berry and Haile (2021)](http://www.econ.yale.edu/~pah29/Foundations.pdf) for a broader overview of demand estimation and associated IO literature

A walkthrough of this replication can be found [here](https://ranielin.github.io/files/blp.html).

### Data and Instruments

Market-level data from BLP (1995) is obtained from the [hdm](https://cran.r-project.org/web/packages/hdm/index.html) (high-dimensional metrics) package for R. Census CPS data on the empirical distribution of income from 1971 to 1990 is obtained from [Gentzkow and Shapiro (2016)](https://web.stanford.edu/~gentzkow/research/blp_replication.zip)'s BLP replication repository.

Following BLP (1995) directly, there are three sets of instruments used for the demand-side: exogenous product characteristics themselves (i.e., non-price attributes), sums of the characteristics of other products produced by the same firm in the same market, and sums of the characteristics of products produced by other rival firms in the same market.

Supply-side instruments are similarly constructed, and include exogenous cost shifters, sums of the cost-shifters of other products produced by the same firm in the same market, sums of the cost-shifters of products produced by other rival firms in the same market, as well as the demand variable excluded from the pricing equation (miles per dollar). Following the [PyBLP data documentation](https://pyblp.readthedocs.io/en/stable/_api/pyblp.data.html#module-pyblp.data), the supply-side "rival" instrument corresponding to the "trend" variable is discarded due to near-perfect collinearity. 

### Simulating Market Shares

Prior to estimation, <img src="https://render.githubusercontent.com/render/math?math=R = 500"> random draws are taken in each market <img src="https://render.githubusercontent.com/render/math?math=t = 1, \dots, T">. The random draws <img src="https://render.githubusercontent.com/render/math?math=\hat F = \{\hat \nu_{it}, \hat D_{it}\}_{i=1}^R"> are simulated random taste shocks <img src="https://render.githubusercontent.com/render/math?math=\{\hat \nu_{it}\}_{i=1}^R \sim N(0, 1)"> and incomes <img src="https://render.githubusercontent.com/render/math?math=\{\ln(\hat y_{it})\}_{i=1}^R \sim N(\mu_{dt}, \sigma_{dt}^2)">, where <img src="https://render.githubusercontent.com/render/math?math=\hat D_{it} = \frac{1}{\hat y_{it}}">. The values <img src="https://render.githubusercontent.com/render/math?math=\mu_{dt}"> and <img src="https://render.githubusercontent.com/render/math?math=\sigma_{dt}^2"> are empirically derived from estimating the distribution of income using Census data. 

Model-implied market shares are approximated as <img src="https://render.githubusercontent.com/render/math?math=\tilde \sigma_{jt} = \frac{1}{R} \sum_{i = 1}^R \frac{\exp(\delta_{jt} %2b \sum_{k} x_{jt}^{(k)} \beta_{\nu}^{(k)} \nu_i^{(k)} - \alpha p_{jt} / y_i)}{1 %2b \sum_{l = 1}^{J_t} \exp(\delta_{lt} %2b \sum_{k} x_{lt}^{(k)} \beta_{\nu}^{(k)} \nu_i^{(k)} - \alpha p_{lt} / y_i)}">, where 
* <img src="https://render.githubusercontent.com/render/math?math=\tilde \sigma_{jt}"> is the approximated model-implied market share of product <img src="https://render.githubusercontent.com/render/math?math=j"> in market <img src="https://render.githubusercontent.com/render/math?math=t">
* <img src="https://render.githubusercontent.com/render/math?math=\delta_{jt}"> is the mean utility of product <img src="https://render.githubusercontent.com/render/math?math=j"> in market <img src="https://render.githubusercontent.com/render/math?math=t"> 
* <img src="https://render.githubusercontent.com/render/math?math=x_{jt}^{(k)}"> is the <img src="https://render.githubusercontent.com/render/math?math=k">'th observed characteristic of product <img src="https://render.githubusercontent.com/render/math?math=j"> in market <img src="https://render.githubusercontent.com/render/math?math=t"> 
* <img src="https://render.githubusercontent.com/render/math?math=\beta_\nu^{(k)}"> is the non-linear random coefficient of the <img src="https://render.githubusercontent.com/render/math?math=k">'th product characteristic
* <img src="https://render.githubusercontent.com/render/math?math=\alpha"> is the price coefficient
* <img src="https://render.githubusercontent.com/render/math?math=p_{jt}"> is the price of product <img src="https://render.githubusercontent.com/render/math?math=j"> in market <img src="https://render.githubusercontent.com/render/math?math=t">.

Note that this is a simpler approach than the original procedure used in BLP (1995), which incorporates importance sampling to reduce simulation error.

### Contraction Mapping

For given values of the non-linear parameters, product and price characteristics, simulated draws, and observed market shares, the iterative contraction mapping <img src="https://render.githubusercontent.com/render/math?math=\delta_t^{new} = \delta_t^{old} %2b \ln(\hat s_t) - \ln(\tilde \sigma_t)"> is applied with initial guess <img src="https://render.githubusercontent.com/render/math?math=\delta_{jt} = \ln(\hat s_{jt} / \hat s_{0t})">, where <img src="https://render.githubusercontent.com/render/math?math=\hat s_{jt}"> denotes observed shares of product <img src="https://render.githubusercontent.com/render/math?math=j"> in market <img src="https://render.githubusercontent.com/render/math?math=t">, until <img src="https://render.githubusercontent.com/render/math?math=|| \delta_t^{new} - \delta_t^{old} || < 10^{-12}">. 

As shown in BLP (1995), this sequence of mean utilities converges to the unique vector of mean utilities equating model-implied market shares with observed market shares. 

### Recovering Marginal Costs

Similar to the simulation of market shares, share-price derivatives are numerically approximated by averaging across simulated draws so that <img src="https://render.githubusercontent.com/render/math?math=-\frac{d \tilde \sigma_{jt}}{d p_{kt}} = \begin{cases} \frac{1}{R} \sum_{i = 1}^R [\frac{\alpha}{y_{it}} f_{ijt}(1 - f_{ijt})] \quad j = k \\ - \frac{1}{R}[\sum_{i = 1}^R \frac{\alpha}{y_{it}} f_{ijt} f_{ikt}] \qquad \: \ j \ne k \end{cases}">

where <img src="https://render.githubusercontent.com/render/math?math=f_{ijt}"> is the probability, conditional on <img src="https://render.githubusercontent.com/render/math?math=D_{it}"> and <img src="https://render.githubusercontent.com/render/math?math=\nu_{it}">, of choosing product <img src="https://render.githubusercontent.com/render/math?math=j"> in market <img src="https://render.githubusercontent.com/render/math?math=t">.

Firms are assumed to set prices in a static Bertrand-Nash equilibrium. From the first-order optimality condition, marginal costs are given by <img src="https://render.githubusercontent.com/render/math?math=mc = p - \Omega^{-1} \hat s">, where <img src="https://render.githubusercontent.com/render/math?math=\Omega"> is a matrix whose <img src="https://render.githubusercontent.com/render/math?math=[j, k]">'th entry is  <img src="https://render.githubusercontent.com/render/math?math=-d\tilde\sigma_{jt}/dp_{kt}"> if products <img src="https://render.githubusercontent.com/render/math?math=j">,  <img src="https://render.githubusercontent.com/render/math?math=k"> are produced by the same firm in market <img src="https://render.githubusercontent.com/render/math?math=t"> and <img src="https://render.githubusercontent.com/render/math?math=0"> otherwise.

### Two-Step GMM Estimation

The objective function to minimize is <img src="https://render.githubusercontent.com/render/math?math=Q(\theta) = (\frac{1}{N} \sum_{j, t} g_{jt}(\theta)^T) \Phi^{-1} (\frac{1}{N} \sum_{j, t} g_{jt}(\theta))">, where
* <img src="https://render.githubusercontent.com/render/math?math=\theta"> are the linear and non-linear model parameters
* <img src="https://render.githubusercontent.com/render/math?math=N"> = <img src="https://render.githubusercontent.com/render/math?math=\sum_t J_t"> denotes the total number of observations 
* <img src="https://render.githubusercontent.com/render/math?math=g_{jt}(\theta)"> is a vector whose <img src="https://render.githubusercontent.com/render/math?math=m">'th entry is the interacted term <img src="https://render.githubusercontent.com/render/math?math=z_{mjt} \xi_{jt}(\theta)">, where <img src="https://render.githubusercontent.com/render/math?math=z_{mjt}"> is the <img src="https://render.githubusercontent.com/render/math?math=m">'th demand or supply instrument and <img src="https://render.githubusercontent.com/render/math?math=\xi_{jt}(\theta)"> is the corresponding model-implied demand or supply structural error
* <img src="https://render.githubusercontent.com/render/math?math=\Phi"> is an appropriate GMM weight matrix.

Let <img src="https://render.githubusercontent.com/render/math?math=\theta = (\theta_1, \theta_2)"> denote the linear and non-linear model parameters, respectively. As described in Nevo (2000), <img src = "https://render.githubusercontent.com/render/math?math=\theta_1"> can be recovered for given values of <img src="https://render.githubusercontent.com/render/math?math=\theta_2"> using the IV projection matrix <img src="https://render.githubusercontent.com/render/math?math=Z \Phi^{-1} Z^T">, so it is sufficient to maximize <img src="https://render.githubusercontent.com/render/math?math=Q(\theta)"> over <img src="https://render.githubusercontent.com/render/math?math=\theta_2">.

Estimation proceeds in two steps. In the first step, <img src="https://render.githubusercontent.com/render/math?math=\theta"> is estimated using the identity weight matrix <img src="https://render.githubusercontent.com/render/math?math=\Phi_{GMM1} = I"> to obtain <img src="https://render.githubusercontent.com/render/math?math=\hat \theta_{GMM1}">. A consistent estimate of the optimal GMM weight matrix <img src="https://render.githubusercontent.com/render/math?math=E[g(\theta) g(\theta)^T]">, where the <img src="https://render.githubusercontent.com/render/math?math=m">'th entry of the vector <img src="https://render.githubusercontent.com/render/math?math=g(\theta)"> is <img src="https://render.githubusercontent.com/render/math?math=z_m \xi(\theta)">, is obtained by taking <img src="https://render.githubusercontent.com/render/math?math=\Phi_{GMM2} = \frac{1}{N} \sum_{j, t} g_{jt}(\hat \theta_{GMM1}) g_{jt}(\hat \theta_{GMM1})^T">. In the second step, <img src="https://render.githubusercontent.com/render/math?math=\theta"> is re-estimated using the weight matrix <img src="https://render.githubusercontent.com/render/math?math=\Phi = \Phi_{GMM2}"> to recover the final estimates <img src="https://render.githubusercontent.com/render/math?math=\hat \theta_{GMM2}">.

Note that in BLP (1995), observations are instead grouped by distinct automobile models and the GMM vectors <img src="https://render.githubusercontent.com/render/math?math=g_{model}(\theta)"> are constructed for each model rather than for each distinct product-market combination. In their approach, the weight matrix <img src="https://render.githubusercontent.com/render/math?math=\Phi_{GMM2}"> is taken to be the sample variance-covariance matrix of the vectors <img src="https://render.githubusercontent.com/render/math?math=g_{model}(\hat \theta_{GMM1})"> rather than across the vectors <img src="https://render.githubusercontent.com/render/math?math=g_{jt}(\hat \theta_{GMM1})">. It is straightforward to adapt this code in a similar way, if desired.

Optimization of <img src="https://render.githubusercontent.com/render/math?math=Q(\theta)"> is performed using the L-BFGS-B gradient-based search routine. The original parameter estimates published in BLP (1995) are used as the starting search values and all elements of <img src="https://render.githubusercontent.com/render/math?math=\theta_2"> are constrained to be non-negative.