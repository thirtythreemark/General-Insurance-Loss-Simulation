# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 16:53:42 2026

@author: Mark
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Jan 25 23:13:18 2026

@author: Mark
"""

import numpy as np


#------- defining parameter ------
M = 100_000 
mu_N = 25
var_N = 50
p = mu_N / var_N
r = mu_N**2 / (var_N - mu_N)

xm = 25_000                
alpha = 1.8      

rng = np.random.default_rng(42) #setting sed

#--------simulating claim frequency------
N = rng.negative_binomial(n=r, p=p, size=M)

#--------simulating aggregate annual net and grosscan losses --------

S_net = np.zeros(M)
S_gross_quote = np.zeros(M)
S_gross_XL = np.zeros(M)

d = 250_000      # retention
L = 2_000_000    # limit
q = 0.2          # quote %
A = 3_500_000    # aggregate retention
LA = 3_000_000   # aggregate limit


for i, n_i in enumerate(N):
    if n_i > 0:
        X = xm * (1 + rng.pareto(alpha, size=n_i)) #if that year have claims(n_i>0), then simulate single claim amount n_i times
        Z_quote = q * X
        Y_quote = (1-q) * X
        Z_XL = np.minimum(np.maximum(X-d,0),L)
        Y_XL = X-np.minimum(np.maximum(X-d,0),L)
        S_net[i] = np.sum(X)
        S_gross_quote[i] = Y_quote.sum()
        S_gross_XL[i] = Y_XL.sum()
       
S_gross_aggXL = S_net - np.minimum(np.maximum( S_net -A,0),LA)

#--------statistic of aggregate loss (net and gross)----------
mean_S_net = S_net.mean()
sd_S_net = S_net.std(ddof=1)
mean_S_gross_XL = S_gross_XL.mean()
sd_S_gross_XL = S_gross_XL.std(ddof=1)
mean_S_gross_quote = S_gross_quote.mean()
sd_S_gross_quote = S_gross_quote.std(ddof=1)
mean_S_gross_aggXL = S_gross_aggXL.mean()
sd_S_gross_aggXL = S_gross_aggXL.std(ddof=1)


def var_tvar_capital(losses, q=0.99):
    mean = losses.mean()
    var_q = np.quantile(losses, q)
    tvar_q = losses[losses >= var_q].mean()
    cap_var = var_q - mean
    cap_tvar = tvar_q - mean
    return var_q, tvar_q, cap_var, cap_tvar


VaR_99_net, TVaR_99_net, cap_VaR_99_net, cap_TVaR_99_net = var_tvar_capital(S_net, q=0.99)
VaR_995_net, TVaR_995_net, cap_VaR_995_net, cap_TVaR_995_net = var_tvar_capital(S_net, q=0.995)
VaR_99_gross_XL, TVaR_99_gross_XL, cap_VaR_99_gross_XL, cap_TVaR_99_gross_XL = var_tvar_capital(S_gross_XL, q=0.99)
VaR_995_gross_XL, TVaR_995_gross_XL, cap_VaR_995_gross_XL, cap_TVaR_995_gross_XL = var_tvar_capital(S_gross_XL, q=0.995)
VaR_99_gross_quote, TVaR_99_gross_quote, cap_VaR_99_gross_quote, cap_TVaR_99_gross_quote = var_tvar_capital(S_gross_quote, q=0.99)
VaR_995_gross_quote, TVaR_995_gross_quote, cap_VaR_995_gross_quote, cap_TVaR_995_gross_quote = var_tvar_capital(S_gross_quote, q=0.995)
VaR_99_gross_aggXL, TVaR_99_gross_aggXL, cap_VaR_99_gross_aggXL, cap_TVaR_99_gross_aggXL = var_tvar_capital(S_gross_aggXL, q=0.99)
VaR_995_gross_aggXL, TVaR_995_gross_aggXL, cap_VaR_995_gross_aggXL, cap_TVaR_995_gross_aggXL = var_tvar_capital(S_gross_aggXL, q=0.995)

#-------------capital calculation-------------------
print("-------------------------------------")
print("Gross Loss:")
print(f"Mean annual net loss : £{mean_S_net:,.0f}")
print(f"Std dev annual net loss : £{sd_S_net:,.0f}")
print(f"VaR 99% : £{VaR_99_net:,.0f} | TVaR 99%: £{TVaR_99_net:,.0f}")
print(f"VaR 99.5% : £{VaR_995_net:,.0f} | TVaR 99.5%: £{TVaR_995_net:,.0f}")
print(f"capital at VaR 99% : £{cap_VaR_99_net:,.0f} | TVaR 99%: £{cap_TVaR_99_net:,.0f}")
print(f"capital at VaR 99.5% : £{cap_VaR_995_net:,.0f} | TVaR 99.5%: £{cap_TVaR_995_net:,.0f}")
print("-------------------------------------")
print("Net loss with per-risk XL reinsurance:")
print(f"Mean annual gross loss : £{mean_S_gross_XL:,.0f}")
print(f"Std dev annual gross loss : £{sd_S_gross_XL:,.0f}")
print(f"VaR 99% after per-risk XL reinsurance: £{VaR_99_gross_XL:,.0f} | TVaR 99%: £{TVaR_99_gross_XL:,.0f}")
print(f"VaR 99.5% after per-risk XL reinsurance: £{VaR_995_gross_XL:,.0f} | TVaR 99.5%: £{TVaR_995_gross_XL:,.0f}")
print(f"capital at VaR 99% after per-risk XL reinsurance: £{cap_VaR_99_gross_XL:,.0f} | TVaR 99%: £{cap_TVaR_99_gross_XL:,.0f}")
print(f"capital at VaR 99.5% after per-risk XL reinsurance: £{cap_VaR_995_gross_XL:,.0f} | TVaR 99.5%: £{cap_TVaR_995_gross_XL:,.0f}")
print("-------------------------------------")
print("Net loss with quote share reinsurance:")
print(f"Mean annual gross loss : £{mean_S_gross_quote:,.0f}")
print(f"Std dev annual gross loss : £{sd_S_gross_quote:,.0f}")
print(f"VaR 99% after quote reinsurance: £{VaR_99_gross_quote:,.0f} | TVaR 99%: £{TVaR_99_gross_quote:,.0f}")
print(f"VaR 99.5% after quote reinsurance: £{VaR_995_gross_quote:,.0f} | TVaR 99.5%: £{TVaR_995_gross_quote:,.0f}")
print(f"capital at VaR 99% after quote share reinsurance: £{cap_VaR_99_gross_quote:,.0f} | TVaR 99%: £{cap_TVaR_99_gross_quote:,.0f}")
print(f"capital at VaR 99.5% after quote share reinsurance: £{cap_VaR_995_gross_quote:,.0f} | TVaR 99.5%: £{cap_TVaR_995_gross_quote:,.0f}")
print("-------------------------------------")
print("Net loss with aggregate XL reinsurance:")
print(f"Mean annual gross loss : £{mean_S_gross_aggXL:,.0f}")
print(f"Std dev annual gross loss : £{sd_S_gross_aggXL:,.0f}")
print(f"VaR 99% after aggregare XL reinsurance: £{VaR_99_gross_aggXL:,.0f} | TVaR 99%: £{TVaR_99_gross_aggXL:,.0f}")
print(f"VaR 99.5% after aggregate XL reinsurance: £{VaR_995_gross_aggXL:,.0f} | TVaR 99.5%: £{TVaR_995_gross_aggXL:,.0f}")
print(f"capital at VaR 99% after aggregate XL reinsurance: £{cap_VaR_99_gross_aggXL:,.0f} | TVaR 99%: £{cap_TVaR_99_gross_aggXL:,.0f}")
print(f"capital at VaR 99.5% after aggregate XL reinsurance: £{cap_VaR_995_gross_aggXL:,.0f} | TVaR 99.5%: £{cap_TVaR_995_gross_aggXL:,.0f}")
print("-------------------------------------")


