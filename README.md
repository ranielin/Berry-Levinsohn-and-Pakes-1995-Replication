# Berry, Levinsohn, and Pakes (1995) Replication

Replication of the estimation of demand for automobiles in [Berry, Levinsohn, and Pakes (1995)](https://www.econometricsociety.org/publications/econometrica/1995/07/01/automobile-prices-market-equilibrium). The code provided is for *expository* purposes, i.e., to convey the basic fundamentals of the BLP demand estimation routine in an easy to understand format. A detailed walkthrough accompanying the code can be found at [tbd].

As explained in [Gandhi and Nevo (2021)](https://www.nber.org/papers/w29257), the BLP algorithm is itself quite simple to implement, but in practice many "bells and whistles" are needed to improve computational speed and efficiency. This code is a bare-bones implementation of the BLP algorithm that generally does not incorporate the most up-to-date practices for demand estimation developed by IO economists. To that end, for practical use of demand estimation, the following resources may be helpful:
* [Conlon and Gortmaker (2020)](https://chrisconlon.github.io/site/pyblp.pdf) and associated [PyBLP](https://pyblp.readthedocs.io/en/stable/index.html) package for what is, to my knowledge, the current best practices for the estimation of demand in differentiated products industries
* [Nevo (2000)](https://onlinelibrary.wiley.com/doi/10.1111/j.1430-9134.2000.00513.x) for a well-known "practitioner's guide" that provides additional tips and guidance on the implementation of BLP
* [Berry and Haile (2021)](http://www.econ.yale.edu/~pah29/Foundations.pdf) for a broader overview of demand estimation in the industrial organization literature

## Data and Instruments

Market-level data from BLP (1995) is obtained from the [hdm](https://cran.r-project.org/web/packages/hdm/index.html) (high-dimensional metrics) package for R. Census CPS data on the empirical distribution of income from 1971 to 1990 is obtained from [Gentzkow and Shapiro (2015)](https://web.stanford.edu/~gentzkow/research/)'s BLP replication repository.

Following BLP (1995) directly, there are three sets of instruments used: exogenous product characteristics themselves (i.e., non-price attributes), sums of the characteristics of other products produced by the same firm in the same market, and sums of the characteristics of products produced by other rival firms in the same market.

## Simulation of Market Shares

Prior to estimation, <img src="https://render.githubusercontent.com/render/math?math=R"> random draws are taken in each market <img src="https://render.githubusercontent.com/render/math?math=t = 1, \dots, T">. The random draws are simulated individuals' random taste shocks <img src="https://render.githubusercontent.com/render/math?math=\{\nu_{it}\}_{i=1}^R \sim N(0, 1)"> and incomes <img src="https://render.githubusercontent.com/render/math?math=\{\log(y_{it}\}_{i=1}^R) \sim N(\mu_{dt}, \sigma_{dt}^2)">, where <img src="https://render.githubusercontent.com/render/math?math=\mu_{dt}"> and  <img src="https://render.githubusercontent.com/render/math?math=\sigma_{dt}^2"> are empirical income estimates from Census data. 

Model-implied market shares are approximated as <img src="https://render.githubusercontent.com/render/math?math=\sigma_{jt} = \frac{1}{R} \sum_{i = 1}^R \frac{\exp(\delta_{jt} %2b \sum_{l} x_{jt}^{(l)} \beta_{\nu}^{(l)} \nu_i^{(l)} - \alpha y_i / p_{jt})}{1 %2b \sum_{k = 1}^{J_t} \exp(\delta_{kt} %2b \sum_{l} x_{kt}^{(l)} \beta_{\nu}^{(l)} \nu_i^{(l)} - \alpha y_i / p_{kt})}"> where 
* <img src="https://render.githubusercontent.com/render/math?math=\sigma_{jt}"> is the model-implied market share of product <img src="https://render.githubusercontent.com/render/math?math=j"> in market <img src="https://render.githubusercontent.com/render/math?math=t">
* <img src="https://render.githubusercontent.com/render/math?math=\delta_{jt}"> is the mean utility of product <img src="https://render.githubusercontent.com/render/math?math=j"> in market <img src="https://render.githubusercontent.com/render/math?math=t"> 
* <img src="https://render.githubusercontent.com/render/math?math=x_{jt}^{(l)}"> is the <img src="https://render.githubusercontent.com/render/math?math=l">'th observed characteristic of product <img src="https://render.githubusercontent.com/render/math?math=j"> in market <img src="https://render.githubusercontent.com/render/math?math=t"> 
* <img src="https://render.githubusercontent.com/render/math?math=\beta_\nu^{(l)}"> is the non-linear random coefficient of the <img src="https://render.githubusercontent.com/render/math?math=l">'th product characteristic
* <img src="https://render.githubusercontent.com/render/math?math=\alpha"> is the price coefficient
* <img src="https://render.githubusercontent.com/render/math?math=p_{jt}"> is the price of product <img src="https://render.githubusercontent.com/render/math?math=j"> in market <img src="https://render.githubusercontent.com/render/math?math=t">.

This is a simpler scheme than the original procedure used in BLP (1995), which incorporates importance sampling to reduce simulation error.

## Contraction Mapping

