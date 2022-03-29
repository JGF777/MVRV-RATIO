"""
CLASS THAT HAS DIFFERENT METHODS TO ANALYZE PROFITABILITY AND VOLATILITY
"""
import pandas as pd
from statistics import mean
import matplotlib.pyplot as plt
import seaborn as sns

# STYLE GUIDE
sns.set_style('darkgrid')  # darkgrid, white grid, dark, white and ticks
plt.rc('axes', titlesize=18)  # fontsize of the axes title
plt.rc('axes', labelsize=14)  # fontsize of the x and y labels
plt.rc('xtick', labelsize=13)  # fontsize of the tick labels
plt.rc('ytick', labelsize=13)  # fontsize of the tick labels
plt.rc('legend', fontsize=13)  # legend fontsize
plt.rc('font', size=13)  # controls default text sizes


class Indicators:

    def __init__(self, dffinal, buy, sell, sellprices, buyprices, fecha_inicio_index, fecha_final_index):
        # INITIATE WITH MAIN DATAFRAME, TRADE'S PRICES AND BENCHMARK DATAFRAME
        self.dffinal = dffinal
        self.sellprices = sellprices
        self.buyprices = buyprices
        self.fecha_inicio_index = fecha_inicio_index
        self.fecha_final_index = fecha_final_index
        self.buy = buy
        self.sell = sell

    def print_trigger(self):
        """
        FUNCTION THAT PRINTS THE TRIGGER POINTS OF THE STRATEGY AND
        THE CORRESPONDING TECHNICAL INDICATORS
        """

        plt.figure(figsize=(12, 4))
        plt.scatter(self.dffinal.iloc[self.buy].index, self.dffinal['market-price'].iloc[self.buy], marker="^",
                    color='green', alpha=1, s=150)
        plt.scatter(self.dffinal.iloc[self.sell].index, self.dffinal['market-price'].iloc[self.sell], marker="v",
                    color='red', alpha=1, s=150)
        plt.plot(self.dffinal['market-price'], label="BTC-USD", color="k", linewidth=2.0)
        plt.plot(self.dffinal["SMA 25"], label="SMA25", color="magenta", linewidth=1.5)
        plt.plot(self.dffinal['SMA 50'], label="SMA50", color='blue', linewidth=1.5)
        plt.plot(self.dffinal["SMA 100"], label="SMA 100", color="b")
        plt.plot(self.dffinal['SMA 200'], label="SMA 200", color='m')
        plt.yscale("log")
        plt.ylabel("BTC-USD PRICE")
        plt.style.use("fivethirtyeight")
        plt.legend()
        plt.show()

    def rentabilidad_estrategia(self):
        """
        FUNCTION THAT CALCUlATES THE RETURN OF THE TRADES
        """

        profitsrel = []

        for i in range(len(self.sellprices)):
            retorno = round(((self.sellprices.values[i] - self.buyprices.values[i]) / self.buyprices.values[i]), 2)
            profitsrel.append(retorno)

        if len(self.buyprices) > len(self.sellprices):
            retorno_trade = round(((self.dffinal['market-price'].iloc[self.fecha_final_index] - self.buyprices.values[
                -1]) / self.buyprices.values[-1]), 2)
            profitsrel.append(retorno_trade)

        retorno_series = pd.DataFrame(profitsrel)
        retorno_series['df_cum_daily_returns'] = retorno_series.values.cumprod()
        acumulado_final = round(retorno_series['df_cum_daily_returns'].iloc[-1].astype(float), 2)
        retorno_medio = round(mean(profitsrel), 2)

        # OUTPUT ABOUT THE STRATEGY AND BENCHMARK RETURNS TO USER
        print(f"Crecimiento de 1$ estrategia {acumulado_final}$")
        print(f"Retorno medio por trade es de {retorno_medio * 100}%")
        return acumulado_final


    def rentabilidad_benchmark(self):
        """
        FUNCTION THAT CALCUlATES THE RETURN OF THE BUY AND HOLD STRATEGY
        """
        #retorno_benchmark = round(((self.dffinal['market-price'].iloc[self.fecha_final_index] - self.buyprices.values[0]) / self.buyprices.values[0]), 2)
        RETORNO_BUY0 = round(((self.dffinal['market-price'].iloc[self.fecha_final_index] - self.dffinal['market-price'].iloc[self.fecha_inicio_index]) /
							  self.dffinal['market-price'].iloc[self.fecha_inicio_index]), 2)


	# OUTPUT ABOUT THE STRATEGY AND BENCHMARK RETURNS TO USER
        print(f"Crecimiento de 1$ buy and hold {RETORNO_BUY0}$")
