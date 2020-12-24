# Chooser option -- after N periods the owner gets to choose a European put or a European call.
# Vladimir Tsepelev, 22 December 2020.

import math

T = 0.25 # time horizon
N = 10 # chooser's expiration time
M = 15 # quantity of steps
t = T/M # step
sigma = 0.3 # volatility
r = 0.02 # interest rate
S0 = 100 # initial underlying stock price
K = 100 # strike
c = 0.01 # dividend yield

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

# price for European style options
def european_call():
    price = math.exp(-r*t)*(p*call_option_prices[i+1][j+1]+q*call_option_prices[i+1][j])
    return price

def european_put():
    price = math.exp(-r*t)*(p*put_option_prices[i+1][j+1]+q*put_option_prices[i+1][j])
    return price

def european_chooser():
    price = math.exp(-r*t)*(p*chooser_option_prices[i+1][j+1]+q*chooser_option_prices[i+1][j])
    return price

# create dictionaries, containing lists of options prices at every time step
call_option_prices = {}
for i in range(0,M+1):
    call_option_prices[i] = [None] * (i + 1)

put_option_prices = {}
for j in range(0,M+1):
    put_option_prices[j] = [None] * (j + 1)

chooser_option_prices = {}
for k in range(0,N+1):
    chooser_option_prices[k] = [None] * (k + 1)

# calculate possible final stock prices
stock_final_prices = []
for i in range(0,M+1):
    stock_final_prices.append(S0*math.pow(u,i)*math.pow(d,M-i))

# calculate possible call and put options final prices
for i in range(0,M+1):
    call_option_prices[M][i] = call(stock_final_prices[i], K)

for i in range(0,M+1):
    put_option_prices[M][i] = put(stock_final_prices[i], K)

# going backwards from call and put maturity time to chooser's maturity time
for i in range(M-1,N-1,-1):
    for j in range(0,i+1):
        call_option_prices[i][j] = european_call()
        put_option_prices[i][j] = european_put()

# calculate chooser's values at expiration
for j in range(0,N+1):
    chooser_option_prices[N][j] = max(call_option_prices[N][j], put_option_prices[N][j])

# going backwards from chooser's maturity time
for i in range(N-1,-1,-1):
    for j in range(0,i+1):
        chooser_option_prices[i][j] = european_chooser()

print('The price is ${0} for {1} steps.'.format(round(chooser_option_prices[0][0],2), M))
