# CRR model with dividend-paying stock.
# Vladimir Tsepelev, 21 December 2020.

import math

T = 0.25 # time horizon
M = 15 # quantity of steps
t = T/M # step
sigma = 0.3 # volatility
r = 0.02 # interest rate
S0 = 100 # initial underlying stock price
K = 110 # option's strike
c = 0.01 # stock's dividend yield

u = math.exp(sigma*math.sqrt(t)) # up-factor
d = 1.0/u # down-factor

# compute risk-neutral probabilities
p = (math.exp((r-c)*t)-math.exp(-sigma*math.sqrt(t)))/(math.exp(sigma*math.sqrt(t))-math.exp(-sigma*math.sqrt(t))) # up
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
    price = math.exp(-r*t)*(p*option_prices[i+1][j+1]+q*option_prices[i+1][j])
    return price

# price for American style, specify call or put in argument
def american(style):
    price = max(style, european())
    return price

# create dictionary, containing lists of options prices at every time step
option_prices = {}
for i in range(0,M+1):
    option_prices[i] = [None] * (i + 1)

# calculate possible final stock prices
stock_final_prices = []
for i in range(0,M+1):
    stock_final_prices.append(S0*math.pow(u,i)*math.pow(d,M-i))

# calculate possible option final prices -- choose call or put function
option_final_prices = []
for i in range(0,M+1):
    option_final_prices.append(put(stock_final_prices[i], K))

option_prices[M] = option_final_prices
early_exercise_nodes = []

# going backwards -- uncomment european or american function, choose call or put for american style
for i in range(M-1,-1,-1):
    for j in range(0,i+1):
        #option_prices[i][j] = european()
        option_prices[i][j] = american(put(S0*math.pow(u,j)*math.pow(d,i-j), K))
        if option_prices[i][j] != math.exp(-r*t)*(p*option_prices[i+1][j+1]+q*option_prices[i+1][j]):
            early_exercise_nodes.append(i) # record early exercise nodes

print('The price is ${0} for {1} steps.'.format(round(option_prices[0][0],2), M))
# uncomment to show the early exercise time for American style option
if len(early_exercise_nodes) != 0:
    print('The early exercise time is t={0}.'.format(early_exercise_nodes[-1]))
else:
    print('It is not optimal to exercise the option early.')
