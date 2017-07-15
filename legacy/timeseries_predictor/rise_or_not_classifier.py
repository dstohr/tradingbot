import numpy
import matplotlib.pyplot as plt
import math
from tsfresh import extract_features
extracted_features = extract_features(timeseries, column_id="id", column_sort="time")
from keras.models import Sequential
from keras.layers import Dense
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from .dataset_generator import get_data
PERIOD_MINUTES = 30
FUTURE_MINUTES = 1800
DAYS = 100
LOOK_BACK = 50
EXPECTED_PRICE_RISE = 1.2
EPOCHS = 200
TRAINSET_PART = 0.8
BASE = "BTC"
DESTINATION = "DASH"
VERBOSE = 2


def create_dataset(dataset, look_back=1, future=0, rise=1.5):
    dataX, dataY = [], []
    total = 0
    data_length = len(dataset)
    for i in range(data_length - look_back - 1 - future):
        a = dataset[i:(i + look_back), :].flatten()
        dataX.append(a)
        future_prices = dataset[i + look_back: i + look_back + future, 0]
        threshhold = dataset[i+look_back - 1, 0] * rise
        if max(future_prices) > threshhold:
            dataY.append(1)
            total += 1
        else:
            dataY.append(0)
    print("{} are true".format(total * 100 / data_length))
    return numpy.array(dataX), numpy.array(dataY)


def inverse_transform_column(current_scaler, data, column_index):
    return current_scaler.data_range_[column_index] * data.astype(numpy.float32) + current_scaler.data_min_[column_index]


def run_experiment(period_minutes=PERIOD_MINUTES, future_minutes=FUTURE_MINUTES, days=DAYS, look_back=LOOK_BACK, rise=EXPECTED_PRICE_RISE,
                   epochs=EPOCHS, trainset_part=TRAINSET_PART, base=BASE, destination=DESTINATION, verbose=VERBOSE, do_plot=True):
    skip = int(period_minutes / 5 - 1)
    future = int(future_minutes / period_minutes)

    dataset = get_data(base, destination, skip, days)

    scaler = MinMaxScaler(feature_range=(0, 1))
    dataset = scaler.fit_transform(dataset)

    train_size = int(len(dataset) * trainset_part)
    train, test = dataset[0:train_size, :], dataset[train_size:len(dataset), :]

    trainX, trainY = create_dataset(train, look_back, future, rise)
    testX, testY = create_dataset(test, look_back, future, rise)

    # trainX = numpy.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
    # testX = numpy.reshape(testX, (testX.shape[0], 1, testX.shape[1]))

    model = Sequential()
    model.add(Dense(16, input_shape=(look_back*3,)))
    # model.add(Dense(16, activation='sigmoid'))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(trainX, trainY, epochs=epochs, batch_size=1, verbose=verbose)

    train_predict = model.predict(trainX)
    test_predict = model.predict(testX)

    train_predict = inverse_transform_column(scaler, train_predict, 0)
    trainY = [inverse_transform_column(scaler, trainY, 0)]
    test_predict = inverse_transform_column(scaler, test_predict, 0)
    testY = [inverse_transform_column(scaler, testY, 0)]

    train_score = math.sqrt(mean_squared_error(trainY[0], train_predict[:, 0]))
    test_score = math.sqrt(mean_squared_error(testY[0], test_predict[:, 0]))

    if do_plot:
        train_predict_plot = numpy.empty_like(dataset)
        train_predict_plot[:, :] = numpy.nan
        train_predict_plot[look_back + future:len(train_predict) + look_back + future, :] = train_predict

        test_predict_plot = numpy.empty_like(dataset)
        test_predict_plot[:, :] = numpy.nan
        test_predict_plot[len(train_predict) + ((look_back + future) * 2) + 1:len(dataset) - 1, :] = test_predict

        main_plot = inverse_transform_column(scaler, dataset[:, 0], 0)

        plt.plot(main_plot)
        plt.plot(train_predict_plot[:, 0])
        plt.plot(test_predict_plot[:, 0])

        plt.show()
    return train_score, test_score

