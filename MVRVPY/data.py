"""
CLASS THAT HAS PULLS THE RELEVANT DATA FROM GLASSNODE
"""
import pandas as pd
import requests


class Data:

    def __init__(self, API_KEY, url, params, name):
        self.API_KEY = API_KEY
        self.url = url
        self.params = params
        self.name = name

    def get_data(self):
        """
        THIS FUNCTION CALLS GLASSNODE API TO OBTAIN UPDATED DATA, SOME INDICATORS ARE LIMITED IN THE FREE VERSION
        IT RETURNS A FORMATTED DATAFRAME
        """

        res = requests.get(self.url, self.params)
        df = pd.read_json(res.text, convert_dates=['t'])
        df.rename(columns={'t': 'Timestamp', 'v': self.name}, inplace=True)
        df.set_index('Timestamp', inplace=True)

        return df

    def combine_frames(*args):
        """
        FUNCTION THAT TAKES THE DATAFRAMES OF THE INDICATORS AND C
        COMBINES THEM IN A FINAL DATAFRAME
        """

        dffinal = pd.concat([*args], axis=1)
        dffinal.index = pd.to_datetime(dffinal.index)

        return dffinal
