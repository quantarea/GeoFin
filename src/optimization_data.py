# GeoFin : a python library for portfolio optimization and index replication
# GeoFin is part of GeomScale project

# Copyright (c) 2024 Cyril Bachelard
# Copyright (c) 2024 Minh Ha Ho

# Licensed under GNU LGPL.3, see LICENCE file



import pandas as pd



class OptimizationData(dict):

    def __init__(self, align = True, lags = {}, *args, **kwargs):
        super(OptimizationData, self).__init__(*args, **kwargs)
        self.__dict__ = self
        if len(lags) > 0:
            for key in lags.keys():
                self[key] = self[key].shift(lags[key])
        if align:
            self.align_dates()

    def intersecting_dates(self, variable_names: list = None,  dropna: bool = True) -> pd.DatetimeIndex:
        if variable_names is None:
            variable_names = list(self.keys())
        index = self.get(variable_names[0]).index
        if dropna:
            for variable_name in variable_names:
                self[variable_name] = self[variable_name].dropna()
        index = self.get(variable_names[0]).index
        for variable_name in variable_names:
            index = index.intersection(self.get(variable_name).index)
        return index

    def align_dates(self, variable_names: list = None) -> None:
        if variable_names is None:
            variable_names = self.keys()
        index = self.intersecting_dates(variable_names = list(variable_names))
        for key in variable_names:
            self[key] = self[key].loc[index]
        return None