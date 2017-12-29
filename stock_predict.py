import os
import sys
import requests
import numpy as np

from keras.models import Sequential
from keras.layers import Dense


# Where the csv file will be stored
FILE_NAME = 'historical.csv'


def get_historical(quote):
    # Download our file from google finance
    url = 'http://www.google.com/finance/historical?q=NASDAQ%3A' + quote + '&output=csv'
    r = requests.get(url, stream=True)

    if r.status_code != 400:
        with open(FILE_NAME, 'wb') as f:
            for chunk in r:
                f.write(chunk)
        return True


def stock_prediction():
    # Collect data from csv
    dataset = []

    with open(FILE_NAME) as f:
        for n, line in enumerate(f):
            if n != 0:
                dataset.append(float(line.split(',')[1]))

    dataset = np.array(dataset)

    # create our dataset matrix (X=t and Y = t+1)
    def create_dataset(data):
        data_X = [data[a + 1] for a in range(len(data) - 2)]
        return np.array(data_X), data[2:]

    train_X, train_y = create_dataset(dataset)

    # Create and fit Multilinear Perceptron model
    model = Sequential()
    model.add(Dense(8, input_dim= 1, activation='relu'))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(train_X, train_y, epochs=200, batch_size=2, verbose=2)

    # Our prediction for tomorrow
    prediction = model.predict(np.array([dataset[0]]))
    result = 'The price will move from %s to %s' % (dataset[0], prediction[0][0])

    return result

# Ask user for a stock quote
stock_quote = input('Enter a stock quote from NASDAQ (e.g. AAPL, FB, GOOGL): ').upper()


# Check if we go to the historical data
if not get_historical(stock_quote):
    print('Google returned an error, re-run script with a stock quote from NASDAQ')
    sys.exit()

# We have our file so we create the neural net and get the prediction
print(stock_prediction())

# We are done so we delete the csv file
os.remove(FILE_NAME)
