import os
import pickle
import pandas as pd
from sklearn.cluster import KMeans

import settings
from match.classification.utils import calculate_wcss, optimal_number_of_clusters


def create_model(data_frame: pd.DataFrame):
    """
    Create a ML model to predict the challenge clusters
    """
    sum_of_squares = calculate_wcss(data_frame)
    n_clusters = optimal_number_of_clusters(sum_of_squares)

    k_means_expertises = KMeans(n_clusters=n_clusters, random_state=0)

    x_train = data_frame.copy()
    x_fit = k_means_expertises.fit(x_train)

    return x_fit


def save_model(model, file_name):
    """
    Save a model using Pickle
    """
    file_name = f"{settings.MODEL_DIR + file_name}.pkl"
    pickle.dump(model, open(file_name, "wb"))


def load_model(file_name):
    """
    Load a model using Pickle
    """

    file_name = f"{settings.MODEL_DIR + file_name}.pkl"

    if os.path.isfile(file_name):
        return pickle.load(open(file_name, "rb"))
    else:
        return None
