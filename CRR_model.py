# Implementation of Cox-Ross-Rubinstein option's pricing model.
# Vladimir Tsepelev, vlt8 at pitt dot edu, September 22 2018.

import math

T = 0.25 # time horizon
M = 99 # quantity of steps
t = T/M # step
sigma = 0.1391 # volatility
r = 0.0214 # interest rate
u = math.exp(sigma*math.sqrt(t)) # up-factor
d = 1.0/u # down-factor
S0 = 2888.60 # initial underlying stock price
K = 2885 # strike

# compute risk-neutral probabilities
p = (math.exp(r*t)-math.exp(-sigma*math.sqrt(t)))/(math.exp(sigma*math.sqrt(t))-math.exp(-sigma*math.sqrt(t))) # up
q = 1 - p # down

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
    price = 1.0/(1+r*t)*(p*option_prices[i+1][j+1]+q*option_prices[i+1][j])
    return price

# price for American style, specify call or put in argument
def american(style):
    price = max(style, european())
    return price

stock_final_prices = []
option_final_prices = []

# create dictionary, containing lists of options prices at every time step
option_prices = {}
for i in range(0,M+1):
    option_prices[i] = [None] * (i + 1)

# calculate possible final stock prices
for i in range(0,M+1):
    stock_final_prices.append(S0*math.pow(u,i)*math.pow(d,M-i))

# calculate possible option final prices -- choose call or put function
for i in range(0,M+1):
    option_final_prices.append(put(stock_final_prices[i], K))

option_prices[M] = option_final_prices

# going backwards -- uncomment european or american function, choose call or put for american style
for i in range(M-1,-1,-1):
    for j in range(0,i+1):
        #option_prices[i][j] = european()
        option_prices[i][j] = american(call(S0*math.pow(u,j)*math.pow(d,i-j), K))

print('The price is ${0} for {1} steps.'.format(option_prices[0][0], M))
