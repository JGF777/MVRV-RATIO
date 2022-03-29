"""
BACKTESTING OF MVRV STRATEGY BASED ON BTC-USD
THE STRATEGY IS BASED ON THE ASSUMPTION THAT THE MARKET IS UNDERVALUED WHEN MVRV ~1
AND OVERVALUED WHEN MVRV >3.7
"""

# REQUIRED MODULES
import data
import datetime
import indicators
import pandas as pd
import streamlit as st
import time



# CONSTANT VARIABLES REGARDING KEY INPUTS: INITIAL DATE, END DATE, MVRV_LOW AND MVRV HIGH
API_KEY = API_KEY
FECHA_INICIO = datetime.datetime(2014, 1, 1)                         
INICIO_UNIX = time.mktime(FECHA_INICIO.timetuple())
FECHA_FINAL = '2021-03-03'
MVRV_LOW = 1.2
MVRV_HIGH = 3.9
PARAMS = {
    'a': 'BTC',
    'api_key': API_KEY,
    's': int(INICIO_UNIX),
    'u': 1615032383             ## OJO ACTUALIZAR FECHA FINAL
}

# DATA REGARDING THE STRATEGY IN THE SELECTED PERIOD, PASS INDICATOR AS A STRING
# GET DATA FOR THE FIRST INDICATOR: PRICE USD CLOSE
url = 'https://api.glassnode.com/v1/metrics/market/price_usd_close'
dfprecios = data.Data(API_KEY, url, PARAMS, 'market-price')
dfprecios = dfprecios.get_data()

# GET DATA FOR THE SECOND INDICATOR: MVRV
url_mvrv = 'https://api.glassnode.com/v1/metrics/market/mvrv'
dfmvrv = data.Data(API_KEY, url_mvrv, PARAMS, 'mvrv')
dfmvrv = dfmvrv.get_data()

# CREATE AN UNIQUE DATAFRAME FOR THE STRATEGY ANALYSIS
dffinal = data.Data.combine_frames(dfprecios, dfmvrv)

# GETS RELEVANT TRADES ACCORDING TO STRATEGY'S LOGIC

class Brain:

    def __init__(self, dffinal):
        self.dffinal = dffinal

    def calculate_sma(self, period):
        self.dffinal[f"SMA {period}"] = self.dffinal['market-price'].rolling((7 * period)).mean()
        return self.dffinal

    def format_index(self):
        # FORMAT DF TO GET THE INDEX VALUES
        valor_inicial = self.dffinal[self.dffinal.index.normalize() == FECHA_INICIO].index.values
        t_inicio = pd.Timestamp(valor_inicial[0])
        fecha_inicio_index = self.dffinal.index.get_loc(t_inicio)
        valor_final = self.dffinal[self.dffinal.index.normalize() == FECHA_FINAL].index.values
        t_final = pd.Timestamp(valor_final[0])
        fecha_final_index = self.dffinal.index.get_loc(t_final)
        return fecha_inicio_index, fecha_final_index

    def get_trades(self):
        """
        FUNCTION RESPONSIBLE FOR THE LOGIC BEHIND THE STRATEGY.
        GETS ALL THE TRIGGER POINTS AND APPENDS THEM TO THE BUY&SELL LISTS
        """
        fecha_inicio_index, fecha_final_index = self.format_index()
        self.calculate_sma(25)
        self.calculate_sma(50)


        #LISTS OF BUYS AND TRADES BY INDEX
        buy = []
        sell = []

        #ITERATION OVER THE DF TO FIND TRADES
        on_trade = False

        for i in range(fecha_inicio_index, fecha_final_index):

            death_cross = self.dffinal["SMA 25"].iloc[i] < self.dffinal["SMA 50"].iloc[i] and \
                          self.dffinal["SMA 25"].iloc[i-1] > self.dffinal["SMA 50"].iloc[i-1] and on_trade

            if self.dffinal.mvrv.iloc[i] < MVRV_LOW and not on_trade:
                buy.append(i)
                on_trade = True
            elif (self.dffinal.mvrv.iloc[i] > MVRV_HIGH and on_trade) or death_cross:
                sell.append(i)
                on_trade = False
        return buy, sell, fecha_inicio_index, fecha_final_index


brain = Brain(dffinal)
buy, sell, fecha_inicio_index, fecha_final_index = brain.get_trades()

# SERIES CONTAINING THE PRICES OF THE PREVIOUS TRADES
buyprices = dffinal['market-price'].iloc[buy]
sellprices = dffinal['market-price'].iloc[sell]


# GRAPH AND RETURNS OF THE STRATEGY AND THE BENCHMARK
indicators = indicators.Indicators(dffinal, buy, sell, sellprices, buyprices, fecha_inicio_index, fecha_final_index)
return_strategy = indicators.rentabilidad_estrategia()
return_benchmark = indicators.rentabilidad_benchmark()
graph_triggers = indicators.print_trigger()




