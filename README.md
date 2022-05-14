# Berry, Levinsohn, and Pakes (1995) Replication

Replication of the estimation of demand for automobiles in [Berry, Levinsohn, and Pakes (1995)](https://www.econometricsociety.org/publications/econometrica/1995/07/01/automobile-prices-market-equilibrium). The code provided is for *expository* purposes, i.e., to convey the basic fundamentals of the BLP demand estimation routine in an easy to understand format. A detailed walkthrough accompanying the code can be found at [tbd].

This code is a bare-bones implementation of the BLP algorithm that generally does not incorporate the most up-to-date practices for demand estimation developed by IO economists. To that end, for practical use of demand estimation, the following resources may be helpful:
* [Conlon and Gortmaker (2020)](https://chrisconlon.github.io/site/pyblp.pdf) and associated [PyBLP](https://pyblp.readthedocs.io/en/stable/index.html) package for what is, to my knowledge, the current best practices for the estimation of demand in differentiated products industries
* [Nevo (2000)](https://onlinelibrary.wiley.com/doi/10.1111/j.1430-9134.2000.00513.x) for a well-known "practitioner's guide" that provides additional tips and guidance on the implementation of BLP
* [Berry and Haile (2021)](http://www.econ.yale.edu/~pah29/Foundations.pdf) for a broader overview of demand estimation and associated IO literature

### Data and Instruments

Market-level data from BLP (1995) is obtained from the [hdm](https://cran.r-project.org/web/packages/hdm/index.html) (high-dimensional metrics) package for R. Census CPS data on the empirical distribution of income from 1971 to 1990 is obtained from [Gentzkow and Shapiro (2015)](https://web.stanford.edu/~gentzkow/research/blp_replication.zip)'s BLP replication repository.

Following BLP (1995) directly, there are three sets of instruments used for the demand-side: exogenous product characteristics themselves (i.e., non-price attributes), sums of the characteristics of other products produced by the same firm in the same market, and sums of the characteristics of products produced by other rival firms in the same market.

Supply-side instruments are similarly constructed, and include exogenous cost shifters, sums of the cost-shifters of other products produced by the same firm in the same market, sums of the cost-shifters of products produced by other rival firms in the same market, as well as the demand variable excluded from the pricing equation (miles per dollar).

### Simulating Market Shares

Prior to estimation, <img src="https://render.githubusercontent.com/render/math?math=R"> random draws are taken in each market <img src="https://render.githubusercontent.com/render/math?math=t = 1, \dots, T">. The random draws are simulated individuals' random taste shocks <img src="https://render.githubusercontent.com/render/math?math=\{\nu_{it}\}_{i=1}^R \sim N(0, 1)"> and incomes <img src="https://render.githubusercontent.com/render/math?math=\{\log(y_{it})\}_{i=1}^R \sim N(\mu_{dt}, \sigma_{dt}^2)">, where <img src="https://render.githubusercontent.com/render/math?math=\mu_{dt}"> and  <img src="https://render.githubusercontent.com/render/math?math=\sigma_{dt}^2"> are empirical income estimates from Census data. 

Model-implied market shares are approximated as <img src="https://render.githubusercontent.com/render/math?math=\tilde \sigma_{jt} \approx \frac{1}{R} \sum_{i = 1}^R \frac{\exp(\delta_{jt} %2b \sum_{l} x_{jt}^{(l)} \beta_{\nu}^{(l)} \nu_i^{(l)} - \alpha p_{jt} / y_i)}{1 %2b \sum_{k = 1}^{J_t} \exp(\delta_{kt} %2b \sum_{l} x_{kt}^{(l)} \beta_{\nu}^{(l)} \nu_i^{(l)} - \alpha p_{kt} / y_i)}">, where 
* <img src="https://render.githubusercontent.com/render/math?math=\tilde \sigma_{jt}"> is the model-implied market share of product <img src="https://render.githubusercontent.com/render/math?math=j"> in market <img src="https://render.githubusercontent.com/render/math?math=t">
* <img src="https://render.githubusercontent.com/render/math?math=\delta_{jt}"> is the mean utility of product <img src="https://render.githubusercontent.com/render/math?math=j"> in market <img src="https://render.githubusercontent.com/render/math?math=t"> 
* <img src="https://render.githubusercontent.com/render/math?math=x_{jt}^{(l)}"> is the <img src="https://render.githubusercontent.com/render/math?math=l">'th observed characteristic of product <img src="https://render.githubusercontent.com/render/math?math=j"> in market <img src="https://render.githubusercontent.com/render/math?math=t"> 
* <img src="https://render.githubusercontent.com/render/math?math=\beta_\nu^{(l)}"> is the non-linear random coefficient of the <img src="https://render.githubusercontent.com/render/math?math=l">'th product characteristic
* <img src="https://render.githubusercontent.com/render/math?math=\alpha"> is the price coefficient
* <img src="https://render.githubusercontent.com/render/math?math=p_{jt}"> is the price of product <img src="https://render.githubusercontent.com/render/math?math=j"> in market <img src="https://render.githubusercontent.com/render/math?math=t">.

This is a simpler scheme than the original procedure used in BLP (1995), which incorporates importance sampling to reduce simulation error.

### Contraction Mapping

For given values of the non-linear parameters, product and price characteristics, simulated individuals, and observed market shares, the iterative contraction mapping <img src="https://render.githubusercontent.com/render/math?math=\delta_t^{new} = \delta_t^{old} %2b \ln(\hat s_t) - \ln(\tilde \sigma_t)"> is applied with initial guess <img src="https://render.githubusercontent.com/render/math?math=\delta_{jt} = \ln(\hat s_{jt} / \hat s_{0t})">, where <img src="https://render.githubusercontent.com/render/math?math=\hat s_{jt}"> denotes oserved shares of product <img src="https://render.githubusercontent.com/render/math?math=j"> in market <img src="https://render.githubusercontent.com/render/math?math=t">, until <img src="https://render.githubusercontent.com/render/math?math=|| \delta_t^{new} - \delta_t^{old} || < 10^{-12}">. 

As shown in BLP (1995), this sequence of mean utilities converges to the unique vector of mean utilities equating model-implied market shares with observed market shares. 

### Recovering Marginal Costs

Similar to the simulation of market shares, share-price derivatives are numerically approximated by averaging across simulated individuals so that <img src="https://render.githubusercontent.com/render/math?math=-d\tilde\sigma_{mt}/dp_{nt} \approx \begin{cases} \frac{1}{R} \sum_{i=1}^{R} [\frac{\alpha}{y_i} f_{imt} (1 - f_{imt})] \quad \text{if} \quad m = n \\ \frac{1}{R} \sum_{i=1}^{R} [\frac{\alpha}{y_i} f_{imt} f_{int}] \quad \text{if} \quad m \ne n \end{cases}">

where <img src="https://render.githubusercontent.com/render/math?math=f_{imt}"> is the probability of (simulated) individual <img src="https://render.githubusercontent.com/render/math?math=i"> choosing product <img src="https://render.githubusercontent.com/render/math?math=m"> in market <img src="https://render.githubusercontent.com/render/math?math=t">.

Firms are assumed to set prices in a static Bertrand-Nash equilibrium. From the first-order optimality condition, marginal costs are given by <img src="https://render.githubusercontent.com/render/math?math=mc = p %2b \Omega^{-1} \hat s">, where <img src="https://render.githubusercontent.com/render/math?math=\Omega"> is a matrix whose [m, n]'th entry is  <img src="https://render.githubusercontent.com/render/math?math=-d\tilde\sigma_{mt}/dp_{nt}"> if products <img src="https://render.githubusercontent.com/render/math?math=m">,  <img src="https://render.githubusercontent.com/render/math?math=n"> are produced by the same firm and  <img src="https://render.githubusercontent.com/render/math?math=0"> otherwise.
