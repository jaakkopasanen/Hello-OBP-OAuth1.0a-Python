import os
import json
from pprint import pprint
from collections import OrderedDict

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import normalize
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

from ObpApi.ObpApi import ObpApi
from ObpApi.api_credentials import *
from test_users import TEST_USERS
from classification.features import (
    get_transaction_weekday, get_transaction_hour, get_transaction_month)
from datasimulation.TransactionManager import TransactionManager

DEFAULT_VAL_TO_REPLACE_MISSING = -9999.0


def get_api():
    return ObpApi(
        host='https://op.openbankproject.com',
        version='2.1.0',
        direct_login_url='/my/logins/direct',
        oauth_url='/oauth',
        oauth_callback_url='http://localhost',
        consumer_key=OBP_CONSUMER_KEY,
        consumer_secret=OBP_CONSUMER_SECRET)


def get_all_transaction_data(users, obp_api):
    # Get all TEST_USERS transactions from public & private accounts
    #  - Produces transactions for 77 accounts
    transactions = []
    for user in users:
        login_success = obp_api.login_direct(user['username'],
                                             user['password'])
        if not login_success:
            continue
        accounts = obp_api.get_accounts_at_all_banks()['accounts']
        for acc in accounts:
            t = obp_api.get_transactions(bank_id=acc['bank_id'],
                                         account=acc['id'])
            if t:
                transactions.append(t)
    return transactions


def get_transaction_amount(transaction):
    # if transaction['details']['value']['currency'].strip().upper() == 'EUR':
    return transaction['details']['value']['amount']
    # else:
    #     raise(Exception("Unknown currency: %s" %
    #                     transaction['details']['value']['currency']))


def get_transaction_description(transaction):
    descr = transaction['details']['description']
    if descr and descr is not None:
        return descr
    else:
        return ''


def user_transactions_to_data_matrix(user_transactions):
    print("Concerting user transactions to data matrix...")
    df_all = pd.DataFrame()
    for transaction in user_transactions:
        row_transaction = pd.DataFrame({
            'amount': float(get_transaction_amount(transaction)),
            'description': get_transaction_description(transaction),
            'counterparty_id': transaction['counterparty']['id'],
            'weekday': get_transaction_weekday(transaction),
            'hour': get_transaction_hour(transaction),
            # 'month': get_transaction_month(transaction),
            # 'type': str(transaction['details']['type'])
        }, index=[transaction['account']['id']])
        df_all = df_all.append([row_transaction], ignore_index=False)
    return df_all


def pre_process(df):
    print("Applying pre processing...")
    # Fill empty strings with NaNs
    df = df.replace('', pd.np.nan, regex=True)
    # Fill white space strings with NaNs
    df = df.replace(r'\s+', pd.np.nan, regex=True)
    # Delete rows with all NA variables
    df = df.dropna(axis=0, how='all')
    # Delete columns with all NA variables
    df = df.dropna(axis=1, how='all')
    # Fill all NaNs with global missing value identifier
    df = df.fillna(DEFAULT_VAL_TO_REPLACE_MISSING)
    # Delete constant columns (1 unique value)
    constant_col_names = []
    for col in df.columns:
        if df[col].unique().size <= 1:  # .unique() counts NaNs as well
            constant_col_names.append(col)
    df = df.drop(labels=constant_col_names, axis=1)
    return df


def factorize_string_cols(df):
    print("Factorizing string columns...")
    factorized_vals = {}
    for col in df.columns:
        if not df[col].dtype in (object, str):
            # Skip non string columns
            continue
        labels, uniques = pd.factorize(df[col])
        factorized_vals[col] = OrderedDict(zip(range(uniques.size), uniques))
        df[col] = labels
    return df, factorized_vals


def get_colors_for_labels(labels):
    colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k']
    # Add 1 because noisy samples are labeled as -1 and -1 cannot be used
    # as an index for the list of colors
    return colors[:len(np.unique(labels))]


