# Calculating P&L from selling M European put or call options and then delta-hedging these options by following a self-financing trading strategy that attempts to replicate the payoff of these options.
# Vladimir Tsepelev, 16 February 2021.

import math
import statistics
import pandas as pd
from scipy.stats import norm

T = 0.25 # option's maturity (T = 1 corresponds for 1 year)
K = 50 # option's strike
r = 0.02 # risk-free interest rate in the money market
c = 0.0 # stock's dividend yield
M = 100000 # number of options
N = 50 # number of hedging periods
sigma = 0.30 # implied volatility
t = T/N # time step

# reading stock prices from .csv file located in the same directory (can enter list of stock prices manually as well)
stock_price = [float(x) for x in pd.read_csv("stock_data.csv").values]

# function computing value of Delta Greek, specify call or put in argument
def delta(type, S, T, K, r, c, sigma) -> float:
    d_1 = (math.log(S/K)+(r-c+math.pow(sigma,2)/2)*T)/(sigma*math.sqrt(T))
    if type == "call":
        return math.exp(-c*T)*norm.cdf(d_1)
    elif type == "put":
        return math.exp(-c*T)*norm.cdf(d_1)-math.exp(-c*T)

# function computing option's payoff at maturity, specify call or put in argument
def option_payoff(type, S, K) -> float:
    if type == "call":
        return max(S - K, 0)
    elif type == "put":
        return max(K - S, 0)

# set up the initial value of portfolio as a price of sold options given by Black-Scholes formula
portfolio = [0] * (N+1)
portfolio[0] = (stock_price[0]*math.exp(-c*T)*norm.cdf((math.log(stock_price[0]/K)+(r-c+math.pow(sigma,2)/2)*T)/(sigma*math.sqrt(T))) - K*math.exp(-r*T)*norm.cdf((math.log(stock_price[0]/K)+(r-c+math.pow(sigma,2)/2)*T)/(sigma*math.sqrt(T))-sigma*math.sqrt(T))) * M

# initialize list containing number of stocks held in portfolio at every time step
N_of_stocks = []

# initialize list containing amount of money invested in money market (cash account) in porfolio at every time step
money_market = []

# initialize list containing log-returns
log_returns = []

# calculating value of self-financing portfolio at every time step -- choose call or put in Delta Greek
for i in range(N):
    N_of_stocks.append(delta("call",stock_price[i],T-t*i,K,r,c,sigma) * M)
    money_market.append(portfolio[i] - N_of_stocks[i] * stock_price[i])
    portfolio[i+1] = portfolio[i] + N_of_stocks[i] * (stock_price[i+1] + stock_price[i]*c*t - stock_price[i]) + money_market[i] * (math.exp(r*t) - 1)
    log_returns.append(math.log(stock_price[i+1]/stock_price[i]))

# rounding calculated values
N_of_stocks = [round(n) for n in N_of_stocks]
money_market = [round(m) for m in money_market]
portfolio = [round(v) for v in portfolio]

# annualized average return
average_return = round(100*((sum(log_returns) / len(log_returns)) / t),2)

# annualized standard deviation of returns
standard_deviation_of_return = round(100*(statistics.stdev(log_returns) * math.sqrt(1/t)),2)

# total hedging P&L -- choose call or put in option's payoff
hedging_PnL = round(portfolio[-1] - option_payoff("call",stock_price[-1],K) * M,2)

print("Total hedging P&L is ${0} with avg return {1}% and std deviation {2}%.".format(hedging_PnL, average_return, standard_deviation_of_return))
