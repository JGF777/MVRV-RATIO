import data
import datetime
import main
import indicators
import pandas as pd
import streamlit as st
import time
from main import Brain



### FORMAT OF THE FRONT END

st.set_page_config(page_title="BTC-MVRV Strategy",
                   page_icon=":bar_chart:")

st.title(":bar_chart:BTC-MVRV BACKTEST")

# HIDE STYLE
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """

st.markdown(hide_st_style, unsafe_allow_html=True)

with st.container():
    st.write('This strategy is based on the MVRV ratio. When ratio is <=1, Bitcoin is considered to be undervalued. '
             'When the ratio is >3.9, it is considered to be overvalued.')
    st.write()

col1, col2 = st.columns(2)
with col1:
    d = st.date_input(
        "SELECT BEGINNING DATE OF THE BACKTEST",
        datetime.date(2014, 1, 1))
    st.write('Date selected:', d)
    e = datetime.datetime.combine(d, datetime.time.min)

with col2:
    d_end = st.date_input(
        "SELECT END DATE OF THE BACKTEST",
        datetime.date(2021, 3, 11))
    st.write('Date selected:', d_end)
    end = datetime.datetime.combine(d_end, datetime.time.min)


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

brain = Brain(dffinal)
buy, sell, fecha_inicio_index, fecha_final_index = brain.get_trades()
buyprices = dffinal['market-price'].iloc[buy]
sellprices = dffinal['market-price'].iloc[sell]



##SIDEBAR
st.sidebar.header("Select inputs here: ")
sma = st.sidebar.multiselect(
    "Select the SMAs: ",
    ['SMA25', 'SMA50', 'SMA100','SMA200']

)
st.sidebar.write("SMAs selected: ", sma)

mvrv_l = st.sidebar.slider("Select MVRV value for the lower range:",
                   value= 1.0, min_value=0.0, max_value=10.0, step=0.1)
st.sidebar.write("MVRV LOW: ", mvrv_l)

mvrv_h = st.sidebar.slider("Select MVRV value for the higher range:",
                   value=3.7, min_value=0.0, max_value=10.0, step=0.1)
st.sidebar.write("MVRV HIGH: ", mvrv_h)

st.set_option('deprecation.showPyplotGlobalUse', False)
# FINAL PART OF TEMPLATE
main_graph = st.pyplot(fig=graph_triggers, clear_figure=True)


with st.container():
    col1, col2, col3 = st.columns(3)

    col1.write("Growth of 1 USD: ")
    col1.metric("Strategy", "1000 USD")

    col2.write("Growth of 1 USD: ")
    col2.metric("Benchmark", "1500 USD")

    col3.write("Average trade's returns: ")
    col3.metric("Average trade", "150%")