def visualize_pca(df, labels=None, file_name_identifier=None):
    """
    Principal Component Analysis (PCA) identifies the combination
    of attributes (principal components, or directions in the feature space)
    that account for the most variance in the data.

    Let's calculate the 2 first principal components of the data,
    and then create a scatter plot visualizing the data examples
    projected on the calculated components.
    """

    # Normalize each feature to unit norm (vector length)
    df_normalized = normalize(df, axis=0)

    # Run PCA
    pca = PCA(n_components=2)
    df_projected = pca.fit_transform(df_normalized)

    # Visualize
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(1, 1, 1)
    if labels is None:
        ax.scatter(df_projected[:, 0], df_projected[:, 1], marker='o',
                   color=(0.0, 0.63, 0.69), edgecolor='whitesmoke',
                   linewidth='1', s=50, alpha=0.7)
    else:
        ax.scatter(df_projected[:, 0], df_projected[:, 1], marker='o',
                   color=get_colors_for_labels(labels), edgecolor='whitesmoke',
                   linewidth='1', s=50, alpha=0.7)
    # plt.title(
    #     "Scatter plot of the training data examples projected on the "
    #     "2 first principal components")
    plt.xlabel("Principal axis 1 - Explains %.1f %% of the variance" % (
        pca.explained_variance_ratio_[0] * 100.0))
    plt.ylabel("Principal axis 2 - Explains %.1f %% of the variance" % (
        pca.explained_variance_ratio_[1] * 100.0))
    # plt.show()

    ims_folder = 'pca_plots'
    if not os.path.exists(ims_folder):
        os.makedirs(ims_folder)
    if file_name_identifier is None:
        plt.savefig(os.path.join(ims_folder, "pca.png"), format='png')
    else:
        plt.savefig(os.path.join(ims_folder, "%s_pca_clusters.png" %
                                 file_name_identifier), format='png')
        plt.close("all")


def cluster_transactions(user_transactions):
    # Prepare data
    data_matrix = user_transactions_to_data_matrix(user_transactions)
    data_matrix, factorized_vals = factorize_string_cols(data_matrix)
    data_matrix = pre_process(data_matrix)
    account_id = data_matrix.index[0]
    # Normalize dataset for easier parameter selection
    data_matrix_scaled = StandardScaler().fit_transform(data_matrix)
    # Cluster
    dbscan = DBSCAN()
    dbscan.fit(data_matrix_scaled)
    # Predicted clusters is as long as rows (transactions) in data_matrix
    predicted_clusters = dbscan.labels_.astype(np.int)

    if all(predicted_clusters == -1):
        # Noisy samples are given the label -1
        print("%s: All samples are labeled as noisy samples" % account_id)
        return None, None
    else:
        print("%s: Clustering successful - found %s clusters" %
              (account_id, len(np.unique(predicted_clusters))))
        # visualize_pca(data_matrix, labels=y_pred,
        #               file_name_identifier=account_id)
        clusters = []
        # Extract individual clusters (subsets of rows in data_frame)
        for uniq_cluster_label in np.unique(predicted_clusters):
            print("  * Number of transactions in cluster %s: %s" % (
                uniq_cluster_label, len([ix for ix, label in
                                 enumerate(predicted_clusters) if
                                 label == uniq_cluster_label and
                                 label != -1])))
            cluster = data_matrix.iloc[
                [i for i, label in enumerate(predicted_clusters) if
                 label == uniq_cluster_label and label != -1]]
            #cluster.to_csv('cluster%s.csv' % uniq_cluster_label)
            clusters.append(cluster)
        return clusters, factorized_vals


if __name__ == '__main__':

    # The following fetches all the transactions from OP DB and cluster them
    # obp_api = get_api()
    # users_transactions = get_all_transaction_data(users=TEST_USERS,
    #                                               obp_api=obp_api)
    # for i, user_transactions in enumerate(users_transactions, start=1):
    #     print("\nProcessing account %s / %s" % (i, len(users_transactions)))
    #     cluster_transactions(user_transactions)

    # The following loads data generated with the datasimulation module
    # and clusters it
    tm = TransactionManager()
    tm.load('/Users/tuomastikkanen/Documents/my_dev/Ultrahack16-UltimateAI/tm.json')
    user_transactions = tm.accounts['1']
    clusters, factorized_vals = cluster_transactions(user_transactions)
