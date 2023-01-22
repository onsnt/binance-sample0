# get data from the Data directory
import os
import glob
import matplotlib.pyplot as plt
import pandas as pd
import mplfinance as mpf
import numpy

from binance_enums import *

# Extracting Data for plotting
# for binance:
#  OpenTime	Open	High	Low	Close	Volume	Close time	Quote asset volume	Number of trades	Taker buy base asset volume	Taker buy quote asset volume	Ignore 
def plot_graph_hourly():

	range1 = [i for i in range(0,5)]
	col_names = ['Date', 'Open', 'High', 'Low', 'Close']

	path=os.path.dirname(os.path.abspath(__file__))
	fullpath = path+"/data/spot/daily/klines/"+DEF_SYMBOL+"/"+DEF_INTERVAL+"/"

	all_files = glob.glob(os.path.join(fullpath, "*.zip"))
	data = pd.concat((pd.read_csv(f,header=None, compression="zip", usecols=range1,names=col_names) for f in all_files),  ignore_index=True)

	ohlc = data.loc[:, ['Date', 'Open', 'High', 'Low', 'Close']]

	# Converting date into datetime format
	ohlc['Date'] = pd.to_datetime(ohlc['Date'], unit='ms')
	ohlc.index = pd.DatetimeIndex(ohlc['Date'])

	mpf.plot(ohlc,type='candle')

def plot_graph_procent():
	range1 = [i for i in range(0,5)]
	col_names = ['Date', 'Open', 'High', 'Low', 'Close']

	path=os.path.dirname(os.path.abspath(__file__))
	fullpath = path+"/data/spot/daily/klines/"+DEF_SYMBOL+"/"+DEF_INTERVAL+"/"

	all_files = glob.glob(os.path.join(fullpath, "*.zip"))
	data = pd.concat((pd.read_csv(f,header=None, compression="zip", usecols=range1,names=col_names) for f in all_files),  ignore_index=True)

	ohlc = data.loc[:, ['Date', 'Open', 'High', 'Low', 'Close']]

	# Converting date into datetime format
	ohlc['Date'] = pd.to_datetime(ohlc['Date'], unit='ms')
	ohlc.index = pd.DatetimeIndex(ohlc['Date'])
	
	ohlc['Close'].pct_change().plot()
	plt.show()


def plot_graph_ta(gr_type):
	if gr_type == 'procent':
		plot_graph_procent()
	elif gr_type == 'hourly':
		plot_graph_hourly()