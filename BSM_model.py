# Implementation of Black-Scholes-Merton option's pricing model.
# Vladimir Tsepelev, vlt8 at pitt dot edu, September 22 2018.

import math

T = 2 # quantity of time steps
u = 2 # up-factor
d = 0.5 # down-factor
r = 0.25 # interest rate
S0 = 4 # initial underlying stock price
K = 5 # strike

# compute risk-neutral probabilities
p = (1+r-d)/(u-d) # up
q = (u-1-r)/(u-d) # down

# profit from call option
def call(stock_price, K):
    price = max(stock_price - K, 0)
    return price

# profit from put option
def put(stock_price, K):
    price = max(K - stock_price, 0)
    return price

# price for European style
def european():
    price = 1.0/(1+r)*(p*option_prices[i+1][j+1]+q*option_prices[i+1][j])
    return price

# price for American style, specify call or put in argument
def american(style):
    price = max(style, european())
    return price

stock_final_prices = []
option_final_prices = []

# create dictionary, containing lists of options prices at every time step
option_prices = {}
for i in range(0,T+1):
    option_prices[i] = [None] * (i + 1)

# calculate possible final stock prices
for i in range(0,T+1):
    stock_final_prices.append(S0*math.pow(u,i)*math.pow(d,T-i))

# calculate possible option final prices -- choose call or put function
for i in range(0,T+1):
    option_final_prices.append(call(stock_final_prices[i], K))

option_prices[T] = option_final_prices

# going backwards -- uncomment european or american function, choose call or put for american style
for i in range(T-1,-1,-1):
    for j in range(0,i+1):
        option_prices[i][j] = european()
        #option_prices[i][j] = american(put(S0*math.pow(u,j)*math.pow(d,i-j), K))

print(option_prices[0][0])
