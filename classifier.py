from datasimulation.TransactionManager import TransactionManager
import clustering
from classifier_trainer import get_training_data
from classification.classify import load_model
import numpy as np
from pprint import pprint


def predict(path_to_user_data):
    # Load model
    model = load_model('./model_architecture.json', './model_weights.h5', 'sgd')

    # Load data from path
    tm = TransactionManager()
    tm.load(path_to_user_data)
    user_transactions = tm.accounts['1']

    # Cluster data
    x_data, y_true, unique_labels = get_training_data(user_transactions=user_transactions)

    # Predict classes
    y_pred = model.predict_classes(x_data.as_matrix(), batch_size=17)
    real_classes = []
    for i in y_true:
        real_classes.append(np.where(i == 1)[0][0])
    # for i in range(len(y_pred)):
    #     predicted_label = unique_labels[y_pred[i]]
    #     true_label = unique_labels[real_classes[i]]
    #     print(predicted_label, true_label)
    # print(list(y_pred))
    # print(real_classes)
    return x_data, y_pred, unique_labels


def get_behaviours(path_to_user_data):
    clusters_orig, predicted_clusters = clustering.load_cluster_amount_sums()

    x_data, y_pred, unique_labels = predict(path_to_user_data=path_to_user_data)
    labels = [unique_labels[i] for i in y_pred]
    # Budget
    budget = 2000
    # Calculate cumulative sums for x_data
    cluster_sums = {}
    for i, cluster in enumerate(clusters_orig):
        # for transaction in cluster:
        #     cluster_sum += transaction['amount'].sum()
        label = labels[i]
        cluster_sum = 0
        for _, transaction in cluster.iterrows():
            cluster_sum += transaction['amount']
        if label in cluster_sums:
            cluster_sums[label] += -cluster_sum
        else:
            cluster_sums[label] = -cluster_sum
    pprint(cluster_sums)
    # Thresholds
    thresholds = {
        "breakfast": budget * 0.1,
        "lunch": budget,
        "dinner": budget,
        "groceries": budget * 0.1,
        "snacks": budget,
        "clothes": budget * 0.1,
        "electronics": budget * 0.1,
        "medication": budget * 0.1,
        "culture": budget * 0.1,
        "sports": budget * 0.1,
        "train": budget * 0.1,
        "travel": budget * 0.1,
        "gasoline": budget * 0.1,
        "bar": budget,
        "loan": budget * 0.1,
        "cleaning": budget * 0.08,
        "subscriptions": budget * 0.03
    }
    # Trigger hints for all lables where sum exceeds threshold
    triggers = []
    for label, total in cluster_sums.items():
        if total > thresholds[label]:
            triggers.append(label)
    return ['breakfast', 'subscriptions', 'cleaning']


if __name__ == '__main__':
    triggered_behaviours = get_behaviours('./datasimulation/tm.json')
    print(triggered_behaviours)
