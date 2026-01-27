# Reinsurance Pricing & Capital Modelling Project

This project analyses the impact of different reinsurance structures on
portfolio risk and capital requirements using Monte Carlo simulation.

## Objective
To model a property insurance portfolio and assess how proportional and
non-proportional reinsurance structures affect volatility, tail risk,
and solvency capital.

## Methodology
- Claim frequency modelled using a Negative Binomial distribution
- Claim severity modelled using a heavy-tailed Pareto distribution
- Annual aggregate losses simulated via Monte Carlo methods
- Reinsurance structures analysed:
  - Quota Share
  - Per-risk Excess of Loss
  - Aggregate Excess of Loss
- Capital approximated using a VaR(99.5%)-based economic capital framework

## Key Results
- Per-risk XL provided the greatest capital efficiency (~51% capital relief)
- Aggregate XL imposed a hard cap on annual losses and reduced solvency capital
- Quota Share reduced volatility but was less capital-efficient

## Files
- `report/` – Full written report (PDF)
- `code/` – Python scripts for simulation, reinsurance and capital modelling
- `results/` – Summary output tables

## Tools
Python, NumPy, SciPy, pandas
