from datasimulation.TransactionManager import TransactionManager
import os
from clustering import cluster_transactions
from classification.features import create_cluster_features
from classification.classify import train
from pprint import pprint
import numpy as np
import pandas as pd


def get_training_data(path_to_user_data=None, user_transactions=None):
    if path_to_user_data is not None:
        tm = TransactionManager()
        tm.load(path_to_user_data)
        user_transactions = tm.accounts['1']

    clusters, cluster_labels, factorized_vals = cluster_transactions(user_transactions)
    # Save first cluster to file
    # clusters[0].to_csv('cluster.csv', index=False)

    # keys are the cluster labels, values are transaction indices in user_transactions
    cluster_index_matrix = {}
    for i, cluster_label in enumerate(cluster_labels):
        if cluster_label in cluster_index_matrix:
            cluster_index_matrix[cluster_label].append(i)
        else:
            cluster_index_matrix[cluster_label] = [i]

    cluster_matrix = pd.DataFrame()
    labels = []
    unique_labels = []
    for _, cluster_indices in cluster_index_matrix.items():
        # transactions = user_transactions[cluster_indices]
        transactions = list(user_transactions[i] for i in cluster_indices)
        feats, feat_names = create_cluster_features(transactions)
        feat_df = pd.DataFrame(dict(zip(feat_names, feats[:-1])), index=[1])
        cluster_matrix = cluster_matrix.append([feat_df], ignore_index=True)
        # All description names
        labels.append(feats[-1])

        if feats[-1] not in unique_labels:
            # Unique description names
            unique_labels.append(feats[-1])

    y_train = []
    one_hot_y = np.eye(len(unique_labels))
    for row_ix, _ in cluster_matrix.iterrows():
        label = labels[row_ix]
        label_ix = np.where(np.array(unique_labels) == label)[0][0]
        y_train.append(one_hot_y[label_ix, :])

    return cluster_matrix, y_train


if __name__ == '__main__':
    p = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'datasimulation/tm.json')
    x_train, y_train = get_training_data('./datasimulation/tm.json')
    train(x_train.as_matrix(), np.array(y_train))
