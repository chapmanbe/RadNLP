import gzip
import json
try:
    import pickle
except:
    import cPickle as pickle


def to_pickle(data, fname, compress=True):
    """
    save analysis to pickle file
    """
    if compress:
        with gzip.open(fname, "wb") as f0:
            pickle.dump(data, f0)
    else:
        with open(fname, "wb") as f0:
            pickle.dump(data, f0)


def to_json(data, fname, compress=True):
    """
    save analysis to json file
    """
    if compress:
        with gzip.open(fname, "wb") as f0:
            json.dump(data, f0)
    else:
        with open(fname, "wb") as f0:
            json.dump(data, f0)


def read_pickle(fname, compress=True):
    """
    read analysis from pickle file
    """
    if compress:
        with gzip.open(fname, "rb") as f0:
            return pickle.load(f0)
    else:
        with open(fname, "rb") as f0:
            return pickle.load(f0)


def read_json(data, fname, compress=True):
    """
    save analysis to json file
    """
    if compress:
        with gzip.open(fname, "wb") as f0:
            json.load(f0)
    else:
        with open(fname, "wb") as f0:
            json.load(f0)
