import numpy
import datetime
import pickle
import os
from coins_api.client import CoinsApi


def get_data(base, destination, skip, days, force=False):
    FILENAME = os.path.join(
        os.path.dirname(__file__),
        'datasets',
        "{}_{}_{}_{}_{}".format("dataset", base, destination, skip, days)
    )

    if os.path.exists(FILENAME) and not force:
        with open(FILENAME, 'rb') as pickle_file:
            return pickle.load(pickle_file)
    dataset = []
    skipped = 0
    quoted_volume_sum = 0
    volume_sum = 0

    for page in CoinsApi.get_candlesticks(
            base_coin=base,
            destination_coin=destination,
            start_date=datetime.datetime.now() - datetime.timedelta(days=days),
            end_date=datetime.datetime.now()
    ):
        for item in page:
            volume_sum += item["volume"]
            quoted_volume_sum += item["quotedVolume"]
            if skipped == skip:
                dataset.append([item["weightAverage"], volume_sum, quoted_volume_sum])
                skipped = 0
                volume_sum = 0
                quoted_volume_sum = 0
            skipped += 1
    dataset = numpy.array(dataset, numpy.float32)
    with open(FILENAME, 'wb') as pickle_file:
        pickle.dump(obj=dataset, file=pickle_file)
    return dataset
