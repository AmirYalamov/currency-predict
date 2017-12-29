# https://goo.gl/AoZQia, one of my GitHub projects' source code
import os
import sys
import requests
import numpy as np
import pandas
import csv
from keras.models import Sequential
from keras.layers import Dense

# https://goo.gl/1aK9Eo, an online tutorial
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

from keras import regularizers

# where csv file will be stored
FILE_NAME = "data.csv"

# returns list of data about currency including: time, open, high, low, close, volumefrom, volumeto
def getData (arg1, arg2):
    CC = arg1
    currency = arg2
    # closing value is 1 day behind, with closing time at 7:00pm EST
    priceH = requests.get("https://min-api.cryptocompare.com/data/histoday?fsym=" + CC + "&tsym=" + currency).json()["Data"]   # gets list of dictionaries
    return priceH

# returns a list of closing values for currency
def closeList (CC, currency):
    arg1 = CC
    arg2 = currency
    dataList = getData(arg1, arg2)
    closeList = []
    counter = 0
    for entry in dataList:
        counter += 1
        for key in entry:
            if key == 'close':
                value = entry.get(key)
                closeList.append(float(value))

    return closeList

# creates csv of closing values for currency
def writeToData(dataList):
    info = dataList
    with open(FILE_NAME, "w", newline='') as file:
        wr = csv.writer(file, quoting=csv.QUOTE_ALL)
        wr.writerow(info)

def price_prediction ():
    # Collect data from csv
    dataset = []

    with open(FILE_NAME, "r") as f:

        for line in f:
            priceL = line.split(",")

            for element in priceL:
                element = element.strip("\"\n")
                dataset.append(element)

    dataset = np.array(dataset)

    # create our dataset matrix (X = t and Y = t + 1)
    def create_dataset(data):
        data_X = [data[a + 2] for a in range(len(data) - 2)]
        return np.array(data_X), data[2:]

    train_X, train_Y = create_dataset(dataset)

    # Create and fit a miltilayer perceptron model
    model = Sequential()
    model.add(Dense(8, input_dim=1, activation='relu'))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(train_X, train_Y, epochs=200, batch_size=2, verbose=2, shuffle=True, initial_epoch=0)
    # Our prediction for tomorrow
    prediction = model.predict(np.array([dataset[2]]))
    result = "The price will move from %s to %s" % (dataset[2], prediction[0][0])

    return result

def main ():
    print("Which cryptocurrency would you like to check on?")
    CC = input("Enter code(e.g. 'BTC', 'ETH'): ")
    CC = CC.upper()
    print("What currency would you like to view the values in?")
    currency = input("Enter currency(e.g. 'USD', 'CAD'): ")
    currency = currency.upper()
    print("Closing price for " + CC + " in " + currency + " for last 31 days, with closing time as 12:00.00AM UTC :")
    print(closeList(CC, currency))
    writeToData(closeList(CC, currency))
    print(price_prediction())

main()
