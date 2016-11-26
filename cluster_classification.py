from datasimulation.TransactionManager import TransactionManager
import os
from clustering import cluster_transactions
from classification.features import create_cluster_features
from pprint import pprint
import numpy as np
import pandas as pd

tm = TransactionManager()
tm.load(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'datasimulation/tm.json'))
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
for _, cluster_indices in cluster_index_matrix.items():
    # transactions = user_transactions[cluster_indices]
    transactions = list(user_transactions[i] for i in cluster_indices)
    feats, feat_names = create_cluster_features(transactions)
    feat_df = pd.DataFrame(dict(zip(feat_names, feats[:-1])), index=[1])
    cluster_matrix = cluster_matrix.append([feat_df], ignore_index=True)
    print(feat_names)
    pprint(feats)
print()
