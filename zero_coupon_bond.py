# Compute the price of a zero-coupon bond that matures at time M and that has face value Z.
# Vladimir Tsepelev, 1 January 2021.

import math

M = 4 # maturity
Z = 100 # face value of bond
r = 0.06 # time zero interest rate
u = 1.25 # up-factor
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
        
print(bond_prices[0][0])
