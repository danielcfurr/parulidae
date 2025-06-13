import pandas as pd
import numpy as np
from itertools import product
from copy import copy
import warnings
from statsmodels.tsa.exponential_smoothing.ets import ETSModel


def rmse(obs, pred):
    err = np.array(obs) - np.array(pred)
    return np.sqrt(np.mean(np.square(err)))


def mad(obs, pred):
    err = np.array(obs) - np.array(pred)
    return np.mean(np.abs(err))


def fit_ets_model(train, test, params):
    params_copy = copy(params)

    model = ETSModel(train, **params_copy)

    with warnings.catch_warnings(record=True) as w:
        fit = model.fit()

    if len(w):
        print("Warnings from", params)
        return None
    else:
        pred = fit.forecast(len(test))
        return {'params': params, 'fit': fit, 'rmse': rmse(test, pred), 'mad': mad(test, pred)}


def search_ets_model(train, test, options, forecast):
    combinations = [
        dict(zip( options.keys(), values))
        for values in product(*options.values())
    ]

    results_list = []
    for params in combinations:
        result = fit_ets_model(train, test, params)
        if result is not None:
            results_list.append(result)

    result_dataframe = pd.DataFrame(results_list)
    best_row = result_dataframe.loc[result_dataframe['mad'].idxmin()]
    best_params = best_row['params']
    print('MAD =', best_row['mad'])
    print(best_params)

    full_model = ETSModel(pd.concat([train, test], axis=0), **best_params)
    full_fit = full_model.fit()
    forecasted_values = full_fit.forecast(forecast)

    return forecasted_values
