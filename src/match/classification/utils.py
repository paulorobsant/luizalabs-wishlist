from math import sqrt
from sklearn.cluster import KMeans


def must_retrain_the_model(curr_trained_amount: int, new_trained_amount: int, threshold=0.7):
    """
    Checks whether the coefficient of the current training reaches the desired threshold for the execution of a new
    training
    """
    calc = get_training_coefficient(
        curr_trained_amount=curr_trained_amount,
        new_trained_amount=new_trained_amount
    )

    return calc < threshold


def get_training_coefficient(curr_trained_amount: int, new_trained_amount: int):
    return (curr_trained_amount - new_trained_amount) / curr_trained_amount


def calculate_wcss(data):
    """
    Search for a number of groups that the within clusters sum of squares
    """
    wcss = []

    for n in range(2, 21):
        k_means = KMeans(n_clusters=n)
        k_means.fit(X=data)
        wcss.append(k_means.inertia_)

    return wcss


def optimal_number_of_clusters(wcss):
    """
    Get the optimal number of clusters
    """
    x1, y1 = 2, wcss[0]
    x2, y2 = 20, wcss[len(wcss) - 1]

    distances = []

    for i in range(len(wcss)):
        x0 = i + 2
        y0 = wcss[i]

        numerator = abs((y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y2 * x1)
        denominator = sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)
        distances.append(numerator / denominator)

    return distances.index(max(distances)) + 2


def create_challenges_request(terms_list, challenges):
    item = {}

    for term in terms_list:
        key_name = term

        if term in challenges:
            item[key_name] = 1
        else:
            item[key_name] = 0

    return item
