# Pricing an option on a zero-coupon bond.
# Vladimir Tsepelev, 3 January 2021.

import math

M = 10 # bond maturity
Z = 100 # face value of bond
N = 6 # option maturity
K = 80 # option strike
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

# profit from call option
def call(bond_price, K):
    price = max(bond_price - K, 0)
    return price

# profit from put option
def put(bond_price, K):
    price = max(K - bond_price, 0)
    return price

# price for European style
def european():
    price = math.pow(1+interest_rates[i][j],-1)*(p*option_prices[i+1][j+1]+q*option_prices[i+1][j])
    return price

# price for American style, specify call or put in argument
def american(style):
    price = max(style, european())
    return price

option_prices = []
for i in range(N):
    option_prices.append([None] * (i+1))
        
# calculate possible option final prices -- choose call or put function
option_final_prices = []
for i in range(0,N+1):
    option_final_prices.append(round(put(bond_prices[N][i], K),2))
option_prices.append(option_final_prices)

# going backwards -- uncomment european or american function, choose call or put for american style
for i in range(N-1,-1,-1):
    for j in range(0,i+1):
        option_prices[i][j] = round(european(),2)
        #option_prices[i][j] = round(american(put(bond_prices[i][j], K)),2)

print(option_prices[0][0])
