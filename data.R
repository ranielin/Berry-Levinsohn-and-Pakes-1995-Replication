# organize market-level automobile data from the hdm
# package for estimation

library(hdm)
library(tidyverse)

dat <- BLP$BLP %>%
  mutate(price = price + 11.761,
         year = cdid + 1970,
         constant = 1,
         trend = trend + 71,
         ln_hpwt = log(hpwt),
         ln_mpg = log(mpg),
         ln_space = log(space)) %>%
  rename(market = cdid,
         product = model.id,
         firm = firm.id) %>%
  arrange(market, product)

# exogenous product characteristics
X <- dat %>%
  select(constant, hpwt, air, mpd, space) 

# cost shifters
W <- dat %>%
  select(constant, ln_hpwt, air, ln_mpg, ln_space, trend)

# prices
p <- dat %>%
  select(price)

# observed market shares
s <- dat %>%
  select(share)

# ln(market share / outside share)
s_s0 <- dat %>%
  select(y)

# number of products in each market t = 1, ..., T
product_markets <- dat %>%
  select(market)

# firm producing each product
product_firms <- dat %>%
  select(firm)
  
write_csv(dat, "./data/estimation/BLP_1995_data.csv")
write_csv(X, "./data/estimation/X.csv")
write_csv(W, "./data/estimation/W.csv")
write_csv(s, "./data/estimation/s.csv")
write_csv(s_s0, "./data/estimation/s_s0.csv")
write_csv(product_markets, "./data/estimation/product_markets.csv")
write_csv(product_firms, "./data/estimation/product_firms.csv")

