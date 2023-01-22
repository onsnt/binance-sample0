import os
import glob
import matplotlib.pyplot as plt
import pandas as pd
from binance_enums import *

from sklearn.linear_model import LinearRegression


def regressionmodel():
    range1 = [i for i in range(0, 5)]
    col_names = ['Date', 'Open', 'High', 'Low', 'Close']

    path = os.path.dirname(os.path.abspath(__file__))
    fullpath = path+"/data/spot/daily/klines/"+DEF_SYMBOL+"/"+DEF_INTERVAL+"/"

    all_files = glob.glob(os.path.join(fullpath, "*.zip"))
    data = pd.concat((pd.read_csv(f, header=None, compression="zip",
                     usecols=range1, names=col_names) for f in all_files),  ignore_index=True)

    ohlc = data.loc[:, ['Date', 'Open', 'High', 'Low', 'Close']]

    # Converting date into datetime format
    ohlc['Date'] = pd.to_datetime(ohlc['Date'], unit='ms')
    ohlc.index = pd.DatetimeIndex(ohlc['Date'])

    ohlc['S_3'] = ohlc['Close'].shift(1).rolling(window=3).mean()
    ohlc['S_9'] = ohlc['Close'].shift(1).rolling(window=9).mean()

    ohlc = ohlc.dropna()

    X = ohlc[['S_3', 'S_9']]
    X.head()

    y = ohlc['Close']
    y.head()

    t = TRAIN_PROC

    t = int(t*len(ohlc))

    # Train dataset
    X_train = X[:t]
    y_train = y[:t]

    # Test dataset
    X_test = X[t:]
    y_test = y[t:]

    linear = LinearRegression().fit(X_train, y_train)

    predicted_price = linear.predict(X_test)
    predicted_price = pd.DataFrame(predicted_price, index=y_test.index, columns=['price'])

    predicted_price.plot(figsize=(10, 5))

    y_test.plot()

    plt.legend(['predicted_price', 'actual_price'])
    plt.ylabel("Price " + DEF_SYMBOL)
    plt.show()
