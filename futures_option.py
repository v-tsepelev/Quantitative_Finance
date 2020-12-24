# CRR model for the option written on a futures contract that expires after M periods.
# Vladimir Tsepelev, 21 December 2020.

import math

T = 0.25 # time horizon
N = 10 # option's maturity
M = 15 # futures' maturity
t = T/M # step
sigma = 0.3 # volatility
r = 0.02 # interest rate
u = math.exp(sigma*math.sqrt(T/M)) # up-factor
d = 1.0/u # down-factor
S0 = 100 # initial underlying stock price
K = 110 # strike
c = 0.01 # dividend yield

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

# create dictionaries, containing lists of option's and futures' prices at every time step
option_prices = {}
for i in range(0,M+1):
    option_prices[i] = [None] * (i + 1)

futures_prices = {}
for i in range(0,M+1):
    futures_prices[i] = [None] * (i + 1)

# final futures prices (same as stock prices)
stock_final_prices = []
for i in range(0,M+1):
    stock_final_prices.append(S0*math.pow(u,i)*math.pow(d,M-i))
futures_prices[M] = stock_final_prices

# going backwards from futures' maturity time to create futures lattice
for i in range(M-1,-1,-1):
    for j in range(0,i+1):
        futures_prices[i][j] = p*futures_prices[i+1][j+1]+q*futures_prices[i+1][j]

# calculate possible option final prices at maturity time -- choose call or put function
option_final_prices = []
for i in range(0,N+1):
    option_final_prices.append(call(futures_prices[N][i], K))

option_prices[N] = option_final_prices
early_exercise_nodes = []

# going backwards from option's maturity time -- uncomment european or american function, choose call or put for american style
for i in range(N-1,-1,-1):
    for j in range(0,i+1):
        #option_prices[i][j] = european()
        option_prices[i][j] = american(call(futures_prices[i][j], K))
        if option_prices[i][j] != math.exp(-r*t)*(p*option_prices[i+1][j+1]+q*option_prices[i+1][j]):
            early_exercise_nodes.append(i) # record early exercise nodes

print('The price is ${0} for {1} steps.'.format(round(option_prices[0][0],2), N))
# uncomment to show the early exercise time for American style option
if len(early_exercise_nodes) != 0:
    print('The early exercise time is t={0}.'.format(early_exercise_nodes[-1]))
else:
    print('It is not optimal to exercise the option early.')
