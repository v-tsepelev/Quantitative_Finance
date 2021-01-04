# Pricing a futures contract on a zero-coupon bond.
# Vladimir Tsepelev, 3 January 2021.

import math

M = 10 # bond maturity
N = 4 # futures maturity
Z = 100 # face value of bond
r = 0.05 # time zero interest rate
u = 1.10 # up-factor
d = 0.9 # down-factor

# risk-neutral probabilities
p = 0.5 # up
q = 1 - p # down

# create a short-rate lattice
interest_rates = []
for i in range(0,M+1):
    interest_rates.append([None] * (i+1))
interest_rates[0][0] = r

for i in range(1,M+1):
    for j in range(0,i+1):
        interest_rates[i][j] = round(r*math.pow(u,j)*math.pow(d,i-j),4)

# calculate bond prices at every node of the lattice
bond_prices = []
for i in range(0,M):
    bond_prices.append([None] * (i+1))
bond_prices.append([Z] * (M+1))

for i in range(M-1,-1,-1):
    for j in range(0,i+1):
        bond_prices[i][j] = round(math.pow(1+interest_rates[i][j],-1)*(p*bond_prices[i+1][j+1]+q*bond_prices[i+1][j]),2)

# calculate futures prices from futures' maturity to time zero
futures_prices = []
for i in range(N):
    futures_prices.append([None] * (i+1))
futures_prices.append(bond_prices[N])

for i in range(N-1,-1,-1):
    for j in range(0,i+1):
        futures_prices[i][j] = round(p*futures_prices[i+1][j+1]+q*futures_prices[i+1][j],2)
        
print(futures_prices[0][0])
