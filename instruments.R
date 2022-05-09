library(hdm)
library(tidyverse)

dat <- read_csv("./data/estimation/BLP_1995_data.csv")
X <- read_csv("./data/estimation/X.csv")

# first set of instruments
# Z1, exogenous observed characteristics x_jt
Z1 <- X %>%
  select(-constant)

# second and third sets of instruments
# Z2, sum of x_j't where j' is also produced by firm j
# Z3, sum of x_j't where j' is produced by firms other than firm j
Z2 <- data.frame(matrix(0, nrow(X), ncol(X))) 
Z3 <- data.frame(matrix(0, nrow(X), ncol(X))) 
colnames(Z2) <- paste0("same_firm_", colnames(X))
colnames(Z3) <- paste0("rival_firm_", colnames(X))

for(idx in 1:nrow(dat)){
  this_market <- dat$market[idx]
  this_product <- dat$product[idx]
  this_firm <- dat$firm[idx]
  
  same_firm_products <- dat %>%
    slice(-idx) %>%
    filter(market == this_market & firm == this_firm) %>%
    select(colnames(X)) %>%
    colSums()
  
  rival_firm_products <- dat %>%
    filter(market == this_market & firm != this_firm) %>%
    select(colnames(X)) %>%
    colSums()
  
  Z2[idx, ] <- same_firm_products
  Z3[idx, ] <- rival_firm_products
  
}

Z <- cbind(Z1, Z2, Z3)
write_csv(Z, "./data/estimation/Z.csv")
